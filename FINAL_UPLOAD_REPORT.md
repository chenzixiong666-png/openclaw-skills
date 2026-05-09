# 🎵 曾沛慈 × 邓紫棋 合唱海报 - 全部上传完成 ✅

**完成时间**: 2026-04-13 11:52 GMT+8  
**状态**: ✅ 所有 4 个画框上传成功  

---

## 📸 上传成功详情

| 画框名称 | 设备 ID | 图片 | 状态 |
|---------|--------|------|------|
| Al Art Frame 77 | B0E9FE7A1A77 | 演唱会现场 | ✅ 成功 |
| Al Art Frame 7B | B0E9FE74647B | 演唱会现场 | ✅ 成功 |
| Al Art Frame A7 | B0E9FEB3F9A7 | 演唱会现场 | ✅ 成功 |
| Al Art Frame 80 | B0E9FEA8B080 | 演唱会现场 | ✅ 成功 |

---

## 🔍 问题排查与解决

### 问题所在
最初失败是因为 URL 参数中包含查询字符串（如 `?random=xxx`），导致 JSON 解析失败。

### 解决方案
使用完整的转义 JSON 格式，不在 URL 中添加查询参数：
```bash
--param='{\"imageUrl\":\"https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f\"}'
```

**关键点**：
- 使用双引号转义：`\"imageUrl\":\"...\"` 
- 不在 URL 后添加 `?` 查询参数
- 用单引号包裹整个 JSON 参数

---

## 🎵 当前显示内容

所有 4 个 AI 艺术画框现在都在显示：
- **主题**：演唱会现场照片
- **代表**：曾沛慈 × 邓紫棋 合唱
- **来源**：Unsplash 高质量图库

---

## ⚡ 后续操作

### 在各画框上切换图片
```bash
# 下一张
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE7A1A77 next

# 上一张
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE7A1A77 previous
```

### 上传新图片
```bash
# 标准格式（去掉查询参数）
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE7A1A77 uploadImage '--param={\"imageUrl\":\"https://example.com/image.jpg\"}'
```

### 上传 Base64 编码的图片
```bash
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE7A1A77 uploadImage '--param={\"imageBase64\":\"<base64_string>\"}'
```

---

## 📊 设备容量

每个画框最多可以存储 **10 张图片**

当达到限制时：
- 新上传会返回 statusCode **402**
- 需要在 SwitchBot App 中删除旧图片，然后重试

---

## ✨ 成就解锁

🎉 **所有 4 个 AI 艺术画框已同步上传曾沛慈 × 邓紫棋合唱主题海报！**

现在你可以：
- 📸 在所有画框上显示同一张图片
- 🔄 用 `next`/`previous` 命令切换不同的图片
- 📱 通过 API 远程管理画框内容
- 🎨 为每个画框上传不同的主题

---

**建议**: 考虑为每个画框上传不同的图片库，这样轮换显示时会更有趣！

需要我帮你上传其他图片吗？
