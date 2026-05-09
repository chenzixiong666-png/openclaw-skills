---
name: ones-testplan-analysis
description: Analyze ONES test plans - execution statistics, priority distribution, blocked module analysis. Use when user mentions 测试计划分析, 用例执行率, 阻塞分析, blocked cases, test plan status, or wants to know pass/fail/blocked distribution of a specific ONES test plan. Also triggers on requests like "帮我看下测试计划执行情况", "哪些模块阻塞了", "测试计划进度".
---

# ONES Test Plan Analysis

Analyze test plan execution data from ONES: statistics, priority breakdown, blocked module identification.

## Overview

Given ONES credentials and a test plan name, this skill:
1. Authenticates to ONES
2. Finds the target test plan
3. Pulls all case execution results (paginated)
4. Computes execution rate, pass rate, failed priority distribution
5. Groups blocked cases by module and identifies fully-blocked modules
6. Outputs structured JSON + markdown report
7. Optionally delivers to Feishu doc

## Quick Start

Run the analysis script:

```bash
python scripts/ones_testplan_analysis.py \
  --email "<ONES_EMAIL>" \
  --password "<ONES_PASSWORD>" \
  --plan "测试计划名称"
```

List all available plans first:

```bash
python scripts/ones_testplan_analysis.py \
  --email "<EMAIL>" --password "<PASSWORD>" \
  --list-plans
```

Output goes to `output/testplan-analysis.json` by default (override with `--json <path>`).

## Workflow

### 1. Collect inputs

Required:
- ONES email
- ONES password
- Test plan name (supports fuzzy matching)

Optional:
- `--json <path>` — custom output path
- `--list-plans` — only list plans, skip analysis

If the user doesn't provide credentials, ask. If a valid session is active from a prior turn, reuse it.

### 2. Run the script

Execute `scripts/ones_testplan_analysis.py`. It handles:
- Login
- Plan discovery and matching
- Paginated case fetching (50/batch, auto-pagination)
- Statistical analysis
- JSON + markdown report generation

### 3. Interpret the output JSON

Structure of `output/testplan-analysis.json`:

```json
{
  "plan": { "uuid": "...", "name": "..." },
  "analysis": {
    "total_cases": 6893,
    "result_distribution": { "Passed": 637, "Failed": 199, "Blocked": 759, "Skipped": 4904, "Todo": 394 },
    "execution_rate_pct": 28.9,
    "pass_rate_pct": 76.2,
    "failed_priority_distribution": { "P0": 41, "P1": 101, "P2": 51, "P3": 5, "P4": 1 },
    "blocked_module_analysis": {
      "模块A > 子模块": { "blocked_count": 35, "total_in_module": 35, "block_rate": 100.0, "priority_dist": {...}, "sample_cases": [...] }
    },
    "blocked_total": 759,
    "failed_total": 199
  },
  "report_markdown": "..."
}
```

### 4. Present results

Default output format:
- **Console**: Summary stats printed to stdout
- **JSON file**: Full structured data for programmatic use
- **Markdown**: `report_markdown` field contains formatted report

When the user wants a Feishu document:
1. Read the generated JSON
2. Use `report_markdown` to create a Feishu doc via `feishu_doc` action
3. Default folder: `A1KmfkVu5lM4Q1dpgdEchSYEnQd`

### 5. Advanced analysis (manual follow-up)

After running the script, the agent can perform deeper analysis:
- Identify fully-blocked modules (block_rate >= 90%) and flag them
- Classify blocking reasons (firmware not ready, feature not implemented, dependency not met)
- Cross-reference with project defect data from `ones-weekly-report` skill
- Compare multiple plan snapshots over time

## Output Interpretation Guide

| Metric | Meaning |
|--------|---------|
| execution_rate_pct | (Passed + Failed + Blocked) / Total |
| pass_rate_pct | Passed / (Passed + Failed + Blocked) |
| block_rate per module | Blocked in module / Total in module |
| ⚠️ 全模块阻塞 | block_rate >= 90% — entire feature blocked |

## GraphQL Reference

See `references/graphql-notes.md` for ONES API query shapes and field details.

## Known Pitfalls

- Large plans (>5000 cases) require many pagination rounds; script handles automatically but takes time
- `result` field is empty string for Todo cases, not null in all environments
- `path` format may vary between projects; top-level category extraction uses `/` splitting
- Plan names may have subtle whitespace differences; fuzzy matching handles this
- Session tokens expire; re-login if 401 errors occur
- Some plans may have cases with no priority set; these are grouped as "未设置"
