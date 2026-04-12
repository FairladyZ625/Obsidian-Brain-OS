# Observer Learnings Index Schema

The `.learnings/observer/index.json` file tracks recurrence counts for all observed anomalies.

## Schema

```json
{
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "recurrenceMap": {
    "<anomaly-key>": {
      "title": "Human-readable title",
      "category": "errors | infrastructure | corrections | insights",
      "severity": "high | medium | low",
      "firstSeen": "YYYY-MM-DD",
      "lastSeen": "YYYY-MM-DD",
      "count": 3,
      "file": "errors/2026-04-01-example-error.md",
      "status": "open | suggested | executed | promoted"
    }
  },
  "promoteCandidates": [
    "<anomaly-key>"
  ]
}
```

## Field descriptions

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Schema version |
| `lastUpdated` | date | Last time this file was written |
| `recurrenceMap` | object | Map of anomaly key → tracking entry |
| `anomaly-key` | string | Slug derived from error type + context, e.g. `gateway-fetch-failed-plugins` |
| `title` | string | Short human-readable description |
| `category` | enum | One of: `errors`, `infrastructure`, `corrections`, `insights` |
| `severity` | enum | `high`, `medium`, or `low` |
| `firstSeen` | date | Date first observed |
| `lastSeen` | date | Date most recently observed |
| `count` | number | Total occurrences tracked |
| `file` | string | Path to the learning markdown file (relative to `.learnings/observer/`) |
| `status` | enum | `open` → `suggested` → `executed` → `promoted` |
| `promoteCandidates` | array | Keys with count >= 7 within 7 days, flagged for human review |

## Promote threshold

An anomaly is flagged as a promote candidate when:
- `count >= 7` AND
- `lastSeen` is within 7 days of today

Promote candidates are listed in the daily iteration plan's "Needs Human Decision" section.

## Key naming convention

```
<category>-<error-type>-<context>
```

Examples:
- `infrastructure-gateway-fetch-failed`
- `infrastructure-failover-timeout`
- `errors-tool-call-retry-sessions_list`
- `corrections-model-preference-updated`
