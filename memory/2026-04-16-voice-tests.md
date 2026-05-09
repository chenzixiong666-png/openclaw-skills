# Session: 2026-04-16 04:17:30 UTC

- **Session Key**: agent:main:main
- **Session ID**: 913d1e30-1bfe-4ed4-89a5-41e12bba4847
- **Source**: webchat

## Conversation Summary

user: A new session was started via /new or /reset. Run your Session Startup sequence - read the required files before responding to the user. Then greet the user in your configured persona, if one is provided. Be yourself - use your defined voice, mannerisms, and mood. Keep it to 1-3 sentences and ask what they want to do. If the runtime model differs from default_model in the system prompt, mention the default model. Do not mention internal steps, files, tools, or reasoning.
Current time: Thursday, April 16th, 2026 - 12:12 (Asia/Hong_Kong) / 2026-04-16 04:12 UTC
assistant: 靓仔，我在这儿。✨  
今天想一起搞点什么？
user: [media attached: C:\Users\woan\.openclaw\media\inbound\90aad714-1625-4570-9a0d-ad08332724b2.jpg (image/jpeg) | C:\Users\woan\.openclaw\media\inbound\90aad714-1625-4570-9a0d-ad08332724b2.jpg]
To send an image back, prefer the message tool (media/path/filePath). If you must inline, use MEDIA:https://example.com/image.jpg (spaces ok, quote if needed) or a safe relative path like MEDIA:./image.jpg. Avoid absolute paths (MEDIA:/...) and ~ paths - they are blocked for security. Keep caption in the text body.
Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b51326a2dd8a8c2e43b0a5c50a31",
  "sender_id": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "sender": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "timestamp": "Thu 2026-04-16 12:15 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "id": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "name": "ou_9c8d825e05f86d5b1794dea7e7a30a36"
}
```

[message_id: om_x100b51326a2dd8a8c2e43b0a5c50a31]
ou_9c8d825e05f86d5b1794dea7e7a30a36: ![image]
根据这个写测试用例
assistant: 我看了图，这是 **AI Hub Show – Voice Interaction（语音交互）流程**，核心逻辑是：

用户说话 → 设备检测唤醒 → 语音识别 → 语义理解 → AI处理 → 返回结果（语音 / 屏幕 / 设备控制）。

按你之前的用例规范，我给你拆了一组 **核心测试用例（示例）**：

---

**ID**: TC_VOICE_001  
**一级模块**: AI Hub Show  
**二级模块**: 语音交互  
**三级模块**: 唤醒与识别  

**用例名称**: 唤醒词触发语音助手  

**优先级**: P0  
**用例类型**: 功能测试  

**前置条件**:  
设备已开机并处于待机状态，语音服务正常

**步骤描述**:  
#用户说出唤醒词  
#设备检测语音并进入语音识别流程  

**预期结果**:  
#设备成功识别唤醒词  
#进入语音交互状态并提示用户说出指令  

---

**ID**: TC_VOICE_002  
**一级模块**: AI Hub Show  
**二级模块**: 语音交互  
**三级模块**: 指令识别  

**用例名称**: 语音指令识别与语义理解  

**优先级**: P0  
**用例类型**: 功能测试  

**前置条件**:  
设备已被唤醒并进入语音交互状态  

**步骤描述**:  
#用户说出语音指令（如：打开客厅灯）  
#系统进行语音识别  
#系统进行语义理解  

**预期结果**:  
#系统正确识别语音文本  
#系统正确解析用户意图  

---

**ID**: TC_VOICE_003  
**一级模块**: AI Hub Show  
**二级模块**: 语音交互  
**三级模块**: AI处理  

**用例名称**: AI生成语音回复  

**优先级**: P1  
**用例类型**: 功能测试  

**前置条件**:  
系统已正确解析用户语音意图  

**步骤描述**:  
#系统将用户意图发送至AI处理模块  
#AI生成回复内容  

**预期结果**:  
#AI成功生成语义合理的回复内容  
#回复内容返回设备端  

---

**ID**: TC_VOICE_004  
**一级模块**: AI Hub Show  
**二级模块**: 语音交互  
**三级模块**: 设备控制  

**用例名称**: 语音控制智能设备  

**优先级**: P0  
**用例类型**: 功能测试  

**前置条件**:  
系统已正确解析用户控制指令，设备在线  

**步骤描述**:  
#用户说出设备控制指令（如：打开空调）  
#系统解析指令并发送控制命令  

**预期结果**:  
#系统正确发送控制指令  
#对应设备状态发生变化  

---

**ID**: TC_VOICE_005  
**一级模块**: AI Hub Show  
**二级模块**: 语音交互  
**三级模块**: 异常处理  

**用例名称**: 无法识别语音指令处理  

**优先级**: P2  
**用例类型**: 异常测试  

**前置条件**:  
设备处于语音交互状态  

**步骤描述**:  
#用户说出模糊或无法识别的语音  
#系统进行识别处理  

**预期结果**:  
#系统识别失败  
#设备提示用户重新说出指令  

---

如果按照 **你现在的项目标准（需求→测试点→测试用例）**，这张图其实还能拆成 **3层结构**：

**1️⃣ 测试点**
- 唤醒词识别
- 语音识别准确性
- 语义理解
- AI回复生成
- 设备控制
- 异常处理

**2️⃣ 测试用例**
每个测试点再展开多个场景。

---

如果你愿意，我可以帮你把 **这张图完整拆成一套系统级测试用例（20~30条，带P0/P1/P2分级）**，基本就是 **一份可以直接交付的测试用例表**。
