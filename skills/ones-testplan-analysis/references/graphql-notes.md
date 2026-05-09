# ONES GraphQL 查询笔记（测试计划相关）

## 端点

```
https://ones.cn/api/project/team/{team_uuid}/items/graphql
```

Headers:
- `Ones-User-Id`: user uuid
- `Ones-Auth-Token`: auth token
- `Content-Type`: application/json

## 查询测试计划列表

```graphql
{
  testcasePlans {
    uuid
    name
    createTime
    planStatus
  }
}
```

## 查询计划内用例执行结果（分页）

```graphql
{
  testcasePlanCases(
    filter: { planUUID: "<PLAN_UUID>" },
    limit: 50,
    after: "<CURSOR>"
  ) {
    uuid
    name
    priority
    result
    path
  }
}
```

### 字段说明

| 字段 | 说明 | 示例值 |
|------|------|--------|
| uuid | 用例唯一标识 | "Fk28evjW" |
| name | 用例名称 | "设备配网成功" |
| priority | 优先级 | "P0" / "P1" / "P2" / "P3" / "P4" |
| result | 执行结果 | "passed" / "failed" / "blocked" / "skipped" / "" (todo) |
| path | 模块路径 | "/固件用例/配网/BLE配网" |

### 分页机制

- `limit`: 每次最多 50 条
- `after`: 传入上一批最后一条的 uuid 作为 cursor
- 当返回数量 < limit 时表示已到末页

## 注意事项

- `result` 为空字符串或 null 表示 Todo（未执行）
- `path` 用 `/` 分割的模块层级路径，第一级通常是根分类
- 不同计划可能共享用例但有独立的执行结果
- 大计划（>5000条）拉取需要多次分页，耐心等待
