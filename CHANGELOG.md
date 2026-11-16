# Changelog

## 0.5.0 — 2026-11-16
- **Stays with your project:** after an interview in a project, a later session there offers once a short practice round on the new work, when 5+ commits (or 10+ changed files) piled up since your last report. It never starts an interview by itself. Turn it off with `/mock-interview watch off`.

## 0.4.0 — 2026-11-16
- **Asks about the code as it is now:** re-reads code right before every question about it, records the code version in the report, and the next interview finds what changed since then and asks about the new work (and about fixed weak spots).

## 0.3.1 — 2026-11-14
- Works in **Codex** too: agent-neutral instructions (file tools in Claude Code, read-only shell with `.env` excluded in Codex), `$skill` commands in Codex, numbered-list questions when there's no question tool. Install steps for Codex in the README.

All notable changes to this project. Downloads and notes for each version: [Releases](https://github.com/Aleksa5000/mock-interview/releases).

## 0.3.0 — 2026-11-13
- Job ad mode: paste a job ad to get questions for every must-have requirement, a job match table (shown / partial / gap), the top 3 things to prepare and a fit pitch.
- Progress tracking: reads earlier reports, includes your weakest categories, and shows a before/after table. `/mock-interview retry` re-asks questions scored 3 or less.
- New focus category **Code & algorithms**: questions quote real snippets from your project and ask you to explain key lines, trace an algorithm with an input, give the complexity, spot edge cases or a bug.

## 0.2.0 — 2026-11-13
- Feedback system: GitHub issue forms (feedback, bug, idea), Discussions, and a one-time prefilled feedback link at the end of each interview (nothing is sent automatically).

## 0.1.1 — 2026-11-13
- Plugin icon (PNG) and SVG logo, animated demo GIF in README.

## 0.1.0 — 2026-11-13
- First release: project-aware mock interviews, Practice/Realistic modes, 8 question categories, 1–5 scoring with stronger model answers, Markdown reports.
