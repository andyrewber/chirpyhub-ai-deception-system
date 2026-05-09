from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "docs" / "activity_log.txt"


def current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def append_activity_log(run_time: str, changes: list[dict]) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("=" * 72 + "\n")
        f.write(f"Activity Run: {run_time}\n")
        f.write("=" * 72 + "\n")

        if not changes:
            f.write("No changes applied.\n\n")
            return

        for change in changes:
            f.write(f"File: {change['path']}\n")
            f.write(f"Change Type: {change['change_type']}\n")
            f.write(f"New ATIME: {change['new_atime']}\n")
            f.write(f"New MTIME: {change['new_mtime']}\n")
            f.write(f"New Size: {change['new_size']}\n")
            f.write("-" * 72 + "\n")

        f.write("\n")