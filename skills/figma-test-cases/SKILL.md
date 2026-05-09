---
name: figma-test-cases
description: 从 Figma 设计稿分析功能并生成测试用例 Excel 表格。使用 browser 工具访问 Figma 设计稿，通过 snapshot 和搜索功能定位功能模块，分析交互逻辑后生成包含测试用例 ID、用例名称、优先级、用例类型、前置条件、测试步骤、预期结果的 xlsx 文件。适用于 UX/UI 设计稿评审、测试用例编写、功能点梳理等场景。
---

# Figma 测试用例生成

## 核心流程

### 1. 访问 Figma 设计稿

```powershell
# 启动浏览器
browser action=start profile=openclaw

# 导航到 Figma 链接
browser action=navigate url=<figma 设计稿 URL>
```

### 2. 获取页面结构

```powershell
# 获取页面元素快照
browser action=snapshot

# 或截取屏幕查看设计内容
browser action=screenshot
```

### 3. 搜索目标功能

```powershell
# 打开 Figma 搜索 (Ctrl+F)
browser action=act kind=press key=Control+f

# 搜索功能关键词
browser action=act kind=type ref=<搜索框 ref> text=<功能名称>

# 查看搜索结果列表，点击目标框架
browser action=act kind=click ref=<目标框架 ref>
```

### 4. 分析功能点

从快照中提取关键信息：
- 页面/框架名称
- 功能描述文本
- 交互逻辑说明
- UI 元素属性（尺寸、颜色等）

**典型功能点分类：**
| 类型 | 示例 |
|------|------|
| 入口显示 | icon 显示、new 标签逻辑 |
| 页面交互 | 页面打开、弹窗显示 |
| 操作流程 | 试装、购买、扫码 |
| 状态变化 | 红点显示/消失、已拥有标识 |
| 异常场景 | 无网络、权限未授权 |

### 5. 生成测试用例 Excel

```powershell
# 使用 PowerShell + Excel COM 生成 xlsx
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$wb = $excel.Workbooks.Add()
$ws = $wb.Worksheets.Item(1)
$ws.Name = "测试用例"

# 设置表头
$headers = @("测试用例 ID","用例名称","优先级","用例类型","前置条件","测试步骤","预期结果")
for($i=0; $i -lt $headers.Count; $i++) {
    $ws.Cells.Item(1, $i+1).Value2 = $headers[$i]
    $ws.Cells.Item(1, $i+1).Font.Bold = $true
}

# 添加测试用例（每行一个数组）
$testCases = @(
    @("TC-001","用例名称","P0","功能","前置条件","1.步骤 1 2.步骤 2","预期结果"),
    # ... 更多用例
)
$row = 2
foreach($tc in $testCases) {
    for($col=0; $col -lt $tc.Count; $col++) {
        $ws.Cells.Item($row, $col+1).Value2 = $tc[$col]
    }
    $row++
}

# 格式化并保存
$ws.Columns.AutoFit() | Out-Null
$wb.SaveAs(<路径>, 51)
$wb.Close($false)
$excel.Quit()
```

## 测试用例设计原则

### 优先级定义
- **P0**: 核心功能，阻断性问题
- **P1**: 重要功能，影响用户体验
- **P2**: 次要功能，优化类问题

### 用例覆盖维度
1. **正常流程** - 主要功能路径
2. **边界条件** - 首次/非首次、已拥有/未拥有
3. **状态变化** - 显示/消失、打开/关闭
4. **异常场景** - 无网络、权限、超时

### 测试步骤格式
- 使用序号分隔：`1.步骤 1 2.步骤 2`
- 避免换行符（会导致 Excel 列错位）
- 保持简洁明确

## 常见功能模块测试点

### 入口/图标类
- icon 显示/隐藏
- new 标签显示逻辑
- 红点提示逻辑
- 动画效果

### 页面/弹窗类
- 页面正常打开
- 弹窗显示/关闭
- 页面元素验证（标题、背景色、尺寸）

### 操作/交互类
- 点击响应
- 试装/换装
- 购买流程
- 扫码功能

