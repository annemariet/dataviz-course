"""Shared local paths and secrets for grading notebooks (06, 07).

Copy `.env.example` to `.env` at the repo root and set `TEACHER_EMAIL`.
Optional path overrides use repo-relative defaults.
"""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(REPO_ROOT / ".env", override=False)


def _path_from_env(name: str, default: Path) -> Path:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    path = Path(raw)
    return path if path.is_absolute() else REPO_ROOT / path


def _require_teacher_email() -> str:
    email = os.environ.get("TEACHER_EMAIL", "").strip().lower()
    if not email:
        raise RuntimeError(
            "TEACHER_EMAIL is not set. Copy .env.example to .env and set your teacher email."
        )
    return email


_load_dotenv()

TEACHER_EMAIL = _require_teacher_email()
EXCLUDED_EMAILS = frozenset({TEACHER_EMAIL})

NOTES_DIR = _path_from_env("NOTES_DIR", REPO_ROOT / "notes")
PROJECT_EVAL_DIR = _path_from_env("PROJECT_EVAL_DIR", REPO_ROOT / "project_eval")
CHART_SCORING_DIR = _path_from_env("CHART_SCORING_DIR", REPO_ROOT / "chart-scoring")

EVAL_CSV = PROJECT_EVAL_DIR / os.environ.get(
    "EVAL_CSV", "Evaluation Sheet - Verified(Sheet1).csv"
)
TEAMS_CSV = PROJECT_EVAL_DIR / os.environ.get(
    "TEAMS_CSV", "Enregistrement pour le mini-projet(Teams).csv"
)
CHART_SCORES_FILE = CHART_SCORING_DIR / os.environ.get(
    "CHART_SCORES_FILE", "Score this chart.xlsx"
)
