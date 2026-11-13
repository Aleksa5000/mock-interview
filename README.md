# 🎤 mock-interview

**Practice job interviews about *your own* project, right in Claude Code.**

You built something, maybe with a lot of help from AI. Can you explain it to an interviewer? `mock-interview` reads your project, interviews you like a real hiring manager, scores every answer, shows you a stronger way to say it, and saves a report so you can track your progress.

Made for vibe coders, self-taught developers and anyone preparing for a developer job.

## ✨ What it does

- 🔍 **Reads your project.** It scans the README, manifests, git history and key files, then asks about *your* code ("Walk me through `useCart`", "Why Supabase instead of your own API?"). No project in the folder? It asks for your role and stack and runs a general interview.
- 🎯 **Covers what real interviews ask:**
  - Project deep-dive and "explain this code"
  - Technical fundamentals for your stack
  - Debugging scenarios
  - **AI-assisted coding** ("How do you verify code the AI wrote?")
  - System design, scaled to your level
  - Live coding (solved *without* AI)
  - Behavioral questions (STAR)
  - Culture fit and "Do you have questions for us?"
- 🧑‍🏫 **Two modes:**
  - **Practice** gives feedback after every answer.
  - **Realistic** runs without interruptions and gives the full debrief at the end.
- 📝 **Feedback on every answer:**
  - a 1–5 score
  - what was good and what was missing
  - 💬 a **stronger model answer** that uses your real project details
  - one concrete tip
- 📄 **A Markdown report** saved to `interview-reports/` with your overall score, hiring signal, strengths, weak spots and a study plan.
- 🌍 **Speaks your language.** It answers in whatever language you write in. Switch to English mid-interview to practice.

## 📦 Install

**Option A: as a plugin (recommended, gets updates)**

Inside Claude Code:
```
/plugin marketplace add Aleksa5000/mock-interview
/plugin install mock-interview@mock-interview
```

**Option B: copy the skill manually**
```bash
git clone https://github.com/Aleksa5000/mock-interview.git
# macOS / Linux
cp -r mock-interview/skills/mock-interview ~/.claude/skills/
# Windows (PowerShell)
Copy-Item -Recurse mock-interview\skills\mock-interview $HOME\.claude\skills\
```

Restart Claude Code after installing.

## 🚀 Usage

Open Claude Code in your project folder and run:
```
/mock-interview
```
(When installed as a plugin, the full name is `/mock-interview:mock-interview`.)

Or just say *"interview me for a junior frontend job"*.

You will pick:
- your **role and level** (e.g. Junior Full-stack)
- the **mode** (Practice or Realistic)
- the **length**: Quick (~5 questions), Standard (~10) or Full (~15)
- the **focus** areas

During the interview you can type `hint`, `skip`, `pause`, `switch mode` or `end`.

## 👀 Example

```
Question 3/10 · Project deep-dive
In app/api/checkout/route.ts you call Stripe directly from the request handler.
What happens if Stripe is slow or returns an error?

> i think it just shows an error to the user

Score: 2/5 · You noticed the user-facing effect, but not the system behavior.

✅ What was good: You thought about the user experience.
⚠️ What was missing: There's no timeout or retry, the error isn't logged, and if the
   request times out after Stripe charged the card, the order may never be saved.
💬 Stronger answer:
> "Right now the handler awaits Stripe with no timeout, so a slow response blocks the
> request and a failure just bubbles up as a 500. I'd add a timeout and log the error with
> the order ID, and show a clear retry message. More importantly, I'd rely on Stripe
> webhooks as the source of truth, so an order gets marked paid even if the original
> request failed after the charge went through."
💡 Tip: For "what if X fails" questions, cover the user, the data, and how you'd find out.
```

See a full sample report in [`examples/sample-report.md`](examples/sample-report.md).

## ❓ FAQ

**Does it change my code?** No. It only reads your project. The one file it writes is the report in `interview-reports/` (you may want to add that folder to `.gitignore`).

**Does it run my code?** No. It won't run builds, tests or installs unless you ask.

**Is the score a real hiring prediction?** No. It's a practice estimate to show you what to improve.

**Can I use it without a project?** Yes. It will ask for your role and stack.

## 🤝 Contributing

Ideas, new question categories and translations are welcome. Open an issue or PR.
The skill lives in [`skills/mock-interview/`](skills/mock-interview/):
- `SKILL.md` is the main flow
- `references/` holds the question bank, the scoring rubric, the project analysis steps and the report template

If this helped you prepare, please ⭐ the repo so more people can find it.

## License

[MIT](LICENSE) © Aleksa Djorovic
