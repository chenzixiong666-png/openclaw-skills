# Excel 缺陷数据解析指南

## Excel 文件来源
用户从 ones 系统导出的缺陷 Excel 文件（.xlsx）

## 解析方法
使用 Python + openpyxl 读取：

```python
import openpyxl

wb = openpyxl.load_workbook(filepath, data_only=True)
ws = wb.active
headers = [cell.value for cell in ws[1]]
```

## 关键字段映射

| Excel 列名 | 用途 | 示例值 |
|-----------|------|-------|
| 标识 / ID | 缺陷编号 | W1141-195774 |
| 标题 | 缺陷描述 | 【屏幕蓝屏】...|
| 优先级 | P级 | 最高/较高/普通/较低 |
| 状态 | 当前状态 | 测试提交/待回归/已关闭/... |
| 负责人 | 处理人 | 陈志禄 |
| 创建时间 | 提交日期 | 用于趋势分析 |
| 分类 | bug/非bug | 用于过滤 |

## 统计逻辑（Python 伪代码）

```python
valid = [d for d in defects if d['状态'] != '已关闭' and d['分类'] != '非bug']
total = len(valid)

# 优先级统计
priority_counts = Counter(d['优先级'] for d in valid)

# 状态统计
status_map = {
    '测试提交': '未解决', '下一版本修复': '未解决',
    '待回归': '待回归', '持续跟踪': '持续跟踪', '待评审': '待评审'
}
status_counts = Counter(status_map.get(d['状态'], '其他') for d in valid)

# 严重缺陷
severe = [d for d in valid if d['优先级'] in ('最高', '较高')]
```

## Windows 环境注意
- Python 命令用 `python`（非 `python3`）
- 中文输出需 `chcp 65001` 设置 UTF-8
- PowerShell JSON 参数避免变量插值
- `tail` 不可用，用 `Get-Content -Tail` 替代
