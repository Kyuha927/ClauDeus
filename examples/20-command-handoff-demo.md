# 20-command Handoff Demo

## Goal

Show how ClauDeus can turn a long session into a fresh handoff.

## Demo flow

1. User sends work commands.
2. ClauDeus records useful commands.
3. When the threshold is reached, ClauDeus builds a context pack.
4. ClauDeus writes a handoff packet.
5. The next provider or chat receives only the compact packet.
6. The dashboard shows the new title and next action.

## Example command

```bash
./dev context-pack "continue the Google Drive mobile inbox connector"
./dev handoff-plan "prepare executor handoff for mobile inbox connector"
```

## Expected outputs

```text
CONTEXT_PACK_READY
HANDOFF_PACKET_READY
```
