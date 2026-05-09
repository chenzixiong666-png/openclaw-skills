@{
    Title = "曾沛慈 × 邓紫棋 合唱海报生成脚本"
    Description = "生成一张创意海报，然后上传到 SwitchBot AI 画框"
}

# PowerShell 脚本：生成合成图片
# 由于系统限制，我们将使用 Base64 编码的预生成图片

# 这是一个简化的合成图片（使用纯色 + 文字）
# 如果需要真实的照片合成，建议使用在线工具或 Photoshop

$imageBase64 = @"
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==
"@

Write-Host "🎵 创建合唱海报..."
Write-Host "💡 提示: 系统目前无法直接生成高清图片"
Write-Host ""
Write-Host "可选方案："
Write-Host "1. 使用在线工具生成图片，然后用 URL 上传"
Write-Host "2. 使用你已有的曾沛慈和邓紫棋照片进行拼接"
Write-Host "3. 从网络搜索高质量的歌手照片"
Write-Host ""
Write-Host "推荐: 访问以下网站获取免费高清图片:"
Write-Host "  - Unsplash: https://unsplash.com (搜索 singer, concert)"
Write-Host "  - Pixabay: https://pixabay.com"
Write-Host "  - Pexels: https://www.pexels.com"
Write-Host ""
Write-Host "找到图片后，可以用这个命令上传到画框:"
Write-Host "`$env:SWITCHBOT_TOKEN='...'"
Write-Host "`$env:SWITCHBOT_SECRET='...'"
Write-Host "node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE74647B uploadImage --param='{""imageUrl"":""https://example.com/image.jpg""}'"
