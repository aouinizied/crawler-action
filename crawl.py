import urllib.request
import json
from datetime import datetime

API_URL = (
    "https://www.clicrdv.com/api/v2/availabletimeslots"
    "?group_id=188769&time_format=datetime&appointments[0][intervention_id]=3453199"
)
NTFY_TOPIC = "clicrdv-8f3k2q9x"
THRESHOLD = datetime(2026, 4, 15, 9, 0)

response = urllib.request.urlopen(API_URL)
data = json.loads(response.read())

early_slots = [
    s for s in data.get("availabletimeslots", [])
    if datetime.strptime(s["start"], "%Y-%m-%d %H:%M:%S") < THRESHOLD
]

if early_slots:
    lines = [f"- {s['start']}" for s in early_slots]
    message = f"{len(early_slots)} slot(s) available before {THRESHOLD}!\n" + "\n".join(lines)
    req = urllib.request.Request(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode(),
        headers={"Title": "ClicRDV Slot Alert"},
    )
    urllib.request.urlopen(req)
    print(f"Notification sent: {len(early_slots)} slot(s) found")
else:
    print("No slots before threshold")
