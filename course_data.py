"""Shared Open Food Facts Parquet path and download helpers for session notebooks."""

from __future__ import annotations

import os
import re
from pathlib import Path

# DuckDB: bind values with $name placeholders and params={...}; allowlist for column names.
ALLOWED_NUTRIENTS = frozenset(
    {
        "energy-kcal_100g",
        "fat_100g",
        "fiber_100g",
        "proteins_100g",
        "salt_100g",
        "saturated-fat_100g",
        "sugars_100g",
    }
)
MIN_SAMPLE_N = 1
MAX_SAMPLE_N = 500_000
_COUNTRY_TAG_RE = re.compile(r"^en:[a-z-]+$")

# Course SharePoint (requires Dauphine login in a browser for manual download).
DEFAULT_PARQUET_SHARE_URL = (
    "https://universitedauphine.sharepoint.com/:u:/r/sites/"
    "upd_25_a5aias150_espacepromo/Documents%20partages/"
    "Visualisation%20de%20donn%C3%A9es/data/openfoodfacts.parquet"
    "?csf=1&web=1&e=XeGvP6"
)

PARQUET_PATH = Path("data/openfoodfacts.parquet")

MANUAL_DOWNLOAD_HELP = """\
Open Food Facts Parquet not found and automated download did not return a valid file.

**Manual download (recommended for SharePoint):**
1. Open the course link in your browser (Dauphine login):
   {url}
2. Download **openfoodfacts.parquet**
3. Create the folder if needed and save the file as:
   {path}

**Optional:** set `PARQUET_URL` to a direct-download URL (no login) if you have one:
   export PARQUET_URL="https://..."
"""


def parquet_bind_path(path: Path | str) -> str:
    """Absolute path string for read_parquet(?) binding."""
    return str(Path(path).resolve())


def validate_sample_n(
    sample_n: int,
    *,
    min_n: int = MIN_SAMPLE_N,
    max_n: int = MAX_SAMPLE_N,
) -> int:
    """Coerce and bound SAMPLE row counts (SQL literals, not bind params)."""
    n = int(sample_n)
    if not min_n <= n <= max_n:
        raise ValueError(f"SAMPLE_N must be between {min_n} and {max_n}, got {sample_n!r}")
    return n


def validate_country(country: str | None) -> str | None:
    """Open Food Facts country tags look like en:france."""
    if country is None:
        return None
    if not isinstance(country, str) or not _COUNTRY_TAG_RE.fullmatch(country):
        raise ValueError(f"COUNTRY must look like 'en:france', got {country!r}")
    return country


def validate_nutrient(nutrient: str) -> str:
    """Allowlist nutrient column names used in dynamic SQL identifiers."""
    if nutrient not in ALLOWED_NUTRIENTS:
        allowed = ", ".join(sorted(ALLOWED_NUTRIENTS))
        raise ValueError(f"nutrient must be one of: {allowed}; got {nutrient!r}")
    return nutrient


def resolve_parquet_url() -> str | None:
    """Environment override, else default SharePoint sharing link."""
    return os.environ.get("PARQUET_URL") or DEFAULT_PARQUET_SHARE_URL


def download_url_candidates(url: str) -> list[str]:
    """Try sharing link, ?download=1, and site-path variants."""
    candidates = [url]
    if "download=1" not in url:
        sep = "&" if "?" in url else "?"
        candidates.append(f"{url}{sep}download=1")
    if "web=1" in url:
        candidates.append(url.replace("web=1", "download=1"))
    if "/:u:/r/" in url:
        direct = url.replace("/:u:/r/", "/").split("?")[0]
        candidates.append(f"{direct}?download=1")
    return list(dict.fromkeys(candidates))


def _looks_like_parquet(path: Path) -> bool:
    try:
        return path.stat().st_size >= 8 and path.read_bytes()[:4] == b"PAR1"
    except OSError:
        return False


def ensure_openfoodfacts_parquet(
    path: Path | None = None,
    url: str | None = None,
) -> Path:
    """Use local Parquet, else attempt HTTP download; raise with manual steps if needed."""
    import requests

    path = Path(path or PARQUET_PATH)
    if path.exists():
        if _looks_like_parquet(path):
            return path
        path.unlink()

    url = url if url is not None else resolve_parquet_url()
    if not url:
        raise FileNotFoundError(
            MANUAL_DOWNLOAD_HELP.format(url="(no URL configured)", path=path.resolve())
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    last_err: Exception | None = None

    for candidate in download_url_candidates(url):
        try:
            with requests.get(
                candidate,
                allow_redirects=True,
                timeout=120,
                stream=True,
                headers={"User-Agent": "dataviz-course/0.1"},
            ) as resp:
                resp.raise_for_status()
                content_type = (resp.headers.get("content-type") or "").lower()
                if "text/html" in content_type or "login.microsoftonline" in resp.url:
                    last_err = RuntimeError("response is a login or HTML page, not Parquet")
                    continue

                tmp = path.with_suffix(".parquet.part")
                with tmp.open("wb") as out:
                    for chunk in resp.iter_content(chunk_size=1 << 20):
                        if chunk:
                            out.write(chunk)

                if not _looks_like_parquet(tmp):
                    tmp.unlink(missing_ok=True)
                    last_err = RuntimeError(
                        f"downloaded file is not Parquet (content-type: {content_type})"
                    )
                    continue

                tmp.replace(path)
                return path
        except Exception as exc:
            last_err = exc

    detail = f"\n\nLast attempt: {last_err}" if last_err else ""
    raise FileNotFoundError(
        MANUAL_DOWNLOAD_HELP.format(url=url, path=path.resolve()) + detail
    )
