# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Feishu Drive Configuration

**Default Output Folder (ALL future documents):**
- URL: https://ihqz5dyhwa.feishu.cn/drive/folder/A1KmfkVu5lM4Q1dpgdEchSYEnQd
- Folder Token: `A1KmfkVu5lM4Q1dpgdEchSYEnQd`
- Rule: 所有自动创建的飞书文档、表格、导出文件默认放在这个文件夹

**Usage:** When creating feishu_doc, feishu_bitable, or uploading files, use this folder as the default destination.

## SwitchBot Configuration

**Skill Location:**
- Path: `skills/switchbot-openapi/`
- CLI: `node skills/switchbot-openapi/scripts/switchbot_cli.js`

**Environment Variables (需要在 Gateway 中设置):**
```bash
SWITCHBOT_TOKEN    # OpenAPI Token (from SwitchBot App)
SWITCHBOT_SECRET   # OpenAPI Secret (from SwitchBot App)
SWITCHBOT_REGION   # Optional: global (default) / na / eu / jp
```

**常见操作：**
```bash
node skills/switchbot-openapi/scripts/switchbot_cli.js list        # 列设备
node skills/switchbot-openapi/scripts/switchbot_cli.js status <id> # 查状态
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd <id> turnOn  # 控制
```

**设备 ID 示例:**
- 灯：DCF9A7E2C3B1（Color Bulb）
- 窗帘：AABBCCDD1122（Curtain 3）
- 门锁：FB3A29024E71（Lock Pro）
- 扫地机：360TY400103021683（Robot Vacuum）
- 红外：01-202503291504-68270897（IR AC）

---

Add whatever helps you do your job. This is your cheat sheet.
