# Universal Model Runtime

## Goal

ClauDeus should route every usable model through a single runtime contract while keeping authentication, failures, and prompt overhead outside the user experience.

## Authentication reality

OAuth is provider-level, not model-level.

ClauDeus supports:

- official OAuth 2.0 Authorization Code + PKCE
- official OAuth 2.0 Device Authorization
- API keys and environment credentials
- authenticated CLIs
- anonymous local runtimes

When a provider does not offer official OAuth, ClauDeus uses its supported API key, CLI, or local route. It does not promise unofficial reuse of subscription credentials.

## Runtime implementation

Primary runtime repo:

```text
Kyuha927/copilot
```

Core files:

```text
scripts/auth_broker.py
scripts/provider_catalog.py
scripts/model_discovery.py
scripts/resilient_router.py
scripts/token_budget.py
scripts/tool_budget.py
scripts/cladeus_runtime.py
scripts/providerctl.py
```

## Every-model routing

A provider catalog can declare multiple models. Each model becomes a separate candidate and adapter route.

A wildcard model entry can be replaced by authenticated `/models` discovery cache data.

```text
provider
├── model A route
├── model B route
└── model C route
```

## Failure containment

ClauDeus cannot prevent provider outages or revoked credentials. It prevents those failures from becoming uncontrolled runtime crashes:

```text
structured auth result
→ bounded retry for transient failures
→ circuit breaker
→ next eligible model
→ readable contained failure when exhausted
```

## Performance target

ClauDeus aims to outperform OpenCode at the local control-plane layer and beat Pi-style prompt overhead through:

- exact duplicate removal
- already-seen delta filtering
- explicit context budgets
- output-token reservation
- capability-scoped tool schema selection
- no provider/auth catalog injected into the prompt
- one route per model

These are targets, not verified superiority claims. A fair comparison must use the same repository, model, task, machine, account tier, and token accounting.

## Commands

Validate and list providers:

```bash
python scripts/providerctl.py validate
python scripts/providerctl.py list
```

OAuth login for an officially configured provider:

```bash
python scripts/providerctl.py login <provider-id>
```

Discover models:

```bash
python scripts/cladeus_runtime.py discover --provider <provider-id>
```

Dry-run route:

```bash
python scripts/cladeus_runtime.py run "inspect this repository" --capability coding
```

Real execution:

```bash
python scripts/cladeus_runtime.py run "inspect this repository" --capability coding --execute
```

Benchmark local control plane:

```bash
python scripts/benchmark_control_plane.py --runs 5 --assert-targets
```
