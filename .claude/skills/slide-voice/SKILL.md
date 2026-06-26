---
name: slide-voice
description: >-
  Anti-LLM voice check for QM 6700 lecture slides. Use when writing or revising ANY lecture-slide
  content, and ALWAYS as the last step before finalizing/committing a topic's slides. Strips AI-slop
  (sentences generic to any course, hype words, em-dash-aside overuse, emphatic-pivot pileups,
  grand-but-empty endings, pre-packaged symmetry) and enforces the course's concrete, case-anchored
  voice for entry-level MSBAIM students. Trigger phrases: "voice check", "anti-LLM pass", "de-slop",
  "make the slides sound human", "slide voice", "does this sound like AI".
---

# Slide-voice — Anti-LLM verification (mandatory, not cosmetic)

Adapted from Davi's anti-LLM rule for papers. Goal: slides read like a sharp instructor who knows
*this* case, not like a generated lecture. **The unit is "every text-bearing slide" (the paper's
"introduction"); the scope inside a slide is the sentence / bullet (the paper's "paragraph").**

## How to run it (procedure)
1. **Mechanical pass (deterministic):** run the linter on the topic's deck and fix every HARD flag:
   ```
   python3 .claude/hooks/slide_voice_lint.py lecture_slides/<NN>_chapter_<slug>/<NN>_chapter_<slug>.qmd
   ```
   (A PostToolUse hook also prints a short summary whenever a slide `.qmd` is edited.)
2. **Judgment pass (read every text slide):** apply the tests below the linter *cannot* run.
3. **Rewrite** each failing passage, anchoring it to the case (a number, a name, a decision, a tool).
4. **Re-render**, verify 0 overflow (print-PDF the changed slides), re-run the linter to confirm
   **0 HARD**, then commit + push + share the webpage link (per CLAUDE.md "Commit / push / share").
   The deck is **not finished until it passes all tests.**

## The tests
After writing, reread EVERY sentence of every text slide and apply:

1. **Generic-to-any-course.** Could this sentence sit on a slide in *any* business/stats course on
   *any* topic? If yes, rewrite it with content specific to *this* case — the Vungle A/B decision,
   the auto-parts chain, a real number ($3.46 vs $3.35), a named tool (Data Analysis ToolPak →
   Descriptive Statistics), a real consequence. *(Exception: a single, standard definition is fine
   if the very next line anchors it concretely.)*
2. **Does removing it lose information?** If a sentence/bullet can be deleted and the slide loses
   nothing, delete it. (Watch motivational filler: "data is everywhere", broad "where it's used" lists.)
3. **Em-dash asides.** Count em dashes (—) **per sentence**. The tell is the *paired aside*
   "X — like Y — Z"; reduce it to 0 or 1 (use commas, parentheses, or split the sentence).
   **Do NOT touch** the idiomatic one-dash bullet **`Term` — definition** — that is house style, not slop.
4. **Emphatic pivots.** Count essay pivots per slide (however, indeed, moreover, furthermore,
   notably, importantly, in fact, that said). If > 2, cut the excess. (Math connectors thus/hence/
   therefore are fine and not counted.)
5. **Grand-but-empty endings.** Does a slide end on something that *sounds* big but says nothing
   ("unlock the power of data", "the foundation of success")? Replace it with a concrete claim
   ("60 rows × 7 variables = 420 values you can name").
6. **Pre-packaged symmetry.** Break suspiciously balanced constructions ("not only X but also Y",
   "isn't just X, it's Y", rule-of-three for cadence). **Keep** legitimate teaching contrasts
   (categorical vs. quantitative, descriptive vs. inferential) — those earn their symmetry.
7. **Hype / AI tells.** Delete: leverage, unlock, seamless, robust, powerful, delve, "the power of",
   "in today's data-driven world", "when it comes to", "it's worth noting", tapestry, realm,
   game-changer, empower, elevate. Say the plain thing instead.

## Voice target (entry-level MSBAIM)
Lead with the decision; define terms on first use; assume no prior statistics; concrete before
abstract; professional but plain. A good test: every claim should point at the data or the decision.

## Also enforced here: student ROLE (CLAUDE.md #8)
The student is the **decision-maker** — always **"the manager"** (never "CEO" or "owner", Davi 2026-06-26), **never the analyst**. The linter HARD-flags
"you're the analyst" / "work as the analyst" / titles like "You're the Analyst", and soft-flags "like
an analyst" / "as an analyst" addressed to students. Frame the Team Sprint as the *management team*
reproducing and interrogating an analyst's proposal, then deciding — deliverable = a call + an
evaluation of the analysis, not "our analysis".
