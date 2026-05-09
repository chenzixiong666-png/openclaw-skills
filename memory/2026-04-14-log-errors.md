# Session: 2026-04-14 06:12:50 UTC

- **Session Key**: agent:main:main
- **Session ID**: dc73e920-d355-46bb-a3ba-c90d2271f4d0
- **Source**: feishu

## Conversation Summary

assistant: 我看了你发的这段 log，核心信息其实很明显：**App 启动时用户是未登录状态**，所以所有设备相关流程都没有继续。

关键几行：

1️⃣  
`本地 accessToken 为空，不发出请求`  
→ 本地没有登录 token，所以 API 请求直接被拦截。

2️⃣  
`获取用户数据和相关流程 failure: 未登录`  
→ 用户中心初始化失败，因为没有登录。

3️⃣  
`iot连接：用户未登录，不连接MQTT`  
→ MQTT 不会连接，所以设备状态不会同步。

4️⃣  
`首页更新了红外设备列表:0`  
→ 设备列表为空。

5️⃣  
`收到退出登录的通知，清除设备列表`  
→ 系统主动清空设备缓存。

总结一下这个 log 的状态：

- App 正常启动 ✅  
- 数据库初始化正常 ✅  
- 网络请求正常 ✅  
- **用户未登录 ❗**
- **设备列表被清空 ❗**
- **IoT MQTT 没有连接 ❗**

所以如果你遇到的是：

- 设备不显示  
- 无法控制设备  
- 首页空白  

原因就是 **当前账号没有登录（或 token 已失效）**。

解决办法：

1. 重新登录 SwitchBot 账号  
2. 登录后 App 会重新：
   - 获取设备列表
   - 建立 MQTT
   - 同步设备状态

如果你愿意，我也可以 **帮你继续把这个 6 万行 log 里真正的异常点抓出来**（比如 crash / API error / BLE 问题），我可以直接给你定位关键行，比人工看快很多。
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b52ee6c5a70b4c2bc19c58271ae0",
  "sender_id": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "sender": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "timestamp": "Tue 2026-04-14 10:10 GMT+8"
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

[message_id: om_x100b52ee6c5a70b4c2bc19c58271ae0]
ou_9c8d825e05f86d5b1794dea7e7a30a36: 筛选报错
assistant: 从你这段 log 里看，**没有真正的 crash 或接口 error**，主要是这些 **warning / 状态类日志**。如果你是要 **“筛选报错”**，可以重点抓下面几类关键词：

建议筛选关键词：

- `❗️`（warning / error 标记）
- `error`
- `fail`
- `failure`
- `Exception`
- `crash`
- `timeout`

在你这段 log 里实际出现的“报错类”主要是：

1️⃣ 本地文件不存在（轻微）
`未能打开文件 “pinDeviceList.txt”，因为它不存在`

原因：  
App 第一次启动或缓存被清理，本地 pin 设备列表不存在。  
影响：无影响，正常情况。

---

2️⃣ SQL 执行警告
`执行SQL语句时出错，错误信息为：nil`

特点：
- 出现了几次
- 但数据库随后 **正常 open 和 create table**

判断：  
属于 **初始化查询失败（可能表还没建）**，不是致命错误。

---

3️⃣ 地理位置权限
`User not authorized`

原因：  
App 没有定位权限。

影响：
- 不能用 **地理围栏自动化**
- 其他功能不影响。

---

4️⃣ IoT 连接未建立（关键状态）
`iot连接：用户未登录，不连接MQTT`

原因：  
当前 **用户未登录**。

影响：
- 不会同步设备状态
- 设备列表为空。

---

✅ **总结**

真正需要关注的只有一个：

**用户未登录 → MQTT 不连接 → 设备列表为空**

其它：

- 文件不存在 ✅ 正常
- SQL warning ✅ 初始化阶段
- 定位未授权 ✅ 权限问题

都不是功能性 bug。

---

如果你是 **做 QA / 提 bug / 写分析报告**，我可以帮你把这段 log **整理成一份标准问题分析（Root Cause + 关键日志）**，直接可以贴到 Jira。
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b52ee660430a0c2b68c7504bb0e8",
  "sender_id": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "sender": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "timestamp": "Tue 2026-04-14 10:12 GMT+8"
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

[message_id: om_x100b52ee660430a0c2b68c7504bb0e8]
ou_9c8d825e05f86d5b1794dea7e7a30a36: 筛选失败
assistant: 从这段 log 里能看到的 **“筛选失败”相关信号其实很弱**，没有直接出现 `filter fail` 之类的日志。但有几个 **可能导致筛选失败的上游状态**：

1️⃣ **用户未登录（最关键）**  
日志多次出现：
- `本地 accessToken 为空，不发出请求`
- `获取用户数据和相关流程 failure: 未登录`
- `iot连接：用户未登录，不连接MQTT`

结果：
- 设备列表为空  
- 首页数据源 = 0  
- 任何设备/列表筛选都会 **返回空结果**

相关日志：
`setAllDatasources 已绑定数据源：0`

---

2️⃣ **设备列表被清空**

日志：
`准备清空设备列表`  
`缓存了内存中的设备数据到本地：0个设备`

如果筛选是针对设备列表，这一步之后：

设备数 = 0  
→ 筛选必然返回空。

---

3️⃣ **分组信息缺失**

日志：
`重新排序失败,原因:无法获取到当前group`

如果筛选依赖 **group / room / family**，这里会影响筛选逻辑。

---

✅ **综合判断**

这段 log 的实际问题链条是：

未登录  
→ accessToken 为空  
→ 不拉设备列表  
→ 设备列表被清空  
→ 数据源 = 0  
→ **筛选返回空 / 看起来像“筛选失败”**

---

✅ **一句话 Root Cause（适合写问题分析）：**

由于用户未登录导致 accessToken 为空，设备列表未加载并被清空，首页数据源为 0，从而导致筛选逻辑返回空结果。

---

如果你愿意，你可以把 **出现“筛选失败”的那一小段 log（操作前后 10 秒）**发出来，我可以帮你 **精准定位是哪一行触发筛选逻辑的**，一般都会有类似：

```
filter start
filter result
filter count
```

那种日志，一眼就能抓出来。
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b52ee7b1c1580c35647f4309d708",
  "sender_id": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "sender": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "timestamp": "Tue 2026-04-14 10:15 GMT+8"
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

[message_id: om_x100b52ee7b1c1580c35647f4309d708]
ou_9c8d825e05f86d5b1794dea7e7a30a36: 汇总结果: 失败 ❌的数据，原因
assistant: 根据这段 log，可以把 **“失败 ❌ 数据原因”**汇总成下面几条（按影响程度）：

1. **用户未登录**
   - 关键日志：`获取用户数据和相关流程 failure: 未登录`
   - 关键日志：`本地 accessToken 为空，不发出请求`
   - 影响：设备列表、消息中心、IoT 等接口都不会请求，导致数据为空。

2. **MQTT 未建立连接**
   - 关键日志：`iot连接：用户未登录，不连接MQTT`
   - 影响：设备状态和实时数据无法同步。

3. **设备列表被清空**
   - 关键日志：`准备清空设备列表`
   - 关键日志：`缓存了内存中的设备数据到本地：0个设备`
   - 影响：首页数据源为空，相关功能（如筛选）返回空结果。

4. **分组信息获取失败**
   - 关键日志：`重新排序失败,原因:无法获取到当前group`
   - 影响：设备分组或排序逻辑异常。

5. **本地缓存文件不存在（轻微）**
   - 关键日志：`未能打开文件“pinDeviceList.txt”，因为它不存在`
   - 原因：首次启动或缓存被清理。
   - 影响：不影响主要功能。

6. **SQL 初始化警告（轻微）**
   - 关键日志：`执行SQL语句时出错，错误信息为：nil`
   - 随后数据库和表均创建成功，属于初始化阶段日志。

7. **定位权限未授权**
   - 关键日志：`User not authorized`
   - 影响：地理围栏相关功能不可用。

✅ **最终结论（Root Cause）：**  
用户未登录导致 accessToken 为空，设备列表未加载并被清空，首页数据源为 0，从而导致筛选结果返回空数据，表现为“失败 ❌”。
user: [media attached: C:\Users\woan\.openclaw\media\inbound\2026.04.10---442e3a83-92ed-422d-97dd-91f1c7637abb.csv (text/csv) | C:\Users\woan\.openclaw\media\inbound\2026.04.10---442e3a83-92ed-422d-97dd-91f1c7637abb.csv]
To send an image back, prefer the message tool (media/path/filePath). If you must inline, use MEDIA:https://example.com/image.jpg (spaces ok, quote if needed) or a safe relative path like MEDIA:./image.jpg. Avoid absolute paths (MEDIA:/...) and ~ paths - they are blocked for security. Keep caption in the text body.
Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b52efc5259968c3224db267bcc22",
  "sender_id": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "sender": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "timestamp": "Tue 2026-04-14 11:47 GMT+8"
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

[Feishu ou_9c8d825e05f86d5b1794dea7e7a30a36 Tue 2026-04-14 11:47 GMT+8] [message_id: om_x100b52efc5259968c3224db267bcc22]
ou_9c8d825e05f86d5b1794dea7e7a30a36: {"file_key":"file_v3_0010o_1c03b2da-5461-46a2-9b5e-f53261b0f8fg","file_name":"2026.04.10.csv"}

<file name="2026.04.10---442e3a83-92ed-422d-97dd-91f1c7637abb.csv" mime="text/csv">

