from dotenv import load_dotenv
import os

print("Before load_dotenv:")
print(f"CLIENT_ID: {os.getenv('CLIENT_ID')}")
print(f"TENANT_ID: {os.getenv('TENANT_ID')}")

load_dotenv()

print("\nAfter load_dotenv:")
print(f"CLIENT_ID: {os.getenv('CLIENT_ID')}")
print(f"TENANT_ID: {os.getenv('TENANT_ID')}")

# Also check if .env file exists and is readable
import os.path
print(f"\n.env file exists: {os.path.exists('.env')}")