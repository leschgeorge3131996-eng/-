from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.services.file_service import FileService


def main() -> None:
    parser = argparse.ArgumentParser(description="Delete expired uploaded documents.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args()

    service = FileService()
    deleted_file_ids = service.cleanup_expired_documents()
    payload = {
        "deleted_count": len(deleted_file_ids),
        "deleted_file_ids": deleted_file_ids,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print(f"Deleted expired documents: {payload['deleted_count']}")
    for file_id in deleted_file_ids:
        print(f"- {file_id}")


if __name__ == "__main__":
    main()
