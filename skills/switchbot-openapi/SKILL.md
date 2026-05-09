---
name: switchbot-openapi
description: 通过 SwitchBot 官方 OpenAPI (v1.1) 控制和查询 SwitchBot 设备。支持列出设备、查询状态、发送命令（turnOn/turnOff/press/lock/unlock/setPosition 等），以及执行 Scenes。需要设置 SWITCHBOT_TOKEN 和 SWITCHBOT_SECRET 环境变量。
metadata:
  openclaw:
    version: 1.0.5
    requires:
      env:
        - SWITCHBOT_TOKEN
        - SWITCHBOT_SECRET
      bins:
        - node
        - curl
        - openssl
        - jq
---

# SwitchBot OpenAPI Skill

通过 SwitchBot 官方 OpenAPI (v1.1) 控制和查询 SwitchBot 设备。

## 快速开始

### 1. 设置环境变量

```bash
export SWITCHBOT_TOKEN="your_token_here"
export SWITCHBOT_SECRET="your_secret_here"
```

### 2. 列出所有设备

```bash
node scripts/switchbot_cli.js list
```

### 3. 控制设备

```bash
# 打开灯
node scripts/switchbot_cli.js cmd <deviceId> turnOn

# 关闭灯
node scripts/switchbot_cli.js cmd <deviceId> turnOff

# 查询状态
node scripts/switchbot_cli.js status <deviceId>

# 执行 Scene
node scripts/switchbot_cli.js scene <sceneId>
```

## 支持的设备

✅ **开关类**：Plug、Plug Mini、Bot
✅ **窗帘类**：Curtain、Curtain 3、Blind Tilt、Roller Shade
✅ **门锁**：Lock、Lock Pro、Lock Ultra、Lock Lite
✅ **灯光**：Color Bulb、Strip Light、Floor Lamp、Ceiling Light
✅ **风扇**：Circulator Fan、Battery Circulator Fan
✅ **加湿器/净化器**：Humidifier、Air Purifier
✅ **扫地机**：S1、S1+、K10+、S10、S20、K11+、K20+ 等
✅ **温度控制**：Smart Radiator Thermostat
✅ **继电器**：Relay Switch 1PM/2PM
✅ **红外设备**：AC、TV、DVD、Speaker、Fan、Light 等
✅ **其他**：Garage Door Opener、Video Doorbell、Keypad、AI Art Frame

## 常用命令参考

详见 `references/commands.md` 和 `references/examples.md`

## 核心脚本文件

- `scripts/switchbot_cli.js` — Node.js CLI（主要工具）
- `scripts/list_devices.sh` — 列设备（curl）
- `scripts/get_status.sh` — 查询状态（curl）
- `scripts/send_command.sh` — 发送命令（curl）
- `scripts/list_scenes.sh` — 列 Scenes（curl）
- `scripts/execute_scene.sh` — 执行 Scene（curl）

## 文档

- `references/commands.md` — 完整命令参考表
- `references/examples.md` — 各设备使用示例
- `README-CLAWHUB.md` — ClawHub 发布说明

## 错误排查

| 错误代码 | 原因 | 解决方案 |
|---------|------|--------|
| 100 | 未授权 | 检查 SWITCHBOT_TOKEN/SECRET |
| 160 | 命令不支持 | 改用 Scenes |
| 190 | Token 无效 | 重新生成 Token |

---

更详细的信息见学习指南：`SWITCHBOT_LEARNING.md`
