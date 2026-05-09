# SwitchBot 设备清单 📋

**更新时间**: 2026-04-13 11:20 GMT+8  
**连接状态**: ✅ 成功  
**总设备数**: 11 台物理设备 + 12 台红外设备

---

## 🏠 物理设备（按家庭分类）

### 家庭：Urc压测
| 设备名 | 设备类型 | 设备ID | Cloud | 状态 |
|-------|---------|--------|-------|------|
| 万能遥控器 96 | remote with screen | B0E9FE502C96 | ❌ | 就绪 |

### 家庭：cc
| 设备名 | 设备类型 | 设备ID | Cloud | Hub |
|-------|---------|--------|-------|-----|
| 温湿度计Pro 04 | MeterPro | B0E9FE51EF04 | ❌ | - |
| 散热器恒温阀 66 | Smart Radiator Thermostat | B0E9FE8B3166 | ✅ | 000000000000 |
| Bot A0 | Bot | F19A73EEBFA0 | ✅ | D6FD8F60F9D7 |

### 家庭：default
| 设备名 | 设备类型 | 设备ID | Cloud | Hub |
|-------|---------|--------|-------|-----|
| 散热器恒温阀 3C | Smart Radiator Thermostat | B0E9FE691E3C | ✅ | 000000000000 |
| Al Art Frame 7B | AI Art Frame | B0E9FE74647B | ✅ | - |
| Al Art Frame 77 | AI Art Frame | B0E9FE7A1A77 | ✅ | - |
| Al Art Frame A7 | AI Art Frame | B0E9FEB3F9A7 | ✅ | - |
| 万能网关Mini D7 | Hub Mini2 | D6FD8F60F9D7 | ✅ | - |

### 家庭：无家庭位置
| 设备名 | 设备类型 | 设备ID | Cloud | Hub |
|-------|---------|--------|-------|-----|
| AI Hub B7 | AI Hub | B0E9FEA2B7B7 | ✅ | - |
| 散热器恒温阀 D2 | Smart Radiator Thermostat | B0E9FEAD69D2 | ✅ | 000000000000 |

---

## 🔴 红外设备（所有设备共享 Hub: D90DC1055D76）

### 空调（4 台）
| 设备名 | 设备ID | 类型 |
|-------|--------|------|
| 空调rili | 01-202405061831-08050414 | Air Conditioner |
| 空调sanlin | 01-202405061831-70616671 | Air Conditioner |
| 空调dakin | 01-202405061831-95941478 | Air Conditioner |
| 空调松下 | 01-202405061832-54776813 | Air Conditioner |

### 电视（4 台）
| 设备名 | 设备ID | 类型 |
|-------|--------|------|
| 电视rili | 01-202405061833-17094580 | TV |
| 电视sanlin | 01-202405061833-51921272 | TV |
| 电视东芝 | 01-202405061833-52059669 | TV |
| 电视sharp | 01-202405061834-17183689 | TV |

### 灯（4 台）
| 设备名 | 设备ID | 类型 |
|-------|--------|------|
| 灯sanlin | 01-202405061834-20200602 | Light |
| 灯rili | 01-202405061835-68308164 | Light |
| 灯sharp | 01-202405061835-73982166 | Light |
| 灯switchbot | 01-202405061836-31902234 | Light |

---

## ⚡ 快速控制命令

### 散热器恒温阀（Smart Radiator Thermostat）

```bash
# 查询状态
node skills/switchbot-openapi/scripts/switchbot_cli.js status B0E9FE691E3C

# 设置模式 (0=计划, 1=手动, 2=关闭, 3=省电, 4=舒适, 5=快速加热)
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE691E3C setMode --param=1

# 设置温度 (4-35°C)
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE691E3C setManualModeTemperature --param=22
```

### Bot（机械臂）

```bash
# 按压
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd F19A73EEBFA0 press
```

### AI Art Frame（艺术画框）

```bash
# 下一张
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE74647B next

# 上一张
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE74647B previous

# 上传图片（URL）
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd B0E9FE74647B uploadImage --param='{"imageUrl":"https://example.com/photo.jpg"}'
```

### 空调（红外）

```bash
# 冷却模式，温度 26°C，自动风
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd 01-202405061831-08050414 setAll --param="26,2,1,on"

# 加热模式，温度 20°C，低风
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd 01-202405061831-08050414 setAll --param="20,5,2,on"

# 关闭空调
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd 01-202405061831-08050414 turnOff
```

### 电视（红外）

```bash
# 切换到第 5 频道
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd 01-202405061833-17094580 SetChannel --param=5

# 音量上
node skills/switchbot-openapi/scripts/switchbot_cli.js cmd 01-202405061833-17094580 volumeAdd

# 音量下
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

## 🔧 设备能力矩阵

| 设备 | turnOn | turnOff | setMode | setTemp | setColor | 备注 |
|-----|--------|---------|---------|---------|----------|------|
| 散热器恒温阀 | ✅ | ✅ | ✅ | ✅ | - | Cloud 启用 |
| Bot | - | - | - | - | - | 仅 press |
| AI Art Frame | - | - | - | - | - | next/previous/uploadImage |
| 空调 | ✅ | ✅ | - | ✅ | - | setAll 模式 |
| 电视 | ✅ | ✅ | - | - | - | SetChannel/volume |
| 灯 | ✅ | ✅ | - | - | - | 仅开关 |

---

## 📝 使用建议

1. **散热器恒温阀**是你最经常控制的设备
   - 支持温度设置（4-35°C）
   - Cloud Service 已启用，远程控制无延迟

2. **AI Art Frame**适合演示和创意应用
   - 支持批量上传图片
   - 最多 10 张，超过后需在 App 中删除

3. **红外设备**（空调/电视/灯）
   - 都通过 Hub 控制，需要 Hub 在线
   - Hub ID: D90DC1055D76

4. **Bot 和温湿度计**
   - Bot 仅支持 press 命令
   - 温湿度计不支持 Cloud，查询受限

---

**下一步**: 测试几个设备控制命令，确认一切正常！
