import os
import requests
from msal import PublicClientApplication, SerializableTokenCache  # type: ignore
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = [
    "User.Read",
    "Calendars.Read",
    "OnlineMeetings.Read",
    "Files.Read",
    "Mail.Read",
    "Sites.Read.All",
    "Presence.Read.All",
    "People.Read"
]

# persist token cache 
TOKEN_CACHE_PATH = ".msal_cache.bin"
token_cache = SerializableTokenCache()
if os.path.exists(TOKEN_CACHE_PATH):
    token_cache.deserialize(open(TOKEN_CACHE_PATH, "r").read())

app = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY, token_cache=token_cache)

# peep silent login first
accounts = app.get_accounts()
if accounts:
    result = app.acquire_token_silent(SCOPES, account=accounts[0])
else:
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise Exception("❌ failed to start device flow")
    print(f"🔐 Go to {flow['verification_uri']} and enter code: {flow['user_code']}")
    result = app.acquire_token_by_device_flow(flow)

if "access_token" not in result:
    print("❌ auth failed.\n", result)
    exit(1)

# save token cache to disk
with open(TOKEN_CACHE_PATH, "w") as f:
    f.write(token_cache.serialize())

access_token = result["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}

# define/call useful MS Graph API endpoints
def graph_call(label, url):
    print(f"\n🔎 {label}:")
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        if isinstance(data, dict) and "value" in data:
            for i, item in enumerate(data["value"][:5]):
                print(f"{i+1}. {item.get('subject') or item.get('displayName') or item.get('name')}")
        else:
            print(data)
    else:
        print(f"❌ Error ({r.status_code}):", r.json())

# calendar events
graph_call("Recent Calendar Events", "https://graph.microsoft.com/v1.0/me/calendar/events?$top=5")

# recent files
graph_call("Recent Files", "https://graph.microsoft.com/v1.0/me/drive/recent")

# my teams presence
graph_call("Presence Status", "https://graph.microsoft.com/v1.0/me/presence")

# mail preview
graph_call("Recent Emails", "https://graph.microsoft.com/v1.0/me/messages?$top=5")

# teams meeting history
graph_call("Online Meetings", "https://graph.microsoft.com/v1.0/me/onlineMeetings?$top=5")

# peeps i interact with
graph_call("Frequent Contacts", "https://graph.microsoft.com/v1.0/me/people?$top=5")

print("\nms-graph status check complete ✅")
