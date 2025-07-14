import os
import requests
import base64
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv
from msal import PublicClientApplication  # type: ignore

load_dotenv()

CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Chat.Read", "Files.Read.All", "Sites.Read.All"]

OUTPUT_DIR = Path("attachments")
OUTPUT_DIR.mkdir(exist_ok=True)

# MSAL setup with token cache for session persistence
token_cache = {}  # could be expanded to file-based for real persistence
app = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)
accounts = app.get_accounts()
if accounts:
    result = app.acquire_token_silent(SCOPES, account=accounts[0])
else:
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise Exception("❌ Failed to start device flow")
    print(f"🔐 Go to {flow['verification_uri']} and enter code: {flow['user_code']}")
    result = app.acquire_token_by_device_flow(flow)

if not result or "access_token" not in result:
    print("❌ Auth failed.")
    print("MSAL response:", result)
    raise SystemExit(1)

access_token = result["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}

# Step 1: List chats
chat_url = "https://graph.microsoft.com/v1.0/me/chats"
chat_resp = requests.get(chat_url, headers=headers)
chats = chat_resp.json().get("value", [])

print(f"💬 Found {len(chats)} chats. Scanning for attachments...\n")

for chat in chats:
    chat_id = chat.get("id")
    topic = chat.get("topic") or "None"
    print(f"🧵 Chat: {topic}")

    messages_url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"
    messages_resp = requests.get(messages_url, headers=headers)
    messages = messages_resp.json().get("value", [])

    for msg in messages:
        for att in msg.get("attachments", []):
            name = att.get("name", "unnamed")
            url = att.get("contentUrl")

            if url and url.startswith("https://"):
                try:
                    encoded_url = base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")
                    content_api = f"https://graph.microsoft.com/v1.0/shares/u!{encoded_url}/driveItem/content"
                    download_resp = requests.get(content_api, headers=headers)

                    if download_resp.ok:
                        file_path = OUTPUT_DIR / name
                        with open(file_path, "wb") as f:
                            f.write(download_resp.content)
                        print(f"📎 Downloaded: {name}\n↳ From Chat: {topic}\n↳ Original SharePoint URL: {url}\n")
                    else:
                        print(f"❌ Failed to download {name}: {download_resp.status_code}")
                        print(f"↳ URL: {url}")
                        try:
                            print("↳ Error:", download_resp.json())
                        except:
                            print("↳ No JSON error body")

                except Exception as e:
                    print(f"⚠️ Exception downloading {name}: {e}")

print("\n✅ All attachments fetched.")
