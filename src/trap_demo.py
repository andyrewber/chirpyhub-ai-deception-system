import time
import hashlib
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BASE_DIR = Path(__file__).resolve().parent.parent
WATCH_DIR = BASE_DIR / "docs" / "decoys"
LOG_FILE = BASE_DIR / "docs" / "trap_alerts.txt"
POLL_INTERVAL = 5

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ]
)


def file_hash(filepath: str):
    try:
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return None


def build_snapshot(watch_dir: Path) -> dict:
    snapshot = {}
    for path in watch_dir.rglob("*"):
        if path.is_file():
            try:
                snapshot[str(path)] = {
                    "atime": path.stat().st_atime,
                    "hash": file_hash(str(path))
                }
            except OSError:
                pass
    return snapshot


def check_for_reads(old_snapshot: dict, watch_dir: Path) -> dict:
    new_snapshot = build_snapshot(watch_dir)

    for filepath, new_info in new_snapshot.items():
        old_info = old_snapshot.get(filepath)
        if old_info is None:
            continue

        atime_changed = new_info["atime"] != old_info["atime"]
        hash_changed = new_info["hash"] != old_info["hash"]

        if atime_changed and not hash_changed:
            logging.info("FILE OPENED / READ | %s", filepath)

    return new_snapshot


class TrapHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logging.info("NEW FILE ADDED | %s", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            logging.info("FILE ALTERED | %s", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            logging.info("FILE DELETED | %s", event.src_path)


def main():
    WATCH_DIR.mkdir(parents=True, exist_ok=True)

    observer = Observer()
    handler = TrapHandler()
    observer.schedule(handler, str(WATCH_DIR), recursive=True)

    logging.info("Trap watcher started | watching: %s", WATCH_DIR)
    observer.start()

    snapshot = build_snapshot(WATCH_DIR)

    print("Watching decoy directories... Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(POLL_INTERVAL)
            snapshot = check_for_reads(snapshot, WATCH_DIR)

    except KeyboardInterrupt:
        observer.stop()
        print("\nTrap watcher stopped.")

    observer.join()


if __name__ == "__main__":
    main()