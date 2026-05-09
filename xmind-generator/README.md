# XMind Generator Skill

一个专门生成 `.xmind` 思维导图文件的 OpenClaw Skill。

## 功能

- 📊 从 JSON 结构生成专业的 XMind 思维导图
- 🔄 支持无限层级嵌套
- 🌐 完全支持中文、Emoji 等 Unicode 字符
- 📁 生成的文件可在 XMind、MindNode 等工具中打开编辑
- ⚡ 快速生成，支持大型思维导图

## 快速开始

### 基本用法

准备你的思维导图数据（JSON 格式）：

```json
{
  "title": "项目计划",
  "children": [
    {
      "title": "阶段 1：规划",
      "children": [
        {"title": "需求分析"},
        {"title": "系统设计"},
        {"title": "时间规划"}
      ]
    },
    {
      "title": "阶段 2：开发",
      "children": [
        {"title": "前端开发"},
        {"title": "后端开发"},
        {"title": "测试"}
      ]
    }
  ]
}
```

脚本会生成一个 `.xmind` 文件，你可以直接用 XMind 打开。

### 数据格式

每个节点都是一个 JSON 对象：

```json
{
  "title": "节点标题",
  "children": [
    {"title": "子节点 1"},
    {"title": "子节点 2"}
  ]
}
```

支持简化格式（直接用字符串）：
```json
["节点 1", "节点 2", "节点 3"]
```

## 使用场景

- 📋 **项目规划** — 分解交付物和时间表
- 🎓 **学习大纲** — 组织课程内容或学习材料
- 💡 **头脑风暴** — 在视觉层级中捕捉想法
- 📚 **文档** — 创建概念图或系统架构概览
- 👥 **团队规划** — 可视化组织结构和职责
- 🔍 **问题分析** — 分解解决方案和依赖关系

## 文件说明

- `SKILL.md` — Skill 描述和使用指南
- `scripts/generate_xmind.py` — Python 脚本（核心功能）
- `test-data.json` — 测试数据示例
- `test-output.xmind` — 生成的示例文件

## 脚本使用

```bash
python scripts/generate_xmind.py <输出文件> <JSON数据> [标题]
```

**示例 1：使用 JSON 文件**
```bash
python scripts/generate_xmind.py output.xmind data.json "我的思维导图"
```

**示例 2：使用内联 JSON**
```bash
python scripts/generate_xmind.py output.xmind '{"title":"根","children":[{"title":"节点1"}]}'
```

## 技术细节

- XMind 文件是 ZIP 格式（`.xmind`），包含 XML 内容
- 支持的工具：XMind、MindNode、Freemind、Freeplane
- 编码：UTF-8（完全支持中文和 Unicode）
- 嵌套深度：无限制

## 开发历史

- v1.0 — 初始版本，支持基础思维导图生成
