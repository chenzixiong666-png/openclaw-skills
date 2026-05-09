import json
import sys
import urllib.request

TEAM = sys.argv[1]
USER = sys.argv[2]
TOKEN = sys.argv[3]
KEY = sys.argv[4]

query = f'''{{
  tasks(filter: {{number_in: ["{KEY}"]}}, limit: 20) {{
    uuid
    name
    number
    status {{ name category }}
    assign {{ name uuid }}
    owner {{ name uuid }}
    priority {{ value }}
    issueType {{ uuid name }}
    issueTypeScope {{ uuid }}
    parent {{ name number uuid }}
  }}
}}'''

payload = json.dumps({"query": query}).encode()
req = urllib.request.Request(
    f"https://ones.cn/api/project/team/{TEAM}/items/graphql",
    data=payload,
    headers={
        "Ones-User-Id": USER,
        "Ones-Auth-Token": TOKEN,
        "Content-Type": "application/json",
    },
)
with urllib.request.urlopen(req, timeout=20) as resp:
    print(resp.read().decode())
