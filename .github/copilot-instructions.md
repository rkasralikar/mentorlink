# Copilot / AI agent instructions for the Mentorlink repository

This file guides Copilot and other AI helpers when editing this project. Keep
suggestions focused on existing conventions and directories.

## Project overview
Mentorlink contains several microservices (`analytics-service`, `app-service`,
`insights-service`, etc.) plus common modules and infrastructure code. Each
service is a standalone Node.js application (see package.json in subfolders).

### Where to make changes
- Business logic lives under `*/src/` in each service (e.g. `app-service/src`).
- Shared utility code is in `common-modules/common_modules/`.
- Deployment manifests and configs are in `infra-service/` or at project root.

## Development workflow
- A service typically uses `npm install && npm run build` or similar.
- Tests (when present) are in `*/test/` directories and run with `npm test`.
- Follow existing style (ESLint rules) and keep the JS idiomatic.

## Planning and SDLC
See the top-level `plans/` directory for templates covering requirements,
design, coding, and testing. Each new feature should have a corresponding
`*-plan.md` document and explicit approvals before moving between stages.

---

If you need more context or a specific template, check `plans/` or ask the
human author.
