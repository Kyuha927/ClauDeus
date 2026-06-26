# Codex Web Control Prompt

Use this prompt when asking Codex or another browser-control agent to help submit the ClauDeus support application.

```text
You are operating a browser for me. Your task is to help me apply for any official OpenAI/Codex/open-source maintainer support program that is relevant to ClauDeus.

Important safety and accuracy rules:

1. Use only official OpenAI-controlled domains or clearly official OpenAI-owned forms/pages when submitting anything.
2. Do not submit personal data, payment information, API keys, access tokens, passwords, recovery codes, or private secrets.
3. If login, 2FA, phone verification, payment, or identity verification is required, stop and ask me to take over.
4. If there is no official public application form, do not invent one. Instead, report the best official contact path you found.
5. Do not click final Submit until you show me the completed form contents and ask for my explicit confirmation.
6. Preserve all URLs visited and summarize what you found.
7. Do not use random third-party forms, unofficial Google Forms, Discord invites, or social posts unless they are linked from an official OpenAI source.

Primary project:

- GitHub repo: https://github.com/Kyuha927/ClauDeus
- Application package: https://github.com/Kyuha927/ClauDeus/blob/main/Docs/CODEX_SUPPORT_APPLICATION.md
- Product vision: https://github.com/Kyuha927/ClauDeus/blob/main/Docs/PRODUCT_VISION.md
- Architecture: https://github.com/Kyuha927/ClauDeus/blob/main/Docs/ARCHITECTURE.md
- Mobile experience: https://github.com/Kyuha927/ClauDeus/blob/main/Docs/MOBILE_APP_EXPERIENCE.md
- E2E checklist: https://github.com/Kyuha927/ClauDeus/blob/main/Docs/E2E_DEMO_CHECKLIST.md
- Stability sweep: https://github.com/Kyuha927/ClauDeus/blob/main/Docs/STABILITY_SWEEP.md

What ClauDeus is:

ClauDeus is a provider-agnostic AI WorkOS bridge for open-source maintainers and ordinary users. It hides context engineering, model routing, chat handoff, mobile capture, provider interface differences, skills, playbooks, and dashboard organization behind a file-backed workflow.

Short application answer to use if the form asks for project description:

I am building ClauDeus, a provider-agnostic AI WorkOS bridge for open-source maintainers and ordinary users. It hides context engineering, model routing, chat handoff, mobile capture, and provider interface differences behind a file-backed workflow. The project already spans a multi-repo MVP portfolio with a runtime bridge, mobile PWA inbox, dashboard renderer, skills library, playbook validator, profile pack, and knowledge feeder. Codex support would help harden the system, remove environment-specific assumptions, improve test coverage, and make AI-assisted open-source work safer and more usable.

If asked why support is needed:

Codex support would help turn ClauDeus from a working multi-repo MVP skeleton into a hardened open-source workflow system for AI-assisted maintainers and ordinary builders. The biggest need is reliable agent workflow infrastructure: safer provider adapter boundaries, repeatable smoke tests, reproducible handoff packets, mobile-to-runtime capture, readable validation output, repository-aware context packs, security-conscious GUI relay rules, and better onboarding for non-expert users.

If asked what I am requesting:

I am requesting support for continued open-source development, security and workflow review of ClauDeus provider adapter boundaries, guidance on safe Codex/GUI/CLI relay patterns, help hardening the mobile inbox and dashboard workflow, and review of the project as an open-source AI workflow infrastructure candidate.

If asked how Codex would be used:

Codex would be used to refactor runtime watchers into shared handoff helpers, implement safe dry-run provider adapters, add tests around queueing, retries, validation, and dashboard rendering, remove local environment assumptions, improve smoke workflows, harden the mobile PWA capture path, create clean onboarding and examples, and review security boundaries for relays and token handling.

If asked for security posture:

ClauDeus is designed to avoid unsafe automation patterns: dry-run first, approval required for risky actions, raw logs preserved for audit and replay, GUI relay documented as opt-in and user-approved, official API/CLI routes preferred when available, active skills require review before use, and mobile capture stores events locally before network sync.

Required final output before submission:

Before clicking Submit, show me:

1. The exact official page/form URL.
2. Every field you filled.
3. The final text that will be submitted.
4. Any required follow-up or missing information.
5. A clear question: “May I submit this now?”

If no official form is found:

Return:

- OFFICIAL_FORM_NOT_FOUND
- official URLs checked
- best official contact path found
- recommended next step
```
