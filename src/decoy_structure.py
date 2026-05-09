import json
import stat
from pathlib import Path
from time import ctime
from prettytable import PrettyTable

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
DECOY_DIR = DOCS_DIR / "decoys"
KNOWN_STATE_FILE = DOCS_DIR / "known_state.json"

STRUCTURE = {
    "workstation": {
        "HR": {
            "employee_notes.txt": """Employee Notes
- James requested updated tax forms
- Nina asked about PTO carryover
- Review onboarding packet next Monday
""",
            "salaries_2025.csv": """employee_id,name,department,salary
1001,Alice Carter,HR,64000
1002,James Porter,IT,71000
1003,Nina Lopez,Operations,68500
"""
        },
        "IT": {
            "passwords.txt": """Temporary Password List
svc_backup: Winter2025!
temp_admin: Welcome123!
vpn_test: ChirpyHub@2025
""",
            "vpn_config.cfg": """[vpn]
host=vpn.chirpyhub.local
port=443
protocol=tcp
reconnect=true
"""
        },
        "Projects": {
            "q4_budget.csv": """category,amount,status
cloud_hosting,12000,approved
security_tools,8500,pending
staff_training,3000,approved
""",
            "workstation_todo.txt": """Workstation To Do
- Replace front desk PC after imaging
- Archive old benefits paperwork
- Verify endpoint protection signatures
"""
        }
    },
    "server": {
        "logs": {
            "access_logs.txt": """2026-04-20 08:11:09 GET /login 200
2026-04-20 08:14:22 POST /api/auth 401
2026-04-20 08:15:48 GET /dashboard 200
""",
            "event_logs.txt": """INFO: nightly cleanup complete
WARN: queue worker retry on node 2
INFO: backup validation passed
"""
        },
        "config": {
            "app_config.cfg": """[app]
name=ChirpyHub
mode=production
debug=false

[database]
host=10.0.2.25
port=5432
""",
            "db_connection.txt": """DB Connection Notes
Primary DB Host: 10.0.2.25
Read Replica: 10.0.2.26
Service Account: chirpy_reader
"""
        },
        "data": {
            "deleted_chirps.csv": """chirp_id,user_id,reason
8842,119,policy_violation
8843,442,duplicate_post
8844,884,spam_link
""",
            "confidential_chirps.csv": """chirp_id,user_id,flag
9101,2001,legal_hold
9102,2009,internal_review
9103,2014,executive_escalation
"""
        }
    }
}


def ensure_directories() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    DECOY_DIR.mkdir(parents=True, exist_ok=True)


def create_decoy_structure() -> None:
    for root_name, subdirs in STRUCTURE.items():
        for subdir_name, files in subdirs.items():
            folder_path = DECOY_DIR / root_name / subdir_name
            folder_path.mkdir(parents=True, exist_ok=True)

            for filename, content in files.items():
                file_path = folder_path / filename
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)


def collect_metadata(file_path: Path) -> dict:
    stats = file_path.stat()
    return {
        "path": str(file_path),
        "mode": stat.filemode(stats.st_mode),
        "size": stats.st_size,
        "atime": stats.st_atime,
        "mtime": stats.st_mtime,
        "ctime": stats.st_ctime,
        "atime_readable": ctime(stats.st_atime),
        "mtime_readable": ctime(stats.st_mtime),
        "ctime_readable": ctime(stats.st_ctime),
    }


def build_known_state() -> dict:
    snapshot = {}
    for path in DECOY_DIR.rglob("*"):
        if path.is_file():
            snapshot[str(path)] = collect_metadata(path)
    return snapshot


def save_known_state(snapshot: dict) -> None:
    with open(KNOWN_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=4)


def print_summary(snapshot: dict) -> None:
    table = PrettyTable(["FILE", "SIZE", "ATIME", "MTIME", "CTIME", "MODE"])
    table.title = "Initial Known State"

    for item in snapshot.values():
        table.add_row([
            Path(item["path"]).name,
            item["size"],
            item["atime_readable"],
            item["mtime_readable"],
            item["ctime_readable"],
            item["mode"]
        ])

    print(table)


def main() -> None:
    ensure_directories()
    create_decoy_structure()
    snapshot = build_known_state()
    save_known_state(snapshot)
    print_summary(snapshot)
    print(f"\nKnown state written to: {KNOWN_STATE_FILE}")


if __name__ == "__main__":
    main()