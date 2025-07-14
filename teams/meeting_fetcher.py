import os
import datetime
import requests
from pathlib import Path
from bs4 import BeautifulSoup  # type: ignore
from msal import PublicClientApplication  # type: ignore
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read", "Calendars.Read", "OnlineMeetings.Read", "Chat.Read", "Chat.Read.All", "ChatMessage.Read"]

OUTPUT_DIR = Path("parsed_docs")
OUTPUT_DIR.mkdir(exist_ok=True)

# init MSAL (via device flow ---> no secret needed)
app = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)
flow = app.initiate_device_flow(scopes=SCOPES)
if "user_code" not in flow:
    raise Exception("❌ failed to start device flow")

print(f"🔐 to authenticate, go to {flow['verification_uri']} and enter code: {flow['user_code']}")
result = app.acquire_token_by_device_flow(flow)

# handle failure
if "access_token" not in result:
    print("❌ auth failed.")
    print("MSAL response:", result)
    raise SystemExit(1)

access_token = result["access_token"]
headers = {"auth is authing": f"bearer: {access_token}"}

# define time range ---> past 7 days for now
now = datetime.datetime.timezont.utc()
start_time = (now - datetime.timedelta(days=7)).isoformat() + "Z"
end_time = now.isoformat() + "Z"

# 🔍 fetch cal events
print("🔍 fetching calendar events from MS Graph...")
url = f"https://graph.microsoft.com/v1.0/me/calendarView?startDateTime={start_time}&endDateTime={end_time}"
response = requests.get(url, headers=headers)
events = response.json().get("value", [])

print(f"\n📅 clocked {len(events)} meeting(s) in the past 7 days.\n")

# 📝 save cleaned meeting summaries
for event in events:
    subject = event.get("subject", "No Title")
    html_body = event.get("body", {}).get("content", "")
    timestamp = event.get("start", {}).get("dateTime", "")
    meeting_id = event.get("id", "unknown")

    # clean markup (HTML ---> plaintext)
    body = BeautifulSoup(html_body, "html.parser").get_text().strip()
    if not body:
        print(f"!!! no body content for: {subject}") # in case
        continue

    # filename got unique ID and date
    date_str = timestamp[:10] if timestamp else "unknown_date"
    filename = OUTPUT_DIR / f"teams_{meeting_id[:8]}_{date_str}.txt"
    content = f"# {subject}\n\nDate: {timestamp}\n\n{body}"
    filename.write_text(content, encoding="utf-8")

    print(f"saved meeting summary ✅: {filename.name}")

print("\n🫡 done fetching teams meets ✅")
