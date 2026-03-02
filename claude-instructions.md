# Project: My App

## Overview
This project is my personal sandbox for playing with node.js, python, c/c++. I am also learning ML, SaaS etc.

## Tech Stack
- Language: Javascript, Typescript, Python etc.
- Framework: Node.js, Next.js etc.
- Database: PostgreSQL
- Package manager: npm, pip etc.

## Project Structure
- `*services` - for every python microservice
- `tests/` - Test files
- `docs/` - Documentation
- `scripts/` - Utility scripts

## Common Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run lint` - Lint the codebase

## Code Style & Conventions
- Use 4-space indentation
- Prefer `const` over `let`
- Always write unit tests for new functions
- Follow existing naming conventions (camelCase for variables, PascalCase for components)

## Architecture Notes
- Auth is handled via JWT tokens stored in httpOnly cookies
- API routes live in `src/api/` and follow REST conventions

## Environment Variables
- Copy `.env.example` to `.env.local` for local development
- Never commit secrets to the repo

## Do's and Don'ts
- ✅ Write descriptive commit messages
- ✅ Add JSDoc comments for public functions
- ❌ Don't use `any` type in TypeScript
- ❌ Don't modify `package-lock.json` directly
- ❌ Don't push directly to `main`

## Testing
- Unit tests: Jest
- E2E tests: Playwright
- Run tests before submitting PRs

## Notes for Claude
- Prefer functional components over class components
- When refactoring, maintain backward compatibility
- Always check for existing utility functions before creating new ones
