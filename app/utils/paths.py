import os
from pathlib import Path


def data_dir() -> Path:
    """Base directory for application data (indexes, logs, etc)."""
    override = os.environ.get("APP_DATA_DIR")
    return Path(override) if override else Path("data")


def _path_from_env(var_name: str, default: Path) -> Path:
    override = os.environ.get(var_name)
    return Path(override) if override else default


def logs_dir() -> str:
    # Change this if you keep logs elsewhere; env var override supported
    path = _path_from_env("APP_LOG_DIR", data_dir() / "logs")
    return str(path)


def index_dir() -> Path:
    return _path_from_env("APP_INDEX_DIR", data_dir() / "index")


def index_manifest_path() -> Path:
    preferred = index_dir() / "manifest.json"
    legacy = data_dir() / "index_manifest.json"
    return preferred if preferred.exists() or not legacy.exists() else legacy


def index_faiss_path() -> Path:
    preferred = index_dir() / "index.faiss"
    legacy = data_dir() / "index.faiss"
    return preferred if preferred.exists() or not legacy.exists() else legacy


def index_meta_path() -> Path:
    preferred = index_dir() / "meta.jsonl"
    legacy = data_dir() / "meta.jsonl"
    return preferred if preferred.exists() or not legacy.exists() else legacy


def ui_events_log_path() -> str:
    return os.path.join(logs_dir(), "ui_events.jsonl")


def conversations_log_path() -> str:
    # Your /chat handler can append to this file after answering
    return os.path.join(logs_dir(), "conversations.jsonl")
