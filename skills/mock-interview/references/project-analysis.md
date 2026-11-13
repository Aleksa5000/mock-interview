# Project analysis

Goal: in a few minutes and with read-only tools, understand the project well enough to ask questions a real interviewer would ask after reading this repo on the candidate's CV. Keep it fast — don't read the whole codebase.

## Ground rules

- **Use the Read, Glob and Grep tools**, not shell commands like `cat`, `head`, `sed`, `find` or `wc`. They work on every OS and don't trigger permission prompts. Only use the shell for `git log` / `git status` / `git shortlog`.
- **Never open secrets:** `.env`, `.env.local`, `.env.production` (anything `.env*` except `.env.example` / `.env.sample`), `*.pem`, `*.key`, `id_rsa*`, `credentials*.json`, `secrets.*`, `*.p12`, cookie/session dumps, database files (`*.db`, `*.sqlite`) or backup folders. If you notice a secret file is committed to git, that is a good interview question ("How do you manage secrets?"); never quote its content.
- **Skip noise:** `node_modules/`, `.venv/`, `venv/`, `dist/`, `build/`, `.next/`, `__pycache__/`, `vendor/`, `target/`, lock files (only check they exist), binaries, images, datasets, office files.
- **Budget:** about 10–15 file reads total. Read the relevant part of a big file (use offset/limit or Grep), not the whole thing.

## 1. Scan (read-only)

1. **Top level:** list the root directory. Note monorepo signs (`apps/`, `packages/`, `pnpm-workspace.yaml`).
2. **README / docs:** read `README*` and anything like `docs/`, `ARCHITECTURE*`, `CLAUDE.md`, `AGENTS.md`. These say what the project is *supposed* to do.
3. **Manifests** (whichever exist): `package.json`, `pnpm-lock.yaml`/`yarn.lock`, `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `composer.json`, `Gemfile`, `*.csproj`, `pubspec.yaml`. Extract: language, framework, key libraries (DB/ORM, auth, state, UI, testing, AI SDKs).
4. **Infra & config:** `Dockerfile`, `docker-compose*`, `.github/workflows/`, `vercel.json`, `netlify.toml`, `.env.example`, DB schema/migrations (`prisma/schema.prisma`, `migrations/`, `supabase/`).
5. **History:** `git log --oneline -20` and `git shortlog -sn --all` (solo vs team). If it's not a git repo, skip this and consider asking "How do you version and back up this project?"
6. **Key files (3–6):** entry point, a core domain module, an API route/handler, a data model, and one test file if tests exist. Prefer files that show decisions (auth, payments, data fetching, state management, error handling).

7. **Key code and algorithms (2–4 pieces):** find the code that does what the project is *for*, plus any real algorithm: sorting/ranking, scheduling (e.g. spaced repetition), searching, scoring, parsing, retries/backoff, caching, rate limiting, recursion, pagination, date math, tricky regex or SQL. Grep for signals like `sort`, `reduce`, `while`, `score`, `rank`, `interval`, `retry`, `cache`, `Math.`, `parse`, `async`/`Promise.all` in source folders, always with `glob: "!**/.env*"`. Note `path:start-end`, what it does, its inputs, one concrete example input and expected result, its complexity, and an edge case. No real algorithm (plain CRUD)? Pick the main request handler and its trickiest lines.

## 2. Build the private project brief

Write down (for yourself, not shown to the user):

- **What it is:** one sentence.
- **Stack:** language, framework, DB, hosting, notable libs.
- **Architecture:** how the parts connect (client ↔ API ↔ DB ↔ external services).
- **Interesting decisions** (3–5): things worth asking "why?" about — e.g. chose Supabase over own backend, global state in Zustand, server actions instead of REST.
- **Key code** (2–4) from step 7: `path:lines`, what it does, an example input → output, complexity, an edge case. Source for "Code & algorithms" questions.
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

| "What is the time complexity of a sort?" | "Here's `pickNextCards` from `srs/scheduler.py:12-30`. What's its complexity, and when would it get slow?" |
| "What is an edge case?" | "What does `calculateTotal` (`cart.ts:40`) return if the cart is empty or a price is negative?" |

Always include at least one **"explain this code"** question that points at a specific function the user (or their AI) wrote, and one question about **a weak spot** — but phrase it as a discussion, not a trap.
