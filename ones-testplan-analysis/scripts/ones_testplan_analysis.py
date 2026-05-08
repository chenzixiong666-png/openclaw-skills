#!/usr/bin/env python3
"""
ONES 测试计划分析脚本
- 登录 ONES
- 查找测试计划
- 拉取计划内所有用例执行结果
- 统计执行概况、优先级分布、模块阻塞分析
- 输出 JSON 供后续飞书文档 / 报告使用
"""

import argparse
import json
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

LOGIN_URL = "https://ones.cn/api/project/auth/login"

# ---------- HTTP helpers ----------

def post_json(url, payload, headers=None, timeout=40):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


# ---------- Auth ----------

def ones_login(email, password):
    data = post_json(LOGIN_URL, {"email": email, "password": password})
    user = (data or {}).get("user") or {}
    team_list = data.get("teams") or []
    token = data.get("token") or user.get("token") or ((data.get("token_info") or {}).get("access_token"))
    if not user or not team_list or not token:
        raise RuntimeError(f"ONES 登录失败或数据不完整: keys={list((data or {}).keys())}")
    return {
        "token": token,
        "user_uuid": user.get("uuid"),
        "team_uuid": team_list[0].get("uuid"),
    }


# ---------- GraphQL ----------

def gql(team_uuid, user_uuid, token, query, timeout=60):
    url = f"https://ones.cn/api/project/team/{team_uuid}/items/graphql"
    headers = {"Ones-User-Id": user_uuid, "Ones-Auth-Token": token}
    return post_json(url, {"query": query}, headers=headers, timeout=timeout)


# ---------- Test plan discovery ----------

def find_testcase_plans(auth):
    """List all test plans visible to the user."""
    query = '{ testcasePlans { uuid name createTime planStatus } }'
    resp = gql(auth["team_uuid"], auth["user_uuid"], auth["token"], query)
    plans = ((resp or {}).get("data") or {}).get("testcasePlans") or []
    return plans


def match_plan(plans, wanted_name):
    """Match plan by name (exact -> normalized -> fuzzy)."""
    if not plans:
        raise RuntimeError("未查询到任何测试计划")
    # exact
    exact = [p for p in plans if (p.get("name") or "") == wanted_name]
    if len(exact) == 1:
        return exact[0]
    # normalized
    norm = lambda s: re.sub(r"\s+", "", (s or "")).lower()
    wanted_norm = norm(wanted_name)
    exact_norm = [p for p in plans if norm(p.get("name")) == wanted_norm]
    if len(exact_norm) == 1:
        return exact_norm[0]
    # fuzzy
    fuzzy = [p for p in plans if wanted_norm in norm(p.get("name")) or norm(p.get("name")) in wanted_norm]
    if len(fuzzy) == 1:
        return fuzzy[0]
    candidates = [p.get("name") for p in (exact or exact_norm or fuzzy or plans[:10])]
    raise RuntimeError(f"计划匹配不唯一或未找到：{wanted_name}；候选：{candidates}")


# ---------- Fetch plan cases with pagination ----------

def fetch_plan_cases(auth, plan_uuid, batch_size=50):
    """Paginate testcasePlanCases for a given plan UUID."""
    all_cases = []
    cursor = ""
    while True:
        after_clause = f', after: "{cursor}"' if cursor else ""
        query = (
            '{ testcasePlanCases('
            f'filter: {{planUUID: "{plan_uuid}"}}, '
            f'limit: {batch_size}{after_clause}'
            ') { uuid name priority result path } }'
        )
        resp = gql(auth["team_uuid"], auth["user_uuid"], auth["token"], query)
        cases = ((resp or {}).get("data") or {}).get("testcasePlanCases") or []
        if not cases:
            break
        all_cases.extend(cases)
        if len(cases) < batch_size:
            break
        cursor = cases[-1].get("uuid") or ""
        if not cursor:
            break
    return all_cases


# ---------- Analysis ----------

RESULT_MAP = {
    "passed": "Passed",
    "failed": "Failed",
    "blocked": "Blocked",
    "skipped": "Skipped",
    "": "Todo",
    None: "Todo",
}

