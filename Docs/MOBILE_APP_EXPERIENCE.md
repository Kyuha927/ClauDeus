# Mobile App-Like Experience Design

## Goal

Make ClauDeus feel smooth on mobile without forcing a full native app on day one.

The best v1 path is:

```text
Installable PWA
→ local offline queue
→ fast optimistic UI
→ mobile inbox API
→ runtime handoff
→ dashboard status updates
```

## Product principle

Mobile users should be able to capture intent in under five seconds, even when the model, provider, runtime, or desktop machine is not ready.

## UX requirements

1. **Installable home-screen app** via web app manifest.
2. **Fast first paint** with cached shell.
3. **Offline capture** using a local queue.
4. **Optimistic send**: show the item immediately as queued.
5. **Retry loop** when the network returns.
6. **Share target** for images, text, PDFs, links, and screenshots.
7. **One-thumb UI**: bottom input, large tap targets, minimal chrome.
8. **Status chips**: queued, syncing, routed, blocked, done.
9. **Handoff title hints** so long work stays organized.
10. **Raw event preservation** for replay and audit.

## Architecture

```text
Mobile PWA
  ├── local queue
  ├── service worker
  ├── manifest
  ├── share/capture UI
  └── sync client
       ↓
Mobile Inbox Connector
       ↓
ClauDeus Runtime
       ↓
Provider Adapter
       ↓
Dashboard Card
```

## Why PWA first

A PWA is the fastest way to prove the product experience:

- works on Android and iOS browser surfaces
- can be installed to the home screen
- avoids app store friction during MVP
- can later be wrapped with Capacitor or a native shell

## Native wrapper later

Only move to native when one of these becomes necessary:

- stable background upload beyond browser limits
- native share-sheet reliability
- push notification integrations
- secure device credential storage
- camera/gallery automation

## MVP event shape

```json
{
  "event_id": "string",
  "created_at": "iso8601",
  "kind": "text|image|file|link|voice|mixed",
  "title": "string",
  "body": "string",
  "attachments": [],
  "status": "queued|syncing|sent|blocked|done",
  "project": "inbox",
  "topic": "mixed"
}
```

## Smoothness checklist

- no blocking spinner for capture
- queue writes happen before network calls
- sync retry is idempotent
- each event has a stable fingerprint
- user can see what is pending
- failed sends keep editable drafts
- dashboard updates are incremental

## First implementation target

Implement `daily/mobile_pwa/` as the mobile capture surface and connect it to the Google Drive/mobile inbox connector.
