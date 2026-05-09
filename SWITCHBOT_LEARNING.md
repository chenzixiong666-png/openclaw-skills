# SwitchBot Cloud API Skill - 详细学习指南

_学习时间：2026-04-13 | 来源：switchbot-cloudapi-1.0.5_

---

## 第一部分：概念理解

### 什么是 SwitchBot OpenAPI？

SwitchBot 官方提供的 HTTP API (v1.1)，用于远程控制 SwitchBot 生态的所有智能设备。

**三层结构：**
```
┌─────────────────┐
│  OpenAPI v1.1   │ (官方 HTTP API)
├─────────────────┤
│  Node CLI       │ (自动处理签名、时间戳、重试)
├─────────────────┤
│ 我们的代理     │ (调用 CLI，无需关心签名细节)
└─────────────────┘
```

### 为什么要用 CLI 而不是直接调用 API？

1. **签名复杂性** — 每个请求需要 HMAC-SHA256 签名，涉及 token + timestamp + nonce
2. **参数拼接** — 某些设备的参数格式奇怪（如窗帘的 "0,ff,50"）
3. **能力检测** — CLI 会自动检查设备是否支持某个命令
4. **重试机制** — 失败自动重试，无需手动处理

**结论**：直接用 `node switchbot_cli.js` — 既简单又可靠。

---

## 第二部分：快速实战

### Step 1: 设置环境变量

```bash
# 在 OpenClaw Gateway 或容器中设置
export SWITCHBOT_TOKEN="your_token_here"
export SWITCHBOT_SECRET="your_secret_here"
export SWITCHBOT_REGION="global"  # 可选
```

### Step 2: 列出所有设备

```bash
node scripts/switchbot_cli.js list
```

**输出示例：**
```
🏠 Home
  └─ 客厅
     ├─ 客厅灯 (Color Bulb) - DCF9A7E2C3B1
     ├─ 客厅窗帘 (Curtain 3) - AABBCCDD1122
  └─ 卧室
     ├─ 卧室空调 (IR AC Hub) - 01-202503291504-68270897

🏠 办公室
  └─ 默认房间
     ├─ 门锁 (Lock Pro) - FB3A29024E71
```

### Step 3: 基础控制

**打开灯：**
```bash
node switchbot_cli.js cmd DCF9A7E2C3B1 turnOn
```

**关闭灯：**
```bash
node switchbot_cli.js cmd DCF9A7E2C3B1 turnOff
```

**打开窗帘（10%）：**
```bash
node switchbot_cli.js cmd AABBCCDD1122 setPosition --pos=10
```

**锁门：**
```bash
node switchbot_cli.js cmd FB3A29024E71 lock
```

### Step 4: 查询设备状态

```bash
node switchbot_cli.js status DCF9A7E2C3B1
```

**输出示例：**
```json
{
  "statusCode": 0,
  "body": {
    "deviceId": "DCF9A7E2C3B1",
    "deviceType": "Color Bulb",
    "power": "on",
    "brightness": 80,
    "colorTemperature": 4000,
    "colorRGB": 16777215
  }
}
```

---

## 第三部分：设备类型完全速查

### 🔌 简单开关类（Plug、Plug Mini、Bot）

```bash
# Plug Mini - 打开
node switchbot_cli.js cmd 3C8427B2118A turnOn

# Plug Mini - 关闭
node switchbot_cli.js cmd 3C8427B2118A turnOff

# Plug Mini - 切换
node switchbot_cli.js cmd 3C8427B2118A toggle

# Bot（机械臂）- 按压
node switchbot_cli.js cmd DFC21012C18F press
```

### 🪟 窗帘类（Curtain、Curtain 3、Blind Tilt、Roller Shade）

