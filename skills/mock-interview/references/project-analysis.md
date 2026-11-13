# Project analysis

Goal: in a few minutes and with read-only tools, understand the project well enough to ask questions a real interviewer would ask after reading this repo on the candidate's CV. Keep it fast — don't read the whole codebase.

## 1. Scan (read-only)

1. **Top level:** list the root directory. Note monorepo signs (`apps/`, `packages/`, `pnpm-workspace.yaml`).
2. **README / docs:** read `README*` and anything like `docs/`, `ARCHITECTURE*`, `CLAUDE.md`, `AGENTS.md`. These say what the project is *supposed* to do.
3. **Manifests** (whichever exist): `package.json`, `pnpm-lock.yaml`/`yarn.lock`, `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `composer.json`, `Gemfile`, `*.csproj`, `pubspec.yaml`. Extract: language, framework, key libraries (DB/ORM, auth, state, UI, testing, AI SDKs).
4. **Infra & config:** `Dockerfile`, `docker-compose*`, `.github/workflows/`, `vercel.json`, `netlify.toml`, `.env.example`, DB schema/migrations (`prisma/schema.prisma`, `migrations/`, `supabase/`).
5. **History:** `git log --oneline -20` and `git log --format='%an' | sort | uniq -c` (solo vs team). Skip if not a git repo.
6. **Key files (3–6):** entry point, a core domain module, an API route/handler, a data model, and one test file if tests exist. Prefer files that show decisions (auth, payments, data fetching, state management, error handling).

## 2. Build the private project brief

Write down (for yourself, not shown to the user):

- **What it is:** one sentence.
- **Stack:** language, framework, DB, hosting, notable libs.
- **Architecture:** how the parts connect (client ↔ API ↔ DB ↔ external services).
- **Interesting decisions** (3–5): things worth asking "why?" about — e.g. chose Supabase over own backend, global state in Zustand, server actions instead of REST.
- **Weak spots / risks** (2–4) with `file:line` where possible: missing input validation, secrets handling, no tests, no error handling around fetches, N+1 queries, no pagination, race conditions, no loading/error states, huge components.
- **Signs of AI-generated code** (neutral, never accusatory): inconsistent styles, unused code, over-generic helpers, comments explaining the obvious. Use them only to ask "walk me through this" questions — vibe coders must be able to explain their code.

## 3. Turn the brief into questions

For each category in the plan, prefer a project-grounded version over a generic one:

| Instead of… | Ask… |
|---|---|
| "What is authentication?" | "Walk me through what happens from the moment a user clicks *Log in* in your app until they see the dashboard." |
| "What is SQL injection?" | "In `api/search.ts` you build the query from user input — how do you make sure that's safe?" |
| "Explain state management." | "Why did you put the cart in a global store instead of local state?" |
| "How do you test code?" | "There are no tests for the payment flow. How would you know it still works after a refactor?" |
| "Design a URL shortener." | "Your app gets featured and traffic goes 100×. What breaks first, and what do you change?" |

Always include at least one **"explain this code"** question that points at a specific function the user (or their AI) wrote, and one question about **a weak spot** — but phrase it as a discussion, not a trap.
