# 日志拉取工具配置文档

**日期:** 2026-04-10  
**时间:** 17:20 - 18:39 GMT+8  
**目标:** 配置 Windows 环境下的自动日志拉取工具

---

## 📋 任务概览

需求：在 Windows 上快速拉取 Android 设备的两个日志目录，按时间戳分类存放，并自动压缩。

| 日志源 | 路径 | 文件数 |
|--------|------|--------|
| Android 系统日志 | `/data/misc/logd/` | 3 |
| SwitchBot 应用日志 | `/data/local/switchbot/log/` | 3 |

---

## 🔧 解决方案演进

### **第 1 阶段：理解需求（17:20-17:30）**
- 接收 4 个脚本文件（bash 和 bat 版本）
- 理解日志持久化流程：启动 → 重现问题 → 拉取

### **第 2 阶段：环境检查（17:30-17:47）**
```bash
✓ adb 已安装（v1.0.41）
✓ 设备已连接（B0E9FE9B33D0）
✓ 执行 startLogcatd.bat - 日志持久化启用成功
✓ 执行 pull_log.bat - 首次日志拉取成功
```

**手动拉取的文件：**
- logcat_pulled (4.8 MB)
- logcat_001_pulled (2.1 MB)
- logcat_002_pulled (2.1 MB)

### **第 3 阶段：添加第二个日志源（17:47-17:58）**
**需求变更：** 一起拉取 `/data/local/switchbot/log/`

**实现方案：** 创建 `pull_all_logs.bat`（双日志版本）

**拉取结果：**
| 路径 | 文件数 | 大小 |
|------|--------|------|
| /data/misc/logd/ | 3 | ~9 MB |
| /data/local/switchbot/log/ | 3 | ~8 MB |

### **第 4 阶段：时间戳分类存放（17:58-18:07）**
**需求变更：** 按日期时间点自动分类存放

**尝试方案：**
1. ❌ PowerShell 脚本 - 编码和引号问题
2. ❌ 批处理脚本 - 变量处理困难
3. ✅ **Python 脚本** - 最终解决方案

**创建脚本：** `pull_all_logs.py`

**特点：**
- 自动生成 `logs_YYYY-MM-DD_HH-MM-SS` 目录
- 按类型分类：`system_logd/` 和 `switchbot_log/`
- 容错处理：单文件失败不中断

### **第 5 阶段：压缩和非压缩双版本（18:13-18:34）**
**需求变更：** 输出压缩和非压缩两种版本

**最终脚本更新：** `pull_all_logs.py`

**输出结果：**
```
Desktop/
├── logs_2026-04-10_18-34-58/          (原始文件)
│   ├── system_logd/
│   │   ├── logcat
│   │   ├── logcat.001
│   │   └── logcat.002
│   └── switchbot_log/
│       ├── 2026-04-10.log
│       ├── central-2026-04-10.log
│       └── dockerd.log
└── logs_2026-04-10_18-34-58.zip       (压缩包 ~9MB)
```

---

## ✅ 最终成果

### **脚本工具**

| 文件 | 功能 | 状态 |
|------|------|------|
| `startLogcatd.bat` | 启用日志持久化 | ✅ 完成 |
| `pull_all_logs.py` | 一键拉取 + 分类 + 压缩 | ✅ 完成 |

### **工作流程**

```
1. python pull_all_logs.py
   ↓
2. 自动拉取两个日志源
   ↓
3. 按时间戳自动分类
   ↓
4. 同步生成：
   - 完整文件夹（查看用）
   - 压缩包（分享用）
```

### **质量指标**

- 系统日志拉取成功率：100% (3/3)
- SwitchBot 日志拉取成功率：100% (3/3)
- 总数据量：约 17 MB
- 压缩率：约 50%（~9 MB）

---

## 🎯 使用指南

### **快速开始**
```cmd
cd C:\Users\woan\.openclaw\workspace
python pull_all_logs.py
```

### **输出位置**
```
C:\Users\woan\Desktop\logs_{timestamp}/
C:\Users\woan\Desktop\logs_{timestamp}.zip
```

### **特点**
- ✅ 自动时间戳，每次不重复
- ✅ 双版本输出（原始 + 压缩）
- ✅ 清晰的目录分类
- ✅ 容错处理（权限错误自动跳过）

---

**配置完成日期：** 2026-04-10 18:39 GMT+8