**Curtain / Curtain 3：**
```bash
# 设置位置 (0=完全开, 100=完全关)
node switchbot_cli.js cmd AABBCCDD setPosition --pos=50

# 打开（等同于 pos=0）
node switchbot_cli.js cmd AABBCCDD turnOn

# 关闭（等同于 pos=100）
node switchbot_cli.js cmd AABBCCDD turnOff

# 暂停
node switchbot_cli.js cmd AABBCCDD pause
```

**Blind Tilt（百叶窗）：**
```bash
# 设置方向和位置 (direction: up/down, pos: 0-100)
node switchbot_cli.js cmd AABB setPosition --param="up;60"

# 完全打开
node switchbot_cli.js cmd AABB fullyOpen

# 向上关闭
node switchbot_cli.js cmd AABB closeUp

# 向下关闭
node switchbot_cli.js cmd AABB closeDown
```

**Roller Shade（卷帘）：**
```bash
# 设置位置 (0=开, 100=关)
node switchbot_cli.js cmd AABB setPosition --pos=50
```

### 🔐 门锁类（Lock、Lock Pro、Lock Ultra、Lock Lite）

```bash
# 上锁
node switchbot_cli.js cmd FB3A29024E71 lock

# 解锁
node switchbot_cli.js cmd FB3A29024E71 unlock

# 触发死栓（离合器）
node switchbot_cli.js cmd FB3A29024E71 deadbolt
```

### 💡 灯类（Color Bulb、Strip Light、Floor Lamp、Ceiling Light、Candle Warmer Lamp）

**彩色灯（RGB）：**
```bash
# 设置 RGB 颜色 (R:G:B, 范围 0-255)
node switchbot_cli.js cmd DC0675A7675A setColor --param="255:100:0"

# 设置亮度 (1-100)
node switchbot_cli.js cmd DC0675A7675A setBrightness --param=80

# 设置色温 (2700-6500K)
node switchbot_cli.js cmd DC0675A7675A setColorTemperature --param=4000

# 打开/关闭
node switchbot_cli.js cmd DC0675A7675A turnOn
node switchbot_cli.js cmd DC0675A7675A turnOff

# 切换
node switchbot_cli.js cmd DC0675A7675A toggle
```

**天花板灯 / Ceiling Light：**
```bash
# 亮度 (1-100)
node switchbot_cli.js cmd AABB setBrightness --param=60

# 色温 (2700-6500K)
node switchbot_cli.js cmd AABB setColorTemperature --param=5000
```

### 🌀 风扇类（Battery Circulator Fan、Circulator Fan、Standing Circulator Fan）

```bash
# 打开
node switchbot_cli.js cmd AABB turnOn

# 设置风模式 (direct/natural/sleep/baby)
node switchbot_cli.js cmd AABB setWindMode --param=natural

# 设置风速 (1-100)
node switchbot_cli.js cmd AABB setWindSpeed --param=50

# 夜灯模式 (off / 1=亮 / 2=暗)
node switchbot_cli.js cmd AABB setNightLightMode --param=1

# 自动关闭延迟 (秒数)
node switchbot_cli.js cmd AABB closeDelay --param=3600
```

### 🌡️ 加湿器 & 空气净化器

**原始加湿器：**
```bash
# 模式：auto/101(34%)/102(67%)/103(100%)
node switchbot_cli.js cmd AABB setMode --param=auto
```

**蒸发式加湿器（带自动补水）：**
```bash
# 模式 1-8，目标湿度 0-100%
node switchbot_cli.js cmd A0A3B32CAE62 setMode --param='{"mode":7,"targetHumidify":60}'

# 儿童锁
node switchbot_cli.js cmd A0A3B32CAE62 setChildLock --param=true
```

**空气净化器（VOC/PM2.5）：**
```bash
# 模式：1=普通, 2=自动, 3=睡眠, 4=宠物；风速 1-3
node switchbot_cli.js cmd ACA704AF64FE setMode --param='{"mode":2,"fanGear":2}'

# 儿童锁
node switchbot_cli.js cmd ACA704AF64FE setChildLock --param=1
```

