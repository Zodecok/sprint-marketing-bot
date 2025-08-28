import os

def logs_dir() -> str:
    # Change this if you keep logs elsewhere; env var override supported
    base = os.environ.get("APP_LOG_DIR", "data/logs")
    return base

def ui_events_log_path() -> str:
    return os.path.join(logs_dir(), "ui_events.jsonl")

def conversations_log_path() -> str:
    # Your /chat handler can append to this file after answering
    return os.path.join(logs_dir(), "conversations.jsonl")
