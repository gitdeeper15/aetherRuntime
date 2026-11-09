#!/usr/bin/env python3
"""
AetherRuntime v2.0.0 — PyPI Uploader (requests-only)

Uploads built distribution files to PyPI or TestPyPI using the PyPI
legacy upload API directly, reading metadata from each file.

Usage:
    python upload_aetherruntime.py            # upload to PyPI
    python upload_aetherruntime.py --test     # upload to TestPyPI
    python upload_aetherruntime.py --check    # only validate dist/

Credentials (env vars):
    PYPI_USERNAME / PYPI_PASSWORD
    TESTPYPI_USERNAME / TESTPYPI_PASSWORD
"""

from __future__ import annotations

import email
import hashlib
import os
import sys
import tarfile
import zipfile
from pathlib import Path

try:
    import requests
except ImportError:
    print("❌ 'requests' is required. Install with: pip install requests")
    sys.exit(1)


PACKAGE_NAME = "aetherruntime-arch"
VERSION = "2.0.0"
ZENODO_DOI = "10.5281/zenodo.24078477"
ORCID_URL = "https://orcid.org/0009-0003-8903-0029"

UPLOAD_URLS = {
    "pypi": "https://upload.pypi.org/legacy/",
    "testpypi": "https://test.pypi.org/legacy/",
}

DIST_DIR = Path(__file__).parent / "dist"


def _dist_files() -> list[Path]:
    if not DIST_DIR.exists():
        return []
    return sorted(p for p in DIST_DIR.iterdir()
                  if p.is_file() and (p.suffix == ".whl" or p.name.endswith(".tar.gz")))


def _credentials(repo: str) -> tuple[str, str]:
    if repo == "testpypi":
        user = os.environ.get("TESTPYPI_USERNAME", "__token__")
        password = os.environ.get("TESTPYPI_PASSWORD", "")
    else:
        user = os.environ.get("PYPI_USERNAME", "__token__")
        password = os.environ.get("PYPI_PASSWORD", "")
    return user, password


def _read_metadata(path: Path) -> dict:
    """Extract Name and Version from wheel or sdist METADATA/PKG-INFO."""
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as zf:
            meta_name = next((n for n in zf.namelist() if n.endswith(".dist-info/METADATA")), None)
            if not meta_name:
                raise RuntimeError(f"No METADATA in {path.name}")
            raw = zf.read(meta_name).decode("utf-8", errors="replace")
    else:  # sdist .tar.gz
        with tarfile.open(path, "r:gz") as tf:
            pkg_info = next((m for m in tf.getmembers() if m.name.endswith("/PKG-INFO")), None)
            if not pkg_info:
                raise RuntimeError(f"No PKG-INFO in {path.name}")
            raw = tf.extractfile(pkg_info).read().decode("utf-8", errors="replace")

    msg = email.message_from_string(raw)
    return {
        "name": msg.get("Name", "").strip(),
        "version": msg.get("Version", "").strip(),
        "summary": msg.get("Summary", ""),
        "author": msg.get("Author", ""),
        "author_email": msg.get("Author-email", msg.get("Author-email", "")),
        "license": msg.get("License", ""),
        "metadata_version": msg.get("Metadata-Version", "2.1"),
        "description": msg.get_payload() or "",
    }


def _md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _upload_one(url: str, auth: tuple[str, str], path: Path) -> int:
    print(f"\n→ Preparing {path.name} ({path.stat().st_size:,} bytes) ...")
    meta = _read_metadata(path)

    if not meta["name"]:
        print(f"  ❌ Metadata in {path.name} has no Name")
        return 1
    if not meta["version"]:
        print(f"  ❌ Metadata in {path.name} has no Version")
        return 1

    print(f"  Name    : {meta['name']}")
    print(f"  Version : {meta['version']}")

    if path.suffix == ".whl":
        filetype = "bdist_wheel"
        pyversion = "py3"
    else:
        filetype = "sdist"
        pyversion = "source"

    fields = {
        ":action": "file_upload",
        "protocol_version": "1",
        "metadata_version": meta["metadata_version"],
        "name": meta["name"],
        "version": meta["version"],
        "filetype": filetype,
        "pyversion": pyversion,
        "summary": meta["summary"],
        "author": meta["author"],
        "author_email": meta["author_email"],
        "license": meta["license"],
        "description": meta["description"],
        "description_content_type": "text/markdown",
        "md5_digest": _md5(path),
        "sha256_digest": _sha256(path),
    }

    print(f"  Type    : {filetype}")
    print(f"  → POST {url}")

    with path.open("rb") as fh:
        resp = requests.post(
            url,
            auth=auth,
            data=fields,
            files={"content": (path.name, fh, "application/octet-stream")},
            timeout=300,
        )

    print(f"  HTTP {resp.status_code}")
    if resp.status_code in (200, 201):
        print(f"  ✅ {path.name} uploaded")
        return 0

    print(f"  ❌ {path.name} failed")
    print("  --- PyPI response (first 2000 chars) ---")
    print(resp.text[:2000])
    print("  ----------------------------------------")
    return 1


def main() -> int:
    args = sys.argv[1:]
    repo = "testpypi" if "--test" in args else "pypi"
    check_only = "--check" in args
    url = UPLOAD_URLS[repo]
    user, password = _credentials(repo)

    print("=" * 70)
    print(f"  {PACKAGE_NAME} v{VERSION} — PyPI Upload (requests)")
    print("=" * 70)
    print(f"  Target : {repo}")
    print(f"  URL    : {url}")
    print(f"  Dist   : {DIST_DIR}")
    print(f"  User   : {user}")
    print(f"  Token  : {'set' if password else 'MISSING'}")
    print("=" * 70)

    files = _dist_files()
    if not files:
        print(f"\n❌ No distribution files in {DIST_DIR}")
        print("   Build first:  python -m build")
        return 1

    print(f"\n📦 {len(files)} file(s):")
    for f in files:
        print(f"   • {f.name}  ({f.stat().st_size:,} bytes)")

    if check_only:
        for f in files:
            m = _read_metadata(f)
            print(f"   → {f.name}: Name={m['name']} Version={m['version']}")
        print("\n✅ --check: no upload performed.")
        return 0

    if not password:
        print("\n❌ No password/token found.")
        print("   Export PYPI_PASSWORD=<your-token> and retry.")
        return 1

    auth = (user, password)
    rc = 0
    for path in files:
        rc |= _upload_one(url, auth, path)

    if rc == 0:
        print("\n" + "=" * 70)
        print(f"✅ All uploads succeeded.")
        print(f"   View at: https://pypi.org/project/{PACKAGE_NAME}/{VERSION}/")
        print("=" * 70)
    else:
        print("\n❌ Some uploads failed (see response above).")
    return rc


if __name__ == "__main__":
    sys.exit(main())
