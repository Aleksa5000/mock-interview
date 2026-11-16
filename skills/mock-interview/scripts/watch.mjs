#!/usr/bin/env node
// mock-interview watch: after the first interview in a project, offer a short practice round once enough new
// work has piled up since the last report. Never starts an interview by itself. No dependencies.
// State: ~/.claude/mock-interview/state.json (MOCK_INTERVIEW_HOME overrides).
//
//   node watch.mjs hook            SessionStart hook (reads the hook JSON on stdin)
//   node watch.mjs on [path]       watch this project (call after saving a report)
//   node watch.mjs off [path]      stop the offers
//   node watch.mjs status          watched projects (JSON)
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join, resolve, sep } from "node:path";

const DIR = process.env.MOCK_INTERVIEW_HOME || join(homedir(), ".claude", "mock-interview");
const STATE = join(DIR, "state.json");
const MIN_COMMITS = 5, MIN_FILES = 10;
const SKIP = new Set([".git", "node_modules", ".venv", "venv", "dist", "build", "out", ".next", "__pycache__", "target", "vendor", "coverage", ".cache", "interview-reports"]);
const SRC = /\.(js|jsx|ts|tsx|mjs|cjs|py|go|rs|java|kt|swift|rb|php|cs|cpp|c|h|vue|svelte|html|css|scss|sql|prisma|dart|gradle|kts)$/i;
const SECRET = /(^|[\\/])(\.env[^\\/]*|.*\.(pem|key|p12)|credentials[^\\/]*|secrets?\.[^\\/]*)$/i;

const norm = (p) => { let r = resolve(p).split(sep).join("/"); if (/^[A-Z]:/.test(r)) r = r[0].toLowerCase() + r.slice(1); return r.replace(/\/+$/, ""); };
const load = () => { try { return JSON.parse(readFileSync(STATE, "utf8")); } catch { return { version: 1, projects: {} }; } };
const save = (s) => { mkdirSync(DIR, { recursive: true }); writeFileSync(STATE, JSON.stringify(s, null, 2)); };
const git = (cwd, ...a) => execFileSync("git", ["-C", cwd, ...a], { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"], timeout: 5000 }).trim();
const root = (d) => { try { return norm(git(d, "rev-parse", "--show-toplevel")); } catch { return null; } };
function find(state, dir) {
  const d = norm(dir);
  let best = null;
  for (const k of Object.keys(state.projects)) if ((d === k || d.startsWith(k + "/")) && (!best || k.length > best.length)) best = k;
  return best;
}
function latestReport(key) {
  const dir = join(key, "interview-reports");
  if (!existsSync(dir)) return null;
  const files = readdirSync(dir).filter((f) => /^mock-interview-.*\.md$/.test(f)).sort();
  return files.length ? join(dir, files[files.length - 1]) : null;
}
function countChanged(dir, since) {
  let n = 0, seen = 0;
  const walk = (d) => {
    if (n >= 50 || seen > 20000) return;
    let es; try { es = readdirSync(d, { withFileTypes: true }); } catch { return; }
    for (const e of es) {
      const f = join(d, e.name);
      if (e.isDirectory()) { if (!SKIP.has(e.name) && !e.name.startsWith(".")) walk(f); }
      else if (e.isFile() && SRC.test(e.name) && !SECRET.test(f)) { seen++; try { if (statSync(f).mtimeMs > since) n++; } catch {} }
    }
  };
  walk(dir);
  return n;
}
function newWork(key) {
  const report = latestReport(key);
  if (!report) return null;
  const text = readFileSync(report, "utf8");
  const sha = (text.match(/\*\*Code version:\*\*\s*([0-9a-f]{7,40})/) || [])[1];
  const date = (text.match(/\*\*Date:\*\*\s*([0-9-]{10})/) || [])[1] || "";
  if (sha) {
    try {
      const log = git(key, "log", "--oneline", "--no-decorate", "-n", "30", `${sha}..HEAD`);
      const commits = log ? log.split("\n") : [];
      return { date, enough: commits.length >= MIN_COMMITS, what: `${commits.length} commit(s) since then: ${commits.slice(0, 5).join("; ")}`, signature: git(key, "rev-parse", "HEAD") };
    } catch {}
  }
  const n = countChanged(key, statSync(report).mtimeMs);
  return { date, enough: n >= MIN_FILES, what: `${n}${n >= 50 ? "+" : ""} changed source files since then`, signature: `files:${n}` };
}

const [cmd, arg] = process.argv.slice(2);
const state = load();
state.projects ||= {};

if (cmd === "hook") {
  try {
    let input = {};
    try { input = JSON.parse(readFileSync(0, "utf8") || "{}"); } catch {}
    const key = find(state, input.cwd || process.cwd());
    if (!key || state.projects[key].on === false) process.exit(0);
    const w = newWork(key);
    if (!w || !w.enough || state.projects[key].nudged === w.signature) process.exit(0);
    state.projects[key].nudged = w.signature;
    save(state);
    const ctx = `[mock-interview] ${"The user's own request always comes first: answer it or do it completely before anything below, and never let this note replace or shorten that answer. "}The user practised job interviews about this project (last report ${w.date}). A lot was built since: ${w.what}. ` +
      `After you answer the user's first message, add ONE short line in their language offering a quick 5-question practice round about the new work (/mock-interview, or $mock-interview in Codex). Ask only once, never start it without a yes, and don't bring it up again if they say no.`;
    process.stdout.write(JSON.stringify({ hookSpecificOutput: { hookEventName: "SessionStart", additionalContext: ctx } }));
  } catch {}
  process.exit(0);
}
if (cmd === "on") {
  const dir = arg || process.cwd();
  const key = find(state, dir) || root(dir) || norm(dir);
  state.projects[key] = { ...(state.projects[key] || {}), on: true, since: new Date().toISOString().slice(0, 10) };
  save(state);
  console.log(JSON.stringify({ ok: true, watching: key }));
} else if (cmd === "off") {
  const key = find(state, arg || process.cwd());
  if (key) { state.projects[key].on = false; save(state); }
  console.log(JSON.stringify({ ok: true, stopped: key }));
} else if (cmd === "status") {
  console.log(JSON.stringify({ stateFile: norm(STATE), projects: Object.fromEntries(Object.entries(state.projects).map(([k, v]) => [k, { ...v, newWork: newWork(k) }])) }, null, 2));
} else {
  console.error("usage: watch.mjs hook | on [path] | off [path] | status");
  process.exit(1);
}
