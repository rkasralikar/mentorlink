# Agent guidance for Mentorlink repository

This document is vendor-neutral and provides general instructions for AI
assistants (Copilot, Claude, etc.) operating in the Mentorlink codebase.

## Overview
This project is a sandbox for exploring Node.js, Python, C/C++, ML, and SaaS
patterns across multiple services.

## Tech Stack
- Languages: JavaScript, TypeScript, Python
- Frameworks: Node.js, Next.js
- Database: PostgreSQL
- Package managers: npm, pip

## Repository Layout
- `analytics-service/` — Python analytics microservice
- `app-service/` — Node.js services: `userService`, `feedService`, `chatService`
- `insights-service/` — insights microservice
- `reco-service/` — recommendation service (Python/ML)
- `bigdata-service/` — data pipeline service
- `uc-service/` — user classification service
- `common-modules/` — shared utilities across services
- `user-app/` — React Native mobile app
- `infra-service/` — AWS/deployment manifests and configs
- `schema/` — shared JSON schemas
- `plans/` — SDLC plans (committed to repo history)

For service-specific tasks, look inside the service folder first. Business logic lives under `*/src/`.

## Common Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run lint` - Lint the codebase

## Architecture Notes
- Auth is handled via JWT tokens stored in httpOnly cookies
- API routes live in `src/api/` and follow REST conventions

## Environment Variables
- Copy `.env.example` to `.env.local` for local development
- Never commit secrets to the repo

## Code Style & Conventions
- Use 4-space indentation
- Prefer `const` over `let`
- Follow existing naming conventions (camelCase for variables, PascalCase for components)
- Don't use `any` type in TypeScript
- Always write unit tests for new functions
- Add JSDoc comments for public functions
- Prefer functional components over class components

## Testing
- Unit tests: Jest
- E2E tests: Playwright
- Run tests before submitting PRs

## Workflow & Change Discipline
- Use small, self-contained changes; avoid cross-cutting refactors without
  explicit approval.
- When drafting plans, place them under `plans/` and commit them as part of
  repo history.
- Follow the SDLC workflow: requirements → design → code → tests. Wait for
  explicit approval before advancing stages.
- Write descriptive commit messages
- Don't modify `package-lock.json` directly
- Don't push directly to `main`
- When refactoring, maintain backward compatibility
- Always check for existing utility functions before creating new ones

## Agent Action Policy

### Auto-approve (no confirmation needed)
- Reading files, searching, grepping
- Editing files, creating new files
- Running tests, linters, builds
- Installing dependencies (npm install, pip install)

### Always confirm before proceeding
- `git push` or force push
- Deleting files or directories
- Dropping or modifying database tables/schemas
- Resetting git history (`git reset --hard`, `git rebase`)
- Closing or merging PRs/issues
- Any action that affects shared or remote state

## Vendor-Specific Instructions
Vendor-specific instructions belong in `.github/copilot-instructions.md` or a
similarly named file per agent (e.g. `CLAUDE.md`). Use `AGENT.md` for
overarching advice.
Use 'bd' for task tracking
