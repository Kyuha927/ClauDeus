# Mobile Inbox Connector

## Purpose

The mobile inbox connector lets a user feed ClauDeus from a phone without installing a desktop sync client.

## Canonical v1

```text
phone upload
→ cloud folder
→ server-side polling
→ normalized mobile event
→ ClauDeus Runtime
→ dashboard card / provider task
```

## Event contract

```json
{
  "event_id": "string",
  "received_at": "iso8601",
  "provider": "google_drive",
  "source_kind": "drive_cloud_file",
  "title": "string",
  "content_type": "image|pdf|text|office|unknown",
  "attachment_name": "string",
  "attachment_path": "string",
  "source_fingerprint": "string",
  "project": "inbox",
  "topic": "mixed"
}
```

## Implementation order

1. dry-run event generator
2. polling worker
3. dedupe state
4. normalized event writer
5. runtime ingest
6. webhook wake-up
7. dashboard review screen

## Guardrails

- Polling-first, webhook second.
- Webhook is wake-up only.
- Keep raw events for replay.
- Do not require desktop sync.
