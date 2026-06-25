# Context Handoff Design

## Problem

Long AI sessions become hard to continue because context windows, model routing, and chat organization are exposed to the user.

## ClauDeus strategy

ClauDeus turns a messy session into a compact file-backed packet.

```text
conversation / project files / logs / skills
→ context pack
→ handoff packet
→ new session or provider adapter
→ dashboard card
```

## Context Pack

A context pack contains:

- current goal
- project slug
- recent state
- relevant files
- active constraints
- selected skills
- failure notes
- expected output contract

## Handoff Packet

A handoff packet contains:

- source
- target
- session id
- turn id
- summary
- next actions
- title hint
- answer excerpt
- raw log pointer

## 20-command rule

The original ClauDeus UX can be implemented as a threshold:

1. collect useful commands or turns
2. when the threshold is reached, generate a handoff packet
3. propose a new title
4. open or prepare a fresh session
5. keep the old session as an audit trail

## User-facing principle

The user should see:

```text
Continue this work
```

not:

```text
compress context, select model, route provider, manage memory, migrate chat
```
