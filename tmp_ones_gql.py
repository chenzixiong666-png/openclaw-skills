import json
import sys
import urllib.request
import urllib.error

TEAM = sys.argv[1]
USER = sys.argv[2]
TOKEN = sys.argv[3]
QUERY = sys.argv[4]

payload = json.dumps({"query": QUERY}).encode()
req = urllib.request.Request(
    f"https://ones.cn/api/project/team/{TEAM}/items/graphql",
    data=payload,
    headers={
        "Ones-User-Id": USER,
        "Ones-Auth-Token": TOKEN,
        "Content-Type": "application/json",
    },
)
try:
    with urllib.request.urlopen(req, timeout=20) as resp:
        print(resp.read().decode())
except urllib.error.HTTPError as e:
    print(e.read().decode())
    raise
