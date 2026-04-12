# Feishu Bitable — Timesheet Field Mapping

Reference for writing timesheet records to a Feishu Bitable (多维表格).

## Prerequisites

1. Create a Feishu app at [open.feishu.cn](https://open.feishu.cn) with Bitable read/write permissions
2. Get `app_id` and `app_secret`
3. Create a Bitable with a timesheet table; note the `app_token` and `table_id`

## Auth — get tenant_access_token

```bash
TOKEN=$(curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$FEISHU_APP_ID\", \"app_secret\": \"$FEISHU_APP_SECRET\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])")
```

## Create a record

```bash
curl -s -X POST \
  "https://open.feishu.cn/open-apis/bitable/v1/apps/$FEISHU_BITABLE_APP_TOKEN/tables/$FEISHU_BITABLE_TABLE_ID/records" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "日期": "2026-04-12",
      "工时": 1.0,
      "里程碑": "M1 — Project Name",
      "KR对齐": "KR1: xxx done ~80%\nKR2: yyy started",
      "状态": "进行中",
      "备注": ""
    }
  }'
```

## Recommended table schema

| Field name | Type | Notes |
|------------|------|-------|
| 日期 | Date | YYYY-MM-DD |
| 工时 | Number | Days (0.5 / 1.0 / 1.5) |
| 里程碑 | Text | e.g. "M1 — Project Name" |
| KR对齐 | Text (long) | Multi-line KR progress |
| 状态 | Select | 进行中 / 已完成 / 阻塞 |
| 备注 | Text | Blockers, notes |

## Query existing records (for dedup)

```bash
curl -s -X GET \
  "https://open.feishu.cn/open-apis/bitable/v1/apps/$APP_TOKEN/tables/$TABLE_ID/records?filter=CurrentValue.[日期]=\"$DATE\"" \
  -H "Authorization: Bearer $TOKEN"
```