### 状态同步类
- 已拥有/未拥有标识
- 数据同步验证
- app 端联动

## 注意事项

1. **Figma 权限** - 确保设计稿可访问（公开或已授权）
2. **搜索定位** - 使用 Figma 内置搜索快速定位功能模块
3. **Excel 编码** - 使用 SaveAs 格式 51 (xlOpenXMLWorkbook) 支持中文
4. **列格式** - 测试步骤避免换行，用空格分隔序号
5. **文件命名** - 使用中文文件名便于识别

## 输出模板

测试用例 Excel 包含 7 列：
1. 测试用例 ID (如 TC-WARDROBE-001)
2. 用例名称
3. 优先级 (P0/P1/P2)
4. 用例类型 (功能)
5. 前置条件
6. 测试步骤
7. 预期结果

##  bundled 资源

### scripts/
- `create_excel_template.ps1` - 创建空白测试用例 Excel 模板
- `generate_test_cases.ps1` - 生成带示例数据的测试用例 Excel

### references/
- `test-case-patterns.md` - 测试用例设计模式、功能点识别清单、优先级标准、常用模板

**使用时加载：** 需要详细测试模式参考时读取 `references/test-case-patterns.md`

## 附录：完整脚本示例

```powershell
param(
    [string]$OutputPath = "测试用例.xlsx"
)

$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$wb = $excel.Workbooks.Add()
$ws = $wb.Worksheets.Item(1)
$ws.Name = "测试用例"

# 表头
$headers = @("测试用例 ID","用例名称","优先级","用例类型","前置条件","测试步骤","预期结果")
for($i=0; $i -lt $headers.Count; $i++) {
    $ws.Cells.Item(1, $i+1).Value2 = $headers[$i]
    $ws.Cells.Item(1, $i+1).Font.Bold = $true
    $ws.Cells.Item(1, $i+1).Interior.Color = 13421772  # 灰色背景
}

# 测试用例数据
$testCases = @(
    @("TC-001","功能入口显示验证","P0","功能","用户已登录","1.打开首页 2.查看功能 icon","功能 icon 正常显示"),
    @("TC-002","首次使用引导提示","P0","功能","用户首次使用","1.首次点击功能入口","显示引导弹窗"),
    @("TC-003","非首次不显示引导","P1","功能","用户已使用过","1.再次点击功能入口","不显示引导弹窗")
)

# 写入数据
$row = 2
foreach($tc in $testCases) {
    for($col=0; $col -lt $tc.Count; $col++) {
        $ws.Cells.Item($row, $col+1).Value2 = $tc[$col]
    }
    $row++
}

# 格式化
$ws.Columns.AutoFit() | Out-Null
$ws.Rows.RowHeight = 20

# 保存
$wb.SaveAs($OutputPath, 51)  # 51 = xlOpenXMLWorkbook
$wb.Close($false)
$excel.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null

Write-Host "测试用例已生成：$OutputPath"
Write-Host "共生成 $($testCases.Count) 条测试用例"
```

### 使用示例

```powershell
# 执行脚本生成测试用例
.\scripts\generate_test_cases.ps1 -OutputPath "衣橱功能测试用例.xlsx"
```

## 参考资源

- **scripts/generate_test_cases.ps1** - PowerShell 脚本，自动生成测试用例 Excel
- **references/common-test-points.md** - 常见功能测试点参考表

## 附录：Figma 常用操作速查

| 操作 | 命令 |
|------|------|
| 启动浏览器 | `browser action=start profile=openclaw` |
| 打开设计稿 | `browser action=navigate url=<figma 链接>` |
| 获取快照 | `browser action=snapshot` |
| 截图 | `browser action=screenshot` |
| 打开搜索 | `browser action=act kind=press key=Control+f` |
| 输入搜索词 | `browser action=act kind=type ref=<ref> text=关键词` |
| 点击元素 | `browser action=act kind=click ref=<元素 ref>` |
| 关闭浏览器 | `browser action=stop` |
