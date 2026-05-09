---
name: ones-project-management
description: |
  Read and write to ONES project management system via REST/GraphQL API. Use when user mentions ONES, project tasks, defects, requirements, milestones, dashboard cards (风险预警/本周总结), or project overview content. Covers: authentication, task/defect/requirement CRUD, dashboard card content updates, comment read/write, user lookup, and milestone queries.
---

# ONES Project Management Skill

Operate ONES (ones.cn) project management system through its REST and GraphQL APIs.

## ⛔ Safety Rules

- **NEVER execute delete operations** (deleteCard, deleteTask, etc.)
- Only read and write (create/update) operations are permitted
- Always backup card content before modifying

## Authentication

Login to get JWT token (valid ~6 months):

```
POST https://ones.cn/api/project/auth/login
Content-Type: application/json
{"email": "<user_email>", "password": "<password>"}
```

All subsequent requests require headers:
- `Ones-User-Id: <user_uuid>` (from login response)
- `Ones-Auth-Token: <jwt_token>`
- `Content-Type: application/json`

Store credentials and team/org UUIDs in the workspace `TOOLS.md` or memory files — never hardcode.

## Setup Checklist

1. Obtain ONES account credentials from user
2. Call login API → save Token + User UUID
3. Record Team UUID (from ONES URL: `/team/<TEAM>/`)
4. Query target project UUID
5. Query project issueType + scope mapping (see [api-reference.md](references/api-reference.md))
6. Query project overview component UUID (from URL: `/component/<COMPONENT>/`)

## Core Operations

### Read Tasks / Requirements / Defects

```
POST https://ones.cn/api/project/team/{TEAM}/items/graphql

{"query": "{ tasks(filter: {project_in: [\"<PROJECT_UUID>\"]}, limit: 500) { uuid name number status { name category } assign { name uuid } owner { name uuid } priority { value } issueType { uuid name } issueTypeScope { uuid } parent { name number uuid } } }"}
```

Filter by type: add `issueType_in: ["<type_uuid>"]` to filter.

### Create Tasks / Requirements / Defects

```
POST https://ones.cn/api/project/team/{TEAM}/tasks/add

{"tasks": [{"uuid": "<16-char-alphanum>", "assign": "<user_uuid>", "name": "Title", "project_uuid": "<project_uuid>", "issue_type_uuid": "<type_uuid>", "issue_type_scope_uuid": "<scope_uuid>"}]}
```

**Critical**: UUID must be exactly 16 alphanumeric chars. Both `issue_type_uuid` and `issue_type_scope_uuid` are required (404 without scope).

Generate UUID: `python3 -c "import random,string; print(''.join(random.choice(string.ascii_letters+string.digits) for _ in range(16)))"`

### Read Dashboard Cards (风险预警 / 本周总结)

```
POST https://ones.cn/api/project/team/{TEAM}/items/graphql

{"query": "{ cards(filter: {objectId_in: [\"<COMPONENT_UUID>\"], status_in: [\"normal\"]}) { uuid name type config } }"}
```

`config` is JSON string containing `content` (HTML rich text) and `project_uuid`.

### Update Dashboard Card Content

```
POST https://ones.cn/api/project/team/{TEAM}/items/graphql

{"query": "mutation($config: String!) { updateCard(key: \"card-<CARD_UUID>\", config: $config) { uuid name } }", "variables": {"config": "{\"content\": \"<HTML>\", \"project_uuid\": \"<PROJECT_UUID>\"}"}}
```

**Note**: Cannot create cards via API (addCard returns 500). User must create card manually in ONES UI (choose "公告/announcement" type), then agent updates content.

### Read Comments

```
GET https://ones.cn/api/project/team/{TEAM}/task/{TASK_UUID}/messages
```

### Write Comments

```
POST https://ones.cn/api/project/team/{TEAM}/task/{TASK_UUID}/send_message

{"uuid": "<unique_id>", "text": "Comment text", "type": "discussion"}
```

### Query Users

```graphql
{ users(limit: 200) { uuid name email } }
```

### Query Milestones (read-only)

```graphql
{ milestones(limit: 50) { uuid name } }
```

## Known Limitations

- Task update (change owner/status): PUT/PATCH → 404, POST /tasks/update → 500
- Card creation via API: addCard → 500 (must create manually)
- GraphQL unavailable fields: `description_text`, `create_time`, `discussion_count`

## References

- [API Reference](references/api-reference.md) — Full endpoint details, GraphQL fields, issueType/scope discovery
