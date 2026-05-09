param(
    [string]$OutputPath = "测试用例.xlsx",
    [string]$SheetName = "测试用例"
)

# 创建 Excel 应用
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$wb = $excel.Workbooks.Add()
$ws = $wb.Worksheets.Item(1)
$ws.Name = $SheetName

# 设置表头
$headers = @("测试用例 ID","用例名称","优先级","用例类型","前置条件","测试步骤","预期结果")
for($i=0; $i -lt $headers.Count; $i++) {
    $ws.Cells.Item(1, $i+1).Value2 = $headers[$i]
    $ws.Cells.Item(1, $i+1).Font.Bold = $true
    $ws.Cells.Item(1, $i+1).Interior.Color = 13421772  # 灰色背景 #CCCCCC
}

# 设置列宽
$ws.Columns.Item("A").ColumnWidth = 18  # 测试用例 ID
$ws.Columns.Item("B").ColumnWidth = 35  # 用例名称
$ws.Columns.Item("C").ColumnWidth = 10  # 优先级
$ws.Columns.Item("D").ColumnWidth = 12  # 用例类型
$ws.Columns.Item("E").ColumnWidth = 30  # 前置条件
$ws.Columns.Item("F").ColumnWidth = 45  # 测试步骤
$ws.Columns.Item("G").ColumnWidth = 45  # 预期结果

# 设置行高
$ws.Rows.RowHeight = 20

# 保存文件
$wb.SaveAs($OutputPath, 51)  # 51 = xlOpenXMLWorkbook
$wb.Close($false)
$excel.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null

Write-Host "✓ Excel 模板已创建：$OutputPath"
Write-Host "✓ 工作表名称：$SheetName"
Write-Host "✓ 列数：7 列（测试用例 ID、用例名称、优先级、用例类型、前置条件、测试步骤、预期结果）"