### 🤖 扫地机（Robot Vacuum S1/S1+/K10+/K10+Pro/S10/S20/K11+/K20+）

**简单款（S1/S1+/K10+/K10+Pro）：**
```bash
# 开始清扫
node switchbot_cli.js cmd 360TY400103021683 start

# 停止
node switchbot_cli.js cmd 360TY400103021683 stop

# 回充
node switchbot_cli.js cmd 360TY400103021683 dock

# 吸力等级 (0=安静, 1=标准, 2=强力, 3=最强)
node switchbot_cli.js cmd 360TY400103021683 PowLevel --param=2
```

**高级款（S10/S20/K10+Pro Combo/K20+Pro/K11+）：**
```bash
# 扫地 + 拖地
node switchbot_cli.js cmd AABB startClean --param='{"action":"sweep_mop","param":{"fanLevel":2,"waterLevel":1,"times":1}}'

# 仅扫地
node switchbot_cli.js cmd AABB startClean --param='{"action":"sweep","param":{"fanLevel":2,"times":1}}'

# 暂停
node switchbot_cli.js cmd AABB pause

# 回充
node switchbot_cli.js cmd AABB dock

# 设置音量 (0-100)
node switchbot_cli.js cmd AABB setVolume --param=50

# 自清洁（仅 S10/S20）(1=洗, 2=烘干, 3=取消)
node switchbot_cli.js cmd AABB selfClean --param=1

# 修改参数
node switchbot_cli.js cmd AABB changeParam --param='{"fanLevel":3,"waterLevel":2,"times":5}'
```

### 🌡️ 智能暖气温控器

```bash
# 模式 (0=计划, 1=手动, 2=关闭, 3=省电, 4=舒适, 5=快速加热)
node switchbot_cli.js cmd AABB setMode --param=1

# 手动模式温度 (4-35°C)
node switchbot_cli.js cmd AABB setManualModeTemperature --param=22
```

### 🎛️ 继电器开关（Relay Switch 1PM/1/2PM）

**单通道（1PM / 1）：**
```bash
# 打开/关闭
node switchbot_cli.js cmd C04E30DFEE06 turnOn
node switchbot_cli.js cmd C04E30DFEE06 turnOff

# 切换
node switchbot_cli.js cmd C04E30DFEE06 toggle

# 工作模式 (0=切换, 1=边缘, 2=离分, 3=瞬间)
node switchbot_cli.js cmd C04E30DFEE06 setMode --param=0
```

**双通道（2PM）：**
```bash
# 通道 1 打开
node switchbot_cli.js cmd AABB turnOn --param="1"

# 通道 2 打开
node switchbot_cli.js cmd AABB turnOn --param="2"

# 通道 1 工作模式
node switchbot_cli.js cmd AABB setMode --param="1;0"
```

### 🚪 车库门开启器

```bash
# 打开（抬起车库门）
node switchbot_cli.js cmd AABB turnOn

# 关闭（放下车库门）
node switchbot_cli.js cmd AABB turnOff
```

### 📹 视频门铃 & 密码键盘

**视频门铃：**
```bash
# 启用人体检测
node switchbot_cli.js cmd AABB enableMotionDetection

# 禁用人体检测
node switchbot_cli.js cmd AABB disableMotionDetection
```

**Keypad / Keypad Touch / Keypad Vision：**
```bash
# 创建永久密码
node switchbot_cli.js cmd DE133622237A createKey --param='{"name":"Front Door","type":"permanent","password":"12345678"}'

# 创建临时密码 (时间限制)
node switchbot_cli.js cmd DE133622237A createKey --param='{"name":"Guest","type":"timeLimit","password":"998877","startTime":1664640056,"endTime":1665331432"}'

# 删除密码
node switchbot_cli.js cmd DE133622237A deleteKey --param='{"id":"11"}'
```