PRIORITY_MAP = {
    "P0": "P0",
    "P1": "P1",
    "P2": "P2",
    "P3": "P3",
    "P4": "P4",
}


def normalize_result(raw):
    if not raw:
        return "Todo"
    return RESULT_MAP.get(raw.lower(), raw)


def normalize_priority(raw):
    if not raw:
        return "未设置"
    upper = raw.upper().strip()
    return PRIORITY_MAP.get(upper, raw)


def extract_module(path_str):
    """Extract top-level and second-level module from path string like '/Root/Module1/Module2/...'."""
    if not path_str:
        return "未分类", "未分类"
    parts = [p.strip() for p in path_str.strip("/").split("/") if p.strip()]
    if len(parts) == 0:
        return "未分类", "未分类"
    top = parts[0] if len(parts) >= 1 else "未分类"
    second = parts[1] if len(parts) >= 2 else top
    return top, second


def analyze_cases(cases):
    """Produce summary statistics from raw cases list."""
    total = len(cases)
    result_dist = Counter()
    priority_dist_by_result = defaultdict(Counter)  # result -> priority -> count
    module_groups = defaultdict(list)  # (top, second) -> [case]

    for c in cases:
        result = normalize_result(c.get("result"))
        priority = normalize_priority(c.get("priority"))
        result_dist[result] += 1
        priority_dist_by_result[result][priority] += 1
        top, second = extract_module(c.get("path"))
        module_groups[(top, second)].append({
            "uuid": c.get("uuid"),
            "name": c.get("name"),
            "priority": priority,
            "result": result,
            "path": c.get("path"),
        })

    # Execution metrics
    executed = result_dist.get("Passed", 0) + result_dist.get("Failed", 0) + result_dist.get("Blocked", 0)
    exec_rate = (executed / total * 100) if total else 0
    pass_rate = (result_dist.get("Passed", 0) / executed * 100) if executed else 0

    # Blocked module analysis
    blocked_modules = {}
    for (top, second), case_list in module_groups.items():
        blocked_in_module = [c for c in case_list if c["result"] == "Blocked"]
        if blocked_in_module:
            total_in_module = len(case_list)
            blocked_count = len(blocked_in_module)
            blocked_modules[f"{top} > {second}"] = {
                "blocked_count": blocked_count,
                "total_in_module": total_in_module,
                "block_rate": round(blocked_count / total_in_module * 100, 1),
                "priority_dist": dict(Counter(c["priority"] for c in blocked_in_module)),
                "sample_cases": [c["name"] for c in blocked_in_module[:5]],
            }
    # Sort by blocked count desc
    blocked_modules = dict(sorted(blocked_modules.items(), key=lambda x: -x[1]["blocked_count"]))

    # Failed priority breakdown
    failed_priority = dict(priority_dist_by_result.get("Failed", {}))

    return {
        "total_cases": total,
        "result_distribution": dict(result_dist),
        "execution_rate_pct": round(exec_rate, 1),
        "pass_rate_pct": round(pass_rate, 1),
        "failed_priority_distribution": failed_priority,
        "blocked_module_analysis": blocked_modules,
        "blocked_total": result_dist.get("Blocked", 0),
        "failed_total": result_dist.get("Failed", 0),
    }


# ---------- Report rendering ----------