<<<EXTERNAL_UNTRUSTED_CONTENT id="2d297139cf37b6ff">>>
Source: External
---
时间戳,当前栈顶页面,类型,内容,备注
1775791050399,,APP启动,构建信息：a6643be27_2026-02-06 20:51:39_app-builder,
1775791050502,,其他类型,mType=No network ,NetworkStatusCallback
1775791050504,,其他类型,初始值memToken = eyJhbGciOiJFUzI1NiIsImlzcyI6InN3aXRjaGJvdC5zMy5hbWF6b25hd3MuY29tIiwia2lkIjoiNGQ3ZmI1OGIzMmFlZTdlNjJmMmE3Mjk4ZTRiYWIyMmIiLCJrdHkiOiJFQyIsInR5cCI6IkpXVCIsInYiOjF9.eyJjaGFubmVsIjoic2VsZiIsInBsYXRmb3JtIjoiQW5kcm9pZCIsImRldmljZUlEIjoiNDFkZS04Yjc3LTVhY2YtNDdlZiIsImNsaWVudF9pZCI6IjVubndtaG1zYTl4eHNrbTE0aGQ4NWxtOWJtIiwidXNlcklEIjoiOTc3MzgyOGMtOTBiYi00NzI1LWEwNGMtMzM5ZTBlZWMzMDBlIiwic3ViIjoiOTc3MzgyOGMtOTBiYi00NzI1LWEwNGMtMzM5ZTBlZWMzMDBlIiwidXNlcm5hbWUiOiI5NzczODI4Yy05MGJiLTQ3MjUtYTA0Yy0zMzllMGVlYzMwMGUiLCJzY29wZSI6InN3aXRjaGJvdCBhY2NvdW50IiwiZXhwIjoxNzc0Nzg4NTA0LCJqdGkiOiIzMWU1NTNjZi03YWNiLTRjNjMtODBlMi0zMDU0Njk0MmM4NjQiLCJpYXQiOjE3NzQ3ODEzMDQsImlzcyI6InN3aXRjaGJvdCJ9.w2Wa17Vf3slGBFlG3IrzQk1_DIqM3vb4R5O4-JyXobtnw6n-K5OolyYGKYCw02Ml7ZQfKEjuO68UIpzXJYbUEQ,
1775791050505,,其他类型,"PartitionManager-->partitionChild=[EndPointRespChild(name=WonderLabsAPI, host=https://l9ren7efdj.execute-api.us-east-1.amazonaws.com, hostWithStage=https://l9ren7efdj.execute-api.us-east-1.amazonaws.com/developStage), EndPointRespChild(name=appMarket, host=https://8hepwbwsoj.execute-api.us-east-1.amazonaws.com, hostWithStage=https://8hepwbwsoj.execute-api.us-east-1.amazonaws.com/developStage), EndPointRespChild(name=limitUserOperation, host=https://9cali86zne.execute-api.us-east-1.amazonaws.com, hostWithStage=https://9cali86zne.execute-api.us-east-1.amazonaws.com/developStage), EndPointRespChild(name=openApiV1, host=https://vxhewp40e8.execute-api.us-east-1.amazonaws.com, hostWithStage=https://vxhewp40e8.execute-api.us-east-1.amazonaws.com/beta), EndPointRespChild(name=publish, host=https://publish.api.switchbot.net, hostWithStage=https://publish.api.switchbot.net/prod), EndPointRespChild(name=account, host=https://account.api.switchbot.net, hostWithStage=https://bana6ys6sk.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=mqttBroker, host=mqtts://a2alhn2dfztqv9-ats.iot.us-east-1.amazonaws.com:8883, hostWithStage=), EndPointRespChild(name=userCore, host=https://fejlvu0ghd.execute-api.us-east-1.amazonaws.com, hostWithStage=https://fejlvu0ghd.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=scene, host=https://4k0nk4gb8b.execute-api.us-east-1.amazonaws.com, hostWithStage=https://4k0nk4gb8b.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=tuyaSignaling, host=https://avkxa6hntj.execute-api.us-east-1.amazonaws.com, hostWithStage=https://avkxa6hntj.execute-api.us-east-1.amazonaws.com/develop), EndPointRespChild(name=command, host=https://6oi8p0504l.execute-api.us-east-1.amazonaws.com, hostWithStage=https://6oi8p0504l.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=userGroup, host=https://rh3axc6yo6.execute-api.us-east-1.amazonaws.com, hostWithStage=https://rh3axc6yo6.execute-api.us-east-1.amazonaws.com/prod",
1775791050505,,其他类型,"), EndPointRespChild(name=camKvsApi, host=https://igkqjo8693.execute-api.us-east-1.amazonaws.com, hostWithStage=https://igkqjo8693.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=sweeperOriginApi, host=https://lonvwnxxn7.execute-api.us-east-1.amazonaws.com, hostWithStage=https://lonvwnxxn7.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=deviceApi, host=https://6oi8p0504l.execute-api.us-east-1.amazonaws.com, hostWithStage=https://6oi8p0504l.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=deviceApiBeta, host=https://6oi8p0504l.execute-api.us-east-1.amazonaws.com, hostWithStage=https://6oi8p0504l.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=msgCenter, host=https://vfe17awnia.execute-api.us-east-1.amazonaws.com/prod, hostWithStage=https://vfe17awnia.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=wonderlabs, host=https://wonderlabs.us.api.switchbot.net, hostWithStage=), EndPointRespChild(name=wonderlabsV2, host=https://wonder.us.api.switchbot.net, hostWithStage=), EndPointRespChild(name=pay, host=https://pay.api.switchbot.net, hostWithStage=), EndPointRespChild(name=MQTTSelfSigned, host=mqtts://core.broker.iot.us.switchbot.net:8883, hostWithStage=)]",
1775791050506,,其他类型,"onCapabilitiesChanged networkCapabilities=[ Transports: WIFI Capabilities: NOT_METERED&INTERNET&NOT_RESTRICTED&TRUSTED&NOT_VPN&VALIDATED&NOT_ROAMING&FOREGROUND&NOT_CONGESTED&NOT_SUSPENDED&NOT_VCN_MANAGED&NOT_BANDWIDTH_CONSTRAINED LinkUpBandwidth>=2449Kbps LinkDnBandwidth>=36252Kbps TransportInfo: <SSID: <unknown ssid>, BSSID: 02:00:00:00:00:00, MAC: 02:00:00:00:00:00, IP: /10.8.68.198, Security type: 2, Supplicant state: COMPLETED, Wi-Fi standard: 11ax, RSSI: -39, Link speed: 286Mbps, Tx Link speed: 286Mbps, Max Supported Tx Link speed: 286Mbps, Rx Link speed: 286Mbps, Max Supported Rx Link speed: 286Mbps, Frequency: 5200MHz, Net ID: -1, Metered hint: false, score: 60, isUsable: true, CarrierMerged: false, SubscriptionId: -1, IsPrimary: -1, Trusted: true, Restricted: false, Ephemeral: false, OEM paid: false, OEM private: false, OSU AP: false, FQDN: <none>, Provider friendly name: <none>, Requesting package name: <none><none>MLO Information: , Is TID-To-Link negotiation supported by the AP: false, AP MLD Address: <none>, AP MLO Link Id: <none>, AP MLO Affiliated links: <none>, Vendor Data: <none>> SignalStrength: -39 UnderlyingNetworks: Null]",NetworkStatusCallback
1775791050506,,其他类型,当前网络状态--networkType--WiFi,NetworkStatusCallback
1775791050506,,其他类型,onCapabilitiesChanged networkCapabilities=[ Transports: CELLULAR Capabilities: SUPL&INTERNET&NOT_RESTRICTED&TRUSTED&NOT_VPN&VALIDATED&NOT_ROAMING&FOREGROUND&NOT_CONGESTED&NOT_SUSPENDED&NOT_VCN_MANAGED&NOT_BANDWIDTH_CONSTRAINED LinkUpBandwidth>=18838Kbps LinkDnBandwidth>=18838Kbps Specifier: <TelephonyNetworkSpecifier [mSubId = 3]> SubscriptionIds: {3} UnderlyingNetworks: Null],NetworkStatusCallback
1775791050506,,其他类型,当前网络状态--networkType--4G,NetworkStatusCallback
1775791050508,,其他类型,needRunMigrate:false,
1775791050512,,其他类型,调用扫地机初始化： DeviceApp,
1775791050512,,其他类型,Google Play内购初始化： DeviceApp,
1775791050514,,其他类型,扫地机sdk当前所在大区：HK,
1775791050519,,其他类型,Initialized with 1172 commands.,BleCmdMatchHelper
1775791050528,,其他类型,getInnerPackageList,com.theswitchbot.device.hotupdate.HotUpdateManager
1775791050536,,其他类型,"firstVersion=1.0.9.0,twoVersion = 1.0.9.0",HotUpdateManager
1775791050540,,其他类型,HotUpdateManager，initJsVersion extVersion=,
1775791050540,,其他类型,HotUpdateManager，initJsVersion assetVersion=1.0.0.2,
1775791050541,,其他类型,"Zendesk, getLoginToken:{""name"":""jk363776610@163.com"",""email"":""jk363776610@163.com"",""token"":""eyJhbGciOiJFUzI1NiIsImlzcyI6InN3aXRjaGJvdC5zMy5hbWF6b25hd3MuY29tIiwia2lkIjoiNGQ3ZmI1OGIzMmFlZTdlNjJmMmE3Mjk4ZTRiYWIyMmIiLCJrdHkiOiJFQyIsInR5cCI6IkpXVCIsInYiOjF9.eyJjaGFubmVsIjoic2VsZiIsInBsYXRmb3JtIjoiQW5kcm9pZCIsImRldmljZUlEIjoiNDFkZS04Yjc3LTVhY2YtNDdlZiIsImNsaWVudF9pZCI6IjVubndtaG1zYTl4eHNrbTE0aGQ4NWxtOWJtIiwidXNlcklEIjoiOTc3MzgyOGMtOTBiYi00NzI1LWEwNGMtMzM5ZTBlZWMzMDBlIiwic3ViIjoiOTc3MzgyOGMtOTBiYi00NzI1LWEwNGMtMzM5ZTBlZWMzMDBlIiwidXNlcm5hbWUiOiI5NzczODI4Yy05MGJiLTQ3MjUtYTA0Yy0zMzllMGVlYzMwMGUiLCJzY29wZSI6InN3aXRjaGJvdCBhY2NvdW50IiwiZXhwIjoxNzc0Nzg4NTA0LCJqdGkiOiIzMWU1NTNjZi03YWNiLTRjNjMtODBlMi0zMDU0Njk0MmM4NjQiLCJpYXQiOjE3NzQ3ODEzMDQsImlzcyI6InN3aXRjaGJvdCJ9.w2Wa17Vf3slGBFlG3IrzQk1_DIqM3vb4R5O4-JyXobtnw6n-K5OolyYGKYCw02Ml7ZQfKEjuO68UIpzXJYbUEQ""}",
1775791050621,,其他类型,WidgetWorker startWork,MeterWidgetService
1775791050627,,其他类型,涂鸦登录账号,TuYaInitializer
1775791050627,,其他类型,"Zendesk, getLoginToken:{""name"":""jk363776610@163.com"",""email"":""jk363776610@163.com"",""token"":""eyJhbGciOiJFUzI1NiIsImlzcyI6InN3aXRjaGJvdC5zMy5hbWF6b25hd3MuY29tIiwia2lkIjoiNGQ3ZmI1OGIzMmFlZTdlNjJmMmE3Mjk4ZTRiYWIyMmIiLCJrdHkiOiJFQyIsInR5cCI6IkpXVCIsInYiOjF9.eyJjaGFubmVsIjoic2VsZiIsInBsYXRmb3JtIjoiQW5kcm9pZCIsImRldmljZUlEIjoiNDFkZS04Yjc3LTVhY2YtNDdlZiIsImNsaWVudF9pZCI6IjVubndtaG1zYTl4eHNrbTE0aGQ4NWxtOWJtIiwidXNlcklEIjoiOTc3MzgyOGMtOTBiYi00NzI1LWEwNGMtMzM5ZTBlZWMzMDBlIiwic3ViIjoiOTc3MzgyOGMtOTBiYi00NzI1LWEwNGMtMzM5ZTBlZWMzMDBlIiwidXNlcm5hbWUiOiI5NzczODI4Yy05MGJiLTQ3MjUtYTA0Yy0zMzllMGVlYzMwMGUiLCJzY29wZSI6InN3aXRjaGJvdCBhY2NvdW50IiwiZXhwIjoxNzc0Nzg4NTA0LCJqdGkiOiIzMWU1NTNjZi03YWNiLTRjNjMtODBlMi0zMDU0Njk0MmM4NjQiLCJpYXQiOjE3NzQ3ODEzMDQsImlzcyI6InN3aXRjaGJvdCJ9.w2Wa17Vf3slGBFlG3IrzQk1_DIqM3vb4R5O4-JyXobtnw6n-K5OolyYGKYCw02Ml7ZQfKEjuO68UIpzXJYbUEQ""}",
1775791050632,,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/wonder/zendesk/getDeleteTickets,wonderUrl替换
1775791050633,,网络请求,"--> POST https://wonder.us.api.switchbot.net/wonder/zendesk/getDeleteTickets
Content-Type: application/json; charset=UTF-8
Content-Length: 31
{""email"":""jk363776610@163.com""}
--> END POST (31-byte body)",
1775791050635,,其他类型,M2: 41de8b775acf47ef,
1775791050774,,其他类型,360 扫地机sdk已初始化,
1775791050782,,网络请求,"--> GET https://wonderlabs.us.api.switchbot.net/wonder/sweeper360/v1/user/getRegion
Content-Type: application/json
--> END GET",
1775791050787,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,初始化：进入启动页,
1775791050801,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,setAppLanguage，configuration暗黑模式:false   屏幕宽:400  屏幕高:890  密度:480  字体缩放:1.0,LocaleUtil
1775791050817,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,从后台到前台,
1775791050820,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,setAppLanguage，configuration暗黑模式:false   屏幕宽:400  屏幕高:890  密度:480  字体缩放:1.0,LocaleUtil
1775791050830,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,"获取Endpoint: curEndPointTime=1774781302303, currentTime=1775791050829, timeGap=1009748526",
1775791050836,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,时间：206,创建引擎
1775791050839,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,lastUserId: curUserId:9773828c-90bb-4725-a04c-339e0eec300e,
1775791050841,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,loadPropertyCfg json:AiHub_Propertys.json,PropertyCfgManager
1775791050841,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,loadPropertyCfg json:AiPet_Propertys.json,PropertyCfgManager
1775791050841,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,loadPropertyCfg json:ArtFrame_Propertys.json,PropertyCfgManager
1775791050842,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,loadPropertyCfg json:FanLight_Propertys.json,PropertyCfgManager
1775791050842,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,loadPropertyCfg json:OscKvs_Propertys.json,PropertyCfgManager
1775791050842,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,loadPropertyCfg json:Propertys.json,PropertyCfgManager
1775791050846,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,loadPropertyCfg json:RelaySwitch_Propertys.json,PropertyCfgManager
1775791050846,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,loadPropertyCfg json:Sweeper_Propertys.json,PropertyCfgManager
1775791050848,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,loadPropertyCfg json:TRV_Propertys.json,PropertyCfgManager
1775791050848,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,loadPropertyCfg json:USVisionDeadbolt_Propertys.json,PropertyCfgManager
1775791050848,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,"Property with type propertyId=4212 deviceTypes=[W1141000, W1141001]",PropertyCfgManager
1775791050848,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,loadPropertyCfg json:WeatherStation_Propertys.json,PropertyCfgManager
1775791050848,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,loadPropertyCfg json:digitalHome_Propertys.json,PropertyCfgManager
1775791050849,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,"Property with type propertyId=835 deviceTypes=[WoFan, WoFan2, WoPlugUS, WoPlugJP, WoPlug, WoBulb, WoStrip, WoFloorLamp, WoStrip3, WoCeiling, WoCeilingPro, W1102003, W1102004, W1102005]",PropertyCfgManager
1775791050849,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,"propertyWithType =[835WoFan2, 835WoFloorLamp, 835WoPlugUS, 835WoStrip, 4212W1141001, 835WoStrip3, 835WoBulb, 835WoFan, 4212W1141000, 835W1102003, 835W1102004, 835WoCeiling, 835W1102005, 835WoCeilingPro, 835WoPlug, 835WoPlugJP]",PropertyCfgManager
1775791050883,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,"PartitionManager-->regionBean=MqttRegionBean(host=core.broker.iot.us.switchbot.net, openPort=8883)",
1775791050884,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,涂鸦不需要登录,TuYaInitializer
1775791050890,com.theswitchbot.switchbot.index.ui.SplashActivity,网络请求,"--> POST https://account.api.switchbot.net/admin/admin/api/v1/botregion/endpoint
Content-Type: application/json; charset=UTF-8
Content-Length: 18
{""botRegion"":""us""}
--> END POST (18-byte body)",
1775791050902,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,MqttService onServiceConnected！,
1775791050931,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,"PartitionManager-->regionBean=MqttRegionBean(host=core.broker.iot.us.switchbot.net, openPort=8883)",
1775791050932,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,======================================,MqttService 连接MQTT
1775791050932,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,MqttService host=core.broker.iot.us.switchbot.net,
1775791050938,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,MqttService Mqtt-Iot-Connecting,
1775791050944,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,"PartitionManager-->regionBean=MqttRegionBean(host=core.broker.iot.us.switchbot.net, openPort=8883)",
1775791050944,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,MqttService MQTT正在连接:Connecting，跳过,
1775791051609,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,5秒内同个地址请求过期次数=====================>0,OkHttp
1775791051609,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,5秒内同个地址请求过期次数=====================>1,OkHttp
1775791051609,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,token过期--->开始,OkHttp
1775791051619,com.theswitchbot.switchbot.index.ui.SplashActivity,网络请求,"--> POST https://account.api.switchbot.net/account/api/v1/user/token/refresh
Content-Type: application/json; charset=UTF-8
Content-Length: 234
switchBotTK: none
{""clientId"":""5nnwmhmsa9xxskm14hd85lm9bm"",""clientSecret"":""vzxjw7rvmduka4rlysdcv0bfke70icql33ol1pvr"",""deviceId"":""41de-8b77-5acf-47ef"",""refreshToken"":""a009169b-7c40-4977-9536-aec91593603e"",""userId"":""9773828c-90bb-4725-a04c-339e0eec300e""}
--> END POST (234-byte body)",
1775791051622,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,360 扫地机sdk已初始化完成: false,
1775791051735,com.theswitchbot.switchbot.index.ui.SplashActivity,网络返回,"
<-- 200 https://account.api.switchbot.net/admin/admin/api/v1/botregion/endpoint (844ms)
content-type: application/json
content-length: 3095
date: Fri, 10 Apr 2026 03:17:32 GMT
x-amzn-remapped-date: Fri, 10 Apr 2026 03:17:32 GMT
x-amzn-requestid: fc3e6ec4-599d-4355-a44b-3d35eac983c3
access-control-allow-origin: *
x-amzn-remapped-content-length: 3095
x-amzn-remapped-connection: keep-alive
x-amz-apigw-id: blXIBGjGIAMEiQA=
switchbot-request-id: e0740e47-c6d2-4d01-a87c-c3ee6a71b97a
x-cache: Miss from cloudfront
via: 1.1 7af4698bea7e964f89ad8d7ae22213a2.cloudfront.net (CloudFront)
x-amz-cf-pop: SFO53-P5
x-amz-cf-id: fm40lvTumq8kLWm1prNJy0MDsrHGjoNuSX6NfK7sZrvjZXQ9VH4KQg==
{""resultCode"":100,""data"":[{""name"":""WonderLabsAPI"",""host"":""https://l9ren7efdj.execute-api.us-east-1.amazonaws.com"",""hostWithStage"":""https://l9ren7efdj.execute-api.us-east-1.amazonaws.com/developStage""},{""name"":""appMarket"",""host"":""https://8hepwbwsoj.execute-api.us-east-1.amazonaws.com"",""hostWithStage"":""https://8hepwbwsoj.execute-api.us-east-1.amazonaws.com/developStage""},{""name"":""limitUserOperation"",""host"":""https://9cali86zne.execute-api.us-east-1.amazonaws.com"",""hostWithStage"":""https://9cali86zne.execute-api.us-east-1.amazonaws.com/developStage""},{""name"":""openApiV1"",""host"":""https://vxhewp40e8.execute-api.us-east-1.amazonaws.com"",""hostWithStage"":""https://vxhewp40e8.execute-api.us-east-1.amazonaws.com/beta""},{""name"":""publish"",""host"":""https://publish.api.switchbot.net"",""hostWithStage"":""https://publish.api.switchbot.net/prod""},{""name"":""account"",""host"":""https://account.api.switchbot.net"",""hostWithStage"":""https://bana6ys6sk.execute-api.us-east-1.amazonaws.com/prod""},{""name"":""mqttBroker"",""host"":""mqtts://a2alhn2dfztqv9-ats.iot.us-east-1.amazonaws.com:8883"",""hostWithStage"":""""},{""name"":""userCore"",""host"":""https://fejlvu0ghd.execute-api.us-east-1.amazonaws.com"",""hostWithStage"":""https://fejlvu0ghd.execute-api.us-east-1.amazonaws.com/prod""},{""name"":""scene"",""host"":""https://4k0nk4gb8b.execute-api.us-east-1.amazonaws.",
1775791051735,com.theswitchbot.switchbot.index.ui.SplashActivity,网络返回,"com"",""hostWithStage"":""https://4k0nk4gb8b.execute-api.us-east-1.amazonaws.com/prod""},{""name"":""tuyaSignaling"",""host"":""https://avkxa6hntj.execute-api.us-east-1.amazonaws.com"",""hostWithStage"":""https://avkxa6hntj.execute-api.us-east-1.amazonaws.com/develop""},{""name"":""command"",""host"":""https://6oi8p0504l.execute-api.us-east-1.amazonaws.com"",""hostWithStage"":""https://6oi8p0504l.execute-api.us-east-1.amazonaws.com/prod""},{""name"":""userGroup"",""host"":""https://rh3axc6yo6.execute-api.us-east-1.amazonaws.com"",""hostWithStage"":""https://rh3axc6yo6.execute-api.us-east-1.amazonaws.com/prod""},{""name"":""camKvsApi"",""host"":""https://igkqjo8693.execute-api.us-east-1.amazonaws.com"",""hostWithStage"":""https://igkqjo8693.execute-api.us-east-1.amazonaws.com/prod""},{""name"":""sweeperOriginApi"",""host"":""https://lonvwnxxn7.execute-api.us-east-1.amazonaws.com"",""hostWithStage"":""https://lonvwnxxn7.execute-api.us-east-1.amazonaws.com/prod""},{""name"":""deviceApi"",""host"":""https://6oi8p0504l.execute-api.us-east-1.amazonaws.com"",""hostWithStage"":""https://6oi8p0504l.execute-api.us-east-1.amazonaws.com/prod""},{""name"":""deviceApiBeta"",""host"":""https://6oi8p0504l.execute-api.us-east-1.amazonaws.com"",""hostWithStage"":""https://6oi8p0504l.execute-api.us-east-1.amazonaws.com/prod""},{""name"":""msgCenter"",""host"":""https://vfe17awnia.execute-api.us-east-1.amazonaws.com/prod"",""hostWithStage"":""https://vfe17awnia.execute-api.us-east-1.amazonaws.com/prod""},{""name"":""wonderlabs"",""host"":""https://wonderlabs.us.api.switchbot.net"",""hostWithStage"":""""},{""name"":""wonderlabsV2"",""host"":""https://wonder.us.api.switchbot.net"",""hostWithStage"":""""},{""name"":""pay"",""host"":""https://pay.api.switchbot.net"",""hostWithStage"":""""},{""name"":""MQTTSelfSigned"",""host"":""mqtts://core.broker.iot.us.switchbot.net:8883"",""hostWithStage"":""""}],""message"":""""}
<-- END HTTP (3095-byte body)",
1775791051736,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,"PartitionManager-->partitionChild=[EndPointRespChild(name=WonderLabsAPI, host=https://l9ren7efdj.execute-api.us-east-1.amazonaws.com, hostWithStage=https://l9ren7efdj.execute-api.us-east-1.amazonaws.com/developStage), EndPointRespChild(name=appMarket, host=https://8hepwbwsoj.execute-api.us-east-1.amazonaws.com, hostWithStage=https://8hepwbwsoj.execute-api.us-east-1.amazonaws.com/developStage), EndPointRespChild(name=limitUserOperation, host=https://9cali86zne.execute-api.us-east-1.amazonaws.com, hostWithStage=https://9cali86zne.execute-api.us-east-1.amazonaws.com/developStage), EndPointRespChild(name=openApiV1, host=https://vxhewp40e8.execute-api.us-east-1.amazonaws.com, hostWithStage=https://vxhewp40e8.execute-api.us-east-1.amazonaws.com/beta), EndPointRespChild(name=publish, host=https://publish.api.switchbot.net, hostWithStage=https://publish.api.switchbot.net/prod), EndPointRespChild(name=account, host=https://account.api.switchbot.net, hostWithStage=https://bana6ys6sk.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=mqttBroker, host=mqtts://a2alhn2dfztqv9-ats.iot.us-east-1.amazonaws.com:8883, hostWithStage=), EndPointRespChild(name=userCore, host=https://fejlvu0ghd.execute-api.us-east-1.amazonaws.com, hostWithStage=https://fejlvu0ghd.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=scene, host=https://4k0nk4gb8b.execute-api.us-east-1.amazonaws.com, hostWithStage=https://4k0nk4gb8b.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=tuyaSignaling, host=https://avkxa6hntj.execute-api.us-east-1.amazonaws.com, hostWithStage=https://avkxa6hntj.execute-api.us-east-1.amazonaws.com/develop), EndPointRespChild(name=command, host=https://6oi8p0504l.execute-api.us-east-1.amazonaws.com, hostWithStage=https://6oi8p0504l.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=userGroup, host=https://rh3axc6yo6.execute-api.us-east-1.amazonaws.com, hostWithStage=https://rh3axc6yo6.execute-api.us-east-1.amazonaws.com/prod",
1775791051736,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,"), EndPointRespChild(name=camKvsApi, host=https://igkqjo8693.execute-api.us-east-1.amazonaws.com, hostWithStage=https://igkqjo8693.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=sweeperOriginApi, host=https://lonvwnxxn7.execute-api.us-east-1.amazonaws.com, hostWithStage=https://lonvwnxxn7.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=deviceApi, host=https://6oi8p0504l.execute-api.us-east-1.amazonaws.com, hostWithStage=https://6oi8p0504l.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=deviceApiBeta, host=https://6oi8p0504l.execute-api.us-east-1.amazonaws.com, hostWithStage=https://6oi8p0504l.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=msgCenter, host=https://vfe17awnia.execute-api.us-east-1.amazonaws.com/prod, hostWithStage=https://vfe17awnia.execute-api.us-east-1.amazonaws.com/prod), EndPointRespChild(name=wonderlabs, host=https://wonderlabs.us.api.switchbot.net, hostWithStage=), EndPointRespChild(name=wonderlabsV2, host=https://wonder.us.api.switchbot.net, hostWithStage=), EndPointRespChild(name=pay, host=https://pay.api.switchbot.net, hostWithStage=), EndPointRespChild(name=MQTTSelfSigned, host=mqtts://core.broker.iot.us.switchbot.net:8883, hostWithStage=)]",
1775791051745,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,"保存Endpoint: userId=9773828c-90bb-4725-a04c-339e0eec300e, currentTime=1775791051745",
1775791051854,com.theswitchbot.switchbot.index.ui.SplashActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/wonder/zendesk/getDeleteTickets (1220ms)
content-type: text/plain; charset=utf-8
content-length: 59
date: Fri, 10 Apr 2026 03:17:32 GMT
switchbot-request-id: 5c1d256e-d96f-43a3-91ad-f1e76bf63b8a
{""statusCode"":100,""body"":{""deleteTickets"":[]},""message"":""""}
<-- END HTTP (59-byte body)",
1775791051856,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/wonder/zendesk/getTicketState,wonderUrl替换
1775791051856,com.theswitchbot.switchbot.index.ui.SplashActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/wonder/zendesk/getTicketState
Content-Type: application/json; charset=UTF-8
Content-Length: 31
{""email"":""jk363776610@163.com""}
--> END POST (31-byte body)",
1775791051896,com.theswitchbot.switchbot.index.ui.SplashActivity,网络返回,"
<-- 200 https://account.api.switchbot.net/account/api/v1/user/token/refresh (275ms)
content-type: application/json
content-length: 861
date: Fri, 10 Apr 2026 03:17:32 GMT
x-amzn-remapped-date: Fri, 10 Apr 2026 03:17:32 GMT
x-amzn-requestid: 41be6448-d1d7-4ab8-b991-e301010c3a43
x-amzn-remapped-content-length: 861
x-amzn-remapped-connection: keep-alive
x-amz-apigw-id: blXIDGVwIAMEfDg=
switchbot-request-id: 2d2f8c8d-3b2d-4d53-a277-501fee362ad7
x-cache: Miss from cloudfront
via: 1.1 7af4698bea7e964f89ad8d7ae22213a2.cloudfront.net (CloudFront)
x-amz-cf-pop: SFO53-P5
x-amz-cf-id: 3D2ZZ8KKBk1QthuFSsfzHctLy8m2d7rOQT2rq3EsefRIbBPvBNKIYA==
{""statusCode"":100,""body"":{""access_token"":""eyJhbGciOiJFUzI1NiIsImlzcyI6InN3aXRjaGJvdC5zMy5hbWF6b25hd3MuY29tIiwia2lkIjoiNGQ3ZmI1OGIzMmFlZTdlNjJmMmE3Mjk4ZTRiYWIyMmIiLCJrdHkiOiJFQyIsInR5cCI6IkpXVCIsInYiOjF9.eyJjaGFubmVsIjoic2VsZiIsInBsYXRmb3JtIjoiQW5kcm9pZCIsImRldmljZUlEIjoiNDFkZS04Yjc3LTVhY2YtNDdlZiIsImNsaWVudF9pZCI6IjVubndtaG1zYTl4eHNrbTE0aGQ4NWxtOWJtIiwidXNlcklEIjoiOTc3MzgyOGMtOTBiYi00NzI1LWEwNGMtMzM5ZTBlZWMzMDBlIiwic3ViIjoiOTc3MzgyOGMtOTBiYi00NzI1LWEwNGMtMzM5ZTBlZWMzMDBlIiwidXNlcm5hbWUiOiI5NzczODI4Yy05MGJiLTQ3MjUtYTA0Yy0zMzllMGVlYzMwMGUiLCJzY29wZSI6InN3aXRjaGJvdCBhY2NvdW50IiwiZXhwIjoxNzc1Nzk4MjUyLCJqdGkiOiJiZDYwYzAzOC1kM2M5LTRiZGEtYjE4Yy1iNWY1ZTY3NjIzMmMiLCJpYXQiOjE3NzU3OTEwNTIsImlzcyI6InN3aXRjaGJvdCJ9.014WqESJtd7_4WESGzim8rin8apXYFzapOX3v7DzdeY-7-onQ71UDQ8WGtXYyszPka1KSn6dDscBBJG88n2B2A"",""expires_in"":7200,""token_type"":""Bearer""},""message"":""success""}
<-- END HTTP (861-byte body)",
1775791051900,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,token过期--->刷新token成功,OkHttp
1775791051901,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,token刷新--->更新本地token信息,OkHttp
1775791051907,com.theswitchbot.switchbot.index.ui.SplashActivity,其他类型,token过期--->完成,OkHttp
1775791052059,,其他类型,setAppLanguage，configuration暗黑模式:false   屏幕宽:400  屏幕高:845  密度:480  字体缩放:1.0,LocaleUtil
1775791052059,,其他类型,setAppLanguage，newConfig暗黑模式:false   屏幕宽:400  屏幕高:845  密度:480  字体缩放:1.0,LocaleUtil
1775791052071,,其他类型,createConfigurationContext，configuration暗黑模式:false   屏幕宽:400  屏幕高:845  密度:480  字体缩放:1.0,LocaleUtil
1775791052074,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,setAppLanguage，configuration暗黑模式:false   屏幕宽:400  屏幕高:845  密度:480  字体缩放:1.0,LocaleUtil
1775791052075,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"<=====    CURRENT PAGE, ONCREATE: MainActivity =====>",
1775791052097,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,checkPermission isFirstOpenApp=false,NfcBaseActivity
1775791052114,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,开始扫描蓝牙设备,DeviceScanner
1775791052114,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,获取扫描器结果 field=android.bluetooth.le.BluetoothLeScanner@d1a3883,BleManager
1775791052115,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,蓝牙快速扫描...,SBBleScanner
1775791052135,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,NetUtils网络列表--名称=MOBILE状态=false,NetUtils
1775791052135,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,NetUtils网络列表--名称=WIFI状态=true,NetUtils
1775791052139,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> GET https://www.wohand.com/version/wocaotech/app/APPUpgradeTipsConfig.json
Domain-Name: staticFileServer
switchBotTK: none
--> END GET",
1775791052142,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> GET https://www.wohand.com/version/wocaotech/release.json
Domain-Name: staticFileServer
switchBotTK: none
--> END GET",
1775791052143,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,DeviceUpgradeManager: versionToNum: 9.23 -> 9023000,
1775791052146,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,DeviceUpgradeManager: 当前版本=9023000 {},
1775791052151,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> GET https://www.wohand.com/version/wocaotech/app/ForceUpgradeVersionConfig.json
Domain-Name: staticFileServer
switchBotTK: none
--> END GET",
1775791052151,com.theswitchbot.switchbot.index.ui.MainActivity,APP启动,TimeZoneId = Asia/Shanghai;系统时区=8;APP版本:9.23;当前账号jk363776610@163.com,
1775791052151,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,lang:cn,appLanguage
1775791052158,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/homepage/v1/system/config/effectiveBatch,wonderUrl替换
1775791052160,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/homepage/v1/system/config/effectiveBatch
Content-Type: application/json; charset=UTF-8
Content-Length: 112
{""serverTypes"":[""MQTTSelfSigned"",""MqttSelfSigned_AppDevice_effective"",""homeDigitalTwin"",""WoCeilingPartsNotify""]}
--> END POST (112-byte body)",
1775791052166,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/groupshare/api/v2/invite/memberQuery,wonderUrl替换
1775791052168,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> GET https://prod-switchbot-icons.s3.amazonaws.com/wo_device_icon.json
Domain-Name: staticFileServer
switchBotTK: none
--> END GET",
1775791052169,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,temp Unit:-1,updateUserInfo
1775791052169,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/homepage/v1/system/config/effective,wonderUrl替换
1775791052169,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/homepage/v1/system/config/effective
Content-Type: application/json; charset=UTF-8
Content-Length: 39
{""serverType"":""recommendsCloudStorage""}
--> END POST (39-byte body)",
1775791052170,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/wonder/user/v1,wonderUrl替换
1775791052170,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/wonder/user/v1
Content-Type: application/json; charset=UTF-8
Content-Length: 369
{""appLanguage"":""cn"",""appName"":""9.23"",""isDebug"":true,""location"":""default"",""osVersion"":""36"",""phoneBranch"":""Xiaomi"",""phoneLanguage"":""zh"",""phoneMode"":""23127PN0CC"",""platform"":""android"",""snsEnv"":"""",""snsToken"":""fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aXdM00tyw"",""versionFlag"":""9.23""}
--> END POST (369-byte body)",
1775791052170,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonderlabs.us.api.switchbot.net/wonder/sweeper360/v1/user/getRegion (1385ms)
content-type: application/json; charset=utf-8
content-length: 150
date: Fri, 10 Apr 2026 03:17:33 GMT
x-amzn-remapped-date: Fri, 10 Apr 2026 03:17:33 GMT
x-amzn-requestid: 014c3bf9-9f22-4735-be9d-e3859e26b322
x-amzn-remapped-content-length: 150
x-amzn-remapped-connection: keep-alive
x-amz-apigw-id: blXIGFwJoAMEiPg=
switchbot-request-id: 200557da-76e1-440b-9f34-46468f753ed4
x-cache: Miss from cloudfront
via: 1.1 af63429cca0caf23ac2ab7e13afc8ebc.cloudfront.net (CloudFront)
x-amz-cf-pop: SFO53-P10
x-amz-cf-id: gLy7XVYSTWReHJXy9uGxYfMm1saxhER7nFzB5nkdZIPSoNq3LTFt-w==
{""statusCode"":100,""body"":{""code"":""HK"",""hosts"":[""ap1-sapp-api.botslab.com""],""name"":""Hong Kong"",""phone_area_code"":""+852"",""region"":""ap1""},""message"":""OK""}
<-- END HTTP (150-byte body)",
1775791052171,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,setAppLanguage，configuration暗黑模式:false   屏幕宽:400  屏幕高:845  密度:480  字体缩放:1.0,LocaleUtil
1775791052172,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"<=====    CURRENT PAGE, ONRESUME: MainActivity =====>",
1775791052172,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,checkPermission isFirstOpenApp isBleEnable=false,NfcBaseActivity
1775791052188,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/groupshare/api/v2/invite/memberQuery
Content-Type: application/json; charset=UTF-8
Content-Length: 2
{}
--> END POST (2-byte body)",
1775791052189,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/homepage/v1/system/config/effective,wonderUrl替换
1775791052189,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/homepage/v1/system/config/effective
Content-Type: application/json; charset=UTF-8
Content-Length: 43
{""serverType"":""recommendsTuyaCloudStorage""}
--> END POST (43-byte body)",
1775791052191,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> GET https://account.api.switchbot.net/account/api/v1/country/codes?clientId=5nnwmhmsa9xxskm14hd85lm9bm&lang=cn
--> END GET",
1775791052192,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://account.api.switchbot.net/account/api/v1/user/userinfo
Content-Type: application/json
Content-Length: 0

--> END POST (0-byte body)",
1775791052192,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/homepage/v1/system/config/effective,wonderUrl替换
1775791052193,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/homepage/v1/system/config/effective
Content-Type: application/json; charset=UTF-8
Content-Length: 30
{""serverType"":""smartSchedule""}
--> END POST (30-byte body)",
1775791052194,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/homepage/v1/gray/status,wonderUrl替换
1775791052197,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> GET https://wonder.us.api.switchbot.net/homepage/v1/gray/status
Content-Type: application/json
--> END GET",
1775791052213,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService Mqtt-Iot-Connected,
1775791052214,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/homepage/v1/userSettings/get,wonderUrl替换
1775791052214,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/homepage/v1/userSettings/get
Content-Type: application/json
Content-Length: 0

--> END POST (0-byte body)",
1775791052253,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型, FamilyManager.getCurFamilyId() = G01-1756371013431-28ad,HomeProFragment
1775791052254,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService 订阅subTopic----------->switchlink/9773828c-90bb-4725-a04c-339e0eec300e/notify_dev_iraction,
1775791052258,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,HomeProFragment,SBCreateFragment
1775791052337,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/wonder/zendesk/getTicketState (479ms)
content-type: text/plain; charset=utf-8
content-length: 69
date: Fri, 10 Apr 2026 03:17:33 GMT
switchbot-request-id: 5948a03c-0eb4-4762-89f7-7878126a6110
{""statusCode"":100,""body"":{""ticketList"":[],""busy"":false},""message"":""""}
<-- END HTTP (69-byte body)",
1775791052363,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"Zendesk, checkUnReadWithOutSDK: 0",
1775791052364,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,loadDBFamily,HomeProFragment
1775791052385,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,reSortProfileRoomSort,
1775791052385,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,重新查询后赋值为:,首页设备RoomId为空
1775791052386,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,重新查询后赋值为:,首页设备RoomId为空
1775791052386,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,重新查询后赋值为:,首页设备RoomId为空
1775791052386,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"显示config=[{""data"":[],""extra"":{""dataSource"":""""},""id"":"""",""name"":"""",""type"":""Temperature"",""visible"":true},{""data"":[],""extra"":{""dataSource"":""""},""id"":"""",""name"":"""",""type"":""Purifier"",""visible"":true},{""data"":[],""extra"":{""dataSource"":""""},""id"":"""",""name"":"""",""type"":""CO2"",""visible"":true},{""data"":[],""extra"":{""dataSource"":""""},""id"":"""",""name"":"""",""type"":""Weather"",""visible"":true},{""data"":[],""extra"":{""dataSource"":""""},""id"":"""",""name"":"""",""type"":""AiHub"",""visible"":true},{""data"":[],""extra"":{""dataSource"":""""},""id"":"""",""name"":""Climate"",""type"":""Climate"",""visible"":true},{""data"":[],""extra"":{""dataSource"":""""},""id"":"""",""name"":""Lights"",""type"":""Lights"",""visible"":true},{""data"":[],""extra"":{""dataSource"":""""},""id"":"""",""name"":""Dynamics"",""type"":""Dynamics"",""visible"":true},{""data"":[""B0E9FEA3BE12""],""extra"":{""dataSource"":""""},""id"":"""",""name"":""Cameras"",""type"":""Cameras"",""visible"":true},{""data"":[],""extra"":{""dataSource"":""""},""id"":"""",""name"":""Scenes"",""type"":""Scenes"",""visible"":true},{""data"":[],""extra"":{""dataSource"":""""},""id"":"""",""name"":""Favorites"",""type"":""Favorites"",""visible"":true},{""data"":[""B0E9FE8D8933"",""B0E9FEA3BE12"",""B0E9FEA59ED0""],""extra"":{""dataSource"":""""},""id"":"""",""name"":""Not in any rooms"",""type"":""DefaultRoom"",""visible"":true},{""data"":[],""extra"":{""dataSource"":""""},""id"":"""",""name"":""NearBy Bots"",""type"":""NearByBots"",""visible"":true}] profileChanged=false",com.theswitchbot.switchbot.index.ui.homepro.utilis.HomeConfigUtils
1775791052386,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"homeAd:[], loopTime:0",
1775791052388,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,HomeViewDynamicItem init: 106422742,
1775791052399,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,SceneProFragment,SBCreateFragment
1775791052400,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,loadDBFamily,SceneProFragment
1775791052401,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/scene/v1/suggest/getList,wonderUrl替换
1775791052401,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/scene/v1/suggest/getList
Content-Type: application/json; charset=UTF-8
Content-Length: 77
{""groupID"":""G01-1756371013431-28ad"",""language"":""cn"",""sceneType"":""automation""}
--> END POST (77-byte body)",
1775791052401,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/scene/v1/geofencing/get,wonderUrl替换
1775791052401,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/scene/v1/geofencing/get
Content-Type: application/json; charset=UTF-8
Content-Length: 36
{""terminalID"":""41de-8b77-5acf-47ef""}
--> END POST (36-byte body)",
1775791052421,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/homepage/v1/system/config/effective (249ms)
content-type: application/json
content-length: 59
date: Fri, 10 Apr 2026 03:17:33 GMT
switchbot-request-id: c920382a-824c-4ef2-8940-d79a3fb8886b
{""resultCode"":100, ""message"":"""", ""data"":{""effective"":true}}
<-- END HTTP (59-byte body)",
1775791052434,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/homepage/v1/system/config/effectiveBatch (272ms)
content-type: application/json
content-length: 163
date: Fri, 10 Apr 2026 03:17:33 GMT
switchbot-request-id: 1ec6f815-3905-4ffe-881f-26caef85376b
{""resultCode"":100, ""message"":"""", ""data"":{""MQTTSelfSigned"":true, ""MqttSelfSigned_AppDevice_effective"":false, ""WoCeilingPartsNotify"":false, ""homeDigitalTwin"":false}}
<-- END HTTP (163-byte body)",
1775791052576,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/homepage/v1/gray/status (379ms)
content-type: application/json
content-length: 73
date: Fri, 10 Apr 2026 03:17:33 GMT
switchbot-request-id: 200d88b6-c9e9-4ecf-bf38-ebc8403b03e1
{""resultCode"":100, ""message"":"""", ""data"":{""appSecondLevelPageCache"":true}}
<-- END HTTP (73-byte body)",
1775791052577,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/groupshare/api/v2/invite/memberQuery (388ms)
content-type: application/json
content-length: 48
date: Fri, 10 Apr 2026 03:17:33 GMT
switchbot-request-id: 50c750e3-f957-4c77-a730-fe5ce2e0c19b
{""resultCode"":100,""message"":""success"",""data"":[]}
<-- END HTTP (48-byte body)",
1775791052577,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/homepage/v1/userSettings/get (363ms)
content-type: application/json
content-length: 221
date: Fri, 10 Apr 2026 03:17:33 GMT
switchbot-request-id: ae978575-10b0-4c2c-bd1b-161c761fedcf
{""resultCode"":100, ""message"":"""", ""data"":{""digitMapPrivatePolicy"":false, ""humidityUnitPercent"":true, ""language"":""cn"", ""recommendsCloudStorage"":false, ""temperatureUnit"":""c"", ""userID"":""9773828c-90bb-4725-a04c-339e0eec300e""}}
<-- END HTTP (221-byte body)",
1775791052580,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/homepage/v1/system/config/effective (390ms)
content-type: application/json
content-length: 59
date: Fri, 10 Apr 2026 03:17:33 GMT
switchbot-request-id: b43bbb0c-25f0-459d-909d-3744ffaf7fec
{""resultCode"":100, ""message"":"""", ""data"":{""effective"":true}}
<-- END HTTP (59-byte body)",
1775791052580,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/homepage/v1/system/config/effective (387ms)
content-type: application/json
content-length: 59
date: Fri, 10 Apr 2026 03:17:33 GMT
switchbot-request-id: 20a3fd58-bed5-4eac-b232-e28d3cda387a
{""resultCode"":100, ""message"":"""", ""data"":{""effective"":true}}
<-- END HTTP (59-byte body)",
1775791052599,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://account.api.switchbot.net/account/api/v1/country/codes?clientId=5nnwmhmsa9xxskm14hd85lm9bm&lang=cn (405ms)
content-type: application/json
content-length: 245
date: Fri, 10 Apr 2026 03:17:33 GMT
x-amzn-remapped-date: Fri, 10 Apr 2026 03:17:33 GMT
x-amzn-requestid: b278aff9-cbbf-423f-8e64-57e113eaaa5f
access-control-allow-origin: *
access-control-allow-headers: Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent
x-amzn-remapped-content-length: 245
x-amzn-remapped-connection: keep-alive
x-amz-apigw-id: blXIKHlKoAMEgGA=
switchbot-request-id: 59045c97-0d80-495c-8f22-74c5fc798f0d
access-control-allow-methods: GET,POST,OPTIONS
x-cache: Miss from cloudfront
via: 1.1 7af4698bea7e964f89ad8d7ae22213a2.cloudfront.net (CloudFront)
x-amz-cf-pop: SFO53-P5
x-amz-cf-id: 9qtvgu48K2ugoeFgGqz2IriohL_rLhxei0b7U9Y917kKdcDydJqjxQ==
{""statusCode"":100,""body"":{""aliCaptcha"":false,""codes"":[{""code"":""CA"",""country"":""加拿大"",""dialCode"":""1"",""maxLen"":10,""minLen"":10,""status"":1},{""code"":""US"",""country"":""美国"",""dialCode"":""1"",""maxLen"":10,""minLen"":10,""status"":1}]},""message"":""success""}
<-- END HTTP (245-byte body)",
1775791052628,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://account.api.switchbot.net/account/api/v1/user/userinfo (435ms)
content-type: application/json
content-length: 248
date: Fri, 10 Apr 2026 03:17:33 GMT
x-amzn-remapped-date: Fri, 10 Apr 2026 03:17:33 GMT
x-amzn-requestid: 3d8091b1-910b-462d-ac32-0ff1a74fc237
access-control-allow-origin: *
access-control-allow-headers: Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent
x-amzn-remapped-content-length: 248
x-amzn-remapped-connection: keep-alive
x-amz-apigw-id: blXIKEguoAMENDA=
switchbot-request-id: a2c7966b-4b98-4a2b-ae6c-49fdf3560339
access-control-allow-methods: GET,POST,OPTIONS
x-cache: Miss from cloudfront
via: 1.1 7af4698bea7e964f89ad8d7ae22213a2.cloudfront.net (CloudFront)
x-amz-cf-pop: SFO53-P5
x-amz-cf-id: PYKPcHb5lB5nxdeFbsLsK-5_3p6hj-xV_BUIiV0r7Fr6OeraKp38mQ==
{""statusCode"":100,""body"":{""botRegion"":""us"",""email"":""jk363776610@163.com"",""isVerified"":true,""locale"":""cn"",""nickName"":"""",""source"":""Android"",""state"":1,""subscribe"":true,""userID"":""9773828c-90bb-4725-a04c-339e0eec300e"",""userName"":""""},""message"":""success""}
<-- END HTTP (248-byte body)",
1775791052809,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,UserFragment,SBCreateFragment
1775791052919,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,从前台到后台,
1775791052927,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,回到首页断开所有蓝牙连接...,BleManager
1775791052930,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://publish.api.switchbot.net/publishplatform/api/v1/rn/plugIn/downloadUrl
Content-Type: application/json; charset=UTF-8
Content-Length: 63
{""platform"":""android"",""rnPluginName"":""dm"",""rnPluginVersion"":""""}
--> END POST (63-byte body)",
1775791052932,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,onLost ,NetworkStatusCallback
1775791052932,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,当前网络状态--networkType--No network,NetworkStatusCallback
1775791052932,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/homepage/v2/mobile/management/getStatus,wonderUrl替换
1775791052932,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,根据参数不打印网络请求日志:https://wonder.us.api.switchbot.net/homepage/v2/mobile/management/getStatus,
1775791052941,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,首页网络状态：true,
1775791052954,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService 订阅subTopic----------->v1_1/9773828c-90bb-4725-a04c-339e0eec300e/#,
1775791052955,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService 订阅subTopic----------->switchlink/9773828c-90bb-4725-a04c-339e0eec300e/#,
1775791052955,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,postAllDeviceStatusMsg from onMqttStatusChanged,MqttDeviceStatusManager
1775791052957,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"MqttService 发布MQTT消息,Topic:$aws/rules/bi_app_fetch_device_status_arch2/switchlink/9773828c-90bb-4725-a04c-339e0eec300e/app_to_device_status     payload:{""appVersion"":""9.23"",""count"":1,""createTime"":0,""messages"":[{""createTime"":1775791052,""data"":{""requestID"":""85367815-b1d6-48fd-9593-dd2c97b3e470"",""createTime"":1775791052},""eventType"":""Wo.All.Status"",""id"":""f81ddc8f-ebb0-468d-82ad-a8d3b1f9891e""}],""platform"":""Android"",""protocolVersion"":2}",
1775791052965,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,吸顶灯组件提示白名单--获取=false,
1775791052965,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,数字孪生白名单--获取=false,
1775791052965,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,首页网络状态：true,
1775791052966,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,自建Broker--获取=false,
1775791052966,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,是否已登陆 true,
1775791052969,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/groupshare/api/v2/group,wonderUrl替换
1775791052970,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/groupshare/api/v2/group
Content-Type: application/json; charset=UTF-8
Content-Length: 22
{""withCountInfo"":true}
--> END POST (22-byte body)",
1775791052971,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,getCountryCode: LocaleUtil.getCountryIso(): CN,getCountryCode
1775791052971,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,获取用户信息-->userInfo--->成功,
1775791053267,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/wonder/user/v1 (407ms)
content-type: application/json; charset=utf-8
content-length: 5645
date: Fri, 10 Apr 2026 03:17:33 GMT
switchbot-request-id: 246d2785-1d71-4473-be53-9a3a6348452e
{""statusCode"":100,""body"":{""targetVersion"":{""WoLinkMiniBleVersion"":36,""hubPlusWifiVersion"":23,""WoCurtainBleVersion"":46,""WoFinderCardBleVersion"":1,""W1128000BleVersion"":1,""WoContactBleVersion"":11,""WoWaterDetectorBleVersion"":1,""hubPlusBleVersion"":24,""hubWifiVersion"":23,""WoIOSensorBleVersion"":4,""WoCamKvs5mpMcuVersion"":16777336,""WoPresenceBleVersion"":13,""WoMeterBleVersion"":27,""WoLinkMiniWifiVersion"":23,""hubBleVersion"":44,""W1079001BleVersion"":1,""WoLockBleVersion"":58,""WoCamKvs5mpCpuVersion"":16777336,""WoHandBleVersion"":64,""W1079000BleVersion"":1,""WoRWSBleVersion"":16},""userName"":""9773828c-90bb-4725-a04c-339e0eec300e"",""openApiToken"":{""exp"":2103526218565,""iat"":1787907018565,""version"":1,""token"":""w010117563710184ec7""},""userActivity"":[{""phoneLanguage"":""zh"",""snsToken"":""fq9Q20_MTfuI43jab5yOtl:APA91bFNmuXW8hZM_Tdqt5N-4lmm6NpS_k08V3FbELsd5LAtYMf3TheiycF0rhQEjFq1cFAn12KW2UTpjpni_ZeGXhxLhN_TCZVV2es7Ol4zbxePhjbXWs8"",""appName"":""10.42.0.13"",""ip"":""113.104.202.139"",""versionFlag"":""10.42.0.13"",""updateTime"":1773984639000,""phoneBranch"":""Xiaomi"",""platform"":""android"",""isDebug"":true,""osVersion"":""36"",""phoneMode"":""23127PN0CC"",""location"":""default"",""appLanguage"":""cn""},{""phoneLanguage"":""zh"",""snsToken"":""fq9Q20_MTfuI43jab5yOtl:APA91bFNmuXW8hZM_Tdqt5N-4lmm6NpS_k08V3FbELsd5LAtYMf3TheiycF0rhQEjFq1cFAn12KW2UTpjpni_ZeGXhxLhN_TCZVV2es7Ol4zbxePhjbXWs8"",""appName"":""10.42.0.13"",""ip"":""113.104.183.196"",""versionFlag"":""10.42.0.13"",""updateTime"":1774161195208,""phoneBranch"":""Xiaomi"",""platform"":""android"",""isDebug"":true,""osVersion"":""36"",""phoneMode"":""23127PN0CC"",""location"":""default"",""appLanguage"":""cn""},{""phoneLanguage"":""zh"",""snsToken"":""fq9Q20_MTfuI43jab5yOtl:APA91bFNmuXW8hZM_Tdqt5N-4lmm6NpS_k08V3FbELsd5LAtYMf3TheiycF0rhQEjFq1cFAn12KW2UTpjpni_ZeGXhxLhN_TCZVV2es7Ol4zbxePhjbXWs8"",""appName"":""10.42.0.1",
1775791053267,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"3"",""ip"":""113.104.181.197"",""versionFlag"":""10.42.0.13"",""updateTime"":1774395154440,""phoneBranch"":""Xiaomi"",""platform"":""android"",""isDebug"":true,""osVersion"":""36"",""phoneMode"":""23127PN0CC"",""location"":""default"",""appLanguage"":""cn""},{""phoneLanguage"":""zh"",""snsToken"":""fq9Q20_MTfuI43jab5yOtl:APA91bFNmuXW8hZM_Tdqt5N-4lmm6NpS_k08V3FbELsd5LAtYMf3TheiycF0rhQEjFq1cFAn12KW2UTpjpni_ZeGXhxLhN_TCZVV2es7Ol4zbxePhjbXWs8"",""appName"":""10.42.0.13"",""ip"":""103.117.76.105"",""versionFlag"":""10.42.0.13"",""updateTime"":1774517130308,""phoneBranch"":""Xiaomi"",""platform"":""android"",""isDebug"":true,""osVersion"":""36"",""phoneMode"":""23127PN0CC"",""location"":""default"",""appLanguage"":""cn""},{""phoneLanguage"":""zh"",""snsToken"":""fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aXdM00tyw"",""appName"":""9.23"",""ip"":""103.117.76.105"",""versionFlag"":""9.23"",""updateTime"":1774523841099,""phoneBranch"":""Xiaomi"",""platform"":""android"",""isDebug"":true,""osVersion"":""36"",""phoneMode"":""23127PN0CC"",""location"":""default"",""appLanguage"":""cn""},{""phoneLanguage"":""zh"",""snsToken"":""fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aXdM00tyw"",""appName"":""9.23"",""ip"":""223.104.79.106"",""versionFlag"":""9.23"",""updateTime"":1774525637116,""phoneBranch"":""Xiaomi"",""platform"":""android"",""isDebug"":true,""osVersion"":""36"",""phoneMode"":""23127PN0CC"",""location"":""default"",""appLanguage"":""cn""},{""phoneLanguage"":""zh"",""snsToken"":""fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aXdM00tyw"",""appName"":""9.23"",""ip"":""223.104.87.128"",""versionFlag"":""9.23"",""updateTime"":1774592790580,""phoneBranch"":""Xiaomi"",""platform"":""android"",""isDebug"":true,""osVersion"":""36"",""phoneMode"":""23127PN0CC"",""location"":""default"",""appLanguage"":""cn""},{""phoneLanguage"":""zh"",""snsToken"":""fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT",
1775791053267,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aXdM00tyw"",""appName"":""9.23"",""ip"":""103.117.76.105"",""versionFlag"":""9.23"",""updateTime"":1774604769761,""phoneBranch"":""Xiaomi"",""platform"":""android"",""isDebug"":true,""osVersion"":""36"",""phoneMode"":""23127PN0CC"",""location"":""default"",""appLanguage"":""cn""},{""phoneLanguage"":""zh"",""snsToken"":""fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aXdM00tyw"",""appName"":""9.23"",""ip"":""103.117.76.105"",""versionFlag"":""9.23"",""updateTime"":1774604800733,""phoneBranch"":""Xiaomi"",""platform"":""android"",""isDebug"":true,""osVersion"":""36"",""phoneMode"":""23127PN0CC"",""location"":""default"",""appLanguage"":""cn""},{""phoneLanguage"":""zh"",""snsToken"":""fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aXdM00tyw"",""appName"":""9.23"",""ip"":""223.104.68.238"",""versionFlag"":""9.23"",""updateTime"":1774781307232,""phoneBranch"":""Xiaomi"",""platform"":""android"",""isDebug"":true,""osVersion"":""36"",""phoneMode"":""23127PN0CC"",""location"":""default"",""appLanguage"":""cn""},{""phoneLanguage"":""zh"",""snsToken"":""fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aXdM00tyw"",""appName"":""9.23"",""ip"":""103.117.76.105"",""versionFlag"":""9.23"",""updateTime"":1775791053455,""phoneBranch"":""Xiaomi"",""platform"":""android"",""isDebug"":true,""osVersion"":""36"",""phoneMode"":""23127PN0CC"",""location"":""default"",""appLanguage"":""cn""}],""testVersion"":{},""userData"":{""enableScene3"":true,""globalNotify"":true,""sceneNotify"":true,""policyStatusV2Timestamp"":""2025-09-05T10:50:48.873Z"",""countryCode"":""HK"",""policyStatusV2"":true,""childrenPolicyTimestamp"":""2025-09-05T10:50:48.873Z"",""childrenPolicyStatus"":true,""notDisturb"":false,""privacyPolicyStatus"":true,""scoreEnable"":true,""customScore"":false,""lockGroupNotify"":false}},""message"":""""}
<-- END HTTP (5645-byte body)",
1775791053268,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/scene/v1/geofencing/get (866ms)
content-type: application/json
content-length: 59
date: Fri, 10 Apr 2026 03:17:33 GMT
switchbot-request-id: d627c73f-6bf8-432d-a137-a182c7daba85
{""resultCode"":100, ""message"":"""", ""data"":{""geofencings"":[]}}
<-- END HTTP (59-byte body)",
1775791053276,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,GeofenceManger getAIPetGeofenceList data:[],
1775791053284,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"userData={""appLanguage"":"""",""confirmTimeAt"":0,""enableScene3"":true,""externalProvider"":false,""local"":"""",""lockGroupNotify"":false,""periodTime"":0,""phoneLanguage"":"""",""startTime"":0,""customScore"":false,""notScoreArray"":[],""score"":1,""scoreEnable"":true}",UserViewModel
1775791053284,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"setOpenApiToken:{""exp"":2103526218565,""iat"":1787907018565,""version"":1.0,""token"":""w010117563710184ec7""}",
1775791053285,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"NetResponse(statusCode=100, body={targetVersion={WoLinkMiniBleVersion=36.0, hubPlusWifiVersion=23.0, WoCurtainBleVersion=46.0, WoFinderCardBleVersion=1.0, W1128000BleVersion=1.0, WoContactBleVersion=11.0, WoWaterDetectorBleVersion=1.0, hubPlusBleVersion=24.0, hubWifiVersion=23.0, WoIOSensorBleVersion=4.0, WoCamKvs5mpMcuVersion=1.6777336E7, WoPresenceBleVersion=13.0, WoMeterBleVersion=27.0, WoLinkMiniWifiVersion=23.0, hubBleVersion=44.0, W1079001BleVersion=1.0, WoLockBleVersion=58.0, WoCamKvs5mpCpuVersion=1.6777336E7, WoHandBleVersion=64.0, W1079000BleVersion=1.0, WoRWSBleVersion=16.0}, userName=9773828c-90bb-4725-a04c-339e0eec300e, openApiToken={exp=2.103526218565E12, iat=1.787907018565E12, version=1.0, token=w010117563710184ec7}, userActivity=[{phoneLanguage=zh, snsToken=fq9Q20_MTfuI43jab5yOtl:APA91bFNmuXW8hZM_Tdqt5N-4lmm6NpS_k08V3FbELsd5LAtYMf3TheiycF0rhQEjFq1cFAn12KW2UTpjpni_ZeGXhxLhN_TCZVV2es7Ol4zbxePhjbXWs8, appName=10.42.0.13, ip=113.104.202.139, versionFlag=10.42.0.13, updateTime=1.773984639E12, phoneBranch=Xiaomi, platform=android, isDebug=true, osVersion=36, phoneMode=23127PN0CC, location=default, appLanguage=cn}, {phoneLanguage=zh, snsToken=fq9Q20_MTfuI43jab5yOtl:APA91bFNmuXW8hZM_Tdqt5N-4lmm6NpS_k08V3FbELsd5LAtYMf3TheiycF0rhQEjFq1cFAn12KW2UTpjpni_ZeGXhxLhN_TCZVV2es7Ol4zbxePhjbXWs8, appName=10.42.0.13, ip=113.104.183.196, versionFlag=10.42.0.13, updateTime=1.774161195208E12, phoneBranch=Xiaomi, platform=android, isDebug=true, osVersion=36, phoneMode=23127PN0CC, location=default, appLanguage=cn}, {phoneLanguage=zh, snsToken=fq9Q20_MTfuI43jab5yOtl:APA91bFNmuXW8hZM_Tdqt5N-4lmm6NpS_k08V3FbELsd5LAtYMf3TheiycF0rhQEjFq1cFAn12KW2UTpjpni_ZeGXhxLhN_TCZVV2es7Ol4zbxePhjbXWs8, appName=10.42.0.13, ip=113.104.181.197, versionFlag=10.42.0.13, updateTime=1.77439515444E12, phoneBranch=Xiaomi, platform=android, isDebug=true, osVersion=36, phoneMode=23127PN0CC, location=default, appLanguage=cn}, {phoneLanguage=zh, snsToken=fq9Q20_MTfuI43jab5yOtl:APA91bFNmuXW8hZM_",userInfo-upload
1775791053285,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"Tdqt5N-4lmm6NpS_k08V3FbELsd5LAtYMf3TheiycF0rhQEjFq1cFAn12KW2UTpjpni_ZeGXhxLhN_TCZVV2es7Ol4zbxePhjbXWs8, appName=10.42.0.13, ip=103.117.76.105, versionFlag=10.42.0.13, updateTime=1.774517130308E12, phoneBranch=Xiaomi, platform=android, isDebug=true, osVersion=36, phoneMode=23127PN0CC, location=default, appLanguage=cn}, {phoneLanguage=zh, snsToken=fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aXdM00tyw, appName=9.23, ip=103.117.76.105, versionFlag=9.23, updateTime=1.774523841099E12, phoneBranch=Xiaomi, platform=android, isDebug=true, osVersion=36, phoneMode=23127PN0CC, location=default, appLanguage=cn}, {phoneLanguage=zh, snsToken=fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aXdM00tyw, appName=9.23, ip=223.104.79.106, versionFlag=9.23, updateTime=1.774525637116E12, phoneBranch=Xiaomi, platform=android, isDebug=true, osVersion=36, phoneMode=23127PN0CC, location=default, appLanguage=cn}, {phoneLanguage=zh, snsToken=fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aXdM00tyw, appName=9.23, ip=223.104.87.128, versionFlag=9.23, updateTime=1.77459279058E12, phoneBranch=Xiaomi, platform=android, isDebug=true, osVersion=36, phoneMode=23127PN0CC, location=default, appLanguage=cn}, {phoneLanguage=zh, snsToken=fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aXdM00tyw, appName=9.23, ip=103.117.76.105, versionFlag=9.23, updateTime=1.774604769761E12, phoneBranch=Xiaomi, platform=android, isDebug=true, osVersion=36, phoneMode=23127PN0CC, location=default, appLanguage=cn}, {phoneLanguage=zh, snsToken=fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aX",userInfo-upload
1775791053285,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"dM00tyw, appName=9.23, ip=103.117.76.105, versionFlag=9.23, updateTime=1.774604800733E12, phoneBranch=Xiaomi, platform=android, isDebug=true, osVersion=36, phoneMode=23127PN0CC, location=default, appLanguage=cn}, {phoneLanguage=zh, snsToken=fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aXdM00tyw, appName=9.23, ip=223.104.68.238, versionFlag=9.23, updateTime=1.774781307232E12, phoneBranch=Xiaomi, platform=android, isDebug=true, osVersion=36, phoneMode=23127PN0CC, location=default, appLanguage=cn}, {phoneLanguage=zh, snsToken=fZfbFCZ9Q1O6gKhQNTMl-L:APA91bFlFO4FENrRJmKa-GDSm-lmlUMAFVe8OxZLjwsK-fH_X4UkISXWv9wlayrCIgCzsDLtQd6guT3MKz3NVjNaJZc0ffzPrsRf6qW7HpO9c7aXdM00tyw, appName=9.23, ip=103.117.76.105, versionFlag=9.23, updateTime=1.775791053455E12, phoneBranch=Xiaomi, platform=android, isDebug=true, osVersion=36, phoneMode=23127PN0CC, location=default, appLanguage=cn}], testVersion={}, userData={enableScene3=true, globalNotify=true, sceneNotify=true, policyStatusV2Timestamp=2025-09-05T10:50:48.873Z, countryCode=HK, policyStatusV2=true, childrenPolicyTimestamp=2025-09-05T10:50:48.873Z, childrenPolicyStatus=true, notDisturb=false, privacyPolicyStatus=true, scoreEnable=true, customScore=false, lockGroupNotify=false}}, message=)",userInfo-upload
1775791053286,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,isNeedShowDialog=false,邀评弹窗
1775791053294,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,GeofenceManger--removeGeofences--intent--success--[],
1775791059266,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"onCapabilitiesChanged networkCapabilities=[ Transports: WIFI Capabilities: NOT_METERED&INTERNET&NOT_RESTRICTED&TRUSTED&NOT_VPN&VALIDATED&NOT_ROAMING&FOREGROUND&NOT_CONGESTED&NOT_SUSPENDED&NOT_VCN_MANAGED&NOT_BANDWIDTH_CONSTRAINED LinkUpBandwidth>=45816Kbps LinkDnBandwidth>=45635Kbps TransportInfo: <SSID: <unknown ssid>, BSSID: 02:00:00:00:00:00, MAC: 02:00:00:00:00:00, IP: /10.8.68.198, Security type: 2, Supplicant state: COMPLETED, Wi-Fi standard: 11ax, RSSI: -37, Link speed: 286Mbps, Tx Link speed: 286Mbps, Max Supported Tx Link speed: 286Mbps, Rx Link speed: 286Mbps, Max Supported Rx Link speed: 286Mbps, Frequency: 5200MHz, Net ID: -1, Metered hint: false, score: 60, isUsable: true, CarrierMerged: false, SubscriptionId: -1, IsPrimary: -1, Trusted: true, Restricted: false, Ephemeral: false, OEM paid: false, OEM private: false, OSU AP: false, FQDN: <none>, Provider friendly name: <none>, Requesting package name: <none><none>MLO Information: , Is TID-To-Link negotiation supported by the AP: false, AP MLD Address: <none>, AP MLO Link Id: <none>, AP MLO Affiliated links: <none>, Vendor Data: <none>> SignalStrength: -37 UnderlyingNetworks: Null]",NetworkStatusCallback
1775791059273,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,当前网络状态--networkType--WiFi,NetworkStatusCallback
1775791059274,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,涂鸦登录账号,TuYaInitializer
1775791059276,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/scene/v1/suggest/getList (6863ms)
content-type: application/json
date: Fri, 10 Apr 2026 03:17:33 GMT
switchbot-request-id: 276514b0-49b0-476a-a3d8-929a74d6a7f7
{""resultCode"":100, ""message"":"""", ""data"":{""suggest"":[{""title"":""智能降温"", ""subTitle"":""维持适宜的室内温度"", ""description"":""让您在炎热的夏天也能保持舒适！只要室内温度超过28°C，空调就会自动开启，首先以较低温度运行10分钟让室内立即降温，之后再以适宜温度运行，为您营造凉爽的家居环境。"", ""suggestID"":""intelligent_cooling"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E6%99%BA%E8%83%BD%E9%99%8D%E6%B8%A9.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""室外温湿度计"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_iometer.png"", ""deviceType"":""WoIOSensor""}, {""deviceName"":""温湿度计"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_meter.png"", ""deviceType"":""WoMeter""}, {""deviceName"":""智能大屏温湿度计"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_meterplus.png"", ""deviceType"":""WoMeterPlus""}, {""deviceName"":""万能遥控器2"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_hub2.png"", ""deviceType"":""WoHub2""}, {""deviceName"":""温湿度计Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_meterpro.png"", ""deviceType"":""W1079000""}, {""deviceName"":""万能网关3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_hub3.png"", ""deviceType"":""W1096000""}, {""deviceName"":""天气站"", ""deviceIcon"":""https://s3.amazonaws.com/www.wohand.com/version/wocaotech/feedback_img/weatherstation.png"", ""deviceType"":""W1070000""}, {""deviceName"":""空调"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E9%81%A5%E6%8E%A7%E5%99%A8_%E7%A9%BA%E8%B0%83.png"", ""deviceType"":""remote_1""}, {""deviceName"":""循环扇"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_fan2_defalut.png"", ""deviceType"":""WoFan2""}, {""deviceName"":""落地循环扇"", ""deviceIcon"":",
1775791059276,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_fan3_dark.png"", ""deviceType"":""W1116000""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E6%99%BA%E8%83%BD%E9%99%8D%E6%B8%A9%403x.png"", ""backColor"":""#68D4D4""}, {""title"":""回家"", ""subTitle"":""自动开灯，温馨回家"", ""description"":""当您回到家时，空调开启到设定的模式和温度，灯光开启并播放音乐欢迎您回家。"", ""suggestID"":""go_home"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E5%9B%9E%E5%AE%B6.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""门窗传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_contactsensor.png"", ""deviceType"":""WoContact""}, {""deviceName"":""智能追踪卡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_findmy_offline.png"", ""deviceType"":""WoFinderCard""}, {""deviceName"":""空调"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E9%81%A5%E6%8E%A7%E5%99%A8_%E7%A9%BA%E8%B0%83.png"", ""deviceType"":""remote_1""}, {""deviceName"":""灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E7%81%AF.png"", ""deviceType"":""remote_14""}, {""deviceName"":""室外摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_osc.png"", ""deviceType"":""WoBatteryCam""}, {""deviceName"":""智能云台摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam""}, {""deviceName"":""智能云台摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam3MP""}, {""deviceName"":""智能摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ipc.png"", ""deviceType"":""WoCamera""}, {""deviceName"":""室外摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoOSC2""}, {""deviceName"":""智能云台摄像机 Plus 2K"", ""deviceIcon"":""https://prod-switch",
1775791059276,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"bot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs""}, {""deviceName"":""智能云台摄像机 Plus 3K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs5mp""}, {""deviceName"":""吸顶灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglight.png"", ""deviceType"":""WoCeiling""}, {""deviceName"":""吸顶灯 Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglightpro.png"", ""deviceType"":""WoCeilingPro""}, {""deviceName"":""彩色灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""WoStrip""}, {""deviceName"":""彩色灯泡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bulb.png"", ""deviceType"":""WoBulb""}, {""deviceName"":""智能开关"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bot.png"", ""deviceType"":""WoHand""}, {""deviceName"":""落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102000""}, {""deviceName"":""灯带3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102001""}, {""deviceName"":""炫彩灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102003""}, {""deviceName"":""炫彩落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102004""}, {""deviceName"":""炫彩钢丝霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102005""}, {""deviceName"":""炫彩霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102006""}, {""deviceName"":""融蜡灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_candle_lamp.png"", ""deviceType"":""W112300",
1775791059276,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"0""}, {""deviceName"":""散热器恒温阀"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_radiator_valve_open.png"", ""deviceType"":""W1128000""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E5%9B%9E%E5%AE%B6%403x.png"", ""backColor"":""#FFD56A""}, {""title"":""离家"", ""subTitle"":""智能安防，无忧离家"", ""description"":""当您出门离家时，自动关闭所有灯光、电源插座和空调，并开启摄像头监控家中动态，确保您的家庭安全且节能。"", ""suggestID"":""leave_home"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E7%A6%BB%E5%AE%B6.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""门窗传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_contactsensor.png"", ""deviceType"":""WoContact""}, {""deviceName"":""智能追踪卡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_findmy_offline.png"", ""deviceType"":""WoFinderCard""}, {""deviceName"":""空调"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E9%81%A5%E6%8E%A7%E5%99%A8_%E7%A9%BA%E8%B0%83.png"", ""deviceType"":""remote_1""}, {""deviceName"":""灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E7%81%AF.png"", ""deviceType"":""remote_14""}, {""deviceName"":""室外摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_osc.png"", ""deviceType"":""WoBatteryCam""}, {""deviceName"":""智能云台摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam""}, {""deviceName"":""智能云台摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam3MP""}, {""deviceName"":""智能摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ipc.png"", ""deviceType"":""WoCamera""}, {""deviceName"":""室外摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoOSC2""}, {""deviceName"":""",
1775791059276,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"智能云台摄像机 Plus 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs""}, {""deviceName"":""智能云台摄像机 Plus 3K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs5mp""}, {""deviceName"":""吸顶灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglight.png"", ""deviceType"":""WoCeiling""}, {""deviceName"":""吸顶灯 Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglightpro.png"", ""deviceType"":""WoCeilingPro""}, {""deviceName"":""彩色灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""WoStrip""}, {""deviceName"":""彩色灯泡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bulb.png"", ""deviceType"":""WoBulb""}, {""deviceName"":""智能开关"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bot.png"", ""deviceType"":""WoHand""}, {""deviceName"":""落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102000""}, {""deviceName"":""灯带3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102001""}, {""deviceName"":""炫彩灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102003""}, {""deviceName"":""炫彩落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102004""}, {""deviceName"":""炫彩钢丝霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102005""}, {""deviceName"":""炫彩霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102006""}, {""deviceName"":""融蜡灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_ico",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"n/icon_32pt_candle_lamp.png"", ""deviceType"":""W1123000""}, {""deviceName"":""散热器恒温阀"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_radiator_valve_close.png"", ""deviceType"":""W1128000""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E7%A6%BB%E5%AE%B6%403x.png"", ""backColor"":""#5797F8""}, {""title"":""起床"", ""subTitle"":""模拟自然光亮，助您轻松起床"", ""description"":""在设定的早起时间，窗帘自动开启，灯光逐渐变亮，帮助你轻松起床。"", ""suggestID"":""get_up"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E8%B5%B7%E5%BA%8A.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""窗帘机器人"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_curtain.png"", ""deviceType"":""WoCurtain""}, {""deviceName"":""智能窗帘3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_curtain.png"", ""deviceType"":""WoCurtain3""}, {""deviceName"":""百叶帘调光器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_blindtilt.png"", ""deviceType"":""WoBlindTilt""}, {""deviceName"":""吸顶灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglight.png"", ""deviceType"":""WoCeiling""}, {""deviceName"":""吸顶灯 Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglightpro.png"", ""deviceType"":""WoCeilingPro""}, {""deviceName"":""融蜡灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_candle_lamp.png"", ""deviceType"":""W1123000""}, {""deviceName"":""彩色灯泡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bulb.png"", ""deviceType"":""WoBulb""}, {""deviceName"":""落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102000""}, {""deviceName"":""灯带3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102001""}, {""deviceName"":""炫彩灯带"", ""deviceIcon"":""https://",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102003""}, {""deviceName"":""炫彩落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102004""}, {""deviceName"":""炫彩钢丝霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102005""}, {""deviceName"":""炫彩霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102006""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E8%B5%B7%E5%BA%8A%403x.png"", ""backColor"":""#FFD362""}, {""title"":""睡眠"", ""subTitle"":""关灯拉帘，营造舒适入睡环境"", ""description"":""在设定的睡觉时间，自动关闭家中灯光，窗帘静音关闭，帮助您入睡。"", ""suggestID"":""to_sleep"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E7%9D%A1%E7%9C%A0.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""窗帘机器人"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_curtain.png"", ""deviceType"":""WoCurtain""}, {""deviceName"":""百叶帘调光器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_blindtilt.png"", ""deviceType"":""WoBlindTilt""}, {""deviceName"":""吸顶灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglight.png"", ""deviceType"":""WoCeiling""}, {""deviceName"":""吸顶灯 Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglightpro.png"", ""deviceType"":""WoCeilingPro""}, {""deviceName"":""融蜡灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_candle_lamp.png"", ""deviceType"":""W1123000""}, {""deviceName"":""彩色灯泡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bulb.png"", ""deviceType"":""WoBulb""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E7%9D%A1%E7%9C%A0%403x.png"", ""backColor"":""#264",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"876""}, {""title"":""自动清洁"", ""subTitle"":""定时打扫，维持干净的家居环境"", ""description"":""当您不在家时，扫地机在设定的时间自动开始打扫，为您维持干净的家居环境。"", ""suggestID"":""automatic_cleaning"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E8%87%AA%E5%8A%A8%E6%B8%85%E6%B4%81.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""智能扫地机器人S1"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_s1.png"", ""deviceType"":""WoSweeper""}, {""deviceName"":""扫地机器人K10+"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_k10%2B.png"", ""deviceType"":""WoSweeperMini""}, {""deviceName"":""智能扫地机器人S1 Plus"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_s1plus.png"", ""deviceType"":""WoSweeperPlus""}, {""deviceName"":""地面清洁机器人S10"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_sweeper_s1_defalut.png"", ""deviceType"":""WoSweeperOrigin""}, {""deviceName"":""扫地机器人K10+ Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_k10%2B.png"", ""deviceType"":""WoSweeperMiniPro""}, {""deviceName"":""智能扫地机器人组合K10+ Pro Combo"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_k10%2B.png"", ""deviceType"":""91AgWZ1n""}, {""deviceName"":""地面清洁机器人S20"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_k10%2B.png"", ""deviceType"":""W1106000""}, {""deviceName"":""扫地机器人K11+"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_k10%2B.png"", ""deviceType"":""W1113000""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E8%87%AA%E5%8A%A8%E6%B8%85%E6%B4%81%403x.png"", ""backColor"":""#62DDB1""}, {""title"":""植物养护"", ""subTitle"":""实时维持绿植湿度"", ""description"":""当传感器检测到植物土壤湿度降低，需要浇水时，使用Bot或Plug Mini自动开启浇水设备，并发送通知给您。"", ""suggestID"":""plant_maintenance"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E6%A4%8D%E7%89%A9%E5%85%BB%E6%8A%A4.png"", ""color"":""",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"""}, ""needDevices"":[{""deviceName"":""室外温湿度计"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_iometer.png"", ""deviceType"":""WoIOSensor""}, {""deviceName"":""温湿度计"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_meter.png"", ""deviceType"":""WoMeter""}, {""deviceName"":""智能大屏温湿度计"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_meterplus.png"", ""deviceType"":""WoMeterPlus""}, {""deviceName"":""万能遥控器2"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_hub2.png"", ""deviceType"":""WoHub2""}, {""deviceName"":""温湿度计Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_meterpro.png"", ""deviceType"":""W1079000""}, {""deviceName"":""万能网关3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_hub3.png"", ""deviceType"":""W1096000""}, {""deviceName"":""天气站"", ""deviceIcon"":""https://s3.amazonaws.com/www.wohand.com/version/wocaotech/feedback_img/weatherstation.png"", ""deviceType"":""W1070000""}, {""deviceName"":""智能插座"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_plug.png"", ""deviceType"":""WoPlug""}, {""deviceName"":""智能插座mini （JP）"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_plugminijp.png"", ""deviceType"":""WoPlugJP""}, {""deviceName"":""智能插座mini （US）"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_plugminius.png"", ""deviceType"":""WoPlugUS""}, {""deviceName"":""智能开关"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bot.png"", ""deviceType"":""WoHand""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E6%A4%8D%E7%89%A9%E5%85%BB%E6%8A%A4%403x.png"", ""backColor"":""#A8CE58""}, {""title"":""门开提醒"", ""subTitle"":""门开提醒，随时关注家门安全"", ""description"":""您的门被打开时，即时发送通知给您，让您随时掌握家门安全。"", ""suggestID"":""door_open_reminder"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/autom",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"ation_icon/icon_32pt_%E9%97%A8%E5%BC%80%E6%8F%90%E9%86%92.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""智能门锁"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_lock.png"", ""deviceType"":""WoLock""}, {""deviceName"":""智能门锁Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_lock.png"", ""deviceType"":""WoLockPro""}, {""deviceName"":""智能门锁Ultra"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_lock.png"", ""deviceType"":""W1091000""}, {""deviceName"":""门窗传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_contactsensor.png"", ""deviceType"":""WoContact""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E9%97%A8%E5%BC%80%E6%8F%90%E9%86%92%403x.png"", ""backColor"":""#A0A7AB""}, {""title"":""安全监控"", ""subTitle"":""实时监控家庭安全"", ""description"":""当家中的摄像头或传感器检测到异常活动时，将响起警报，开启灯光，并发送通知给您。"", ""suggestID"":""security_monitoring"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E5%AE%89%E5%85%A8%E7%9B%91%E6%8E%A7.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""室外摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_osc.png"", ""deviceType"":""WoBatteryCam""}, {""deviceName"":""智能门铃"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_video_doorbell_form.png"", ""deviceType"":""W1050001""}, {""deviceName"":""智能云台摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam""}, {""deviceName"":""智能云台摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam3MP""}, {""deviceName"":""智能摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ipc.png"", ""deviceType"":""WoCamera""}, {""deviceName"":""室外摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", """,
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"deviceType"":""WoOSC2""}, {""deviceName"":""智能云台摄像机 Plus 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs""}, {""deviceName"":""智能云台摄像机 Plus 3K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs5mp""}, {""deviceName"":""门窗传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_contactsensor.png"", ""deviceType"":""WoContact""}, {""deviceName"":""灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E7%81%AF.png"", ""deviceType"":""remote_14""}, {""deviceName"":""吸顶灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglight.png"", ""deviceType"":""WoCeiling""}, {""deviceName"":""吸顶灯 Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglightpro.png"", ""deviceType"":""WoCeilingPro""}, {""deviceName"":""智能开关"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bot.png"", ""deviceType"":""WoHand""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E5%AE%89%E5%85%A8%E7%9B%91%E6%8E%A7%403x.png"", ""backColor"":""#5797F8""}, {""title"":""人来开灯"", ""subTitle"":""自动为您照亮"", ""description"":""当您经过时，自动开灯，为您照亮当前环境。"", ""suggestID"":""people_come_light_on"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E4%BA%BA%E6%9D%A5%E5%BC%80%E7%81%AF.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""人体传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_motionsensor.png"", ""deviceType"":""WoPresence""}, {""deviceName"":""存在传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_presencesensor.png"", ""deviceType"":""W1101000""}, {""deviceName"":""落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102000""}, {""deviceName"":""灯带",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102001""}, {""deviceName"":""炫彩灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102003""}, {""deviceName"":""炫彩落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102004""}, {""deviceName"":""炫彩钢丝霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102005""}, {""deviceName"":""炫彩霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102006""}, {""deviceName"":""灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E7%81%AF.png"", ""deviceType"":""remote_14""}, {""deviceName"":""吸顶灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglight.png"", ""deviceType"":""WoCeiling""}, {""deviceName"":""吸顶灯 Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglightpro.png"", ""deviceType"":""WoCeilingPro""}, {""deviceName"":""彩色灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""WoStrip""}, {""deviceName"":""彩色灯泡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bulb.png"", ""deviceType"":""WoBulb""}, {""deviceName"":""智能开关"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bot.png"", ""deviceType"":""WoHand""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E4%BA%BA%E6%9D%A5%E5%BC%80%E7%81%AF%403x.png"", ""backColor"":""#FFD56A""}, {""title"":""人走关灯"", ""subTitle"":""人走灯灭，省心节电"", ""description"":""当您离开时，自动关闭灯光，节能又省力。"", ""suggestID"":""people_leave_light_off"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E4%BA%",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"BA%E8%B5%B0%E5%85%B3%E7%81%AF.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""人体传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_motionsensor.png"", ""deviceType"":""WoPresence""}, {""deviceName"":""存在传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_presencesensor.png"", ""deviceType"":""W1101000""}, {""deviceName"":""灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E7%81%AF.png"", ""deviceType"":""remote_14""}, {""deviceName"":""吸顶灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglight.png"", ""deviceType"":""WoCeiling""}, {""deviceName"":""吸顶灯 Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglightpro.png"", ""deviceType"":""WoCeilingPro""}, {""deviceName"":""彩色灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""WoStrip""}, {""deviceName"":""彩色灯泡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bulb.png"", ""deviceType"":""WoBulb""}, {""deviceName"":""智能开关"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bot.png"", ""deviceType"":""WoHand""}, {""deviceName"":""落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102000""}, {""deviceName"":""灯带3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102001""}, {""deviceName"":""炫彩灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102003""}, {""deviceName"":""炫彩落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102004""}, {""deviceName"":""炫彩钢丝霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102005""},",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回," {""deviceName"":""炫彩霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102006""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E4%BA%BA%E8%B5%B0%E5%85%B3%E7%81%AF%403x.png"", ""backColor"":""#264876""}, {""title"":""漏水提醒"", ""subTitle"":""漏水提醒，随时守护家庭安全"", ""description"":""当传感器检测到漏水时，为您发送消息通知"", ""suggestID"":""water_leakage_reminder"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E6%BC%8F%E6%B0%B4%E6%8F%90%E9%86%92.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""水浸传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_waterdetector%403x.png"", ""deviceType"":""WoWaterDetector""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E6%BC%8F%E6%B0%B4%E6%8F%90%E9%86%92%403x.png"", ""backColor"":""#5797F8""}, {""title"":""夜间未关门"", ""subTitle"":""守护您的爱车安全，让您一夜安心。"", ""description"":""当夜间车库门仍为开启状态，将为您发送消息通知"", ""suggestID"":""nighttime_not_closed_reminder"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_%E5%A4%9C%E9%97%B4%E6%9C%AA%E5%85%B3%E9%97%A8.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""车库门控制器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/device_icon/icon_32pt_gargedoor_open.png"", ""deviceType"":""W1083003""}], ""background"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E5%A4%9C%E9%97%B4%E6%9C%AA%E5%85%B3%E9%97%A8.png"", ""backColor"":""#264876""}, {""title"":""未关门提醒"", ""subTitle"":""守护您的爱车安全，避免忘关车库门的烦恼。"", ""description"":""当车库门超过一定时长仍为开启状态，将为您发送消息通知"", ""suggestID"":""timeout_not_closed_reminder"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_%E6%9C%AA%E5%85%B3%E9%97%A8%E6%8F%90%E9%86%92.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""车库门控制器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/device_icon/icon_32pt_garge",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"door_open.png"", ""deviceType"":""W1083003""}], ""background"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E6%9C%AA%E5%85%B3%E9%97%A8%E6%8F%90%E9%86%92.png"", ""backColor"":""#5797F8""}, {""title"":""回家提醒"", ""subTitle"":""回到家时，发送提醒"", ""description"":""当您的家人回到家时，为您发送提醒"", ""suggestID"":""go_home_reminder"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/automation_icon/icon_32pt_%E5%9B%9E%E5%AE%B6%E6%8F%90%E9%86%92.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""安全报警器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/device_icon/icon_32pt_safety_alarm_online.png"", ""deviceType"":""W1110000""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E5%9B%9E%E5%AE%B6%403x.png"", ""backColor"":""#FFD56A""}, {""title"":""离家提醒"", ""subTitle"":""离开家时，发送提醒"", ""description"":""当您的家人离开家时，为您发送提醒"", ""suggestID"":""leave_home_reminder"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/automation_icon/icon_32pt_%E7%A6%BB%E5%AE%B6%E6%8F%90%E9%86%92.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""安全报警器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/device_icon/icon_32pt_safety_alarm_offline.png"", ""deviceType"":""W1110000""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E7%A6%BB%E5%AE%B6%403x.png"", ""backColor"":""#5797F8""}, {""title"":""回家布防报警"", ""subTitle"":""回家后监控室内外环境，安全守护"", ""description"":""当设备检测到异常时，执行消息推送与报警。"", ""suggestID"":""go_home_build_defenses_alarm"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/automation_icon/icon_%E8%87%AA%E5%8A%A8%E5%8C%96_%E5%9B%9E%E5%AE%B6%E5%B8%83%E9%98%B2_%E6%8A%A5%E8%AD%A6.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""智能门铃"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_video_doorbell_form.png"", ""deviceType"":""W1050001""}, {""deviceName"":""水浸传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazona",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"ws.com/device_icon/icon_waterdetector%403x.png"", ""deviceType"":""WoWaterDetector""}, {""deviceName"":""门窗传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_contactsensor.png"", ""deviceType"":""WoContact""}, {""deviceName"":""室外摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoBatteryCam""}, {""deviceName"":""室外摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoOSC2""}, {""deviceName"":""智能云台摄像机 Plus 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs""}, {""deviceName"":""智能云台摄像机 Plus 3K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs5mp""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E5%9B%9E%E5%AE%B6%E5%B8%83%E9%98%B2.png"", ""backColor"":""#5797F8""}, {""title"":""离家布防报警"", ""subTitle"":""离家后识别异常，安全守护"", ""description"":""设备监测到室内外异常时，执行消息推送与报警"", ""suggestID"":""leave_home_build_defenses_alarm"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/automation_icon/icon_%E8%87%AA%E5%8A%A8%E5%8C%96_%E7%A6%BB%E5%AE%B6%E5%B8%83%E9%98%B2_%E6%8A%A5%E8%AD%A6.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""智能摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ipc.png"", ""deviceType"":""WoCamera""}, {""deviceName"":""智能云台摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam""}, {""deviceName"":""智能云台摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam3MP""}, {""deviceName"":""智能云台摄像机 Plus 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs""}, {""deviceName"":""智能云台摄像机 Plus 3K"", ""deviceIcon"":""https://prod-switchbot-",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs5mp""}, {""deviceName"":""智能门铃"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_video_doorbell_form.png"", ""deviceType"":""W1050001""}, {""deviceName"":""室外摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoBatteryCam""}, {""deviceName"":""室外摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoOSC2""}, {""deviceName"":""人体传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_motionsensor.png"", ""deviceType"":""WoPresence""}, {""deviceName"":""水浸传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_waterdetector%403x.png"", ""deviceType"":""WoWaterDetector""}, {""deviceName"":""门窗传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_contactsensor.png"", ""deviceType"":""WoContact""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E7%A6%BB%E5%AE%B6%E5%B8%83%E9%98%B2.png"", ""backColor"":""#264876""}]}}
<-- END HTTP (36073-byte body)",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 OK https://prod-switchbot-icons.s3.amazonaws.com/wo_device_icon.json (7101ms)
x-amz-id-2: yeM74bNePR0MI78BEG2jsmqN2td4O9WHQkgQWLpEWRL92u7jvWJ4rNkn1saTH4G+7mVAQZVC5WbtpUKrMJ3vLPv6BIS8z0Iq
x-amz-request-id: 0MWTAZ7BE3DPXDFT
Date: Fri, 10 Apr 2026 03:17:35 GMT
Last-Modified: Fri, 10 Apr 2026 02:19:20 GMT
ETag: ""3e6156f0be15dc384de8f9b7f5a0242f""
x-amz-server-side-encryption: AES256
Accept-Ranges: bytes
Content-Type: binary/octet-stream
Content-Length: 20062
Server: AmazonS3
{
    ""camera_shape_AiHubThirdPartyCam"": ""camera_shape_AiHubThirdPartyCam.png"",
    ""camera_shape_WoBatteryCam"": ""camera_shape_WoBatteryCam.png"",
    ""camera_shape_WoCamera"": ""camera_shape_WoCamera.png"",
    ""camera_shape_WoCamKvs"": ""camera_shape_WoCamKvs.png"",
    ""camera_shape_WoCamKvs5mp"": ""camera_shape_WoCamKvs5mp.png"",
    ""camera_shape_W1156000"": ""camera_shape_W1156000.png"",
    ""camera_shape_WoOSC2"": ""camera_shape_WoOSC2.png"",
    ""camera_shape_WoPanTiltCam"": ""camera_shape_WoPanTiltCam.png"",
    ""camera_shape_WoPanTiltCam3MP"": ""camera_shape_WoPanTiltCam3MP.png"",
    ""camera_shape_W1050000"": ""camera_shape_W1050000.png"",
    ""camera_shape_W1050001"": ""camera_shape_W1050001.png"",
    ""camera_shape_W1050002"": ""camera_shape_W1050002.png"",
    ""camera_type_default"": ""camera_type_default.png"",
    ""camera_type_privacy"": ""camera_type_privacy.png"",
    ""camera_type_doorbell_default"": ""camera_type_doorbell_default.png"",
    ""camera_type_doorbell_privacy"": ""camera_type_doorbell_privacy.png"",
    ""camera_type_aihub_third_party"": ""camera_type_aihub_third_party.png"",
    ""curtain_shape_WoBlindTilt"": ""curtain_shape_WoBlindTilt.png"",
    ""curtain_shape_WoCurtain"": ""curtain_shape_WoCurtain.png"",
    ""curtain_shape_WoCurtain3"": ""curtain_shape_WoCurtain3.png"",
    ""curtain_shape_W1100000"": ""curtain_shape_W1100000.png"",
    ""curtain_shape_WoRollerShade"": ""curtain_shape_WoRollerShade.png"",
    ""curtain_type_bindtilt_default"": ""curtain_type_bindtilt_default.png"",
    ""curtain_type_bindtilt_on"": ""curtain_",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"type_bindtilt_on.png"",
    ""curtain_type_default"": ""curtain_type_version1_default.png"",
    ""curtain_type_group_default"": ""curtain_type_group_version1_default.png"",
    ""curtain_type_group_on"": ""curtain_type_group_version1_on.png"",
    ""curtain_type_on"": ""curtain_type_version1_on.png"",
    ""curtain_type_rollershade_off"": ""curtain_type_rollershade_off.png"",
    ""curtain_type_rollershade_on"": ""curtain_type_rollershade_on.png"",
    ""curtain_type_rollershade_some_on"": ""curtain_type_rollershade_some_on.png"",
    ""unknown_default"": ""unknown_default.png"",
    ""env_shape_WoAirPurifier"": ""env_shape_WoAirPurifier.png"",
    ""env_shape_WoAirPurifierPro"": ""env_shape_WoAirPurifierPro.png"",
    ""env_shape_WoAirPurifierJP"": ""env_shape_WoAirPurifierJP.png"",
    ""env_shape_WoAirPurifierUS"": ""env_shape_WoAirPurifierUS.png"",
    ""env_shape_WoAirPurifierJPPro"": ""env_shape_WoAirPurifierJPPro.png"",
    ""env_shape_WoAirPurifierUSPro"": ""env_shape_WoAirPurifierUSPro.png"",
    ""env_shape_WoFan"": ""env_shape_WoFan.png"",
    ""env_shape_WoFan2"": ""env_shape_WoFan2.png"",
    ""env_shape_W1160000"": ""env_shape_WoFan2.png"",
    ""env_shape_W1116000"": ""env_shape_W1116000.png"",
    ""env_shape_WoHumi"": ""env_shape_WoHumi.png"",
    ""env_shape_WoHumi2"": ""env_shape_WoHumi2.png"",
    ""env_shape_WoHumi2Plus"": ""env_shape_WoHumi2Plus.png"",
    ""env_type_fan_default"": ""env_type_fan_default.png"",
    ""env_type_fan_on"": ""env_type_fan_on.png"",
    ""env_type_humi_defalut"": ""env_type_humi_defalut.png"",
    ""env_type_humi_on"": ""env_type_humi_on.png"",
    ""env_type_humi2_default"": ""env_type_humi2_default.png"",
    ""env_type_humi2_on"": ""env_type_humi2_on.png"",
    ""env_type_purifier_0"": ""env_type_purifier_0.png"",
    ""env_type_purifier_1"": ""env_type_purifier_1.png"",
    ""env_type_purifier_2"": ""env_type_purifier_2.png"",
    ""env_type_purifier_3"": ""env_type_purifier_3.png"",
    ""env_type_purifier_default"": ""env_type_purifier_default.png"",
    ""hub_type_default"": ""hub_type_default.png"",
    ""hub_type_temperature_default"": ",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"""hub_type_temperature_default.png"",
    ""hub_type_humidity_default"": ""hub_type_humidity_default.png"",
    ""hub_type_temperature_alarm"": ""hub_type_temperature_alarm.png"",
    ""hub_type_humidity_alarm"": ""hub_type_humidity_alarm.png"",
    ""hub_type_abs_humidity_default"": ""hub_type_abs_humidity_default.png"",
    ""hub_type_abs_humidity_alarm"": ""hub_type_abs_humidity_alarm.png"",
    ""hub_shape_WoLinkMini"": ""hub_shape_WoLinkMini.png"",
    ""hub_shape_WoLinkPlus"": ""hub_shape_WoLinkPlus.png"",
    ""hub_shape_WoHub2"": ""hub_shape_WoHub2.png"",
    ""hub_shape_WoLinkMatter"": ""hub_shape_WoLinkMatter.png"",
    ""hub_shape_W1096000"": ""hub_shape_W1096000.png"",
    ""hub_shape_W1095000"": ""hub_shape_W1095000.png"",
    ""ir_type_1"": ""ir_type_1.png"",
    ""ir_type_2"": ""ir_type_2.png"",
    ""ir_type_3"": ""ir_type_3.png"",
    ""ir_type_4"": ""ir_type_4.png"",
    ""ir_type_5"": ""ir_type_5.png"",
    ""ir_type_6"": ""ir_type_6.png"",
    ""ir_type_7"": ""ir_type_7.png"",
    ""ir_type_8"": ""ir_type_8.png"",
    ""ir_type_9"": ""ir_type_9.png"",
    ""ir_type_10"": ""ir_type_10.png"",
    ""ir_type_11"": ""ir_type_11.png"",
    ""ir_type_12"": ""ir_type_12.png"",
    ""ir_type_13"": ""ir_type_13.png"",
    ""ir_type_14"": ""ir_type_14.png"",
    ""ir_shape_1"": ""ir_shape_1.png"",
    ""ir_shape_2"": ""ir_shape_2.png"",
    ""ir_shape_3"": ""ir_shape_3.png"",
    ""ir_shape_4"": ""ir_shape_4.png"",
    ""ir_shape_5"": ""ir_shape_5.png"",
    ""ir_shape_6"": ""ir_shape_6.png"",
    ""ir_shape_7"": ""ir_shape_7.png"",
    ""ir_shape_8"": ""ir_shape_8.png"",
    ""ir_shape_9"": ""ir_shape_9.png"",
    ""ir_shape_10"": ""ir_shape_10.png"",
    ""ir_shape_11"": ""ir_shape_11.png"",
    ""ir_shape_12"": ""ir_shape_12.png"",
    ""ir_shape_13"": ""ir_shape_13.png"",
    ""ir_shape_14"": ""ir_shape_14.png"",
    ""light_shape_WoBulb"": ""light_shape_WoBulb.png"",
    ""light_shape_WoCeiling"": ""light_shape_WoCeiling.png"",
    ""light_shape_WoCeilingPro"": ""light_shape_WoCeilingPro.png"",
    ""light_shape_WoStrip"": ""light_shape_WoStrip.png"",
    ""light_type_icon_32pt_ceilinglamp_default"": ""light_type_icon_32pt",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"_ceilinglamp_default.png"",
    ""light_type_icon_32pt_ceilinglamp_highlight"": ""light_type_icon_32pt_ceilinglamp_highlight.png"",
    ""light_type_icon_32pt_desklamp_default"": ""light_type_icon_32pt_desklamp_default.png"",
    ""light_type_icon_32pt_desklamp_highlight"": ""light_type_icon_32pt_desklamp_highlight.png"",
    ""light_type_icon_32pt_floorlamp_default"": ""light_type_icon_32pt_floorlamp_default.png"",
    ""light_type_icon_32pt_floorlamp_highlight"": ""light_type_icon_32pt_floorlamp_highlight.png"",
    ""light_type_icon_32pt_light_default"": ""light_type_icon_32pt_light_default.png"",
    ""light_type_icon_32pt_light_highlight"": ""light_type_icon_32pt_light_highlight.png"",
    ""light_type_icon_32pt_lightstrip_default"": ""light_type_icon_32pt_lightstrip_default.png"",
    ""light_type_icon_32pt_lightstrip_highlight"": ""light_type_icon_32pt_lightstrip_highlight.png"",
    ""light_shape_W1102000"": ""light_shape_W1102000.png"",
    ""light_type_icon_32pt_W1102000_default"": ""light_type_icon_32pt_W1102000_default.png"",
    ""light_type_icon_32pt_W1102000_highlight"": ""light_type_icon_32pt_W1102000_highlight.png"",
    ""light_shape_W1102001"": ""light_shape_W1102001.png"",
    ""light_shape_W1102002"": ""light_shape_W1102002.png"",
    ""light_shape_W1102003"": ""light_shape_W1102003.png"",
    ""light_shape_W1102004"": ""light_shape_W1102004.png"",
    ""light_shape_W1102005"": ""light_shape_W1102005.png"",
    ""light_shape_W1102006"": ""light_shape_W1102006.png"",
    ""light_shape_W1102007"": ""light_shape_W1102007.png"",
    ""light_shape_W1123000"": ""light_shape_W1123000.png"",
    ""lock_shape_WoLock"": ""lock_shape_WoLock.png"",
    ""lock_shape_WoLockPro"": ""lock_shape_WoLockPro.png"",
    ""lock_shape_WoLockLite"": ""lock_shape_WoLockLite.png"",
    ""lock_shape_W1091000"": ""lock_shape_W1091000.png"",
    ""lock_shape_W1114000"": ""lock_shape_WoLockPro.png"",
    ""lock_shape_W1141000"": ""lock_shape_W1141000.png"",
    ""lock_shape_W1141001"": ""lock_shape_W1141001.png"",
    ""lock_type_default"": ""lock_type_default.png"",
    ""lock_type_",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"unlocked"": ""lock_type_unlocked.png"",
    ""remote_shape_WoButton"": ""remote_shape_WoButton.png"",
    ""remote_shape_WoRWS"": ""remote_shape_WoRWS.png"",
    ""remote_type_WoButton"": ""remote_type_WoButton.png"",
    ""remote_type_WoRWS"": ""remote_type_WoRWS.png"",
    ""sensor_shape_WoContact"": ""sensor_shape_WoContact.png"",
    ""sensor_shape_WoIOSensor"": ""sensor_shape_WoIOSensor.png"",
    ""sensor_shape_WoMeter"": ""sensor_shape_WoMeter.png"",
    ""sensor_shape_WoMeterPlus"": ""sensor_shape_WoMeterPlus.png"",
    ""sensor_shape_WoPresence"": ""sensor_shape_WoPresence.png"",
    ""sensor_shape_W1079000"": ""sensor_shape_W1079000.png"",
    ""sensor_shape_W1079001"": ""sensor_shape_W1079001.png"",
    ""sensor_shape_WoWaterDetector"": ""sensor_shape_WoWaterDetector.png"",
    ""sensor_shape_W1111000"": ""sensor_shape_W1111000.png"",
    ""sensor_shape_W1070000"": ""sensor_shape_W1070000.png"",
    ""sensor_type_W1070000_default"": ""sensor_type_W1070000_default.png"",
    ""sensor_type_humidity_alarm"": ""sensor_type_humidity_alarm.png"",
    ""sensor_type_humidity_default"": ""sensor_type_humidity_default.png"",
    ""sensor_type_abs_humidity_alarm"": ""sensor_type_abs_humidity_alarm.png"",
    ""sensor_type_abs_humidity_default"": ""sensor_type_abs_humidity_default.png"",
    ""sensor_type_icon_32pt_contact_default"": ""sensor_type_icon_32pt_contact_default.png"",
    ""sensor_type_icon_32pt_contact_highlight"": ""sensor_type_icon_32pt_contact_highlight.png"",
    ""sensor_type_icon_32pt_doors_default"": ""sensor_type_icon_32pt_doors_default.png"",
    ""sensor_type_icon_32pt_doors_highlight"": ""sensor_type_icon_32pt_doors_highlight.png"",
    ""sensor_type_icon_32pt_motion_default"": ""sensor_type_icon_32pt_motion_version1_default.png"",
    ""sensor_type_icon_32pt_motion_highlight"": ""sensor_type_icon_32pt_motion_version1_highlight.png"",
    ""sensor_type_icon_32pt_windows_default"": ""sensor_type_icon_32pt_windows_default.png"",
    ""sensor_type_icon_32pt_windows_highlight"": ""sensor_type_icon_32pt_windows_highlight.png"",
    ""sensor_type_meter_def",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"ault"": ""sensor_type_meter_default.png"",
    ""sensor_type_temperature_alarm"": ""sensor_type_temperature_alarm.png"",
    ""sensor_type_temperature_default"": ""sensor_type_temperature_default.png"",
    ""sensor_type_waterdetector_default"": ""sensor_type_waterdetector_default.png"",
    ""sensor_type_waterdetector_in_alarm"": ""sensor_type_waterdetector_in_alarm.png"",
    ""sensor_type_waterdetector_in_default"": ""sensor_type_waterdetector_in_default.png"",
    ""sensor_type_waterdetector_out_alarm"": ""sensor_type_waterdetector_out_alarm.png"",
    ""sensor_type_waterdetector_out_default"": ""sensor_type_waterdetector_out_default.png"",
    ""sensor_type_co2_level_good"": ""sensor_type_co2_level_good.png"",
    ""sensor_type_co2_level_mid"": ""sensor_type_co2_level_mid.png"",
    ""sensor_type_co2_level_low"": ""sensor_type_co2_level_low.png"",
    ""sensor_type_meter_pro_default"": ""sensor_type_meter_pro_default.png"",
    ""sensor_type_meter_pro_co2_default"": ""sensor_type_meter_pro_co2_default.png"",
    ""sweeper_shape_W1113000"": ""sweeper_shape_W1113000.png"",
    ""sweeper_shape_tpqXG5pD"": ""sweeper_shape_tpqXG5pD.png"",
    ""sweeper_shape_91AgWZ1n"": ""sweeper_shape_91AgWZ1n.png"",
    ""sweeper_shape_sH5cQeLF"": ""sweeper_shape_WoSweeperMini.png"",
    ""sweeper_shape_WoSweeper"": ""sweeper_shape_WoSweeper.png"",
    ""sweeper_shape_WoSweeperMini"": ""sweeper_shape_WoSweeperMini.png"",
    ""sweeper_shape_WoSweeperMiniPro"": ""sweeper_shape_WoSweeperMiniPro.png"",
    ""sweeper_shape_WoSweeperOrigin"": ""sweeper_shape_WoSweeperOrigin.png"",
    ""sweeper_shape_WoSweeperPlus"": ""sweeper_shape_WoSweeperPlus.png"",
    ""sweeper_type_default"": ""sweeper_type_default.png"",
    ""sweeper_type_on"": ""sweeper_type_on.png"",
    ""sweeper_type_platform_no_comb_offline"": ""sweeper_type_platform_no_comb_offline.png"",
    ""sweeper_type_platform_no_comb_online"": ""sweeper_type_platform_no_comb_online.png"",
    ""sweeper_type_platform_comb_offline"": ""sweeper_type_platform_comb_offline.png"",
    ""sweeper_type_platform_comb_online"": ""sweeper_type_pla",
1775791059277,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"tform_comb_online.png"",
    ""sweeper_shape_W1106000"": ""sweeper_shape_W1106000.png"",
    ""sweeper_shape_W1107000"": ""sweeper_shape_W1107000.png"",
    ""switch_type_icon_32pt_socket_highlight"": ""switch_type_icon_32pt_socket_highlight.png"",
    ""switch_type_icon_32pt_socket_default"": ""switch_type_icon_32pt_socket_default.png"",
    ""switch_type_icon_32pt_lightstrip_highlight"": ""switch_type_icon_32pt_lightstrip_highlight.png"",
    ""switch_type_icon_32pt_lightstrip_default"": ""switch_type_icon_32pt_lightstrip_default.png"",
    ""switch_type_icon_32pt_light_highlight"": ""switch_type_icon_32pt_light_highlight.png"",
    ""switch_type_icon_32pt_light_default"": ""switch_type_icon_32pt_light_default.png"",
    ""switch_type_icon_32pt_coffeemachine_highlight"": ""switch_type_icon_32pt_coffeemachine_highlight.png"",
    ""switch_type_icon_32pt_coffeemachine_default"": ""switch_type_icon_32pt_coffeemachine_default.png"",
    ""switch_type_icon_32pt_floorlamp_highlight"": ""switch_type_icon_32pt_floorlamp_highlight.png"",
    ""switch_type_icon_32pt_floorlamp_default"": ""switch_type_icon_32pt_floorlamp_default.png"",
    ""switch_type_icon_32pt_desklamp_highlight"": ""switch_type_icon_32pt_desklamp_highlight.png"",
    ""switch_type_icon_32pt_desklamp_default"": ""switch_type_icon_32pt_desklamp_default.png"",
    ""switch_type_icon_32pt_ceilinglamp_highlight"": ""switch_type_icon_32pt_ceilinglamp_highlight.png"",
    ""switch_type_icon_32pt_ceilinglamp_default"": ""switch_type_icon_32pt_ceilinglamp_default.png"",
    ""switch_type_icon_32pt_bathtub_highlight"": ""switch_type_icon_32pt_bathtub_highlight.png"",
    ""switch_type_icon_32pt_bathtub_default"": ""switch_type_icon_32pt_bathtub_default.png"",
    ""switch_type_icon_32pt_switch_highlight"": ""switch_type_icon_32pt_switch_highlight.png"",
    ""switch_type_icon_32pt_switch_default"": ""switch_type_icon_32pt_switch_default.png"",
    ""switch_type_icon_32pt_television_highlight"": ""switch_type_icon_32pt_television_highlight.png"",
    ""switch_type_icon_32pt_television_default"": """,
1775791059278,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"switch_type_icon_32pt_television_default.png"",
    ""switch_type_icon_32pt_boiler_highlight"": ""switch_type_icon_32pt_boiler_highlight.png"",
    ""switch_type_icon_32pt_boiler_default"": ""switch_type_icon_32pt_boiler_default.png"",
    ""switch_type_icon_32pt_heater_highlight"": ""switch_type_icon_32pt_heater_highlight.png"",
    ""switch_type_icon_32pt_heater_default"": ""switch_type_icon_32pt_heater_default.png"",
    ""switch_type_icon_32pt_cooler_highlight"": ""switch_type_icon_32pt_cooler_highlight.png"",
    ""switch_type_icon_32pt_cooler_default"": ""switch_type_icon_32pt_cooler_default.png"",
    ""switch_type_icon_32pt_washer_highlight"": ""switch_type_icon_32pt_washer_highlight.png"",
    ""switch_type_icon_32pt_washer_default"": ""switch_type_icon_32pt_washer_default.png"",
    ""switch_type_icon_32pt_fridge_highlight"": ""switch_type_icon_32pt_fridge_highlight.png"",
    ""switch_type_icon_32pt_fridge_default"": ""switch_type_icon_32pt_fridge_default.png"",
    ""switch_type_icon_32pt_cookware_highlight"": ""switch_type_icon_32pt_cookware_highlight.png"",
    ""switch_type_icon_32pt_cookware_default"": ""switch_type_icon_32pt_cookware_default.png"",
    ""switch_type_icon_32pt_pool_highlight"": ""switch_type_icon_32pt_pool_highlight.png"",
    ""switch_type_icon_32pt_pool_default"": ""switch_type_icon_32pt_pool_default.png"",
    ""switch_type_icon_32pt_ventilator_highlight"": ""switch_type_icon_32pt_ventilator_highlight.png"",
    ""switch_type_icon_32pt_ventilator_default"": ""switch_type_icon_32pt_ventilator_default.png"",
    ""switch_type_icon_2pm_all_off"": ""switch_type_icon_2pm_all_off.png"",
    ""switch_type_icon_2pm_all_on"": ""switch_type_icon_2pm_all_on.png"",
    ""switch_type_icon_2pm_on1"": ""switch_type_icon_2pm_on1.png"",
    ""switch_type_icon_2pm_on2"": ""switch_type_icon_2pm_on2.png"",
    ""switch_type_icon_2pm_rollershade_off"": ""switch_type_icon_2pm_rollershade_off.png"",
    ""switch_type_icon_2pm_rollershade_on"": ""switch_type_icon_2pm_rollershade_on.png"",
    ""switch_type_icon_2pm_rollershade_some_on"": ""s",
1775791059278,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"witch_type_icon_2pm_rollershade_some_on.png"",
    ""switch_type_icon_gdo_opened"": ""switch_type_icon_gdo_version1_opened.png"",
    ""switch_type_icon_gdo_closed"": ""switch_type_icon_gdo_version1_closed.png"",
    ""switch_shape_W1083000"": ""switch_shape_W1083000.png"",
    ""switch_shape_W1083001"": ""switch_shape_W1083001.png"",
    ""switch_shape_W1083002"": ""switch_shape_W1083002.png"",
    ""switch_shape_W1083003"": ""switch_shape_W1083003.png"",
    ""switch_shape_W1104000"": ""switch_shape_W1104000.png"",
    ""switch_shape_WoPlugUS"": ""switch_shape_WoPlugUS.png"",
    ""switch_shape_WoHand"": ""switch_shape_WoHand.png"",
    ""switch_shape_WoPlug"": ""switch_shape_WoPlug.png"",
    ""switch_shape_WoPlugJP"": ""switch_shape_WoPlugJP.png"",
    ""tag_shape_default"": ""tag_shape_default.png"",
    ""key_shape_WoFinderCard"": ""key_shape_WoFinderCard.png"",
    ""key_shape_WoKeypad"": ""key_shape_WoKeypad.png"",
    ""key_shape_WoKeypadTouch"": ""key_shape_WoKeypadTouch.png"",
    ""key_shape_W1115000"": ""key_shape_W1115000.png"",
    ""key_shape_W1135000"": ""key_shape_W1135000.png"",
    ""key_shape_W1110000"": ""key_shape_W1110000.png"",
    ""key_type_icon_32pt_fc_briefcase_lose"": ""key_type_icon_32pt_fc_briefcase.png"",
    ""key_type_icon_32pt_fc_briefcase"": ""key_type_icon_32pt_fc_briefcase.png"",
    ""key_type_icon_32pt_fc_cat_lose"": ""key_type_icon_32pt_fc_cat.png"",
    ""key_type_icon_32pt_fc_cat"": ""key_type_icon_32pt_fc_cat.png"",
    ""key_type_icon_32pt_fc_child_lose"": ""key_type_icon_32pt_fc_child.png"",
    ""key_type_icon_32pt_fc_child"": ""key_type_icon_32pt_fc_child.png"",
    ""key_type_icon_32pt_fc_default_lose"": ""key_type_icon_32pt_fc_default.png"",
    ""key_type_icon_32pt_fc_default"": ""key_type_icon_32pt_fc_default.png"",
    ""key_type_icon_32pt_fc_dog_lose"": ""key_type_icon_32pt_fc_dog.png"",
    ""key_type_icon_32pt_fc_dog"": ""key_type_icon_32pt_fc_dog.png"",
    ""key_type_icon_32pt_fc_elder_lose"": ""key_type_icon_32pt_fc_elder.png"",
    ""key_type_icon_32pt_fc_elder"": ""key_type_icon_32pt_fc_elder.png"",
    ""key_type_icon_32",
1775791059278,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"pt_fc_handbag_lose"": ""key_type_icon_32pt_fc_handbag.png"",
    ""key_type_icon_32pt_fc_handbag"": ""key_type_icon_32pt_fc_handbag.png"",
    ""key_type_icon_32pt_fc_headset_lose"": ""key_type_icon_32pt_fc_headset.png"",
    ""key_type_icon_32pt_fc_headset"": ""key_type_icon_32pt_fc_headset.png"",
    ""key_type_icon_32pt_fc_key_lose"": ""key_type_icon_32pt_fc_key.png"",
    ""key_type_icon_32pt_fc_key"": ""key_type_icon_32pt_fc_key.png"",
    ""key_type_icon_32pt_fc_leave_home"": ""key_type_icon_32pt_fc_leave_home.png"",
    ""key_type_icon_32pt_fc_phone_lose"": ""key_type_icon_32pt_fc_phone.png"",
    ""key_type_icon_32pt_fc_phone"": ""key_type_icon_32pt_fc_phone.png"",
    ""key_type_icon_32pt_fc_trunk_lose"": ""key_type_icon_32pt_fc_trunk.png"",
    ""key_type_icon_32pt_fc_trunk"": ""key_type_icon_32pt_fc_trunk.png"",
    ""key_type_icon_32pt_fc_wallet_lose"": ""key_type_icon_32pt_fc_wallet.png"",
    ""key_type_icon_32pt_fc_wallet"": ""key_type_icon_32pt_fc_wallet.png"",
    ""key_type_keypad_default"": ""key_type_keypad_default.png"",
    ""doorbellIndoor_type_default"": ""doorbellIndoor_type_default.png"",
    ""doorbellOutdoor_type_default"": ""doorbellOutdoor_type_default.png"",
    ""key_type_icon_32pt_safety_alarm_default"": ""key_type_icon_32pt_safety_alarm_default.png"",
    ""key_type_icon_32pt_safety_alarm_leave_home"": ""key_type_icon_32pt_safety_alarm_leave_home.png"",
    ""sensor_shape_W1101000"": ""sensor_shape_W1101000.png"",
    ""aiPet_shape_W1121000"": ""aiPet_shape_W1121000.png"",
    ""aiPet_type_default"": ""aiPet_type_default.png"",
    ""aiPet_type_happy"": ""aiPet_type_happy.png"",
    ""aiPet_type_sleep"": ""aiPet_type_sleep.png"",
    ""auto_shape_W1128000"": ""auto_shape_W1128000.png"",
    ""auto_type_W1128000_default"": ""auto_shape_W1128000.png"",
    ""auto_type_W1128000_on"": ""auto_type_W1128000_on.png"",
    ""env_type_W1130000_default"": ""env_type_W1130000_default.png"",
    ""env_shape_W1130000"": ""env_shape_W1130000.png"",
    ""aiPinNote_type_default"": ""aiPinNote_type_default.png"",
    ""env_shape_W1071000"": ""env_shape_W1071000",
1775791059278,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,".png"",
    ""aiPinNote_shape_W1145000"": ""aiPinNote_type_default.png"",
    ""env_type_W1071000_default"": ""env_type_W1071000_default.png"",
    ""env_type_W1071000_all_on"": ""env_type_W1071000_all_on.png"",
    ""env_type_W1071000_fan_on"": ""env_type_W1071000_fan_on.png"",
    ""env_type_W1071000_light_on"": ""env_type_W1071000_light_on.png"",
    ""camera_shape_W1099001"": ""camera_shape_W1099001.png"",
    ""camera_shape_W1099000"": ""camera_shape_W1099000.png"",
    ""light_shape_W1162000"": ""light_shape_WoCeilingPro.png"",
    ""camera_type_indoor_default"": ""camera_type_indoor_default.png""
}

<-- END HTTP (20062-byte body)",
1775791059287,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/groupshare/api/v2/group (6315ms)
content-type: application/json
content-length: 486
date: Fri, 10 Apr 2026 03:17:34 GMT
switchbot-request-id: f1c665b3-eb79-4dba-8d28-544de5df86a9
{""resultCode"":100,""message"":""success"",""data"":[{""userID"":""9773828c-90bb-4725-a04c-339e0eec300e"",""groupID"":""G01-1756371013431-28ad"",""userName"":""jk363776610@163.com"",""nickName"":"""",""groupNickName"":"""",""groupName"":""default"",""tyHomeID"":262440005,""isMaster"":true,""ownerUserID"":""9773828c-90bb-4725-a04c-339e0eec300e"",""ownerUserName"":"""",""timezoneID"":"""",""role"":""admin"",""createdTime"":1756371014947,""updatedTime"":1756371014947,""deviceShareType"":""all"",""roomCount"":0,""deviceCount"":3,""memberCount"":1}]}
<-- END HTTP (486-byte body)",
1775791059316,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://www.wohand.com/version/wocaotech/release.json (7171ms)
content-type: application/json
last-modified: Thu, 24 Apr 2025 10:07:31 GMT
server: AmazonS3
x-amz-server-side-encryption: AES256
x-amz-version-id: SV8LF8aDjjvF76vMT7LKfHTGKT3SDGBH
date: Fri, 10 Apr 2026 02:26:00 GMT
etag: W/""5e468f65d12055ade74ec5f2684fbb6c""
vary: Accept-Encoding
x-cache: Hit from cloudfront
via: 1.1 f36f624a55d1f8e293ed0f1adac5e8b0.cloudfront.net (CloudFront)
x-amz-cf-pop: SFO53-P10
x-amz-cf-id: 9_RPvqwnCB2EdnjRRHQ1NhgoRlQfk8E_SgfPcq03Jh8MSow5DEAVbg==
age: 3094
{
    ""name"": ""Wohand"",
    ""note"": ""Android version would be upgraded to V2.7"",
    ""release_code"": 10,
    ""url"": ""https://www.wohand.com/"",
    ""apk_url"": ""https://www.wohand.com/version/wocaotech/android/Wohand_V23.apk"",
    ""wohand_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoHand/WoHand_app_V42.zip"",
    ""wobutton_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoButton/WoButton_beacon_app_V26.zip"",
    ""wolink_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoLink/WoLink_app_V40.zip"",
    ""wolink_esp_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoLink/aws_iot_V08.bin"",
    ""wolinkplus_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoLinkPlus/WoLinkPlus_app_V20.zip"",
    ""wolinkplus_esp_url"": ""version/wocaotech/firmware/WoLinkPlus/aws_iot_V10.bin"",
    ""remote_db_url"": ""https://www.wohand.com/version/wocaotech/remotedb/IRLibaray_V2.zip"",
    ""apkcode"": 23,
    ""wohandcode"": 42,
    ""wobuttoncode"": 26,
    ""wolinkcode"": 30,
    ""wolinkespcode"": 8,
    ""wolinkpluscode"": 10,
    ""wolinkplusespcode"": 10,
    ""woplug_code"": 15,
    ""remote_db"": 2,
    ""wohand_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoHand/WoHand_app_V"",
    ""wohand_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoHand/WoHand_rtl_app_V"",
    ""wohand_freq_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoHand/WoHand_freq_app_V"",
   ",
1775791059316,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回," ""wolink_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoLink/WoLink_app_V"",
    ""wolinkplus_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoLinkPlus/WoLinkPlus_app_V"",
    ""wolinkmini_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoLinkMini/WoLinkMini_app_V"",
    ""wolinkmini_52833_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoLinkMini/WoLinkMini_52833_app_V"",
    ""wofan_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoFan/WoFan_app_V"",
    ""wometer_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoMeter/WoMeter_app_V"",
    ""wometer_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoMeter/WoMeter_rtl_app_V"",
    ""wometer_freq_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoMeter/WoMeter_freq_app_V"",
    ""wocurtain_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoCurtain/WoCurtain_app_V"",
    ""wocurtain_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoCurtain/WoCurtain_rtl_app_V"",
    ""wocontact_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoContact/WoContact_app_V"",
    ""wopresence_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoPresence/WoPresence_app_V"",
    ""wobutton_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoButton/WoButton_app_V"",
    ""wobutton_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoButton/WoButton_app_V"",
    ""wobutton_rtl_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoButton/WoButton_rtl_app_V"",
    ""wobutton_ble_rtl_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoButton/WoButton_rtl_app_V"",
    ""wobutton_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoButton/WoButton_rtl_app_V"",
    ""wobutton_freq_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoButton/WoButton_freq_app_V"",
    ""wometerplus_rtl_ble_ba",
1775791059316,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"se_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoMeterPlus/WoMeterPlus_rtl_app_V"",
    ""wometerplus_freq_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoMeterPlus/WoMeterPlus_freq_app_V"",
    ""woiosensor_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoIOSensor/WoIOSensor_rtl_app_V"",
    ""wolock_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoLock/WoLock_app_V"",
    ""wolock_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoLock/WoLock_rtl_app_V"",
    ""wolockpro_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoLockPro/WoLockPro_rtl_app_V"",
    ""wokeypad_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoKeypad/WoKeypad_app_V"",
    ""wokeypad_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoKeypad/WoKeypad_rtl_app_V"",
    ""woceiling_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoCeiling/WoCeiling_app_V"",
    ""woceilingpro_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoCeilingPro/WoCeilingPro_app_V"",
    ""wobatterycam_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoBatteryCam/WoBatteryCam_rtl_app_V"",
    ""woosc2_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoOSC2/WoOSC2_rtl_app_V"",
    ""woblindtilt_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoBlindTilt/WoBlindTilt_rtl_app_V"",
    ""wohub2_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoHub2/WoHub2_app_V"",
    ""wolinkmatter_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoLinkMatter/WoLinkMatter_app_V"",
    ""wosweepermini_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoSweeperMini/WoSweeperMini_rtl_app_V"",
    ""wosweeperminibarrel_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoSweeperMiniBarrel/WoSweeperMiniBarrel_rtl_app_V"",
    ""wocurtain3_rtl_ble_base_url""",
1775791059316,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,": ""https://www.wohand.com/version/wocaotech/firmware/WoCurtain3/WoCurtain3_rtl_app_V"",
    ""wofan2_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoFan2/WoFan2_app_V"",
    ""wofan2_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoFan2/WoFan2_rtl_app_V"",
    ""worws_freq_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoRWS/WoRWS_freq_app_V"",
    ""wopresence_freq_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoPresence/WoPresence_freq_app_V"",
    ""wocontact_freq_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoContact/WoContact_freq_app_V"",
    ""wofindercard_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoFinderCard/WoFinderCard_rtl_app_V"",
    ""worollershade_rtl_ble_base_url"": ""https://www.wohand.com/version/wocaotech/firmware/WoRollerShade/WoRollerShade_rtl_app_V"",
    ""wohand_v1"": [
        {
            ""ble"": 65,
            ""wifi"": 0
        },
        {
            ""ble"": 66,
            ""wifi"": 0
        }
    ],
    ""wohand_rtl_v1"": [
        {
            ""ble"": 65,
            ""wifi"": 0
        },
        {
            ""ble"": 66,
            ""wifi"": 0
        }
    ],
    ""wohand_freq_v1"": [
        {
            ""ble"": 65,
            ""wifi"": 0
        },
        {
            ""ble"": 66,
            ""wifi"": 0
        }
    ],
    ""wolink_v1"": [
        {
            ""ble"": 44,
            ""wifi"": 23
        }
    ],
    ""wolinkplus_v1"": [
        {
            ""ble"": 24,
            ""wifi"": 23
        }
    ],
    ""wolinkmini_v1"": [
        {
            ""ble"": 31,
            ""wifi"": 23
        },
        {
            ""ble"": 36,
            ""wifi"": 23
        },
        {
            ""ble"": 37,
            ""wifi"": 23
        },
        {
            ""ble"": 39,
            ""wifi"": 26
        },
        {
            ""ble"": 53,
            ""wifi"": 38
        },
        {
            ""ble"": 54,
            ""wifi"": 38
        }
    ],
    ",
1775791059325,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"""wolinkmini_52833_v1"": [
        {
            ""ble"": 39,
            ""wifi"": 26
        },
        {
            ""ble"": 52,
            ""wifi"": 33
        },
        {
            ""ble"": 53,
            ""wifi"": 38
        },
        {
            ""ble"": 54,
            ""wifi"": 38
        }
    ],
    ""wohumi_v1"": [],
    ""wometer_v1"": [
        {
            ""ble"": 29,
            ""wifi"": 0
        },
        {
            ""ble"": 30,
            ""wifi"": 0
        }
    ],
    ""wometer_rtl_v1"": [
        {
            ""ble"": 29,
            ""wifi"": 0
        },
        {
            ""ble"": 30,
            ""wifi"": 0
        }
    ],
    ""wometer_freq_v1"": [
        {
            ""ble"": 29,
            ""wifi"": 0
        },
        {
            ""ble"": 30,
            ""wifi"": 0
        }
    ],
    ""wocurtain_v1"": [
        {
            ""ble"": 46,
            ""wifi"": 0
        },
        {
            ""ble"": 63,
            ""wifi"": 0
        },
        {
            ""ble"": 64,
            ""wifi"": 0
        }
    ],
    ""wocurtain_rtl_v1"": [
        {
            ""ble"": 46,
            ""wifi"": 0
        },
        {
            ""ble"": 63,
            ""wifi"": 0
        },
        {
            ""ble"": 64,
            ""wifi"": 0
        }
    ],
    ""wocontact_v1"": [
        {
            ""ble"": 9,
            ""wifi"": 0
        },
        {
            ""ble"": 11,
            ""wifi"": 0
        }
    ],
    ""wocontact_freq_v1"": [],
    ""wopresence_v1"": [
        {
            ""ble"": 13,
            ""wifi"": 0
        }
    ],
    ""wopresence_freq_v1"": [],
    ""wobutton_v1"": [
        {
            ""ble"": 44,
            ""wifi"": 0
        },
        {
            ""ble"": 45,
            ""wifi"": 0
        },
        {
            ""ble"": 46,
            ""wifi"": 0
        }
    ],
    ""wobutton_rtl_v1"": [
        {
            ""ble"": 44,
            ""wifi"": 0
        },
        {
            ""ble"": 45,
            ""wifi"": 0
        },
        {
            ""ble"": 46,
          ",
1775791059325,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"  ""wifi"": 0
        }
    ],
    ""wobutton_freq_v1"": [
        {
            ""ble"": 46,
            ""wifi"": 0
        }
    ],
    ""wometerplus_rtl_v1"": [
        {
            ""ble"": 6,
            ""wifi"": 0
        },
        {
            ""ble"": 7,
            ""wifi"": 0
        }
    ],
    ""wometerplus_freq_v1"": [
        {
            ""ble"": 6,
            ""wifi"": 0
        },
        {
            ""ble"": 7,
            ""wifi"": 0
        }
    ],
    ""wolock_v1"": [
        {
            ""ble"": 65,
            ""wifi"": 0
        },
        {
            ""ble"": 67,
            ""wifi"": 0
        },
        {
            ""ble"": 68,
            ""wifi"": 0
        }
    ],
    ""wolock_rtl_v1"": [
        {
            ""ble"": 67,
            ""wifi"": 0
        },
        {
            ""ble"": 68,
            ""wifi"": 0
        }
    ],
    ""wolockpro_rtl_v1"": [
        {
            ""ble"": 11,
            ""wifi"": 0
        },
        {
            ""ble"": 15,
            ""wifi"": 0
        },
        {
            ""ble"": 16,
            ""wifi"": 0
        },
        {
            ""ble"": 17,
            ""wifi"": 0
        },
        {
            ""ble"": 18,
            ""wifi"": 0
        }
    ],
    ""wokeypad_v1"": [
        {
            ""ble"": 16,
            ""wifi"": 0
        },
        {
            ""ble"": 17,
            ""wifi"": 0
        },
        {
            ""ble"": 18,
            ""wifi"": 0
        }
    ],
    ""wokeypad_rtl_v1"": [
        {
            ""ble"": 17,
            ""wifi"": 0
        },
        {
            ""ble"": 18,
            ""wifi"": 0
        }
    ],
    ""woceiling_v1"": [
        {
            ""ble"": 30,
            ""wifi"": 10
        },
        {
            ""ble"": 13,
            ""wifi"": 4
        },
        {
            ""ble"": 14,
            ""wifi"": 4
        }
    ],
    ""woceilingpro_v1"": [
        {
            ""ble"": 30,
            ""wifi"": 10
        },
        {
            ""ble"": 13,
            ""wifi"": 4
        },
        {
            ",
1775791059325,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"""ble"": 14,
            ""wifi"": 4
        }
    ],
    ""homekit_plugmini"": {
        ""ble"": 0,
        ""wifi"": 12
    },
    ""homekit_curtain"": {
        ""ble"": 52,
        ""wifi"": 0
    },
    ""homekit_lock"": {
        ""ble"": 60,
        ""wifi"": 0
    },
    ""wobatterycam_rtl_v1"": [
        {
            ""ble"": 10,
            ""wifi"": 0
        },
        {
            ""ble"": 11,
            ""wifi"": 0
        }
    ],
    ""woblindtilt_rtl_v1"": [
        {
            ""ble"": 20,
            ""wifi"": 0
        },
        {
            ""ble"": 21,
            ""wifi"": 0
        },
        {
            ""ble"": 22,
            ""wifi"": 0
        }
    ],
    ""wohub2_v1"": [
        {
            ""ble"": 11,
            ""wifi"": 10
        },
        {
            ""ble"": 15,
            ""wifi"": 10
        },
        {
            ""ble"": 20,
            ""wifi"": 12
        }
    ],
    ""wolinkmatter_v1"": [
        {
            ""ble"": 10,
            ""wifi"": 9
        },
        {
            ""ble"": 20,
            ""wifi"": 12
        }
    ],
    ""woiosensor_rtl_v1"": [
        {
            ""ble"": 3,
            ""wifi"": 0
        },
        {
            ""ble"": 4,
            ""wifi"": 0
        }
    ],
    ""woplug_v1"": [],
    ""wosweepermini_rtl_v1"": [
        {
            ""ble"": 4,
            ""wifi"": 0
        },
        {
            ""ble"": 2,
            ""wifi"": 0
        },
        {
            ""ble"": 3,
            ""wifi"": 0
        }
    ],
    ""wosweeperminibarrel_rtl_v1"": [
        {
            ""ble"": 3,
            ""wifi"": 0
        },
        {
            ""ble"": 4,
            ""wifi"": 0
        }
    ],
    ""wocurtain3_rtl_v1"": [
        {
            ""ble"": 9,
            ""wifi"": 0
        },
        {
            ""ble"": 11,
            ""wifi"": 0
        },
        {
            ""ble"": 7,
            ""wifi"": 0
        }
    ],
    ""worollershade_rtl_v1"": [],
    ""worws_freq_v1"": [
        {
            ""ble"": 9,
            ""wifi"": 0
        },
        {
       ",
1775791059326,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"     ""ble"": 10,
            ""wifi"": 0
        },
        {
            ""ble"": 11,
            ""wifi"": 0
        }
    ],
    ""WoFan2_v1"": [
        {
            ""ble"": 4,
            ""wifi"": 0
        },
        {
            ""ble"": 5,
            ""wifi"": 0
        }
    ],
    ""WoOSC2_v1"": [
        {
            ""ble"": 7,
            ""wifi"": 0
        },
        {
            ""ble"": 8,
            ""wifi"": 0
        }
    ],
    ""wofan_v1"": [],
    ""app_ios"": 22,
    ""app_android"": 22,
    ""force_upgrade"": ""null""
}
<-- END HTTP (13944-byte body)",
1775791059326,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://www.wohand.com/version/wocaotech/app/ForceUpgradeVersionConfig.json (7167ms)
content-type: binary/octet-stream
content-length: 2
last-modified: Mon, 14 Oct 2024 10:10:55 GMT
x-amz-server-side-encryption: AES256
x-amz-version-id: A9GWZ7KpHJ1369tcr31pTLiKPYHSoSEZ
accept-ranges: bytes
server: AmazonS3
date: Fri, 10 Apr 2026 03:05:26 GMT
etag: ""99914b932bd37a50b983c5e7c90ae93b""
vary: Accept-Encoding
x-cache: Hit from cloudfront
via: 1.1 f36f624a55d1f8e293ed0f1adac5e8b0.cloudfront.net (CloudFront)
x-amz-cf-pop: SFO53-P10
x-amz-cf-id: iY-7otAKXvCmQ30_nlBj1hxGX9ZWfqJc8_QRWpQr3DWWkUxUhVss2w==
age: 731
{}
<-- END HTTP (2-byte body)",
1775791059326,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService schedule Reconnect attempt 0 of 20 in 1 seconds.,
1775791059327,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://www.wohand.com/version/wocaotech/app/APPUpgradeTipsConfig.json (7156ms)
content-type: binary/octet-stream
content-length: 4167
last-modified: Tue, 29 Oct 2024 07:05:25 GMT
x-amz-server-side-encryption: AES256
x-amz-version-id: uiWW0UjZoyUx_AudhwfIgp.A7b9qLQR1
accept-ranges: bytes
server: AmazonS3
date: Fri, 10 Apr 2026 02:30:41 GMT
etag: ""a5d67a88ac4a2845f86dcbe472659a8e""
vary: Accept-Encoding
x-cache: Hit from cloudfront
via: 1.1 f36f624a55d1f8e293ed0f1adac5e8b0.cloudfront.net (CloudFront)
x-amz-cf-pop: SFO53-P10
x-amz-cf-id: kRqVe20P6HBrN7ZecvrhJDc20i9_STMh4BX8_SUpnIS8SuUFpXZEjQ==
age: 2813
{""ios"": {""effective"": false, ""level"": 1, ""repeat"": false, ""interval"": 60, ""desc"": {""en"": ""The current app version is outdated, which will affect normal use. Please update to the latest version."", ""cn"": ""\u5f53\u524dApp\u7248\u672c\u8fc7\u4f4e\uff0c\u65e0\u6cd5\u6b63\u5e38\u4f7f\u7528\u3002\u8bf7\u5347\u7ea7\u81f3\u6700\u65b0\u7248\u672c\u4f7f\u7528\u3002"", ""ja"": ""\u73fe\u5728\u306e\u30a2\u30d7\u30ea\u306f\u30d0\u30fc\u30b8\u30e7\u30f3\u304c\u53e4\u3044\u305f\u3081\u3001\u30a2\u30d7\u30ea\u306e\u6b63\u5e38\u306a\u4f7f\u7528\u306b\u5f71\u97ff\u3092\u53ca\u307c\u3059\u53ef\u80fd\u6027\u304c\u3042\u308a\u307e\u3059\u3002\u30b9\u30c8\u30a2\u306b\u3066\u6700\u65b0\u30d0\u30fc\u30b8\u30e7\u30f3\u306b\u30a2\u30c3\u30d7\u30c7\u30fc\u30c8\u3057\u3066\u304b\u3089\u3054\u5229\u7528\u304f\u3060\u3055\u3044\u3002"", ""de"": ""Die aktuelle App-Version ist veraltet und kann die normale Nutzung beeintr\u00e4chtigen. Bitte aktualisieren Sie auf die neueste Version."", ""es"": ""La versi\u00f3n actual de la aplicaci\u00f3n est\u00e1 desactualizada, lo que afectar\u00e1 su uso normal. Por favor, actualice a la \u00faltima versi\u00f3n."", ""fr"": ""La version actuelle de l'application est obsol\u00e8te, ce qui peut affecter l'utilisation normale. Veuillez mettre \u00e0 jour vers la derni\u00e8re version."", ""it"": ""La versione attuale dell'app \u00e8 obsoleta, il che influir\u00e0 sul normal",
1775791059327,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"e utilizzo. Si prega di aggiornare all'ultima versione."", ""ko"": ""\ud604\uc7ac \uc571 \ubc84\uc804\uc774 \uc624\ub798\ub418\uc5b4 \uc815\uc0c1\uc801\uc778 \uc0ac\uc6a9\uc5d0 \uc601\ud5a5\uc744 \uc904 \uc218 \uc788\uc2b5\ub2c8\ub2e4. \ucd5c\uc2e0 \ubc84\uc804\uc73c\ub85c \uc5c5\ub370\uc774\ud2b8\ud574 \uc8fc\uc138\uc694."", ""nl"": ""De huidige app-versie is verouderd, wat de normale werking kan be\u00efnvloeden. Werk alstublieft bij naar de nieuwste versie."", ""zh"": ""\u76ee\u524dApp\u7248\u672c\u904e\u4f4e\uff0c\u7121\u6cd5\u6b63\u5e38\u4f7f\u7528\u3002\u8acb\u5347\u7d1a\u81f3\u6700\u65b0\u7248\u672c\u4f7f\u7528\u3002""}, ""effectAPPVersionList"": [{""start"": ""9.3"", ""end"": ""9.3""}], ""configVersion"": 13}, ""android"": {""effective"": false, ""level"": 1, ""repeat"": false, ""interval"": 60, ""desc"": {""en"": ""The current app version is outdated, which will affect normal use. Please update to the latest version."", ""cn"": ""\u5f53\u524dApp\u7248\u672c\u8fc7\u4f4e\uff0c\u65e0\u6cd5\u6b63\u5e38\u4f7f\u7528\u3002\u8bf7\u5347\u7ea7\u81f3\u6700\u65b0\u7248\u672c\u4f7f\u7528\u3002"", ""ja"": ""\u73fe\u5728\u306e\u30a2\u30d7\u30ea\u306f\u30d0\u30fc\u30b8\u30e7\u30f3\u304c\u53e4\u3044\u305f\u3081\u3001\u30a2\u30d7\u30ea\u306e\u6b63\u5e38\u306a\u4f7f\u7528\u306b\u5f71\u97ff\u3092\u53ca\u307c\u3059\u53ef\u80fd\u6027\u304c\u3042\u308a\u307e\u3059\u3002\u30b9\u30c8\u30a2\u306b\u3066\u6700\u65b0\u30d0\u30fc\u30b8\u30e7\u30f3\u306b\u30a2\u30c3\u30d7\u30c7\u30fc\u30c8\u3057\u3066\u304b\u3089\u3054\u5229\u7528\u304f\u3060\u3055\u3044\u3002"", ""de"": ""Die aktuelle App-Version ist veraltet und kann die normale Nutzung beeintr\u00e4chtigen. Bitte aktualisieren Sie auf die neueste Version."", ""es"": ""La versi\u00f3n actual de la aplicaci\u00f3n est\u00e1 desactualizada, lo que afectar\u00e1 su uso normal. Por favor, actualice a la \u00faltima versi\u00f3n."", ""fr"": ""La version actuelle de l'application est obsol\u00e8te, ce qui peut affecter l'utilisation normale. Veuillez mettre \u00e0 jour vers la derni\u00e8re versio",
1775791059327,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"n."", ""it"": ""La versione attuale dell'app \u00e8 obsoleta, il che influir\u00e0 sul normale utilizzo. Si prega di aggiornare all'ultima versione."", ""ko"": ""\ud604\uc7ac \uc571 \ubc84\uc804\uc774 \uc624\ub798\ub418\uc5b4 \uc815\uc0c1\uc801\uc778 \uc0ac\uc6a9\uc5d0 \uc601\ud5a5\uc744 \uc904 \uc218 \uc788\uc2b5\ub2c8\ub2e4. \ucd5c\uc2e0 \ubc84\uc804\uc73c\ub85c \uc5c5\ub370\uc774\ud2b8\ud574 \uc8fc\uc138\uc694."", ""nl"": ""De huidige app-versie is verouderd, wat de normale werking kan be\u00efnvloeden. Werk alstublieft bij naar de nieuwste versie."", ""zh"": ""\u76ee\u524dApp\u7248\u672c\u904e\u4f4e\uff0c\u7121\u6cd5\u6b63\u5e38\u4f7f\u7528\u3002\u8acb\u5347\u7d1a\u81f3\u6700\u65b0\u7248\u672c\u4f7f\u7528\u3002""}, ""effectAPPVersionList"": [{""start"": ""9.3"", ""end"": ""9.3""}], ""configVersion"": 9}}
<-- END HTTP (4167-byte body)",
1775791059331,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,DeviceUpgradeManager: devicesMap Size: 0,
1775791059334,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"PartitionManager-->regionBean=MqttRegionBean(host=core.broker.iot.us.switchbot.net, openPort=8883)",
1775791059334,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService MQTT正在连接:Connected，跳过,
1775791059336,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,首页网络状态：true,
1775791059336,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"DeviceUpgradeManager: false getAppUpgradeInfo: UpgradeConfig(effective=false, level=1, repeat=false, interval=60, desc=Description(en=The current app version is outdated, which will affect normal use. Please update to the latest version., cn=当前App版本过低，无法正常使用。请升级至最新版本使用。, zh=目前App版本過低，無法正常使用。請升級至最新版本使用。, ja=現在のアプリはバージョンが古いため、アプリの正常な使用に影響を及ぼす可能性があります。ストアにて最新バージョンにアップデートしてからご利用ください。, de=Die aktuelle App-Version ist veraltet und kann die normale Nutzung beeinträchtigen. Bitte aktualisieren Sie auf die neueste Version., es=La versión actual de la aplicación está desactualizada, lo que afectará su uso normal. Por favor, actualice a la última versión., fr=La version actuelle de l'application est obsolète, ce qui peut affecter l'utilisation normale. Veuillez mettre à jour vers la dernière version., it=La versione attuale dell'app è obsoleta, il che influirà sul normale utilizzo. Si prega di aggiornare all'ultima versione., ko=현재 앱 버전이 오래되어 정상적인 사용에 영향을 줄 수 있습니다. 최신 버전으로 업데이트해 주세요., nl=De huidige app-versie is verouderd, wat de normale werking kan beïnvloeden. Werk alstublieft bij naar de nieuwste versie.), targetAPPVersion=null, effectAPPVersionList=[VersionRange(start=9.3, end=9.3)], configVersion=9)",
1775791059348,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,ReactNativeEvent init 160830114,
1775791059352,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService Mqtt-Iot-Reconnecting,
1775791059354,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,启动延迟初始化完成,
1775791059354,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/wonder/device/v3/getdevice,wonderUrl替换
1775791059354,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/wonder/device/v3/getdevice
Content-Type: application/json; charset=UTF-8
Content-Length: 23
{""required_type"":""All""}
--> END POST (23-byte body)",
1775791059357,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,涂鸦不需要登录,TuYaInitializer
1775791059359,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/wonder/zendesk/getDeleteTickets,wonderUrl替换
1775791059360,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,从后台到前台,
1775791059360,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,NetWorkingManager catch message=Canceled,OkHttp
1775791059360,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 408 network error https://wonder.us.api.switchbot.net/wonder/device/v3/getdevice (6ms)
<-- END HTTP (0-byte body)",
1775791059361,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/wonder/zendesk/getDeleteTickets
Content-Type: application/json; charset=UTF-8
Content-Length: 31
{""email"":""jk363776610@163.com""}
--> END POST (31-byte body)",
1775791059363,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"PartitionManager-->regionBean=MqttRegionBean(host=core.broker.iot.us.switchbot.net, openPort=8883)",
1775791059363,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService Mqtt-Iot-ConnectionLost,
1775791059363,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService Mqtt连接发生异常:,
1775791059363,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,======================================,MqttService 连接MQTT
1775791059363,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService Mqtt-Iot-ConnectionLost,
1775791059363,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService Mqtt连接发生异常:,
1775791059363,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService host=core.broker.iot.us.switchbot.net,
1775791059365,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,网络请求发生异常:Canceled,DefaultErrorHandler
1775791059368,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService Mqtt-Iot-Connecting,
1775791059369,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,fetchHomeConfigDataFinish,HomeProFragment
1775791059371,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"isDeviceOnline:bleScan:false,iotOnline:true",WoAiHubDevice:B0E9FE8D8933
1775791059372,com.theswitchbot.switchbot.index.ui.MainActivity,设备电量,mac:B0E9FE8D8933;电量:100,
1775791059373,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,设备Code为：W1156000,识别到未知设备
1775791059378,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> GET https://wonderlabs.us.api.switchbot.net/message/msgcenter/api/v1/msg/hasread
Content-Type: application/json
--> END GET",
1775791059380,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"allDeviceInfo=[{""inRoomFirst"":false,""inRoomLast"":false,""isCheck"":false,""isMaster"":true,""isSingleInRoom"":false,""itemType"":0,""roomName"":""不在任何房间""},{""deviceMac"":""B0E9FE8D8933"",""deviceName"":""姜轲的AI Hub "",""deviceType"":""W1095000"",""inRoomFirst"":false,""inRoomLast"":false,""isCheck"":false,""isMaster"":true,""isSingleInRoom"":false,""itemType"":1,""roomName"":""不在任何房间""},{""deviceMac"":""B0E9FEA3BE12"",""deviceName"":""智能户外云台摄像机 3K 12"",""deviceType"":""W1156000"",""inRoomFirst"":false,""inRoomLast"":false,""isCheck"":false,""isMaster"":true,""isSingleInRoom"":false,""itemType"":1,""roomName"":""不在任何房间""},{""deviceMac"":""B0E9FEA59ED0"",""deviceName"":""Al Art Frame D0"",""deviceType"":""W1130000"",""inRoomFirst"":false,""inRoomLast"":false,""isCheck"":false,""isMaster"":true,""isSingleInRoom"":false,""itemType"":1,""roomName"":""不在任何房间""}]",
1775791059381,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,postAllDeviceStatusMsg from refresh,MqttDeviceStatusManager
1775791059382,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/groupshare/api/v2/device/relation,wonderUrl替换
1775791059382,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/groupshare/api/v2/device/relation
Content-Type: application/json; charset=UTF-8
Content-Length: 51
{""deviceIDs"":[],""groupID"":""G01-1756371013431-28ad""}
--> END POST (51-byte body)",
1775791059385,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"PartitionManager-->regionBean=MqttRegionBean(host=core.broker.iot.us.switchbot.net, openPort=8883)",
1775791059385,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService MQTT正在连接:Connecting，跳过,
1775791059387,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/homepage/v1/group/locale/get,wonderUrl替换
1775791059388,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/homepage/v1/group/locale/get
Content-Type: application/json; charset=UTF-8
Content-Length: 36
{""groupID"":""G01-1756371013431-28ad""}
--> END POST (36-byte body)",
1775791059388,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,cacheEmail=,UserFragment
1775791059392,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/scene/v1/suggest/getList,wonderUrl替换
1775791059392,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/scene/v1/suggest/getList
Content-Type: application/json; charset=UTF-8
Content-Length: 77
{""groupID"":""G01-1756371013431-28ad"",""language"":""cn"",""sceneType"":""automation""}
--> END POST (77-byte body)",
1775791059394,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,setAppLanguage，configuration暗黑模式:false   屏幕宽:400  屏幕高:845  密度:480  字体缩放:1.0,LocaleUtil
1775791059395,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"<=====    CURRENT PAGE, ONRESUME: MainActivity =====>",
1775791059403,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"StandaloneCoroutine was cancelled : kotlinx.coroutines.JobCancellationException: StandaloneCoroutine was cancelled; job=StandaloneCoroutine{Cancelling}@6f433df
",
1775791059403,com.theswitchbot.switchbot.index.ui.MainActivity,异常捕获,"StandaloneCoroutine was cancelled : kotlinx.coroutines.JobCancellationException: StandaloneCoroutine was cancelled; job=StandaloneCoroutine{Cancelling}@6f433df
",
1775791059403,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,回到首页断开所有蓝牙连接...,BleManager
1775791059403,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,HomeProFragment:全屋动态数据发生变化,
1775791059414,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"Rect, itemView的parent: 0.0",
1775791059416,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"Rect, itemView的parent: 0.0",
1775791059423,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,Doorbell状态--isDeviceOnline：true--deviceId：B0E9FE8D8933,
1775791059432,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,Doorbell状态--isDeviceOnline：false--deviceId：B0E9FEA3BE12,
1775791059432,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,设备Code为：W1156000,识别到未知设备
1775791059436,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,Doorbell状态--isDeviceOnline：true--deviceId：B0E9FEA59ED0,
1775791059448,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,是否已登陆 true,
1775791059449,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,收到isShowClimateBg通知，mac=,
1775791059451,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"Rect, itemView的parent: 33.0",
1775791059452,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"Rect, itemView的parent: 33.0",
1775791059453,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,Doorbell状态--isDeviceOnline：true--deviceId：B0E9FE8D8933,
1775791059454,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,Doorbell状态--isDeviceOnline：false--deviceId：B0E9FEA3BE12,
1775791059454,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,设备Code为：W1156000,识别到未知设备
1775791059454,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,Doorbell状态--isDeviceOnline：true--deviceId：B0E9FEA59ED0,
1775791059456,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/groupshare/api/v2/group,wonderUrl替换
1775791059456,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/groupshare/api/v2/group
Content-Type: application/json; charset=UTF-8
Content-Length: 22
{""withCountInfo"":true}
--> END POST (22-byte body)",
1775791060088,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/groupshare/api/v2/device/relation (705ms)
content-type: application/json
content-length: 48
date: Fri, 10 Apr 2026 03:17:40 GMT
switchbot-request-id: e7bff5f7-c0d5-431b-a3cc-26be43f6e439
{""resultCode"":100,""message"":""success"",""data"":[]}
<-- END HTTP (48-byte body)",
1775791060088,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"检查设备是否缺失约束设备结果,[]",
1775791060250,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://publish.api.switchbot.net/publishplatform/api/v1/rn/plugIn/downloadUrl (7319ms)
date: Fri, 10 Apr 2026 03:17:41 GMT
content-type: application/json
content-length: 78
x-amzn-requestid: 14114b6a-08c3-4d43-81ab-03f650e6c91d
access-control-allow-origin: *
x-amz-apigw-id: blXJWHEjoAMEvrw=
x-amzn-trace-id: Root=1-69d86bd5-79afd5ef15b6d0986d32dafc;Parent=0d553c1bb6d60709;Sampled=0;Lineage=2:8d2030ba:0
{""resultCode"":100,""data"":{""downloadUrl"":"""",""rnPluginVersion"":""""},""message"":""""}
<-- END HTTP (78-byte body)",
1775791060251,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonderlabs.us.api.switchbot.net/message/msgcenter/api/v1/msg/hasread (871ms)
content-type: application/json
content-length: 63
date: Fri, 10 Apr 2026 03:17:41 GMT
x-amzn-remapped-date: Fri, 10 Apr 2026 03:17:41 GMT
x-amzn-requestid: 7e5d2dd4-2dd6-44e6-82d7-88a3d7360d29
access-control-allow-origin: *
x-amzn-remapped-content-length: 63
x-amz-apigw-id: blXJWEAMoAMETyQ=
x-cache: Miss from cloudfront
via: 1.1 d52fd2fab09abcfe30af9217f6f15ef8.cloudfront.net (CloudFront)
x-amz-cf-pop: SFO53-P10
x-amz-cf-id: jDf7TdSxX8VkvU4h2-qWdy4Y150cvkPGOGWaiPJR3BLojZij0lseWg==
{""statusCode"":100,""message"":""success"",""body"":{""hasRead"":false}}
<-- END HTTP (63-byte body)",
1775791060252,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,js热更 到这里了,com.theswitchbot.device.hotupdate.HotUpdateManager
1775791060253,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"HotUpdateManager,js热更成功状态=0",
1775791060253,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,lastUserId:9773828c-90bb-4725-a04c-339e0eec300e curUserId:9773828c-90bb-4725-a04c-339e0eec300e,
1775791060257,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,loadPropertyCfg json:AiHub_Propertys.json,PropertyCfgManager
1775791060257,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,loadPropertyCfg json:AiPet_Propertys.json,PropertyCfgManager
1775791060257,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,loadPropertyCfg json:ArtFrame_Propertys.json,PropertyCfgManager
1775791060257,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,loadPropertyCfg json:FanLight_Propertys.json,PropertyCfgManager
1775791060257,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,loadPropertyCfg json:OscKvs_Propertys.json,PropertyCfgManager
1775791060257,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,loadPropertyCfg json:Propertys.json,PropertyCfgManager
1775791060259,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,loadPropertyCfg json:RelaySwitch_Propertys.json,PropertyCfgManager
1775791060259,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,loadPropertyCfg json:Sweeper_Propertys.json,PropertyCfgManager
1775791060259,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,loadPropertyCfg json:TRV_Propertys.json,PropertyCfgManager
1775791060259,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,loadPropertyCfg json:USVisionDeadbolt_Propertys.json,PropertyCfgManager
1775791060260,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"Property with type propertyId=4212 deviceTypes=[W1141000, W1141001]",PropertyCfgManager
1775791060260,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,loadPropertyCfg json:WeatherStation_Propertys.json,PropertyCfgManager
1775791060260,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,loadPropertyCfg json:digitalHome_Propertys.json,PropertyCfgManager
1775791060260,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"Property with type propertyId=835 deviceTypes=[WoFan, WoFan2, WoPlugUS, WoPlugJP, WoPlug, WoBulb, WoStrip, WoFloorLamp, WoStrip3, WoCeiling, WoCeilingPro, W1102003, W1102004, W1102005]",PropertyCfgManager
1775791060260,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"propertyWithType =[835WoFan2, 835WoFloorLamp, 835WoPlugUS, 835WoStrip, 4212W1141001, 835WoStrip3, 835WoBulb, 835WoFan, 4212W1141000, 835W1102003, 835W1102004, 835WoCeiling, 835W1102005, 835WoCeilingPro, 835WoPlug, 835WoPlugJP]",PropertyCfgManager
1775791060287,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,设备Code为：W1156000,识别到未知设备
1775791060337,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/homepage/v1/group/locale/get (949ms)
content-type: application/json
content-length: 106
date: Fri, 10 Apr 2026 03:17:41 GMT
switchbot-request-id: 4fe51e7b-bea2-4710-ad11-1601bedead88
{""resultCode"":100, ""message"":"""", ""data"":{""longitude"":0, ""latitude"":0, ""locationName"":"""", ""timezoneID"":""""}}
<-- END HTTP (106-byte body)",
1775791060338,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/wonder/zendesk/getDeleteTickets (976ms)
content-type: text/plain; charset=utf-8
content-length: 59
date: Fri, 10 Apr 2026 03:17:41 GMT
switchbot-request-id: 1c87504b-4821-40b7-be4d-66eceaf2ad66
{""statusCode"":100,""body"":{""deleteTickets"":[]},""message"":""""}
<-- END HTTP (59-byte body)",
1775791060338,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,wonderUrl替换--newUrl=https://wonder.us.api.switchbot.net/wonder/zendesk/getTicketState,wonderUrl替换
1775791060339,com.theswitchbot.switchbot.index.ui.MainActivity,网络请求,"--> POST https://wonder.us.api.switchbot.net/wonder/zendesk/getTicketState
Content-Type: application/json; charset=UTF-8
Content-Length: 31
{""email"":""jk363776610@163.com""}
--> END POST (31-byte body)",
1775791060348,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"Rect, itemView的parent: 33.0",
1775791060442,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService scheduleReconnect mqttClient.isConnected()=false  connectionState=Disconnected,
1775791060611,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"Rect, itemView的parent2: false",
1775791060617,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService Mqtt-Iot-Connected,
1775791060620,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService 订阅subTopic----------->v1_1/9773828c-90bb-4725-a04c-339e0eec300e/#,
1775791060622,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"MqttService 发布MQTT消息,Topic:$aws/rules/bi_app_notify_all_device_property_arch2/switchlink/9773828c-90bb-4725-a04c-339e0eec300e/notify_all_device_property     payload:{""protocolVersion"":2,""groups"":[""G01-1756371013431-28ad""]}",
1775791060622,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService 订阅subTopic----------->switchlink/9773828c-90bb-4725-a04c-339e0eec300e/#,
1775791060623,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,postAllDeviceStatusMsg from onMqttStatusChanged,MqttDeviceStatusManager
1775791060623,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,"MqttService 发布MQTT消息,Topic:$aws/rules/bi_app_fetch_device_status_arch2/switchlink/9773828c-90bb-4725-a04c-339e0eec300e/app_to_device_status     payload:{""appVersion"":""9.23"",""count"":1,""createTime"":0,""messages"":[{""createTime"":1775791060,""data"":{""requestID"":""d16ff938-9990-4e8c-8c24-129606d63710"",""createTime"":1775791060},""eventType"":""Wo.All.Status"",""id"":""320ebda9-b9ea-410c-be90-41aa63024d4a""}],""platform"":""Android"",""protocolVersion"":2}",
1775791060623,com.theswitchbot.switchbot.index.ui.MainActivity,其他类型,MqttService 已经存在通配符匹配的订阅，不再重复订阅: switchlink/9773828c-90bb-4725-a04c-339e0eec300e/notify_dev_iraction   匹配通配符: switchlink/9773828c-90bb-4725-a04c-339e0eec300e/#,
1775791060783,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/groupshare/api/v2/group (1327ms)
content-type: application/json
content-length: 486
date: Fri, 10 Apr 2026 03:17:41 GMT
switchbot-request-id: 8720530f-20bd-447e-847c-4d21a4f231af
{""resultCode"":100,""message"":""success"",""data"":[{""userID"":""9773828c-90bb-4725-a04c-339e0eec300e"",""groupID"":""G01-1756371013431-28ad"",""userName"":""jk363776610@163.com"",""nickName"":"""",""groupNickName"":"""",""groupName"":""default"",""tyHomeID"":262440005,""isMaster"":true,""ownerUserID"":""9773828c-90bb-4725-a04c-339e0eec300e"",""ownerUserName"":"""",""timezoneID"":"""",""role"":""admin"",""createdTime"":1756371014947,""updatedTime"":1756371014947,""deviceShareType"":""all"",""roomCount"":0,""deviceCount"":3,""memberCount"":1}]}
<-- END HTTP (486-byte body)",
1775791060784,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"
<-- 200 https://wonder.us.api.switchbot.net/scene/v1/suggest/getList (945ms)
content-type: application/json
date: Fri, 10 Apr 2026 03:17:41 GMT
switchbot-request-id: 6b8c148c-d14a-4fb6-9149-7b42db635d08
{""resultCode"":100, ""message"":"""", ""data"":{""suggest"":[{""title"":""智能降温"", ""subTitle"":""维持适宜的室内温度"", ""description"":""让您在炎热的夏天也能保持舒适！只要室内温度超过28°C，空调就会自动开启，首先以较低温度运行10分钟让室内立即降温，之后再以适宜温度运行，为您营造凉爽的家居环境。"", ""suggestID"":""intelligent_cooling"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E6%99%BA%E8%83%BD%E9%99%8D%E6%B8%A9.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""室外温湿度计"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_iometer.png"", ""deviceType"":""WoIOSensor""}, {""deviceName"":""温湿度计"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_meter.png"", ""deviceType"":""WoMeter""}, {""deviceName"":""智能大屏温湿度计"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_meterplus.png"", ""deviceType"":""WoMeterPlus""}, {""deviceName"":""万能遥控器2"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_hub2.png"", ""deviceType"":""WoHub2""}, {""deviceName"":""温湿度计Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_meterpro.png"", ""deviceType"":""W1079000""}, {""deviceName"":""万能网关3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_hub3.png"", ""deviceType"":""W1096000""}, {""deviceName"":""天气站"", ""deviceIcon"":""https://s3.amazonaws.com/www.wohand.com/version/wocaotech/feedback_img/weatherstation.png"", ""deviceType"":""W1070000""}, {""deviceName"":""空调"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E9%81%A5%E6%8E%A7%E5%99%A8_%E7%A9%BA%E8%B0%83.png"", ""deviceType"":""remote_1""}, {""deviceName"":""循环扇"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_fan2_defalut.png"", ""deviceType"":""WoFan2""}, {""deviceName"":""落地循环扇"", ""deviceIcon"":""",
1775791060784,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_fan3_dark.png"", ""deviceType"":""W1116000""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E6%99%BA%E8%83%BD%E9%99%8D%E6%B8%A9%403x.png"", ""backColor"":""#68D4D4""}, {""title"":""回家"", ""subTitle"":""自动开灯，温馨回家"", ""description"":""当您回到家时，空调开启到设定的模式和温度，灯光开启并播放音乐欢迎您回家。"", ""suggestID"":""go_home"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E5%9B%9E%E5%AE%B6.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""门窗传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_contactsensor.png"", ""deviceType"":""WoContact""}, {""deviceName"":""智能追踪卡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_findmy_offline.png"", ""deviceType"":""WoFinderCard""}, {""deviceName"":""空调"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E9%81%A5%E6%8E%A7%E5%99%A8_%E7%A9%BA%E8%B0%83.png"", ""deviceType"":""remote_1""}, {""deviceName"":""灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E7%81%AF.png"", ""deviceType"":""remote_14""}, {""deviceName"":""室外摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_osc.png"", ""deviceType"":""WoBatteryCam""}, {""deviceName"":""智能云台摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam""}, {""deviceName"":""智能云台摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam3MP""}, {""deviceName"":""智能摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ipc.png"", ""deviceType"":""WoCamera""}, {""deviceName"":""室外摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoOSC2""}, {""deviceName"":""智能云台摄像机 Plus 2K"", ""deviceIcon"":""https://prod-switchb",
1775791060784,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"ot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs""}, {""deviceName"":""智能云台摄像机 Plus 3K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs5mp""}, {""deviceName"":""吸顶灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglight.png"", ""deviceType"":""WoCeiling""}, {""deviceName"":""吸顶灯 Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglightpro.png"", ""deviceType"":""WoCeilingPro""}, {""deviceName"":""彩色灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""WoStrip""}, {""deviceName"":""彩色灯泡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bulb.png"", ""deviceType"":""WoBulb""}, {""deviceName"":""智能开关"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bot.png"", ""deviceType"":""WoHand""}, {""deviceName"":""落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102000""}, {""deviceName"":""灯带3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102001""}, {""deviceName"":""炫彩灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102003""}, {""deviceName"":""炫彩落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102004""}, {""deviceName"":""炫彩钢丝霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102005""}, {""deviceName"":""炫彩霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102006""}, {""deviceName"":""融蜡灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_candle_lamp.png"", ""deviceType"":""W1123000",
1775791060784,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"""}, {""deviceName"":""散热器恒温阀"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_radiator_valve_open.png"", ""deviceType"":""W1128000""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E5%9B%9E%E5%AE%B6%403x.png"", ""backColor"":""#FFD56A""}, {""title"":""离家"", ""subTitle"":""智能安防，无忧离家"", ""description"":""当您出门离家时，自动关闭所有灯光、电源插座和空调，并开启摄像头监控家中动态，确保您的家庭安全且节能。"", ""suggestID"":""leave_home"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E7%A6%BB%E5%AE%B6.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""门窗传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_contactsensor.png"", ""deviceType"":""WoContact""}, {""deviceName"":""智能追踪卡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_findmy_offline.png"", ""deviceType"":""WoFinderCard""}, {""deviceName"":""空调"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E9%81%A5%E6%8E%A7%E5%99%A8_%E7%A9%BA%E8%B0%83.png"", ""deviceType"":""remote_1""}, {""deviceName"":""灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E7%81%AF.png"", ""deviceType"":""remote_14""}, {""deviceName"":""室外摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_osc.png"", ""deviceType"":""WoBatteryCam""}, {""deviceName"":""智能云台摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam""}, {""deviceName"":""智能云台摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam3MP""}, {""deviceName"":""智能摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ipc.png"", ""deviceType"":""WoCamera""}, {""deviceName"":""室外摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoOSC2""}, {""deviceName"":""智",
1775791060784,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"能云台摄像机 Plus 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs""}, {""deviceName"":""智能云台摄像机 Plus 3K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs5mp""}, {""deviceName"":""吸顶灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglight.png"", ""deviceType"":""WoCeiling""}, {""deviceName"":""吸顶灯 Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglightpro.png"", ""deviceType"":""WoCeilingPro""}, {""deviceName"":""彩色灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""WoStrip""}, {""deviceName"":""彩色灯泡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bulb.png"", ""deviceType"":""WoBulb""}, {""deviceName"":""智能开关"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bot.png"", ""deviceType"":""WoHand""}, {""deviceName"":""落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102000""}, {""deviceName"":""灯带3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102001""}, {""deviceName"":""炫彩灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102003""}, {""deviceName"":""炫彩落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102004""}, {""deviceName"":""炫彩钢丝霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102005""}, {""deviceName"":""炫彩霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102006""}, {""deviceName"":""融蜡灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon",
1775791060784,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"/icon_32pt_candle_lamp.png"", ""deviceType"":""W1123000""}, {""deviceName"":""散热器恒温阀"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_radiator_valve_close.png"", ""deviceType"":""W1128000""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E7%A6%BB%E5%AE%B6%403x.png"", ""backColor"":""#5797F8""}, {""title"":""起床"", ""subTitle"":""模拟自然光亮，助您轻松起床"", ""description"":""在设定的早起时间，窗帘自动开启，灯光逐渐变亮，帮助你轻松起床。"", ""suggestID"":""get_up"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E8%B5%B7%E5%BA%8A.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""窗帘机器人"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_curtain.png"", ""deviceType"":""WoCurtain""}, {""deviceName"":""智能窗帘3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_curtain.png"", ""deviceType"":""WoCurtain3""}, {""deviceName"":""百叶帘调光器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_blindtilt.png"", ""deviceType"":""WoBlindTilt""}, {""deviceName"":""吸顶灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglight.png"", ""deviceType"":""WoCeiling""}, {""deviceName"":""吸顶灯 Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglightpro.png"", ""deviceType"":""WoCeilingPro""}, {""deviceName"":""融蜡灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_candle_lamp.png"", ""deviceType"":""W1123000""}, {""deviceName"":""彩色灯泡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bulb.png"", ""deviceType"":""WoBulb""}, {""deviceName"":""落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102000""}, {""deviceName"":""灯带3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102001""}, {""deviceName"":""炫彩灯带"", ""deviceIcon"":""https://p",
1775791060784,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"rod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102003""}, {""deviceName"":""炫彩落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102004""}, {""deviceName"":""炫彩钢丝霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102005""}, {""deviceName"":""炫彩霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102006""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E8%B5%B7%E5%BA%8A%403x.png"", ""backColor"":""#FFD362""}, {""title"":""睡眠"", ""subTitle"":""关灯拉帘，营造舒适入睡环境"", ""description"":""在设定的睡觉时间，自动关闭家中灯光，窗帘静音关闭，帮助您入睡。"", ""suggestID"":""to_sleep"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E7%9D%A1%E7%9C%A0.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""窗帘机器人"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_curtain.png"", ""deviceType"":""WoCurtain""}, {""deviceName"":""百叶帘调光器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_blindtilt.png"", ""deviceType"":""WoBlindTilt""}, {""deviceName"":""吸顶灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglight.png"", ""deviceType"":""WoCeiling""}, {""deviceName"":""吸顶灯 Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglightpro.png"", ""deviceType"":""WoCeilingPro""}, {""deviceName"":""融蜡灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_candle_lamp.png"", ""deviceType"":""W1123000""}, {""deviceName"":""彩色灯泡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bulb.png"", ""deviceType"":""WoBulb""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E7%9D%A1%E7%9C%A0%403x.png"", ""backColor"":""#2648",
1775791060784,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"76""}, {""title"":""自动清洁"", ""subTitle"":""定时打扫，维持干净的家居环境"", ""description"":""当您不在家时，扫地机在设定的时间自动开始打扫，为您维持干净的家居环境。"", ""suggestID"":""automatic_cleaning"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E8%87%AA%E5%8A%A8%E6%B8%85%E6%B4%81.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""智能扫地机器人S1"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_s1.png"", ""deviceType"":""WoSweeper""}, {""deviceName"":""扫地机器人K10+"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_k10%2B.png"", ""deviceType"":""WoSweeperMini""}, {""deviceName"":""智能扫地机器人S1 Plus"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_s1plus.png"", ""deviceType"":""WoSweeperPlus""}, {""deviceName"":""地面清洁机器人S10"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_sweeper_s1_defalut.png"", ""deviceType"":""WoSweeperOrigin""}, {""deviceName"":""扫地机器人K10+ Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_k10%2B.png"", ""deviceType"":""WoSweeperMiniPro""}, {""deviceName"":""智能扫地机器人组合K10+ Pro Combo"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_k10%2B.png"", ""deviceType"":""91AgWZ1n""}, {""deviceName"":""地面清洁机器人S20"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_k10%2B.png"", ""deviceType"":""W1106000""}, {""deviceName"":""扫地机器人K11+"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_k10%2B.png"", ""deviceType"":""W1113000""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E8%87%AA%E5%8A%A8%E6%B8%85%E6%B4%81%403x.png"", ""backColor"":""#62DDB1""}, {""title"":""植物养护"", ""subTitle"":""实时维持绿植湿度"", ""description"":""当传感器检测到植物土壤湿度降低，需要浇水时，使用Bot或Plug Mini自动开启浇水设备，并发送通知给您。"", ""suggestID"":""plant_maintenance"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E6%A4%8D%E7%89%A9%E5%85%BB%E6%8A%A4.png"", ""color"":""""",
1775791060784,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"}, ""needDevices"":[{""deviceName"":""室外温湿度计"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_iometer.png"", ""deviceType"":""WoIOSensor""}, {""deviceName"":""温湿度计"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_meter.png"", ""deviceType"":""WoMeter""}, {""deviceName"":""智能大屏温湿度计"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_meterplus.png"", ""deviceType"":""WoMeterPlus""}, {""deviceName"":""万能遥控器2"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_hub2.png"", ""deviceType"":""WoHub2""}, {""deviceName"":""温湿度计Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_meterpro.png"", ""deviceType"":""W1079000""}, {""deviceName"":""万能网关3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_hub3.png"", ""deviceType"":""W1096000""}, {""deviceName"":""天气站"", ""deviceIcon"":""https://s3.amazonaws.com/www.wohand.com/version/wocaotech/feedback_img/weatherstation.png"", ""deviceType"":""W1070000""}, {""deviceName"":""智能插座"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_plug.png"", ""deviceType"":""WoPlug""}, {""deviceName"":""智能插座mini （JP）"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_plugminijp.png"", ""deviceType"":""WoPlugJP""}, {""deviceName"":""智能插座mini （US）"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_plugminius.png"", ""deviceType"":""WoPlugUS""}, {""deviceName"":""智能开关"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bot.png"", ""deviceType"":""WoHand""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E6%A4%8D%E7%89%A9%E5%85%BB%E6%8A%A4%403x.png"", ""backColor"":""#A8CE58""}, {""title"":""门开提醒"", ""subTitle"":""门开提醒，随时关注家门安全"", ""description"":""您的门被打开时，即时发送通知给您，让您随时掌握家门安全。"", ""suggestID"":""door_open_reminder"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automa",
1775791060784,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"tion_icon/icon_32pt_%E9%97%A8%E5%BC%80%E6%8F%90%E9%86%92.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""智能门锁"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_lock.png"", ""deviceType"":""WoLock""}, {""deviceName"":""智能门锁Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_lock.png"", ""deviceType"":""WoLockPro""}, {""deviceName"":""智能门锁Ultra"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_lock.png"", ""deviceType"":""W1091000""}, {""deviceName"":""门窗传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_contactsensor.png"", ""deviceType"":""WoContact""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E9%97%A8%E5%BC%80%E6%8F%90%E9%86%92%403x.png"", ""backColor"":""#A0A7AB""}, {""title"":""安全监控"", ""subTitle"":""实时监控家庭安全"", ""description"":""当家中的摄像头或传感器检测到异常活动时，将响起警报，开启灯光，并发送通知给您。"", ""suggestID"":""security_monitoring"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E5%AE%89%E5%85%A8%E7%9B%91%E6%8E%A7.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""室外摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_osc.png"", ""deviceType"":""WoBatteryCam""}, {""deviceName"":""智能门铃"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_video_doorbell_form.png"", ""deviceType"":""W1050001""}, {""deviceName"":""智能云台摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam""}, {""deviceName"":""智能云台摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam3MP""}, {""deviceName"":""智能摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ipc.png"", ""deviceType"":""WoCamera""}, {""deviceName"":""室外摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""d",
1775791060784,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"eviceType"":""WoOSC2""}, {""deviceName"":""智能云台摄像机 Plus 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs""}, {""deviceName"":""智能云台摄像机 Plus 3K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs5mp""}, {""deviceName"":""门窗传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_contactsensor.png"", ""deviceType"":""WoContact""}, {""deviceName"":""灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E7%81%AF.png"", ""deviceType"":""remote_14""}, {""deviceName"":""吸顶灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglight.png"", ""deviceType"":""WoCeiling""}, {""deviceName"":""吸顶灯 Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglightpro.png"", ""deviceType"":""WoCeilingPro""}, {""deviceName"":""智能开关"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bot.png"", ""deviceType"":""WoHand""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E5%AE%89%E5%85%A8%E7%9B%91%E6%8E%A7%403x.png"", ""backColor"":""#5797F8""}, {""title"":""人来开灯"", ""subTitle"":""自动为您照亮"", ""description"":""当您经过时，自动开灯，为您照亮当前环境。"", ""suggestID"":""people_come_light_on"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E4%BA%BA%E6%9D%A5%E5%BC%80%E7%81%AF.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""人体传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_motionsensor.png"", ""deviceType"":""WoPresence""}, {""deviceName"":""存在传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_presencesensor.png"", ""deviceType"":""W1101000""}, {""deviceName"":""落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102000""}, {""deviceName"":""灯带3",
1775791060785,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,""", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102001""}, {""deviceName"":""炫彩灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102003""}, {""deviceName"":""炫彩落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102004""}, {""deviceName"":""炫彩钢丝霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102005""}, {""deviceName"":""炫彩霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102006""}, {""deviceName"":""灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E7%81%AF.png"", ""deviceType"":""remote_14""}, {""deviceName"":""吸顶灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglight.png"", ""deviceType"":""WoCeiling""}, {""deviceName"":""吸顶灯 Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglightpro.png"", ""deviceType"":""WoCeilingPro""}, {""deviceName"":""彩色灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""WoStrip""}, {""deviceName"":""彩色灯泡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bulb.png"", ""deviceType"":""WoBulb""}, {""deviceName"":""智能开关"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bot.png"", ""deviceType"":""WoHand""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E4%BA%BA%E6%9D%A5%E5%BC%80%E7%81%AF%403x.png"", ""backColor"":""#FFD56A""}, {""title"":""人走关灯"", ""subTitle"":""人走灯灭，省心节电"", ""description"":""当您离开时，自动关闭灯光，节能又省力。"", ""suggestID"":""people_leave_light_off"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E4%BA%B",
1775791060785,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"A%E8%B5%B0%E5%85%B3%E7%81%AF.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""人体传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_motionsensor.png"", ""deviceType"":""WoPresence""}, {""deviceName"":""存在传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_presencesensor.png"", ""deviceType"":""W1101000""}, {""deviceName"":""灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_%E7%BA%A2%E5%A4%96%E7%81%AF.png"", ""deviceType"":""remote_14""}, {""deviceName"":""吸顶灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglight.png"", ""deviceType"":""WoCeiling""}, {""deviceName"":""吸顶灯 Pro"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ceilinglightpro.png"", ""deviceType"":""WoCeilingPro""}, {""deviceName"":""彩色灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""WoStrip""}, {""deviceName"":""彩色灯泡"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bulb.png"", ""deviceType"":""WoBulb""}, {""deviceName"":""智能开关"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_bot.png"", ""deviceType"":""WoHand""}, {""deviceName"":""落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102000""}, {""deviceName"":""灯带3"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102001""}, {""deviceName"":""炫彩灯带"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102003""}, {""deviceName"":""炫彩落地灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102004""}, {""deviceName"":""炫彩钢丝霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102005""}, ",
1775791060785,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"{""deviceName"":""炫彩霓虹灯"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_striplight.png"", ""deviceType"":""W1102006""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E4%BA%BA%E8%B5%B0%E5%85%B3%E7%81%AF%403x.png"", ""backColor"":""#264876""}, {""title"":""漏水提醒"", ""subTitle"":""漏水提醒，随时守护家庭安全"", ""description"":""当传感器检测到漏水时，为您发送消息通知"", ""suggestID"":""water_leakage_reminder"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_32pt_%E6%BC%8F%E6%B0%B4%E6%8F%90%E9%86%92.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""水浸传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_waterdetector%403x.png"", ""deviceType"":""WoWaterDetector""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E6%BC%8F%E6%B0%B4%E6%8F%90%E9%86%92%403x.png"", ""backColor"":""#5797F8""}, {""title"":""夜间未关门"", ""subTitle"":""守护您的爱车安全，让您一夜安心。"", ""description"":""当夜间车库门仍为开启状态，将为您发送消息通知"", ""suggestID"":""nighttime_not_closed_reminder"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_%E5%A4%9C%E9%97%B4%E6%9C%AA%E5%85%B3%E9%97%A8.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""车库门控制器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/device_icon/icon_32pt_gargedoor_open.png"", ""deviceType"":""W1083003""}], ""background"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E5%A4%9C%E9%97%B4%E6%9C%AA%E5%85%B3%E9%97%A8.png"", ""backColor"":""#264876""}, {""title"":""未关门提醒"", ""subTitle"":""守护您的爱车安全，避免忘关车库门的烦恼。"", ""description"":""当车库门超过一定时长仍为开启状态，将为您发送消息通知"", ""suggestID"":""timeout_not_closed_reminder"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.amazonaws.com/automation_icon/icon_%E6%9C%AA%E5%85%B3%E9%97%A8%E6%8F%90%E9%86%92.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""车库门控制器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/device_icon/icon_32pt_garged",
1775791060785,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"oor_open.png"", ""deviceType"":""W1083003""}], ""background"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E6%9C%AA%E5%85%B3%E9%97%A8%E6%8F%90%E9%86%92.png"", ""backColor"":""#5797F8""}, {""title"":""回家提醒"", ""subTitle"":""回到家时，发送提醒"", ""description"":""当您的家人回到家时，为您发送提醒"", ""suggestID"":""go_home_reminder"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/automation_icon/icon_32pt_%E5%9B%9E%E5%AE%B6%E6%8F%90%E9%86%92.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""安全报警器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/device_icon/icon_32pt_safety_alarm_online.png"", ""deviceType"":""W1110000""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E5%9B%9E%E5%AE%B6%403x.png"", ""backColor"":""#FFD56A""}, {""title"":""离家提醒"", ""subTitle"":""离开家时，发送提醒"", ""description"":""当您的家人离开家时，为您发送提醒"", ""suggestID"":""leave_home_reminder"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/automation_icon/icon_32pt_%E7%A6%BB%E5%AE%B6%E6%8F%90%E9%86%92.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""安全报警器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/device_icon/icon_32pt_safety_alarm_offline.png"", ""deviceType"":""W1110000""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E7%A6%BB%E5%AE%B6%403x.png"", ""backColor"":""#5797F8""}, {""title"":""回家布防报警"", ""subTitle"":""回家后监控室内外环境，安全守护"", ""description"":""当设备检测到异常时，执行消息推送与报警。"", ""suggestID"":""go_home_build_defenses_alarm"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/automation_icon/icon_%E8%87%AA%E5%8A%A8%E5%8C%96_%E5%9B%9E%E5%AE%B6%E5%B8%83%E9%98%B2_%E6%8A%A5%E8%AD%A6.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""智能门铃"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_video_doorbell_form.png"", ""deviceType"":""W1050001""}, {""deviceName"":""水浸传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaw",
1775791060785,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"s.com/device_icon/icon_waterdetector%403x.png"", ""deviceType"":""WoWaterDetector""}, {""deviceName"":""门窗传感器"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_contactsensor.png"", ""deviceType"":""WoContact""}, {""deviceName"":""室外摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoBatteryCam""}, {""deviceName"":""室外摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoOSC2""}, {""deviceName"":""智能云台摄像机 Plus 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs""}, {""deviceName"":""智能云台摄像机 Plus 3K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs5mp""}], ""background"":""https://prod-switchbot-icons.s3.amazonaws.com/background/%E8%87%AA%E5%8A%A8%E5%8C%96_%E5%9B%9E%E5%AE%B6%E5%B8%83%E9%98%B2.png"", ""backColor"":""#5797F8""}, {""title"":""离家布防报警"", ""subTitle"":""离家后识别异常，安全守护"", ""description"":""设备监测到室内外异常时，执行消息推送与报警"", ""suggestID"":""leave_home_build_defenses_alarm"", ""icon"":{""css"":""https://prod-switchbot-icons.s3.us-east-1.amazonaws.com/automation_icon/icon_%E8%87%AA%E5%8A%A8%E5%8C%96_%E7%A6%BB%E5%AE%B6%E5%B8%83%E9%98%B2_%E6%8A%A5%E8%AD%A6.png"", ""color"":""""}, ""needDevices"":[{""deviceName"":""智能摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ipc.png"", ""deviceType"":""WoCamera""}, {""deviceName"":""智能云台摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam""}, {""deviceName"":""智能云台摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoPanTiltCam3MP""}, {""deviceName"":""智能云台摄像机 Plus 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs""}, {""deviceName"":""智能云台摄像机 Plus 3K"", ""deviceIcon"":""https://prod-switchbot-i",
1775791060785,com.theswitchbot.switchbot.index.ui.MainActivity,网络返回,"cons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoCamKvs5mp""}, {""deviceName"":""智能门铃"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_video_doorbell_form.png"", ""deviceType"":""W1050001""}, {""deviceName"":""室外摄像机"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoBatteryCam""}, {""deviceName"":""室外摄像机 2K"", ""deviceIcon"":""https://prod-switchbot-icons.s3.amazonaws.com/device_icon/icon_32pt_ptc.png"", ""deviceType"":""WoOSC2""}, {""deviceName"":""人体传感器"", ""deviceIcon"":""htt
<<<END_EXTERNAL_UNTRUSTED_CONTENT id="2d297139cf37b6ff">>>
</file>
assistant: 我把你这个 CSV 日志扫了一遍，**真正可以归到“失败 ❌”的点主要有 4 个**，其余基本都是正常流程日志。

可以这样汇总：

一、设备列表接口请求失败  
日志：
`POST https://wonder.us.api.switchbot.net/wonder/device/v3/getdevice`  
返回：
`408 network error`

原因：  
请求在发送时被 **Canceled / 网络中断**。

相关日志：
- `NetWorkingManager catch message=Canceled`
- `<-- 408 network error`

影响：  
首次设备列表获取失败，可能导致首页设备加载异常或延迟。

---

二、MQTT 连接异常  
日志：

`MqttService Mqtt-Iot-ConnectionLost`  
`MqttService Mqtt连接发生异常`

原因：  
网络状态变化导致 MQTT 断开。

后续日志：
`MqttService Mqtt-Iot-Reconnecting`  
`MqttService Mqtt-Iot-Connected`

说明：  
系统自动重连成功。

影响：  
短时间设备状态不同步。

---

三、设备类型识别异常  
日志：

`设备Code为：W1156000,识别到未知设备`

说明：  
App 当前版本没有识别这个设备型号。

设备：
`W1156000`

影响：

- UI 可能用默认设备展示
- 功能可能不完整

---

四、协程任务被取消  
日志：

`StandaloneCoroutine was cancelled : JobCancellationException`

原因：

通常是 **页面生命周期变化（切后台 / 页面销毁）**。

影响：

基本没有实际功能影响。

---

✅ **最终结论（可以直接写报告）**

失败数据主要由以下原因导致：

1. 设备列表接口请求返回 408（网络请求被取消）  
2. MQTT 连接短暂中断后自动重连  
3. App 未识别设备型号 W1156000  
4. 页面生命周期导致协程任务取消

其中 **最关键的是第一条：设备列表接口 408**。

---

如果你需要，我可以帮你把这个 **整理成标准 QA 问题分析格式**（包含：  
复现现象 → 关键日志 → Root Cause → 影响范围 → 结论），直接可以贴到 **Jira / Tapd**。
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b52efd59838a4c34b18a51718263",
  "sender_id": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "sender": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "timestamp": "Tue 2026-04-14 11:51 GMT+8"
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

[message_id: om_x100b52efd59838a4c34b18a51718263]
ou_9c8d825e05f86d5b1794dea7e7a30a36: 报错的内容，以及问题归纳
assistant: 可以这样整理 **“报错内容 + 问题归纳”**：

一、报错内容

1. 设备列表接口请求失败  
日志：  
`POST https://wonder.us.api.switchbot.net/wonder/device/v3/getdevice`  
返回：  
`408 network error`  
相关日志：  
`NetWorkingManager catch message=Canceled`

2. MQTT 连接异常  
日志：  
`MqttService Mqtt-Iot-ConnectionLost`  
`MqttService Mqtt连接发生异常`  
后续：  
`MqttService Mqtt-Iot-Reconnecting`  
`MqttService Mqtt-Iot-Connected`

3. 设备型号识别异常  
日志：  
`设备Code为：W1156000,识别到未知设备`

4. 协程任务取消异常  
日志：  
`StandaloneCoroutine was cancelled : JobCancellationException`

---

二、问题归纳

本次日志中出现的异常主要包括：

- 设备列表接口请求返回 **408 network error**，请求被取消，可能与网络状态变化有关。  
- MQTT 连接在运行过程中出现 **ConnectionLost**，随后自动重连成功。  
- App 未识别设备型号 **W1156000**，提示未知设备。  
- 页面生命周期变化导致 **协程任务取消（JobCancellationException）**。

其中 **设备列表接口 408 请求失败是主要异常点**，其余异常为网络波动或系统状态变化引起的短暂问题，对整体功能影响较小。
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b52efd02ee494c4a72207dc0d41d",
  "sender_id": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "sender": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "timestamp": "Tue 2026-04-14 11:52 GMT+8"
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

[message_id: om_x100b52efd02ee494c4a72207dc0d41d]
ou_9c8d825e05f86d5b1794dea7e7a30a36: 蓝牙连接正常吗
assistant: 从这份日志看，**蓝牙本身是正常启动的，没有看到蓝牙连接失败的报错**。

关键日志：

1. 蓝牙扫描启动  
`开始扫描蓝牙设备`  
`获取扫描器结果 field=android.bluetooth.le.BluetoothLeScanner`  
`蓝牙快速扫描...`

说明：  
BLE 扫描正常启动。

2. 没有出现常见蓝牙错误  
日志里 **没有看到**这些典型问题：

- `BluetoothAdapter disabled`
- `BLE connect fail`
- `GATT error`
- `Scan failed`

3. 设备状态判断  
日志中有：

`isDeviceOnline:bleScan:false,iotOnline:true`

意思是：

- BLE 扫描没有发现该设备  
- 设备是通过 **IoT（MQTT）在线**

所以设备是 **云端在线，而不是通过蓝牙直连**。

4. 页面切换时主动断开蓝牙  
日志：

`回到首页断开所有蓝牙连接...`

这是 **正常逻辑**，不是异常。

✅ 结论  
- 蓝牙扫描功能正常启动  
- 没有蓝牙连接失败日志  
- 当前设备主要通过 **IoT 在线而不是 BLE 连接**

所以从日志看 **蓝牙连接没有异常**。
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b52efe836d8b4c4a903b9a7415be",
  "sender_id": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "sender": "ou_9c8d825e05f86d5b1794dea7e7a30a36",
  "timestamp": "Tue 2026-04-14 11:54 GMT+8"
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

[message_id: om_x100b52efe836d8b4c4a903b9a7415be]
ou_9c8d825e05f86d5b1794dea7e7a30a36: 检查这个时间段的错误2026/04/10 14:46
assistant: 这个时间段（**2026‑04‑10 14:46 附近**）日志里能看到的异常主要有下面几条：

一、设备列表接口请求失败  
日志：  
POST https://wonder.us.api.switchbot.net/wonder/device/v3/getdevice  
返回：  
408 network error  

相关日志：  
NetWorkingManager catch message=Canceled  

说明：  
设备列表请求被取消，导致接口返回 408。

影响：  
可能造成首页设备列表加载失败或延迟。

---

二、MQTT 连接异常  
日志：  
MqttService Mqtt‑Iot‑ConnectionLost  
MqttService Mqtt连接发生异常  

随后日志：  
MqttService Mqtt‑Iot‑Connecting  
MqttService Mqtt‑Iot‑Connected  

说明：  
MQTT 在该时间点出现断开，但随后自动重连成功。

影响：  
短时间设备状态无法同步。

---

三、未知设备类型  
日志：  
设备Code为：W1156000，识别到未知设备  

说明：  
当前 App 版本没有识别该设备型号。

影响：  
设备可能用默认图标或部分功能不可用。

---

四、协程任务取消  
日志：  
StandaloneCoroutine was cancelled  
JobCancellationException  

说明：  
页面生命周期变化导致任务取消（常见于页面刷新或后台切换）。

影响：  
通常无实际功能影响。

---

总结（14:46 时间段）：

主要异常有三类：  
- **设备列表接口 408 请求失败**  
- **MQTT 短暂断开后重连**  
- **设备型号 W1156000 未识别**

其中 **最关键的问题是设备列表接口 408 网络错误**。
