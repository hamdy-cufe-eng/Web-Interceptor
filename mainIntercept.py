from mitmproxy import http ,ctx
import json
import requests
import threading
import time

TARGET_PREFIX = ""
TARGET_SUFFIX = "/all"
 # Store the fixed response
fixed_response_cache = None

FIXED_GAME_ID = ""  # Game ID to copy response from
API_ENDPOINT = ""

cookies = {
    "visitorid": ":2c54:ffff:41.238.192.213",
    "me": '{"deviceId":"17895936-9bca-11ef-a4d4-835f3b048baa"}',
    "GCLB": "COnEr9DStOjI2QEQAw",
    "theme_cache_id": "721168121072fd96d3bb1c5590ae0bf6a2249629:3ab55f4a-9bca-11ef-8ab8-9f80a44f27c8",
    "intercom-session-qzot1t7g": "UFgwbkhKTTFoTDFkTkU3LzllR2JRc09jQUtoUGxlM0NQSVJZSFV5bTFTNDBxQ2V0WHpNWGc3NUYvNzNZY29nV1ZYdlpvV3lVaWprdHdzY01NL2dLenhkSDB1R05NUUNTREg3bmNTUHdvejg9LS13bUQ0YUVJVG1QZStRbkV4N0hibU9nPT0=--d3cd4354a9b3e1916fc201f39c8884911c258fb5",
    "intercom-device-id-qzot1t7g": "2e041bbe-4733-40cc-9e10-6a7518935a41",
    "psid": "327d38ff-9d20-4c79-9e84-b0a775d01277",
    "asset_push": "20250313132332;567b2,af051,da310,a7fc5,215a5",
    "PHPSESSID": "03a398efb2b8141f61b009889fe271b9",
    "__cf_bm": "55QC.NTJefdnByGA_6ESFH1aQ_cinvpgqi1NY4UtAb8-1741940036-1.0.1.1-P5TfDaPLD0vMI9w7kfvA0byZCdniDukyk7oEFfSoqZSwppKMtAXsoEOtgMqntjt_A5FgEWut5HNjcpwGEe8.A5QvNfLnHvv2XzeG_a.scCKeh22p5yV9mNpKbdM9frct",
    "amp_5cc41a": "17895936-9bca-11ef-a4d4-835f3b048baa.NDAwNjc3OTIx..1im9hdcjt.1im9s49v5.h.b0.bh",
    "ATTRIBUTION_V1": '{"initialAttribution":{"source":"unknown","medium":"unknown","campaign":null,"term":null,"content":null,"route":"/home","referer":"unknown","version":"1.0.0","createDateTime":"1739626358"},"lastAttribution":{"source":"unknown","medium":"unknown","campaign":null,"term":null,"content":null,"route":"/callback/auth/service/analysis?game_id=136139545156&game_type=live","referer":"unknown","version":"1.0.0","createDateTime":"1741941202"}}'
}
cached_fixed_response = None
def fetch_fixed_response():
    """Continuously fetch and store the fixed game response in a loop."""
    global cached_fixed_response

    while True:
        try:
            r = requests.get(url=API_ENDPOINT, cookies=cookies, verify=False)
            if r.status_code == 200:
                cached_fixed_response = r.text
                print(f"✅ Captured fixed game response: {API_ENDPOINT}")
            else:
                print(f"⚠️ Failed to fetch fixed response, status: {r.status_code}")

        except Exception as e:
            print(f"❌ Error fetching fixed response: {e}")

        time.sleep(10)  # ✅ Fetch every 10 seconds (adjust as needed)

threading.Thread(target=fetch_fixed_response, daemon=True).start()

def response(flow: http.HTTPFlow) -> None:

    global cached_fixed_response
    url = flow.request.url

    # ✅ Modification 1: Change `analysisLogExists` in game analysis response
    if url.startswith(TARGET_PREFIX) and url.endswith(TARGET_SUFFIX):
        print(f"✅ Intercepted analysis log response: {url}")

        try:
            data = json.loads(flow.response.text)
            if "analysisLogExists" in data:
                data["analysisLogExists"] = True
            flow.response.text = json.dumps(data)
            print("✍️ Modified analysisLogExists to True.")

        except Exception as e:
            print(f"❌ Error modifying analysisLogExists: {e}")

    elif url.startswith(ANALYSIS_URL) and "game_id=" in url:



        fixed_response_cache = json.loads(cached_fixed_response)

        print(f"🔄 Intercepted Analasis request: {url}")
        flow.response = http.Response.make(
            200,
            json.dumps(fixed_response_cache),
            {"Content-Type": "application/json"}
        )
