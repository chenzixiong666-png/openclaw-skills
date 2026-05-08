---
name: ones-weekly-report
description: Generate weekly report style summaries from ONES project data. Use when the user wants a 周报 / 测试周报 / 项目周报 based on ONES, especially when they provide ONES account credentials plus a project name and want output in report format, summary statistics, major defects, status distribution, or Feishu doc delivery. Supports cross-project reuse by discovering the target ONES project, identifying project-specific defect issue types/scopes, aggregating selected defect categories, and formatting output in the established weekly report style.
---

# ONES Weekly Report

Generate a reusable weekly-report summary from ONES project data.

## Overview

Take ONES credentials and a target project name, discover the real project UUID and project-specific issue type mappings, then aggregate defect data and format it into a weekly-report style output. Prefer structured summaries first, then Feishu doc output when the user asks to generate or publish a report.

## Workflow

### 1. Validate the input

Collect or confirm these inputs:
- ONES email
- ONES password
- target project name
- optional target defect categories
- optional reporting window / round / version / manpower fields
- optional delivery target (default to Feishu doc when the user says 周报 / 飞书周报 / 按昨天周报格式)

If the user only gives a project name, ask for credentials unless valid reusable credentials are already available in the current secure context.

### 2. Authenticate to ONES

Use the login API:

```http
POST https://ones.cn/api/project/auth/login
Content-Type: application/json
{"email":"<email>","password":"<password>"}
```

Store these runtime values for subsequent requests:
- `Ones-User-Id`
- `Ones-Auth-Token`
- team UUID

Do not hardcode credentials inside the skill. Reuse secure local notes only when explicitly available and appropriate.

### 3. Discover the target project

Query project list and match by project name.

Preferred GraphQL root query shape:

```graphql
{ projects(limit: 200) { uuid name key } }
```

Match the requested name conservatively:
- first exact match
- then case-insensitive exact match
- then normalized fuzzy match only if one clear winner exists

If multiple candidate projects match, stop and ask the user to choose.

### 4. Pull project tasks and infer defect categories

Do not assume every project uses the same issueType UUID or scope UUID.

Query enough project tasks to infer the issue types actually used in that project:

```graphql
{
  tasks(filter: {project_in: ["<PROJECT_UUID>"]}, limit: 500) {
    uuid
    name
    number
    status { name category }
    priority { value }
    issueType { uuid name }
    issueTypeScope { uuid }
    assign { name uuid }
    owner { name uuid }
  }
}
```

Build a frequency table of `(issueType.name, issueType.uuid, issueTypeScope.uuid)` and identify the project-specific categories the user asked for.

Typical target categories may include:
- 固件缺陷
- RN缺陷
- 后台缺陷
- 需求缺陷
- Android缺陷
- iOS缺陷
- 硬件缺陷
- 结构缺陷

Use project evidence, not global assumptions.

### 5. Aggregate the requested report data

For each requested defect category, compute:
- total count
- status distribution
- priority distribution
- detailed rows: 编号 / 标题 / 状态 / 状态分类 / 优先级 / 处理人 / 负责人

When the user asks for a weekly report summary, also identify severe or notable defects:
- prefer 严重 / 较高 priority items
- include unresolved or regression-related items first
- if too many, shortlist the most report-worthy issues

### 6. Format the weekly report output

Default output should follow the established report style:
- 项目基本信息
- 进展与缺陷
- 严重缺陷
- 缺陷看板
- 风险与需求
- 下周测试计划

Keep the wording compact and editable. When some fields are unknown, mark them clearly as 待确认 / 待补充 instead of inventing values.

When the user wants the ONES defect summary merged directly into the 周报模板的“缺陷看板”, prefer this compact board format by default:
- only keep the requested target categories; for this user preference default to：固件缺陷 / RN缺陷 / 后台缺陷 / 需求缺陷
- exclude 回归通过 / 关闭 / 非bug unless the user explicitly asks otherwise
- first list total count plus each category count
- then group issues by 模块 under each category
- add one short summary sentence under each module
- each issue line should be compact, preferring: `缺陷简称【状态】【优先级】[【跳转】](链接)`
- use `【跳转】` as the hyperlink text instead of exposing the raw URL inline
- keep the whole section short enough to paste directly into Feishu weekly reports

If the user asked for a Feishu weekly report, treat this formatting step as preparation for immediate Feishu publishing rather than a terminal text-only result.

## Feishu delivery

When the user asks to generate a Feishu document or says things like “生成飞书周报 / 出飞书周报 / 按昨天周报格式发飞书文档”, treat Feishu delivery as the default end-to-end path instead of a separate optional post-step.

Execute this flow:
1. Run `scripts/ones_fetch_and_summarize.py`
2. Read the generated JSON to obtain:
   - `report_title`
   - `report_markdown`
   - `basic_info_table`
3. Create a Feishu doc immediately
4. Write `report_markdown`
5. Add the 项目基本信息 table separately with `create_table_with_values` using `basic_info_table`
6. If the user supplied screenshots or chart images, upload them after the defect board section
7. If folder creation fails with 403, fall back to the default writable location and clearly tell the user
8. Return the final doc link as the primary output

Default behavior:
- If the user explicitly asks for a Feishu weekly report, do not stop at JSON / CSV unless the write step fails
- JSON / CSV become intermediate artifacts, not the final user-facing deliverable
- Prefer one-shot completion: statistics + formatted content + Feishu link in the same turn when inputs are sufficient

Important:
- Do not rely on markdown tables for Docx tables
- Prefer fewer large writes over many tiny edits
- Keep 阻塞情况 user-editable; do not invent detailed blockers unless the user provided them
- Use caller-provided report fields when available; otherwise fill with `待确认` / `待补充` / `/`

## Output expectations

### Structured summary

Provide at minimum:
- target project name
- selected defect categories
- total counts
- status distribution
- priority distribution
- severe defect shortlist

### CSV-friendly export

When useful, prepare rows with columns:
- 缺陷类型
- 编号
- 标题
- 状态
- 状态分类
- 优先级
- 处理人
- 负责人

### Feishu report

Use yesterday/established weekly report style when the user asks for “按昨天周报格式” or similar wording.

When the user explicitly requests Feishu delivery, the expected final deliverable is:
- a created Feishu doc
- populated report content
- populated 项目基本信息 table
- final shareable doc link

Do not treat raw JSON / CSV as sufficient final output in that case unless doc creation/write fails.

## Known pitfalls

- Browser access to ONES may fail due to environment policy; prefer API when possible
- `project_in` must use the real project UUID, not the human-readable project code
- Some GraphQL filters may reject formatted issue keys like `W1149-195794`; project-level task pull + post-filtering is often more reliable
- Console encoding may garble Chinese during CLI inspection; preserve raw API data and post-process carefully
- Different projects may expose different issue types/scopes for seemingly similar categories
- Feishu target folder creation may return 403 even when plain document creation succeeds

## Resources

### references/
- Put reusable weekly report structure, field mapping notes, and ONES category heuristics here if the skill grows.

### scripts/
- Add deterministic helper scripts for ONES login, task pull, aggregation, or CSV export if repeated execution becomes common.
