import sys
from pathlib import Path

parent_folder = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_folder))

import dotenv
dotenv.load_dotenv()

import argparse
from backend.domains.authentication.services.position_service import create_position
from backend.domains.authentication.schemas.position_schema import CreatePositionRequestSchema, PositionResponseSchema


parser = argparse.ArgumentParser(description="Create a new position")

parser.add_argument("--role", required=True, help="Role")

args = parser.parse_args()

def main():
    position = create_position(CreatePositionRequestSchema(
        role=args.role
    ))

    print(f"Created position with id: {position.position_id}")

if __name__ == '__main__':
    main()
