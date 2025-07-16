import os
from msal import PublicClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

app = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)
flow = app.initiate_device_flow(scopes=SCOPES)

if "user_code" not in flow:
    raise Exception("Failed to initiate device login.")

print(f"🔐 Go to {flow['verification_uri']} and enter code: {flow['user_code']}")
result = app.acquire_token_by_device_flow(flow)

if "access_token" in result:
    print("\nAccess token:")
    print(result["access_token"])
else:
    print("Authentication failed:", result)