⚠️ **Keypad 命令是异步的** — 结果通过 webhook 返回，不是 HTTP 响应。

### 🎨 AI 艺术画框

```bash
# 下一张
node switchbot_cli.js cmd B0E9FEB6F885 next

# 上一张
node switchbot_cli.js cmd B0E9FEB6F885 previous

# 上传图片（URL）
node switchbot_cli.js cmd B0E9FEB6F885 uploadImage --param='{"imageUrl":"https://example.com/photo.jpg"}'

# 上传图片（Base64）
node switchbot_cli.js cmd B0E9FEB6F885 uploadImage --param='{"imageBase64":"iVBORw0KGgoAAAANS..."}'
```

⚠️ statusCode 402 = 达到上限（最多 10 张），需要在 App 中删除。

### 🔴 红外设备（空调、电视、其他）

**红外空调：**
```bash
# 设置所有参数 (温度,模式,风速,电源)
# 模式: 0/1=自动, 2=冷却, 3=干燥, 4=风扇, 5=加热
# 风速: 1=自动, 2=低, 3=中, 4=高
# 电源: on/off

# 冷却模式，26°C，自动风，打开
node switchbot_cli.js cmd 01-202503291504-68270897 setAll --param="26,2,1,on"

# 加热模式，20°C，低风，打开
node switchbot_cli.js cmd 01-202503291504-68270897 setAll --param="20,5,2,on"

# 关闭
node switchbot_cli.js cmd 01-202503291504-68270897 turnOff
```

**红外电视：**
```bash
# 切换到第 5 频道
node switchbot_cli.js cmd 01-202504011717-10628124 SetChannel --param=5

# 音量上
node switchbot_cli.js cmd 01-202504011717-10628124 volumeAdd

# 音量下
node switchbot_cli.js cmd 01-202504011717-10628124 volumeSub

# 下一频道
node switchbot_cli.js cmd 01-202504011717-10628124 channelAdd

# 上一频道
node switchbot_cli.js cmd 01-202504011717-10628124 channelSub
```

**红外播放器（DVD/Speaker）：**
```bash
node switchbot_cli.js cmd AABB setMute        # 静音
node switchbot_cli.js cmd AABB FastForward    # 快进
node switchbot_cli.js cmd AABB Rewind         # 快退
node switchbot_cli.js cmd AABB Next           # 下一曲
node switchbot_cli.js cmd AABB Previous       # 上一曲
node switchbot_cli.js cmd AABB Pause          # 暂停
node switchbot_cli.js cmd AABB Play           # 播放
node switchbot_cli.js cmd AABB Stop           # 停止
```

**红外风扇：**
```bash
node switchbot_cli.js cmd AABB swing          # 摇头
node switchbot_cli.js cmd AABB timer          # 定时
node switchbot_cli.js cmd AABB lowSpeed       # 低速
node switchbot_cli.js cmd AABB middleSpeed    # 中速
node switchbot_cli.js cmd AABB highSpeed      # 高速
```

**自定义红外（DIY）：**
```bash
# 必须使用 --commandType=customize
node switchbot_cli.js cmd 01-XXXX myButtonName --commandType=customize
```

---

## 第四部分：Scenes（场景）使用

当某个设备不支持直接命令时，用 Scenes 代替。

### 列出所有 Scenes

```bash
node switchbot_cli.js scenes
```

**输出示例：**
```
Scene ID                    Scene Name
T02-20230101-xxxxxxxx      下班回家
T02-20230102-yyyyyyyy      睡前关闭所有灯
T02-20230103-zzzzzzzz      早上起床
```

### 执行 Scene

```bash
node switchbot_cli.js scene T02-20230101-xxxxxxxx
```

---

## 第五部分：常见参数格式详解

### ❌ 常见错误

