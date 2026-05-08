---
name: weekly-test-report
description: 从 Excel 缺陷数据生成飞书单品项目测试周报。当用户提到"周报"、"测试周报"、"生成周报"、发送缺陷 Excel 文件并要求生成报告时触发。支持：(1) 解析 ones 导出的缺陷 Excel，(2) 统计缺陷优先级/状态分布，(3) 按定稿模板在飞书创建格式化周报文档，(4) 填充项目信息表格、进展、严重缺陷、缺陷看板数据。项目：AI Hub Show 单品项目。
---

# 周报生成流程

## 输入
- 用户提供缺陷 Excel 文件（ones 导出的 .xlsx）
- 用户提供或确认：日期范围、版本号、人力投入、测试进度等项目信息

## 步骤

### 1. 解析 Excel
- 用 Python + openpyxl 读取缺陷数据
- 详细字段映射和统计逻辑见 [references/excel-parsing.md](references/excel-parsing.md)
- 剔除已关闭和非 bug 缺陷，得到有效缺陷数
- 统计优先级分布、状态分布
- 筛选严重缺陷（最高+较高）

### 2. 创建飞书文档
- 用 `feishu_doc action=create` 创建新文档
- 默认文件夹 token：`A1KmfkVu5lM4Q1dpgdEchSYEnQd`（用户指定的默认输出文件夹）
- 标题格式：`AI Hub Show单品项目测试周报（{YYYYMMDD}~{MMDD}）`

### 3. 写入内容
按模板结构依次写入，完整模板见 [references/template.md](references/template.md)

写入顺序：
1. `feishu_doc action=write` 写入全部文本内容（H1/H2/H3/bullet）
2. `feishu_doc action=list_blocks` 获取 block ID
3. `feishu_doc action=create_table` 在"1）项目基本信息"后插入 4×6 表格
4. `feishu_doc action=write_table_cells` 填充表格数据
5. 如需图表：`feishu_doc action=upload_image` 插入缺陷看板数据之后

### 4. 提醒用户补充
以下内容 AI 无法自动生成，需提醒用户手动补充：
- **阻塞情况**（多级 bullet 树，按模块分类的阻塞项）
- **风险与需求**（除非用户明确告知）
- **下周测试计划**（除非用户明确告知）

## 关键规则
- 严重缺陷**带负责人和 ones 链接**
- 缺陷统计**剔除关闭和非 bug**
- 图表由用户自行截图贴入，除非用户要求生成
- ⚠️ **禁止对 Page 块使用 update_block**（会清空文档）
- 表格列宽固定：[140, 218, 144, 318]
