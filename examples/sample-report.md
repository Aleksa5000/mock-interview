# Mock Interview Report

- **Date:** 2026-11-13 18:40
- **Role / level:** Junior Full-stack
- **Mode:** Practice · **Length:** Quick
- **Project:** `shopnest` — Next.js + Supabase e-commerce demo with Stripe checkout

## Summary

**Overall score:** 3.2/5 · **Hiring signal:** Lean hire. You know what your app does and communicate clearly, but you're shaky on *why* the code works and on failure cases.

| Category | Score |
|---|---|
| Project deep-dive | 3.0 |
| AI-assisted coding | 3.0 |
| Technical fundamentals | 4.0 |
| Behavioral | 3.0 |
| Live coding | 3.0 |

### Top 3 strengths
1. Clear, friendly two-minute project pitch.
2. Solid understanding of React state vs props.
3. Honest about what you didn't know, instead of bluffing.

### Top 3 things to practice
1. Failure handling: timeouts, retries, webhooks, logging.
2. Explaining AI-generated code line by line (`lib/cart.ts`).
3. STAR structure: say what *you* did and give a measurable result.

### Study plan
- **Stripe webhooks and idempotency:** read the Stripe "fulfill orders" guide, then add a webhook handler to the project.
- **Error handling in fetch/async code:** practice `try/catch`, timeouts with `AbortController`, and user-facing error states.
- **STAR answers:** write 3 stories (hardest bug, a mistake, learning something fast) in STAR format and say each out loud in under 2 minutes.
- **Retry these questions:** Q2, Q3, Q5

---

## Questions & feedback

### Q1 · Warm-up: 4/5
**Question:** Walk me through this project in two minutes.

**Your answer (summary):** An online shop where users browse products, add them to a cart and pay with Stripe. Built with Next.js and Supabase, deployed on Vercel. You built it to learn full-stack development.

✅ **What was good:** Clear structure (what, who, stack, why) and a good length.
⚠️ **What was missing:** No mention of what *you* found hardest or are proudest of. That's the hook interviewers follow up on.
💬 **Stronger answer:**
> "Shopnest is an online store I built to learn full-stack development end to end. Users can browse products, keep a cart that survives refreshes, and pay with Stripe. It's Next.js with server routes, Supabase for auth and the database, and it's deployed on Vercel. The part I'm proudest of is the checkout flow, because I had to learn how payments and order states work."

💡 **Tip:** End your pitch with one thing you're proud of. It steers the next question to your strongest ground.

### Q2 · Project deep-dive: 2/5
**Question:** In `app/api/checkout/route.ts` you call Stripe directly. What happens if Stripe is slow or returns an error?

**Your answer (summary):** "It just shows an error to the user."

✅ **What was good:** You considered the user-facing effect.
⚠️ **What was missing:** No timeout, no logging, and the risk that the card is charged but the order is never saved.
💬 **Stronger answer:**
> "Right now the handler awaits Stripe with no timeout, so a failure becomes a 500. I'd add a timeout, log the error with the order ID, and show a clear retry message. Most importantly, I'd use Stripe webhooks as the source of truth, so the order is marked paid even if the original request failed after the charge."

💡 **Tip:** For "what if X fails" questions, cover three things: the user, the data, and how you'd find out.

### Q3 · AI-assisted coding: 3/5
**Question:** `lib/cart.ts` has a `mergeCarts` function. How do you know it's correct?

**Your answer (summary):** Claude wrote it; you tested it by adding items while logged out and then logging in, and it worked.

**Follow-up:** "What if the same product is in both carts?" → You weren't sure.

✅ **What was good:** You were honest about using AI and you did manual testing.
⚠️ **What was missing:** You couldn't explain the duplicate-item logic, and there are no automated tests for the edge cases.
💬 **Stronger answer:**
> "Claude drafted it, and I reviewed it before keeping it. It takes the guest cart from localStorage and the user's cart from the database and combines them. If the same product is in both, it adds up the quantities, capped at the stock limit. I tested that manually, but I'd add unit tests for the empty, duplicate and over-stock cases, because cart bugs cost money."

💡 **Tip:** For any AI-written function you might be asked about, be able to say what it takes in, what it returns, and one edge case it handles.

### Q4 · Technical fundamentals: 4/5
**Question:** What's the difference between props and state in React?

**Your answer (summary):** Props come from the parent and are read-only; state is owned by the component and changing it re-renders the component.

✅ **What was good:** Correct and concise.
⚠️ **What was missing:** An example from your own project would make it stick.
💬 **Stronger answer:**
> "Props are inputs passed from a parent and are read-only. State is data a component owns, and updating it triggers a re-render. In my app, `ProductCard` gets the product as a prop, while the quantity selector keeps the chosen quantity in state."

💡 **Tip:** Answer, then add "for example, in my project…". It proves you've actually used it.

### Q5 · Behavioral: 3/5
**Question:** Tell me about a time you were stuck for a long time.

**Your answer (summary):** Login didn't work after deploying to Vercel; after a few days you found the redirect URL was wrong in Supabase.

✅ **What was good:** A real, relevant story with a clear resolution.
⚠️ **What was missing:** No *process*: how you narrowed it down. No result or lesson.
💬 **Stronger answer:**
> "After my first deploy, login worked locally but failed on Vercel (Situation). I had to fix it before showing the project to a mentor (Task). I compared the network requests in both environments, saw the OAuth callback was going to localhost, and traced it to the redirect URL in Supabase and a missing env variable on Vercel (Action). Login worked after I fixed both. Now I keep a deploy checklist for env variables and auth URLs, and I haven't hit that issue again (Result)."

💡 **Tip:** Name the S, T, A, R parts in your head while answering, and spend most of the time on the Action.

---
*Generated by [mock-interview](https://github.com/Aleksa5000/mock-interview). Practice estimate, not a real hiring decision.*
