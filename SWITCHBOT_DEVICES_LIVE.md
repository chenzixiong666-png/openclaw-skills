# 📱 SwitchBot 设备清单（实时）

**更新时间**: 2026-04-13 11:31 GMT+8  
**连接状态**: ✅ 成功  
**总设备数**: 12 台物理设备 + 12 台红外设备 = **24 台**

---

## 🏠 物理设备（12 台）

### 家庭：default

| 📱 设备名 | 设备类型 | 设备 ID | Cloud | 状态 |
|---------|---------|--------|-------|------|
| 散热器恒温阀 3C | Smart Radiator Thermostat | `B0E9FE691E3C` | ✅ | 就绪 |
| Al Art Frame 7B | AI Art Frame | `B0E9FE74647B` | ✅ | 就绪 |
| Al Art Frame 77 | AI Art Frame | `B0E9FE7A1A77` | ✅ | 就绪 |
| Al Art Frame A7 | AI Art Frame | `B0E9FEB3F9A7` | ✅ | 就绪 |
| 万能网关Mini D7 | Hub Mini2 | `D6FD8F60F9D7` | ✅ | 就绪 |

### 家庭：cc

| 📱 设备名 | 设备类型 | 设备 ID | Cloud | 状态 |
|---------|---------|--------|-------|------|
| 温湿度计Pro 04 | MeterPro | `B0E9FE51EF04` | ❌ | 离线 |
| 散热器恒温阀 66 | Smart Radiator Thermostat | `B0E9FE8B3166` | ✅ | 就绪 |
| Bot A0 | Bot | `F19A73EEBFA0` | ✅ | 就绪 |

### 家庭：无家庭位置

| 📱 设备名 | 设备类型 | 设备 ID | Cloud | 状态 |
|---------|---------|--------|-------|------|
| AI Hub B7 | AI Hub | `B0E9FEA2B7B7` | ✅ | 就绪 |
| 散热器恒温阀 D2 | Smart Radiator Thermostat | `B0E9FEAD69D2` | ✅ | 就绪 |

### 家庭：Urc压测

| 📱 设备名 | 设备类型 | 设备 ID | Cloud | 状态 |
|---------|---------|--------|-------|------|
| 万能遥控器 96 | remote with screen | `B0E9FE502C96` | ❌ | 离线 |

### 家庭：相框

| 📱 设备名 | 设备类型 | 设备 ID | Cloud | 状态 |
|---------|---------|--------|-------|------|
| Al Art Frame 80 | AI Art Frame | `B0E9FEA8B080` | ✅ | 就绪 |

---

## 🔴 红外设备（12 台）

所有红外设备共享 Hub: `D90DC1055D76`

### 空调（4 台）

| ❄️ 设备名 | 控制类型 | 设备 ID |
|----------|---------|--------|
| 空调rili | Air Conditioner | `01-202405061831-08050414` |
| 空调sanlin | Air Conditioner | `01-202405061831-70616671` |
| 空调dakin | Air Conditioner | `01-202405061831-95941478` |
| 空调松下 | Air Conditioner | `01-202405061832-54776813` |

### 电视（4 台）

| 📺 设备名 | 控制类型 | 设备 ID |
|----------|---------|--------|
| 电视rili | TV | `01-202405061833-17094580` |
| 电视sanlin | TV | `01-202405061833-51921272` |
| 电视东芝 | TV | `01-202405061833-52059669` |
| 电视sharp | TV | `01-202405061834-17183689` |

### 灯（4 台）

| 💡 设备名 | 控制类型 | 设备 ID |
|----------|---------|--------|
| 灯sanlin | Light | `01-202405061834-20200602` |
| 灯rili | Light | `01-202405061835-68308164` |
| 灯sharp | Light | `01-202405061835-73982166` |
| 灯switchbot | Light | `01-202405061836-31902234` |

---

## ⚡ 常用快速命令

### 散热器恒温阀（3 台）

```bash
# 查询状态
node skills/switchbot-openapi/scripts/switchbot_cli.js status B0E9FE691E3C

# 设置温度 22°C
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE691E3C setManualModeTemperature --param=22

# 设置模式（0=计划 1=手动 2=关闭 3=省电 4=舒适 5=快速）
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE691E3C setMode --param=1
```

### AI 艺术画框（4 台）

```bash
# 下一张
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE74647B next

# 上一张
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE74647B previous

# 上传图片
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE74647B uploadImage --param='{"imageUrl":"https://example.com/photo.jpg"}'
```

### Bot（机械臂）

```bash
# 按压
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd F19A73EEBFA0 press
```

### 空调（红外）

```bash
# 冷却模式，26°C，自动风，打开
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd 01-202405061831-08050414 setAll --param="26,2,1,on"

# 关闭
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd 01-202405061831-08050414 turnOff
```

### 电视（红外）

```bash
# 切换频道
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd 01-202405061833-17094580 SetChannel --param=5

# 音量上升
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd 01-202405061833-17094580 volumeAdd

# 音量下降
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd 01-202405061833-17094580 volumeSub
```

### 灯（红外）

```bash
# 打开
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd 01-202405061834-20200602 turnOn

# 关闭
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd 01-202405061834-20200602 turnOff
```

---

## 📊 设备统计

| 分类 | 数量 | 已启用 Cloud | 备注 |
|------|------|------------|------|
| 散热器恒温阀 | 3 | 3 | ⭐ 主要控制设备 |
| AI 艺术画框 | 4 | 4 | 支持图片上传 |
| Hub/Gateway | 2 | 2 | 控制红外设备 |
| Bot | 1 | 1 | 仅支持 press |
| 温湿度计 | 1 | 0 | 查询受限 |
| 万能遥控器 | 1 | 0 | 离线 |
| **红外设备** | **12** | - | 空调 4、电视 4、灯 4 |
| **合计** | **24** | **16** | - |

---

## 🎯 推荐控制的设备

1. **散热器恒温阀** — 支持温度设置，Cloud 启用，随时可控 ✅
2. **空调** — 完整的温度和模式控制，通过 Hub 在线 ✅
3. **电视** — 频道、音量控制，通过 Hub 在线 ✅
4. **AI 画框** — 图片管理和显示，支持 URL 和 Base64 ✅
5. **Bot** — 机械臂按压，适合演示 ✅

---

**下一步**: 选择一个设备测试控制命令！建议从散热器恒温阀开始。
