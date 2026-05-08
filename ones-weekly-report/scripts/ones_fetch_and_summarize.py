#!/usr/bin/env python3
import argparse
import csv
import json
import re
import sys
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path

LOGIN_URL = "https://ones.cn/api/project/auth/login"
DEFAULT_CATEGORIES = ["固件缺陷", "RN缺陷", "后台缺陷", "需求缺陷"]


def post_json(url, payload, headers=None, timeout=40):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def ones_login(email, password):
    data = post_json(LOGIN_URL, {"email": email, "password": password})
    user = (((data or {}).get("user") or {}))
    team_list = data.get("teams") or []
    token = data.get("token") or (((data.get("user") or {}).get("token")) or ((data.get("token_info") or {}).get("access_token")))
    if not user or not team_list or not token:
        raise RuntimeError(f"ONES 登录成功但返回数据不完整: keys={list((data or {}).keys())}")
    return {
        "token": token,
        "user_uuid": user.get("uuid"),
        "team_uuid": team_list[0].get("uuid"),
        "raw": data,
    }


def gql(team_uuid, user_uuid, token, query):
    url = f"https://ones.cn/api/project/team/{team_uuid}/items/graphql"
    headers = {"Ones-User-Id": user_uuid, "Ones-Auth-Token": token}
    return post_json(url, {"query": query}, headers=headers)


def normalize(text):
    if text is None:
        return ""
    return re.sub(r"\s+", "", str(text)).lower()


def find_project(projects, wanted_name):
    if not projects:
        raise RuntimeError("未查询到任何项目")
    exact = [p for p in projects if (p.get("name") or "") == wanted_name]
    if len(exact) == 1:
        return exact[0]
    wanted_norm = normalize(wanted_name)
    exact_norm = [p for p in projects if normalize(p.get("name") or "") == wanted_norm]
    if len(exact_norm) == 1:
        return exact_norm[0]
    fuzzy = [
        p for p in projects
        if wanted_norm in normalize(p.get("name") or "") or normalize(p.get("name") or "") in wanted_norm
    ]
    if len(fuzzy) == 1:
        return fuzzy[0]
    names = [p.get("name") for p in (exact or exact_norm or fuzzy or projects[:10])]
    raise RuntimeError(f"项目匹配不唯一或未找到：{wanted_name}；候选：{names}")


def detect_types(tasks, categories):
    matched = {}
    for cat in categories:
        target = normalize(cat)
        for t in tasks:
            issue_type = (t.get("issueType") or {})
            issue_name = issue_type.get("name") or ""
            if normalize(issue_name or "") == target:
                matched[cat] = {
                    "issue_type_uuid": issue_type.get("uuid"),
                    "issue_type_name": issue_name,
                    "scope_uuid": ((t.get("issueTypeScope") or {}).get("uuid")),
                }
                break
    return matched


def aggregate(tasks, mapping):
    result = {}
    for label, meta in mapping.items():
        rows = []
        for t in tasks:
            issue_type = t.get("issueType") or {}
            scope_uuid = ((t.get("issueTypeScope") or {}).get("uuid"))
            if issue_type.get("uuid") == meta["issue_type_uuid"] and scope_uuid == meta["scope_uuid"]:
                rows.append({
                    "缺陷类型": label,
                    "编号": t.get("number"),
                    "标题": t.get("name"),
                    "状态": ((t.get("status") or {}).get("name")),
                    "状态分类": ((t.get("status") or {}).get("category")),
                    "优先级": ((t.get("priority") or {}).get("value")),
                    "处理人": ((t.get("assign") or {}).get("name")) or "",
                    "负责人": ((t.get("owner") or {}).get("name")) or "",
                })
        rows.sort(key=lambda x: (x["编号"] is None, x["编号"]))
        result[label] = {
            "count": len(rows),
            "status_distribution": dict(Counter(r["状态"] for r in rows)),
            "priority_distribution": dict(Counter(r["优先级"] for r in rows)),
            "rows": rows,
        }
    return result


def severe_shortlist(aggregated):
    rank = {"严重": 3, "较高": 2, "高": 2, "普通": 1, "低": 0}
    all_rows = []
    for defect_type, info in aggregated.items():
        for row in info["rows"]:
            if row.get("优先级") in ("严重", "较高", "高"):
                row = dict(row)
                row["缺陷类型"] = defect_type
                all_rows.append(row)
    all_rows.sort(key=lambda r: (-rank.get(r.get("优先级"), -1), r.get("编号") or 0))
    return all_rows[:10]


