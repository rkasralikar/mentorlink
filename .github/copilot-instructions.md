# Copilot instructions

See [AGENT.md](../AGENT.md) for full project conventions, architecture notes, and action policy.

## Quick reference

**Services:** `analytics-service`, `app-service` (userService, feedService, chatService), `insights-service`, `reco-service`, `bigdata-service`, `uc-service`
**Mobile:** `user-app/` (React Native)
**Shared:** `common-modules/common_modules/`
**Infra:** `infra-service/`

**Business logic:** `*/src/` in each service. Tests in `*/test/`.

**Build:** `npm install && npm run build` per service. Tests: `npm test`.

**PRs:** One concern per PR. Follow existing ESLint style. Don't push directly to `main`.