def render_markdown(plan_name, analysis):
    lines = []
    lines.append(f"# ONES 测试计划分析：{plan_name}")
    lines.append("")
    lines.append("## 执行概况")
    lines.append("")
    lines.append(f"- **总用例数**：{analysis['total_cases']}")
    for status, count in sorted(analysis["result_distribution"].items(), key=lambda x: -x[1]):
        pct = round(count / analysis["total_cases"] * 100, 1)
        lines.append(f"- {status}：{count}（{pct}%）")
    lines.append(f"- **实际执行率**：{analysis['execution_rate_pct']}%")
    lines.append(f"- **已执行通过率**：{analysis['pass_rate_pct']}%")
    lines.append("")

    if analysis["failed_priority_distribution"]:
        lines.append("## Failed 用例优先级分布")
        lines.append("")
        for p in ["P0", "P1", "P2", "P3", "P4", "未设置"]:
            count = analysis["failed_priority_distribution"].get(p, 0)
            if count:
                lines.append(f"- {p}：{count}")
        lines.append("")

    if analysis["blocked_module_analysis"]:
        lines.append(f"## 阻塞用例分析（共 {analysis['blocked_total']} 条）")
        lines.append("")
        lines.append("### 按模块汇总（按阻塞数量排序）")
        lines.append("")
        for module, info in analysis["blocked_module_analysis"].items():
            block_rate = info["block_rate"]
            label = "⚠️ 全模块阻塞" if block_rate >= 90 else f"阻塞率 {block_rate}%"
            lines.append(f"**{module}**（{info['blocked_count']}/{info['total_in_module']}，{label}）")
            # Priority
            pri_parts = [f"{k}:{v}" for k, v in sorted(info["priority_dist"].items())]
            if pri_parts:
                lines.append(f"- 优先级：{' / '.join(pri_parts)}")
            # Samples
            if info["sample_cases"]:
                lines.append(f"- 示例用例：{'、'.join(info['sample_cases'][:3])}")
            lines.append("")

    return "\n".join(lines)


# ---------- Main ----------

def main():
    ap = argparse.ArgumentParser(description="ONES 测试计划分析")
    ap.add_argument("--email", required=True, help="ONES 登录邮箱")
    ap.add_argument("--password", required=True, help="ONES 密码")
    ap.add_argument("--plan", required=True, help="测试计划名称（支持模糊匹配）")
    ap.add_argument("--json", default="output/testplan-analysis.json", help="JSON 输出路径")
    ap.add_argument("--list-plans", action="store_true", help="仅列出所有测试计划，不做分析")
    args = ap.parse_args()

    # Login
    print("[1/4] 登录 ONES...", flush=True)
    auth = ones_login(args.email, args.password)
    print(f"  ✅ 登录成功 (team: {auth['team_uuid']})")

    # List plans
    print("[2/4] 查询测试计划...", flush=True)
    plans = find_testcase_plans(auth)
    print(f"  ✅ 找到 {len(plans)} 个测试计划")

    if args.list_plans:
        for p in plans:
            print(f"  - {p.get('name')} (uuid: {p.get('uuid')}, status: {p.get('planStatus')})")
        return

    # Match plan
    plan = match_plan(plans, args.plan)
    plan_uuid = plan["uuid"]
    plan_name = plan.get("name") or args.plan
    print(f"  ✅ 匹配计划：{plan_name} (uuid: {plan_uuid})")

    # Fetch cases
    print("[3/4] 拉取测试用例执行数据（分页）...", flush=True)
    cases = fetch_plan_cases(auth, plan_uuid)
    print(f"  ✅ 共获取 {len(cases)} 条用例")

    # Analyze
    print("[4/4] 分析统计...", flush=True)
    analysis = analyze_cases(cases)
    report_md = render_markdown(plan_name, analysis)

    # Output
    payload = {
        "plan": {"uuid": plan_uuid, "name": plan_name},
        "analysis": analysis,
        "report_markdown": report_md,
    }
    Path(args.json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ 分析完成，结果已写入：{args.json}")
    print(f"   总用例：{analysis['total_cases']} | 执行率：{analysis['execution_rate_pct']}% | 通过率：{analysis['pass_rate_pct']}%")
    print(f"   Failed：{analysis['failed_total']} | Blocked：{analysis['blocked_total']}")

    # Also print summary JSON to stdout for piping
    print("\n" + json.dumps({
        "plan_name": plan_name,
        "total_cases": analysis["total_cases"],
        "execution_rate_pct": analysis["execution_rate_pct"],
        "pass_rate_pct": analysis["pass_rate_pct"],
        "failed_total": analysis["failed_total"],
        "blocked_total": analysis["blocked_total"],
        "json_output": args.json,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(str(e), file=sys.stderr)
        sys.exit(1)
