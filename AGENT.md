# Agent guidance for Mentorlink repository

This document is vendor-neutral and provides general instructions for AI
assistants (Copilot, Claude, etc.) operating in the Mentorlink codebase.

- Respect the repository layout: multiple services, shared modules, and
  infrastructure code.
- For service-specific tasks, look inside the service folder first.
- Use small, self-contained changes; avoid cross-cutting refactors without
  explicit approval.
- When drafting plans, place them under `plans/` and commit them as part of
  repo history.
- Follow the SDLC workflow: requirements → design → code → tests. Wait for
  explicit approval before advancing stages.

Vendor-specific instructions belong in `.github/copilot-instructions.md` or a
similarly named file per agent (e.g. `claude-instructions.md`). Use
`AGENT.md` for overarching advice.
