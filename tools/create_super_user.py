import sys
from pathlib import Path

parent_folder = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_folder))

import dotenv
dotenv.load_dotenv()

import argparse
from domains.authentication.services.user_service import create_user
from domains.authentication.schemas.user_schema import CreateUserResponseSchema, CreateUserRequestSchema


parser = argparse.ArgumentParser(description="Create a new user")

parser.add_argument("--user_name", required=True, help="Username")
parser.add_argument("--email", required=True, help="Email")
parser.add_argument("--phone", required=True, help="Phone")
parser.add_argument("--address", required=True, help="Address")
parser.add_argument("--password", required=True, help="Password")

args = parser.parse_args()

def main():
    created_user_response = create_user(CreateUserRequestSchema(
        user_name=args.user_name,
        email=args.email,
        phone=args.phone,
        address=args.address,
        password=args.password
    ))
    print(f"Created user with ID: {created_user_response.user_id}")

if __name__ == '__main__':
    main()

