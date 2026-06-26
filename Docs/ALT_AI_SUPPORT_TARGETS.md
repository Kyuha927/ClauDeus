# Alternative AI Support Targets

## Purpose

This document tracks non-OpenAI support, credit, free-tier, or partnership targets that may help ClauDeus development.

## Important distinction

Not every target is an official open-source maintainer grant. Many are one of:

- free developer tier
- free API/token migration offer
- open-weight model ecosystem
- startup/cloud credit program
- public beta access
- academic/research access
- community sponsorship path

## Priority tiers

### Tier A — apply or use immediately

| Target | Type | Why it matters for ClauDeus | Action |
| --- | --- | --- | --- |
| OpenAI Patch the Planet / Codex Security | open-source security/workflow support | closest match to ClauDeus support ask | keep application package ready |
| Google Gemini CLI / Code Assist free tier | free coding-agent capacity | useful fallback provider and CLI route | add provider adapter / use for E2E work |
| Zhipu GLM migration/free-token offer | Chinese model free-token/coding package signal | likely best Chinese-model support angle | prepare Chinese/English pitch |
| DeepSeek | open-weight + low-cost API route | strong low-cost provider adapter candidate | add provider adapter and benchmark |
| Alibaba Qwen | open-weight + cloud/API ecosystem | strong Chinese open model ecosystem | add Qwen adapter and benchmark |
| Moonshot Kimi | open-weight K2 + coding/agent positioning | strong agentic coding story | add Kimi adapter and benchmark |

### Tier B — monitor and contact

| Target | Type | Why it matters | Action |
| --- | --- | --- | --- |
| MiniMax | Chinese model/API ecosystem | possible low-cost provider | look for official credits/startup path |
| Baidu ERNIE | Chinese model/app/API ecosystem | free consumer model and enterprise cloud route | monitor API/free developer route |
| Tencent Hunyuan | open model + Tencent cloud route | potential open model/provider adapter | monitor official credits |
| Mistral | open-weight + coding models | non-Chinese open model option | add Devstral/Codestral adapter later |
| Cohere | enterprise/API + research models | multilingual/enterprise option | monitor research/startup access |
| GitHub Sponsors | open-source funding | not model credits, but useful funding path | set up sponsor profile later |

## Provider-specific notes

### OpenAI / Codex

ClauDeus application package lives at:

- `Docs/CODEX_SUPPORT_APPLICATION.md`
- `Docs/CODEX_WEB_CONTROL_PROMPT.md`

### Google Gemini / Antigravity

Use for free/large developer capacity and as a provider adapter target. Verify current CLI migration state before depending on Gemini CLI directly.

### Zhipu GLM

Best current lead among Chinese vendors because public reporting indicates a Claude migration offer with free tokens and a developer coding package. Treat as time-sensitive and verify on official Zhipu/BigModel pages before submitting.

### Alibaba Qwen

Strong open-weight ecosystem. Pitch ClauDeus as a Qwen-compatible provider-agnostic WorkOS with dashboard/mobile capture and E2E smoke tests.

### Moonshot Kimi

Strong agentic/coding positioning through Kimi K2. Pitch ClauDeus as a workflow shell that can make Kimi/K2 useful across mobile, dashboard, and provider adapters.

### DeepSeek

Strong low-cost and open-weight story. Pitch ClauDeus as a safe adapter and validation layer for low-cost open-weight coding models.

## Reusable outreach pitch

```text
I am building ClauDeus, a provider-agnostic AI WorkOS bridge for ordinary users and open-source maintainers. It hides context engineering, model routing, chat handoff, mobile capture, provider interface differences, skills, playbooks, and dashboard organization behind a file-backed workflow.

ClauDeus is intentionally model-agnostic. I am looking for model/API credits, developer access, or technical guidance to add and benchmark a safe provider adapter for your model ecosystem.

Current MVP components include a runtime bridge, mobile PWA inbox, dashboard renderer, skills validator, playbook validator, profile pack, and knowledge feeder. Support would help me harden the adapter, improve tests, and publish a clean open-source integration guide.
```

## Web-control search prompt

```text
Find official support, grant, free-credit, startup, developer, or open-source maintainer programs for ClauDeus across OpenAI, Google Gemini, Zhipu GLM, Alibaba Qwen, Moonshot Kimi, DeepSeek, MiniMax, Baidu ERNIE, Tencent Hunyuan, Mistral, Cohere, Together, Groq, OpenRouter, Hugging Face, Replicate, Modal, and major cloud providers. Use only official pages for submission. Do not submit anything without confirmation. Return official URLs, eligibility, benefits, and application steps. If no official program exists for a provider, mark OFFICIAL_PROGRAM_NOT_FOUND.
```
