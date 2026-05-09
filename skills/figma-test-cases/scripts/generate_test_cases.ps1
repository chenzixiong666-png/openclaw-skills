param(
    [string]$OutputPath = "测试用例.xlsx",
    [string]$SheetName = "测试用例",
    [switch]$AddSampleData
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
    $ws.Cells.Item(1, $i+1).Interior.Color = 13421772
}

# 设置列宽
$ws.Columns.Item("A").ColumnWidth = 18
$ws.Columns.Item("B").ColumnWidth = 35
$ws.Columns.Item("C").ColumnWidth = 10
$ws.Columns.Item("D").ColumnWidth = 12
$ws.Columns.Item("E").ColumnWidth = 30
$ws.Columns.Item("F").ColumnWidth = 45
$ws.Columns.Item("G").ColumnWidth = 45

if ($AddSampleData) {
    # 示例测试用例数据
    $testCases = @(
        @("TC-001","功能入口显示验证","P0","功能","用户已登录","1.打开首页 2.查看功能 icon","功能 icon 正常显示"),
        @("TC-002","首次使用引导提示","P0","功能","用户首次使用","1.首次点击功能入口","显示引导弹窗"),
        @("TC-003","非首次不显示引导","P1","功能","用户已使用过","1.再次点击功能入口","不显示引导弹窗"),
        @("TC-004","功能页面正常打开","P0","功能","用户在首页","1.点击功能入口 2.等待加载","成功进入功能页面"),
        @("TC-005","页面背景色验证","P2","功能","用户已打开页面","1.查看页面背景色","背景色符合设计稿"),
        @("TC-006","购买按钮显示","P0","功能","查看未拥有商品","1.查看商品详情","显示购买按钮"),
        @("TC-007","已拥有标识显示","P1","功能","查看已拥有商品","1.查看商品详情","显示已拥有标识"),
        @("TC-008","无网络提示","P1","功能","设备无网络","1.断开网络 2.打开页面","显示无网络提示"),
        @("TC-009","权限未授权提示","P1","功能","相机权限未授权","1.点击需要权限的功能","提示授权权限"),
        @("TC-010","页面加载超时","P2","功能","网络信号差","1.打开页面","显示加载超时提示")
    )

    # 写入数据
    $row = 2
    foreach($tc in $testCases) {
        for($col=0; $col -lt $tc.Count; $col++) {
            $ws.Cells.Item($row, $col+1).Value2 = $tc[$col]
        }
        $row++
    }

    Write-Host "✓ 已添加 $($testCases.Count) 条示例测试用例"
}

# 自动调整列宽
$ws.Columns.AutoFit() | Out-Null
$ws.Rows.RowHeight = 20

# 保存文件
$wb.SaveAs($OutputPath, 51)
$wb.Close($false)
$excel.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null

Write-Host "✓ Excel 文件已创建：$OutputPath"
Write-Host "✓ 工作表名称：$SheetName"