def write_csv(path, aggregated):
    rows = []
    for info in aggregated.values():
        rows.extend(info["rows"])
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["缺陷类型", "编号", "标题", "状态", "状态分类", "优先级", "处理人", "负责人"])
        writer.writeheader()
        writer.writerows(rows)


def default_text(v, fallback):
    return v if v else fallback


def make_title(project_name, report_start, report_end):
    if not report_start or not report_end:
        return f"{project_name}单品项目测试周报（待确认）"
    start = datetime.strptime(report_start, "%Y-%m-%d")
    end = datetime.strptime(report_end, "%Y-%m-%d")
    return f"{project_name}单品项目测试周报（{start.strftime('%Y%m%d')}~{end.strftime('%m%d')}）"


def make_period_line(report_start, report_end):
    if not report_start or not report_end:
        return "待确认"
    start = datetime.strptime(report_start, "%Y-%m-%d")
    end = datetime.strptime(report_end, "%Y-%m-%d")
    return f"{start.strftime('%Y%m%d')}~{end.strftime('%m%d')}"


def build_basic_info(args, aggregated):
    test_scope = default_text(args.test_scope, " / ".join(aggregated.keys()))
    return [
        ["计划测试内容", default_text(args.plan_test_content, f"{args.project} 项目缺陷统计与周报整理"), "测试代表", default_text(args.test_owner, "待确认")],
        ["固件版本", default_text(args.firmware_version, "待确认"), "本周计划人力投入", default_text(args.planned_manpower, "待确认")],
        ["APP版本", default_text(args.app_version, "待确认"), "实际测试人力投入", default_text(args.actual_manpower, "待确认")],
        ["本轮提测时间", default_text(args.submit_time, "待确认"), "其他投入时间", default_text(args.other_time, "/")],
        ["目标完成时间", default_text(args.target_finish_time, "待确认"), "其他投入时间说明", default_text(args.other_time_note, "/")],
        ["测试范围", test_scope, "当前轮次", default_text(args.current_round, "待确认")],
    ]


