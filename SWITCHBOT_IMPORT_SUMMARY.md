# SwitchBot Skill 导入完成 ✅

**导入时间**：2026-04-13 11:13 GMT+8  
**版本**：1.0.5  
**状态**：✅ 已就绪

---

## 📁 导入路径

```
C:\Users\woan\.openclaw\workspace\
└─ skills/
   └─ switchbot-openapi/
      ├─ SKILL.md ........................ 技能描述（已本地化）
      ├─ README-CLAWHUB.md .............. ClawHub 发布说明
      ├─ _meta.json ..................... 元数据
      ├─ scripts/
      │  ├─ switchbot_cli.js ............ ✨ 主工具（Node CLI）
      │  ├─ list_devices.sh
      │  ├─ get_status.sh
      │  ├─ send_command.sh
      │  ├─ list_scenes.sh
      │  └─ execute_scene.sh
      └─ references/
         ├─ commands.md ................. 完整命令参考
         └─ examples.md ................. 使用示例
```

---

## 🔑 环境变量配置

**需要在 OpenClaw Gateway 中设置以下环境变量：**

```bash
SWITCHBOT_TOKEN=<your_token>
SWITCHBOT_SECRET=<your_secret>
# SWITCHBOT_REGION=global  (可选，默认 global)
```

**如何获取 Token 和 Secret：**
1. 打开 SwitchBot App
2. 进入「设置」→「开发者选项」（或「Advanced」）
3. 点击「API Token」→ 显示/生成 Token 和 Secret
4. 复制并设置到环境变量

---

## 🚀 快速开始（3 步）

### 1️⃣ 验证环境变量已设置

```bash
echo $SWITCHBOT_TOKEN
echo $SWITCHBOT_SECRET
```

### 2️⃣ 列出所有设备

```bash
node C:\Users\woan\.openclaw\workspace\skills\switchbot-openapi\scripts\switchbot_cli.js list
```

**输出示例：**
```
🏠 Home
  └─ 客厅
     ├─ 客厅灯 (Color Bulb) - DCF9A7E2C3B1
     └─ 客厅窗帘 (Curtain 3) - AABBCCDD1122
```

### 3️⃣ 控制设备

```bash
# 打开灯
node C:\Users\woan\.openclaw\workspace\skills\switchbot-openapi\scripts\switchbot_cli.js cmd DCF9A7E2C3B1 turnOn

# 关闭灯
node C:\Users\woan\.openclaw\workspace\skills\switchbot-openapi\scripts\switchbot_cli.js cmd DCF9A7E2C3B1 turnOff

# 查询状态
node C:\Users\woan\.openclaw\workspace\skills\switchbot-openapi\scripts\switchbot_cli.js status DCF9A7E2C3B1
```

---

## 📚 学习资源

### 已为你创建的文档

| 文件名 | 用途 |
|-------|------|
| `SWITCHBOT_LEARNING.md` | 📖 详细学习指南（7 章节，12000+ 字） |
| `MEMORY.md` | 🧠 核心要点速查（已更新） |
| `TOOLS.md` | 🔧 SwitchBot 配置笔记（已更新） |
| `skills/switchbot-openapi/SKILL.md` | ⭐ Skill 本地文档 |

### 官方参考

- `skills/switchbot-openapi/references/commands.md` — 完整命令表（15+ 设备类型）
- `skills/switchbot-openapi/references/examples.md` — 各设备使用示例

---

## 🛠️ 常用命令速记

```bash
# 核心路径（为了方便，可以设为别名）
SKILL="C:\Users\woan\.openclaw\workspace\skills\switchbot-openapi\scripts\switchbot_cli.js"

# 列设备
node $SKILL list

# 查状态
node $SKILL status <deviceId>

# 开/关/切换
node $SKILL cmd <deviceId> turnOn|turnOff|toggle

# 窗帘位置 (0-100)
node $SKILL cmd <deviceId> setPosition --pos=50

# 门锁
node $SKILL cmd <deviceId> lock|unlock

# 灯光
node $SKILL cmd <deviceId> setBrightness --param=80
node $SKILL cmd <deviceId> setColor --param="255:100:0"

# Scenes
node $SKILL scenes
node $SKILL scene <sceneId>
```

---

## 🔍 验证清单

- [ ] 环境变量已设置（SWITCHBOT_TOKEN, SWITCHBOT_SECRET）
- [ ] 能运行 `node ... list` 列出设备
- [ ] 至少控制一个设备成功
- [ ] 读过 `SWITCHBOT_LEARNING.md` 学习指南
- [ ] 记住 3 个常用命令：list、status、cmd

---

## ⚡ 常见问题

### Q: 运行 CLI 报错 "Missing SWITCHBOT_TOKEN"
**A**: 检查环境变量是否已设置。可以运行 `echo $SWITCHBOT_TOKEN` 验证。

### Q: 某个设备显示错误代码 160
**A**: 该设备不支持这个命令，改用 Scenes 代替。

### Q: 想要自动化控制（如定时打开灯）
**A**: 写一个简单的 bash 脚本，调用多个 `node $SKILL cmd ...` 命令。

---

## 📋 下一步

1. **设置环境变量** → 在 OpenClaw Gateway 中配置 SWITCHBOT_TOKEN/SECRET
2. **测试 list 命令** → 验证能连接到 SwitchBot API
3. **学习参数格式** → 读 `SWITCHBOT_LEARNING.md` 第四部分
4. **写自动化脚本** → 参考第七部分的场景示例
5. **（可选）设置别名** → 为 skill 路径创建 PowerShell 别名或函数

---

**🎉 导入完成！现在你可以开始控制 SwitchBot 设备了。**

有问题？查看：
- 📖 `SWITCHBOT_LEARNING.md` — 详细教程
- 📚 `skills/switchbot-openapi/references/commands.md` — 命令参考
- 🧠 `MEMORY.md` — 核心速查
