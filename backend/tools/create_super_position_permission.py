import sys
from pathlib import Path

parent_folder = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_folder))

import dotenv
dotenv.load_dotenv()

import argparse
from backend.domains.authentication.services.position_permission_service import create_position_permission
from backend.domains.authentication.schemas.position_permission_schema import CreatePositionPermissionSchema, PositionPermissionSchema
from backend.repository import SessionLocal

parser = argparse.ArgumentParser(description="Create a new position permission")

parser.add_argument("--position_id", required=True, help="Position_id")
parser.add_argument("--permission_id", required=True, help="Permission_id")

args = parser.parse_args()

def main():
    # Initiate a new session
    db = SessionLocal()
    try:
        create_position_permission(CreatePositionPermissionSchema(
            position_id=args.position_id,
            permission_id=args.permission_id
        ), db)
    except Exception as e:
        print(e)
    finally:
        db.close()

if __name__ == '__main__':
    main()