def render_report(project_name, aggregated, args):
    total = sum(v["count"] for v in aggregated.values())
    title = make_title(project_name, args.report_start, args.report_end)
    period_line = make_period_line(args.report_start, args.report_end)
    shortlist = severe_shortlist(aggregated)

    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"# 1、{period_line}")
    lines.append("")
    lines.append("## 1）项目基本信息")
    lines.append("")
    lines.append("## 2）进展与缺陷")
    lines.append("")
    lines.append("### 测试进展：")
    lines.append(f"- 任务1：{default_text(args.progress_task, f'{project_name} 项目缺陷梳理与统计')}" )
    lines.append(f"- 总完成：{default_text(args.progress_overall, '进行中（已完成 ONES 指定缺陷类型数据拉取与统计）')}" )
    lines.append(f"- 本周完成：{default_text(args.progress_weekly, f'本周统计缺陷 {total} 个')}" )
    lines.append(f"- ones测试计划：{default_text(args.ones_plan_text, project_name)}")
    lines.append("")
    lines.append("### 阻塞情况：")
    lines.append(f"- 阻塞项：{default_text(args.blockers, '待补充')}")
    lines.append("")
    lines.append("### 严重缺陷：")
    if shortlist:
        for i, row in enumerate(shortlist, 1):
            lines.append(f"- 严重缺陷{i}：{project_name}-{row['编号']}【{row['缺陷类型']}】{row['标题']} — {row['优先级']} — {row['状态']}")
    else:
        lines.append("- 暂无严重/较高优先级缺陷")
    lines.append("")
    lines.append("### 缺陷看板：")
    lines.append(f"- 缺陷总数：{total}")
    for k, v in aggregated.items():
        lines.append(f"- {k}：{v['count']}")
    for k, v in aggregated.items():
        status_text = "；".join(f"{name}{count}" for name, count in v["status_distribution"].items()) or "无"
        lines.append(f"- {k}状态分布：{status_text}")
    for k, v in aggregated.items():
        priority_text = "；".join(f"{name}{count}" for name, count in v["priority_distribution"].items()) or "无"
        lines.append(f"- {k}优先级分布：{priority_text}")
    lines.append("")
    lines.append("## 3）风险与需求")
    lines.append("")
    lines.append(f"- {default_text(args.risk_summary_1, '当前风险主要集中在缺陷数量最多的类别，需要优先推进修复闭环')}" )
    lines.append(f"- {default_text(args.risk_summary_2, '仍有待提交或未开始问题，需确认是否纳入本轮修正范围')}" )
    lines.append("")
    lines.append("### 测试需求：")
    lines.append(f"- {default_text(args.test_need_1, '补充阻塞项、版本信息、截图等正式周报字段')}" )
    if args.test_need_2:
        lines.append(f"- {args.test_need_2}")
    lines.append("")
    lines.append("## 4）下周测试计划")
    lines.append("")
    lines.append(f"- {default_text(args.next_plan_1, '继续跟进目标缺陷类型整改进度')}" )
    lines.append(f"- {default_text(args.next_plan_2, '重点关注严重缺陷、待回归问题与未开始问题状态变化')}" )
    return {
        "title": title,
        "period_line": period_line,
        "markdown": "\n".join(lines),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--email", required=True)
    ap.add_argument("--password", required=True)
    ap.add_argument("--project", required=True)
    ap.add_argument("--categories", default=",".join(DEFAULT_CATEGORIES))
    ap.add_argument("--csv", default="output/ones-weekly-report.csv")
    ap.add_argument("--json", default="output/ones-weekly-report.json")
    ap.add_argument("--report-start")
    ap.add_argument("--report-end")
    ap.add_argument("--plan-test-content")
    ap.add_argument("--test-owner")
    ap.add_argument("--firmware-version")
    ap.add_argument("--app-version")
    ap.add_argument("--planned-manpower")
    ap.add_argument("--actual-manpower")
    ap.add_argument("--submit-time")
    ap.add_argument("--other-time")
    ap.add_argument("--target-finish-time")
    ap.add_argument("--other-time-note")
    ap.add_argument("--test-scope")
    ap.add_argument("--current-round")
    ap.add_argument("--progress-task")
    ap.add_argument("--progress-overall")
    ap.add_argument("--progress-weekly")
    ap.add_argument("--ones-plan-text")
    ap.add_argument("--blockers")
    ap.add_argument("--risk-summary-1")
    ap.add_argument("--risk-summary-2")
    ap.add_argument("--test-need-1")
    ap.add_argument("--test-need-2")
    ap.add_argument("--next-plan-1")
    ap.add_argument("--next-plan-2")
    args = ap.parse_args()

    categories = [x.strip() for x in args.categories.split(",") if x.strip()]
    auth = ones_login(args.email, args.password)
    projects_resp = gql(auth["team_uuid"], auth["user_uuid"], auth["token"], '{ projects(limit: 200) { uuid name key } }')
    projects = (((projects_resp or {}).get("data") or {}).get("projects")) or []
    project = find_project(projects, args.project)

    query = '{ tasks(filter: {project_in: ["%s"]}, limit: 500) { uuid name number status { name category } priority { value } issueType { uuid name } issueTypeScope { uuid } assign { name uuid } owner { name uuid } } }' % project["uuid"]
    tasks_resp = gql(auth["team_uuid"], auth["user_uuid"], auth["token"], query)
    tasks = ((((tasks_resp or {}).get("data") or {}).get("tasks")) or [])

    mapping = detect_types(tasks, categories)
    if not mapping:
        raise RuntimeError("未识别到任何目标缺陷类型，请检查项目名或 categories")
    aggregated = aggregate(tasks, mapping)
    report = render_report(project.get("name") or args.project, aggregated, args)
    basic_info_rows = build_basic_info(args, aggregated)

    payload = {
        "project": project,
        "mapping": mapping,
        "summary": aggregated,
        "report_title": report["title"],
        "report_period": report["period_line"],
        "report_markdown": report["markdown"],
        "basic_info_table": basic_info_rows,
    }
    Path(args.json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(args.csv, aggregated)
    print(json.dumps({
        "project": project,
        "matched_categories": list(mapping.keys()),
        "json": args.json,
        "csv": args.csv,
        "report_title": report["title"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(str(e), file=sys.stderr)
        sys.exit(1)
