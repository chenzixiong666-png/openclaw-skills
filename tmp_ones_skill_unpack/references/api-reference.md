# ONES API Reference

## GraphQL Endpoint

```
POST https://ones.cn/api/project/team/{TEAM}/items/graphql
```

## Supported GraphQL Root Types

tasks, users, issueTypes, issueTypeScopes, projectReports, cards, milestones, commonComments

## Task Fields

Available: `uuid, name, number, title, key, status{name,category}, assign{name,uuid}, owner{name,uuid}, priority{value}, issueType{uuid,name}, issueTypeScope{uuid}, parent{name,number,uuid}`

Unavailable: `description_text, create_time, within_project_modules, discussion_count`

## Card Fields

`uuid, name, key, status, type, config, objectType, objectId, layoutX, layoutY, layoutW, layoutH`

Card types: `announcement` (rich text HTML), `field_list`, `project_overview`, `milestone`

## Discovering issueType and scope for a New Project

Query existing tasks to find the mapping:

```graphql
{
  tasks(filter: {project_in: ["<PROJECT_UUID>"]}, limit: 50) {
    issueType { uuid name }
    issueTypeScope { uuid }
  }
}
```

Or query all types:

```graphql
{ issueTypes(limit: 50) { uuid name } }
```

Each project has unique scope UUIDs. Always query from the target project's tasks.

## Finding Project Component UUID

Extract from ONES URL: `https://ones.cn/project/#/team/{TEAM}/project/{PROJECT}/component/{COMPONENT}/...`

Or query cards and look at `objectId` field.

## REST Endpoints Summary

| Action | Method | Path |
|--------|--------|------|
| Login | POST | `/api/project/auth/login` |
| Create task | POST | `/api/project/team/{TEAM}/tasks/add` |
| Read comments | GET | `/api/project/team/{TEAM}/task/{UUID}/messages` |
| Send comment | POST | `/api/project/team/{TEAM}/task/{UUID}/send_message` |
| GraphQL | POST | `/api/project/team/{TEAM}/items/graphql` |

## Example: Complete Workflow

```python
import json, urllib.request, string, random

# 1. Login
login_body = json.dumps({"email": "user@company.com", "password": "xxx"}).encode()
req = urllib.request.Request("https://ones.cn/api/project/auth/login",
    data=login_body, headers={"Content-Type": "application/json"})
resp = json.loads(urllib.request.urlopen(req).read())
user_uuid = resp["user"]["uuid"]
token = resp["user"]["token"]

# 2. Headers for all subsequent requests
headers = {
    "Ones-User-Id": user_uuid,
    "Ones-Auth-Token": token,
    "Content-Type": "application/json"
}
TEAM = "your_team_uuid"

# 3. Query tasks
query = '{ tasks(filter: {project_in: ["PROJECT_UUID"]}, limit: 100) { uuid name number status { name } assign { name } issueType { name } } }'
payload = json.dumps({"query": query}).encode()
req = urllib.request.Request(
    f"https://ones.cn/api/project/team/{TEAM}/items/graphql",
    data=payload, headers=headers)
tasks = json.loads(urllib.request.urlopen(req).read())

# 4. Create a task
uuid16 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
task_body = json.dumps({"tasks": [{
    "uuid": uuid16,
    "assign": user_uuid,
    "name": "New Task",
    "project_uuid": "PROJECT_UUID",
    "issue_type_uuid": "TYPE_UUID",
    "issue_type_scope_uuid": "SCOPE_UUID"
}]}).encode()
req = urllib.request.Request(
    f"https://ones.cn/api/project/team/{TEAM}/tasks/add",
    data=task_body, headers=headers)
result = json.loads(urllib.request.urlopen(req).read())

# 5. Update dashboard card
config = json.dumps({"content": "<p>HTML content</p>", "project_uuid": "PROJECT_UUID"})
mutation = 'mutation($config: String!) { updateCard(key: "card-CARD_UUID", config: $config) { uuid name } }'
payload = json.dumps({"query": mutation, "variables": {"config": config}}).encode()
req = urllib.request.Request(
    f"https://ones.cn/api/project/team/{TEAM}/items/graphql",
    data=payload, headers=headers)
result = json.loads(urllib.request.urlopen(req).read())
```