| 参数 | ❌ 错误写法 | ✅ 正确写法 |
|------|-----------|----------|
| 窗帘位置 | `--pos=50` （忘记转换） | `--pos=50` (CLI 自动转成 "0,ff,50") |
| RGB 色 | `255, 100, 0` | `"255:100:0"` （冒号不是逗号） |
| JSON | `{mode:1}` | `'{"mode":1}'` （双引号 + 单引号包裹） |
| 空调模式 | 参数写反 | `"温度,模式,风速,电源"` 不是 "模式,温度,..." |

### ✅ 格式总结

| 设备类型 | 参数格式 | 示例 |
|---------|--------|------|
| 窗帘位置 | `--pos=<0-100>` | `--pos=50` |
| RGB 颜色 | `"<R>:<G>:<B>"` | `"255:100:0"` |
| 色温 | `<2700-6500>` | `4000` |
| 亮度 | `<0-100>` | `80` |
| JSON 对象 | `'{"key":"value"}'` | 用单引号包裹 |
| 逗号分隔 | `"val1,val2,val3"` | 空调参数 |
| 分号分隔 | `"dir;value"` | 百叶窗 `"up;60"` |

---

## 第六部分：排查与调试

### 常见错误代码

| 代码 | 含义 | 解决方案 |
|-----|-----|--------|
| 0 | 成功 | ✅ 没问题 |
| 100 | 未授权 / Token 错误 | 检查 SWITCHBOT_TOKEN 和 SWITCHBOT_SECRET |
| 160 | 命令不支持 | 该设备类型不支持这个命令，改用 Scenes |
| 190 | Token 无效 | Token 过期或错误；检查 SwitchBot App 重新生成 |
| 1001 | Hub 离线 | Hub 设备不在线，检查网络 |

### 调试技巧

**1. 打印详细日志**

CLI 会自动输出请求和响应，用于排查。

**2. 检查设备能力**

```bash
# 先查询设备状态，看是否返回详细信息
node switchbot_cli.js status <deviceId>
```

**3. 验证签名（高级）**

如果怀疑签名问题，查看 `scripts/switchbot_cli.js` 的签名算法：
```javascript
const sign = crypto.createHmac('sha256', secret).update(token + t + nonce).digest('base64');
```

---

## 第七部分：实战场景

### 场景 A：回家自动化

```bash
#!/bin/bash
# 回家时：打开玄关灯，打开窗帘，解锁门

node switchbot_cli.js cmd DC0675A7675A turnOn              # 玄关灯开
node switchbot_cli.js cmd AABBCCDD setPosition --pos=20   # 窗帘打开 20%
node switchbot_cli.js cmd FB3A29024E71 unlock              # 解锁
```

### 场景 B：睡前关闭

```bash
#!/bin/bash
# 睡前：关闭所有灯，关闭窗帘，锁门

node switchbot_cli.js cmd DC0675A7675A turnOff             # 卧室灯关
node switchbot_cli.js cmd AABBCCDD setPosition --pos=100   # 窗帘关闭
node switchbot_cli.js cmd FB3A29024E71 lock                # 上锁
```

### 场景 C：清晨启动

```bash
#!/bin/bash
# 早上：打开台灯，启动扫地机，设置空调 23°C

node switchbot_cli.js cmd AABB setBrightness --param=30   # 台灯 30%
node switchbot_cli.js cmd 360TY400103021683 start          # 扫地机启动
node switchbot_cli.js cmd 01-202503291504-68270897 setAll --param="23,5,2,on"  # 加热 23°C
```

---

## 📚 参考资源

- **完整命令表**：`references/commands.md`
- **更多示例**：`references/examples.md`
- **官方文档**：https://developer.switch-bot.com/docs/

---

**🎓 学习完成标志**

你现在可以：
- ✅ 列出所有设备和家庭结构
- ✅ 用正确的参数格式控制各类设备
- ✅ 判断何时使用 Scenes 兜底
- ✅ 排查常见错误
- ✅ 写出自动化脚本

祝你用得愉快！🚀
