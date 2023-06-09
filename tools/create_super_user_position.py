import sys
from pathlib import Path

parent_folder = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_folder))

import dotenv
dotenv.load_dotenv()

import argparse
from domains.authentication.services.user_position_service import create_user_position, get_user_by_id, get_position_by_name
from domains.authentication.schemas.user_position_schema import CreateUserPositionResponseSchema, CreateUserPositionRequestSchema
from repository import SessionLocal

parser = argparse.ArgumentParser(description="Create a new user position")

parser.add_argument("--user_id", required=True, help="User_id")
parser.add_argument("--role", required=True, help="Role")

args = parser.parse_args()

# Create a hierarchy dict to hold position creation order
position_hierarchy = {
    'admin': ['admin', 'manager', 'casher'],
    'manager': ['manager', 'casher'],
    'casher': ['casher']
}

def main():
    # Initiate a new session
    db = SessionLocal()
    try:
        # Check if position_name entered by user exists in our hierarchy
        if args.role not in position_hierarchy:
            raise ValueError(f"Invalid position_name: {args.role}")

        # Create user_position entries based on the hierarchy
        for role in position_hierarchy[args.role]:
            role = get_position_by_name(role, db)
            if not role:
                raise ValueError(f"No position found with name {role}")

            create_user_position(CreateUserPositionRequestSchema(
                user_id=args.user_id,
                position_id=role.position_id
            ), db)

            print(f"User position with user_id: {args.user_id} and position_name: {role} created successfully")

    except Exception as e:
        print(e)
    finally:
        db.close()

if __name__ == '__main__':
    main()
