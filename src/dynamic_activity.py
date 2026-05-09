import json
import os
import random
from pathlib import Path
from datetime import datetime, timedelta
from time import ctime
from prettytable import PrettyTable

from activity_log import append_activity_log, current_timestamp

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
DECOY_DIR = DOCS_DIR / "decoys"
KNOWN_STATE_FILE = DOCS_DIR / "known_state.json"
TRACKED_FILES_FILE = DOCS_DIR / "files_touched.json"

WORK_HOUR_START = 8
WORK_HOUR_END = 18

CONTENT_POOL = {
    ".txt": [
        "Reviewed by admin during morning audit.\n",
        "Added follow-up note after routine system check.\n",
        "Updated entry after help desk review.\n",
        "Appended internal note for next shift.\n",
    ],
    ".csv": [
        "9999,test_record,review_pending\n",
        "7777,service_account,retained\n",
        "8888,backup_user,queued\n",
    ],
    ".cfg": [
        "\n# reviewed during routine maintenance\n",
        "\n# verified by admin after restart\n",
        "\n# backup setting checked\n",
    ]
}


def get_all_files() -> list[Path]:
    return [p for p in DECOY_DIR.rglob("*") if p.is_file()]


def realistic_datetime(now: datetime) -> datetime:
    weekday = now.weekday()

    if weekday < 5:
        hour = random.randint(WORK_HOUR_START, WORK_HOUR_END)
    else:
        hour = random.choice([10, 11, 14, 15])

    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    fake_dt = now.replace(hour=hour, minute=minute, second=second, microsecond=0)

    if fake_dt > now:
        fake_dt = fake_dt - timedelta(days=1)

    return fake_dt


def append_believable_content(file_path: Path) -> None:
    suffix = file_path.suffix.lower()
    content_choices = CONTENT_POOL.get(suffix, ["\nRoutine review completed.\n"])
    new_line = random.choice(content_choices)

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(new_line)


def load_touched_files() -> set[str]:
    if TRACKED_FILES_FILE.exists():
        with open(TRACKED_FILES_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_touched_files(touched: set[str]) -> None:
    with open(TRACKED_FILES_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(list(touched)), f, indent=4)


def choose_files(files: list[Path], touched: set[str], per_run: int = 3) -> list[Path]:
    untouched = [f for f in files if str(f) not in touched]

    if len(untouched) >= per_run:
        return random.sample(untouched, per_run)

    selected = untouched[:]
    remaining_needed = per_run - len(selected)

    remaining_pool = [f for f in files if str(f) not in {str(x) for x in selected}]
    if remaining_pool:
        selected.extend(random.sample(remaining_pool, min(remaining_needed, len(remaining_pool))))

    return selected


def collect_metadata(file_path: Path) -> dict:
    stats = file_path.stat()
    return {
        "path": str(file_path),
        "mode": stats.st_mode,
        "size": stats.st_size,
        "atime": stats.st_atime,
        "mtime": stats.st_mtime,
        "ctime": stats.st_ctime,
        "atime_readable": ctime(stats.st_atime),
        "mtime_readable": ctime(stats.st_mtime),
        "ctime_readable": ctime(stats.st_ctime),
    }


def update_known_state() -> dict:
    snapshot = {}
    for file_path in get_all_files():
        snapshot[str(file_path)] = collect_metadata(file_path)

    with open(KNOWN_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=4)

    return snapshot


def print_summary_table(changes: list[dict]) -> None:
    table = PrettyTable(["FILE", "CHANGE TYPE", "NEW MTIME", "NEW SIZE"])
    table.title = "Dynamic Activity Summary"

    for change in changes:
        table.add_row([
            Path(change["path"]).name,
            change["change_type"],
            change["new_mtime"],
            change["new_size"]
        ])

    print(table)


def simulate_activity() -> None:
    files = get_all_files()

    if not files:
        print("No decoy files found. Run decoy_structure.py first.")
        return

    touched = load_touched_files()
    selected_files = choose_files(files, touched, per_run=3)

    changes = []
    now = datetime.now()

    for file_path in selected_files:
        before_size = file_path.stat().st_size

        append_believable_content(file_path)

        fake_time = realistic_datetime(now)
        fake_epoch = fake_time.timestamp()
        os.utime(file_path, (fake_epoch, fake_epoch))

        stats = file_path.stat()
        changes.append({
            "path": str(file_path),
            "change_type": "timestamp + content + size",
            "new_atime": ctime(stats.st_atime),
            "new_mtime": ctime(stats.st_mtime),
            "new_size": stats.st_size
        })

        if stats.st_size == before_size:
            changes[-1]["change_type"] = "timestamp + content"

        touched.add(str(file_path))

    save_touched_files(touched)
    update_known_state()
    print_summary_table(changes)

    run_time = current_timestamp()
    append_activity_log(run_time, changes)

    print(f"\nKnown state updated: {KNOWN_STATE_FILE}")
    print(f"Tracked files updated: {TRACKED_FILES_FILE}")


if __name__ == "__main__":
    simulate_activity()