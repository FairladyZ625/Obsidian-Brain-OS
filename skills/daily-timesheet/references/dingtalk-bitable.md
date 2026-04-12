# DingTalk AI Table — Timesheet Field Mapping

Reference for writing timesheet records to a DingTalk AI Table (钉钉 AI 表格).

## Prerequisites

1. Create a DingTalk app at [open.dingtalk.com](https://open.dingtalk.com) with AI Table read/write permissions
2. Get `app_key` and `app_secret`
3. Create an AI Table with a timesheet sheet; note the `base_id` and `table_id`

## Auth — get access_token

```bash
TOKEN=$(curl -s -X POST https://api.dingtalk.com/v1.0/oauth2/accessToken \
  -H "Content-Type: application/json" \
  -d "{\"appKey\": \"$DINGTALK_APP_KEY\", \"appSecret\": \"$DINGTALK_APP_SECRET\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['accessToken'])")
```

## Create a record

```bash
curl -s -X POST \
  "https://api.dingtalk.com/v1.0/doc/bases/$DINGTALK_BASE_ID/tables/$DINGTALK_TABLE_ID/records" \
  -H "x-acs-dingtalk-access-token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [{
      "fields": {
        "日期": "2026-04-12",
        "工时": 1.0,
        "里程碑": "M1 — Project Name",
        "KR对齐": "KR1: xxx done ~80%\nKR2: yyy started",
        "状态": "进行中"
      }
    }]
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
curl -s -X POST \
  "https://api.dingtalk.com/v1.0/doc/bases/$DINGTALK_BASE_ID/tables/$DINGTALK_TABLE_ID/records/query" \
  -H "x-acs-dingtalk-access-token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"filter\": {\"conditions\": [{\"fieldName\": \"日期\", \"operator\": \"is\", \"value\": [\"$DATE\"]}]}}"
```

## Notes

- DingTalk AI Table API is in beta; field names must match exactly as configured in your table
- `base_id` is the long alphanumeric ID in the table URL, not the display name
- For linked record fields, use `{"linkedRecordIds": ["recordId1"]}` format
