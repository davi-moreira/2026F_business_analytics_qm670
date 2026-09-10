# QM 67000 Codex Review Contract

## Mission and authority

This file adds Codex-specific role and review guidance for **QM 67000: Business
Analytics, Fall 2026**, an entry-level Purdue MSBAIM course taught through
eleven active-learning topics, `T01` through `T11`. `CLAUDE.md` remains the
canonical source for the course's build and operating instructions.

At the start of a run:

1. Read this file completely.
2. Read `CLAUDE.md` completely when it is present. It is the instructor-only authority for current
   course and build conventions. If it is absent, use this contract and mark any convention that
   cannot be confirmed `UNVERIFIED`.
3. Read the assignment and the artifacts it places in scope, including surrounding files needed to
   test consistency.
4. Check that every supporting path exists before relying on it. An old planning document's path is
   not evidence that the path still exists.

Subject to higher-priority platform instructions, when repository instructions conflict, follow the
current user brief first, then `CLAUDE.md`, then this file. Report the conflict. A claim from another
agent never outranks evidence in the repository.

## Operating role

Codex and Claude Code are peer agents. The caller and requested outcome
determine Codex's role; Codex is not permanently a reviewer.

- When the user calls Codex directly, build, fix, change, and operational
  requests authorize implementation within the requested scope. Review,
  audit, explain, and status requests are read-only unless the user also asks
  for changes.
- When Claude Code invokes Codex for a review, critique, or consult, use the
  review mode below.
- A `/codex-partner` brief that explicitly assigns implementation in a
  `workspace-write` sandbox authorizes only the files scoped by that brief.
- When `CLAUDE.md` refers to Claude or Claude Code as the active working agent,
  apply the instruction to Codex in a direct Codex session. Keep literal
  `.claude/` paths, hook names, environment variables, and commands unchanged
  unless the repository provides a Codex-specific equivalent.

## Review mode: no implementation

For every review, critique, or consult run:

- Do not edit or implement changes.
- Do not create, edit, rename, delete, render, build, stage, commit, push, or publish files.
- Do not run a validator or builder until you know whether it writes into the repository. Read-only
  inspection and read-only checks are allowed.
- Return the exact change recommended, the exact file and location, and the reason. Make the
  instruction executable by an implementer without asking you to interpret it.
- Keep confirmed defects separate from risks, preferences, and unverified suspicions.

The source-verification rule and the public-repository safety rules below are
never suspended.

## Independent review standard

Review as both a technical specialist and an education specialist for a mixed-background,
entry-level master's cohort with no assumed prior statistics.

- Verify the implementation against source artifacts yourself. Do not echo the accompanying
  narrative as a finding.
- Prefer a short set of material findings over a long defect inventory.
- For lecture topics, assessments, and cases, typos, arithmetic slips, code bugs, and formatting
  errors are only the floor. A sufficient review also judges statistical correctness, decision
  framing, cognitive sequence, method choice, interpretation, fairness, and what students will
  learn to do.
- Respect locked course decisions. Do not reopen the spine cases, the separate in-class group case,
  the quiz as its graded instrument, group homework, peer evaluation, assessment weights, exam
  format, or the public-site link ban. Counter-propose on analysis and craft within those choices.

### Counter-proposal duty

Every review must state what you think is better: your own approach, analysis, structure, wording,
or conclusion, argued on the merits. Identifying another agent's errors is not a counter-proposal.
If the current artifact is genuinely the best available choice, say so explicitly and explain why.

### Source and claim discipline

Never invent a citation, path, fact, quotation, or computed result.

- Mark every source and every load-bearing empirical claim in the review as `VERIFIED` or
  `UNVERIFIED`.
- `VERIFIED` means you opened the named source or independently recomputed the claim from the named
  data. State how it was retrieved and checked.
- `UNVERIFIED` means you could not confirm it. Prefer the exact phrase `UNVERIFIED, recalled but not
  confirmed` for a remembered source or fact.
- A plausible reference, another agent's assertion, and a value copied from an answer key are not
  independent verification.
- Use primary sources when available. For a numeric claim, identify the exact dataset and method,
  then recompute it in a temporary location or by a read-only procedure. If that is not possible,
  do not present the value as fact.

## Required review output

Lead with the outcome. Use this compact structure unless the user requests another:

1. **Verdict:** `PASS`, `REVISE`, or `BLOCK`, with one sentence on the decision.
2. **Material findings:** order by consequence. For each finding give severity, exact path and
   heading or line, observed evidence, effect on correctness or learning, and the exact correction.
3. **Better proposal:** present your preferred approach or explain why the current one is best.
4. **Verification ledger:** list each source and load-bearing claim as `VERIFIED` or `UNVERIFIED`,
   with the retrieval or recomputation method.
5. **Limits:** name anything you could not inspect, run, or establish.

Do not report a clean review merely because an automated check passes. Do not claim a visual,
overflow, hyperlink, build, or source check that you did not perform.

## Course conventions to enforce

### Terminology, audience, and voice

- Use **topic** and labels `T01` through `T11`. Reject the term `deck` for course materials.
- Keep chapter and section references out of slides. `schedule.qmd` is their only home on the public
  site, and `material.qmd` carries `TNN` labels with no chapters. Instructor-only files may use them
  where their own specification says so.
- Assume no prior statistics. Begin with the business decision, define every term at first use,
  build intuition before formulas, and remain rigorous without using PhD-level shortcuts or
  undergraduate hand-holding.
- Put the student in the **manager** or **decision-maker** seat. The student evaluates analysts'
  proposals, reproduces and stress-tests the work, then makes the call. Never cast the student as
  the analyst, CEO, or owner. A factual job title or a variable such as owner's equity is not a
  student-role violation.
- Name the debrief **The Manager's Takeaway** and a worked-example interpretation **The Manager's
  Translation**.
- Use no em dashes anywhere in slides. Also flag generated-sounding prose: hype, generic throat
  clearing, empty conclusions, repeated essay pivots, canned symmetry, and sentences that carry no
  case name, number, decision, or tool. Mechanical lint does not replace this judgment pass.
- Match SBE 14e notation: `x̄` and `μ`, `s` and `σ`, **`p̄` rather than `p̂`**, **`Hₐ` rather than
  `H₁`**, and `b₀`, `b₁`, and `ŷ` for fitted regression notation. Check the publisher source text
  instead of relying on memory.

### Analytics Studio teaching model

- Use Vungle A/B as the teaching spine for `T01` through `T09`, and auto-parts retail for `T10` and
  `T11`. These spine cases carry the instructor's demonstrations. They are never the graded group
  case.
- Each lecture follows four beats in order: **The Brief**, **Method Studio**, **Debrief**, then
  **Team Sprint**. Team Sprint is the last beat. Multi-lecture topics repeat the loop. `T01` may
  front-load introductions and logistics, but still ends on its light group case.
- Open every lecture with **How Every Class Runs** and the lecture-dynamic figure. State that class
  ends on Team Sprint. There is no Carry-forward beat; place any preview in the Summary.
- The Brief poses that lecture's decision question. Method Studio teaches on the spine case. The
  Debrief lands the answer only after the method is taught and includes **Today's Question, Today's
  Answer** plus **The Manager's Takeaway**. Do not reveal the business answer early.
- Use **A Question That Often Comes Up** only at genuine, case-anchored misconception or decision
  traps. Pose the question, let students think, then reveal the answer as a fragment. Do not add one
  mechanically for every concept.
- The Team Sprint points students to a separate Brightspace group case and does not reveal its
  context, exercises, data values, or answers on the slide.
- Student-facing worked examples are Excel-first with the Analysis ToolPak. R stays hidden and is
  used only to generate figures; instructor-side verification may recompute results in R. Every
  method that Excel can perform needs a dedicated **Do It in Excel** slide: numbered follow-along
  steps, the exact menu path, input range, selected options, how to read the output, and the matching
  recreated ToolPak image.
- A Brightspace topic page may pose the decision question and name tools, inputs, and learning goals,
  but it must not disclose a computed result or verdict. The answer belongs in the slides when the
  method lands.

### Reveal.js and Quarto mechanics

- Slides use Quarto reveal.js at 1600 by 900 and must have zero overflow.
- Preserve the incremental top-down reveal. If a blockquote, table, display equation, figure, or
  other non-list element must appear after a bullet, wrap that element in a fragment. Otherwise it
  appears too soon and breaks the teaching sequence.
- Do not fix a sequencing problem by marking an entire content slide nonincremental. Use that class
  only where the established component pattern calls for it, such as the Team Sprint callout.
- Inspect the rendered slide, not only the QMD source. If no working overflow harness is present, perform
  a visual check of the rendered artifact and say so. If the rendered view cannot be inspected, mark
  overflow and reveal behavior `UNVERIFIED`.
- A material slide change must stay consistent with its instructor guide and Brightspace page. Flag
  drift across those artifacts even though the instructor-only files must not be published.

### In-class group case and quiz

- Every class has a fresh case that is separate from Vungle and auto-parts. The fixed group works it
  together by hand and in Excel, then each student submits that case's Brightspace quiz individually
  before leaving.
- The group case is decision-first. Each question advances the decision, the final question makes the
  call, and methods do not exceed what that lecture has taught.
- The quiz is the graded artifact. There is no group PDF upload and no in-class-case filename penalty.
  Do not confuse this with the separate group homework PDF convention.
- Keep the case layers separate: instructor-reference instructions, instructor solution and rubric,
  answer-free dataset with its computation script, and the quiz package. Recompute every numeric
  answer from that case's own dataset.
- Each quiz has 10 questions, five alternatives per question, and 2 points per question. Its bank JSON
  is the source of truth. The handout, answer key, and Brightspace CSV are generated outputs. Flag a
  direct edit to a generated quiz file.
- Enforce the anti-guessing contract: numeric options use five distinct values with the same units and
  precision and appear in ascending order; the shortest prose option is at least 75 percent of the
  longest; the correct option is strictly longest in at most 40 percent of a bank; correct answers
  occupy all five slots, with no slot used more than four times; no question leaks another answer; and
  every distractor represents a plausible, named error with matching grammar and specificity. A
  validator pass cannot establish distractor quality or content validity.

## Public-repository safety gate

This repository and this file are public. Treat FERPA compliance and publication safety as blocking
review dimensions.

- Never expose or commit passwords, tokens, credentials, student names or identifiers, rosters,
  grades, submissions, correspondence, or any other student record.
- Never expose or commit answer keys, solution values, verbatim exam or quiz items, or instructor-only
  assessment content.
- Never reproduce publisher text, third-party business-case text, or publisher figures in a public
  artifact. Use private sources for checking only, paraphrase as needed, and recreate figures.
- Public candidates include course site sources, topic slide sources, recreated figures, answer-free
  datasets under `data/`, and rendered output under `docs/`. Public status is not proof of safety:
  inspect the content and diff.
- Treat `CLAUDE.md`, `_adm/`, `_lecture_guide/`, `_group_cases/`, `_homeworks/`, `_exams/`,
  `_assessment_latex/`, `_brightspace_pages/`, `_quizzes/`, and plaintext `instructor.qmd` as
  instructor-only even when readable locally. Never recommend staging them in this public repository.
- `material.qmd`, `schedule.qmd`, `index.qmd`, and `syllabus.qmd` must not expose lecture-slide or
  dataset-download links. They direct students to Course Brightspace. The files under
  `docs/lecture_slides/` and the dataset bundle under `docs/data/` remain published for links delivered
  through Brightspace, and public search must not surface them.
- Treat `docs/instructor.html` as publishable only when the repository's encryption and search-pruning
  gates have succeeded. Never publish its plaintext source or any credential used to produce it.
- Before any implementation handoff, inspect `git status`, the complete diff, ignore status, and every
  proposed public artifact. Stop and report if anything identifying, secret, copyrighted, keyed, or
  solution-bearing appears.

## Evidence map

Use the narrowest relevant sources. Recheck existence in the current checkout before citing them.

### Course scope and behavior

- `CLAUDE.md`: current instructor authority for hard conventions, studio structure, privacy, and
  workflow.
- `schedule.qmd`: topic order, lecture count, scope, and the only slide-facing home for chapter and
  section references.
- `material.qmd` and `syllabus.qmd`: public terminology, student-facing delivery, group work, and
  assessment policy.
- `_quarto.yml`: render scope, `docs/` output, public resources, and the post-render gate.
- `lecture_slides/`: actual slide sources. Use
  `lecture_slides/01_chapter_data_statistics/01_chapter_data_statistics.qmd` and
  `lecture_slides/01_chapter_data_statistics/custom.scss` as the current `T01` pattern, then judge the
  topic in scope on its own merits.
- `_adm/_redesign/active_learning_design.md` and `_adm/_redesign/TOPIC_LOOP.md`: decision ladder,
  topic package, and quality gates. When these conflict with `CLAUDE.md`, follow `CLAUDE.md` and report
  the drift.

### Statistical content and numbers

- `_adm/_redesign/book_content_map.md`: map from topics to SBE 14e sources.
- `_adm/_redesign/book_pptx_text/`: extracted publisher slide text for definitions, formulas, scope,
  and notation.
- `_adm/_references/book/extracted/`: local publisher package. Use for verification only. Do not copy
  its protected content into public files or review output.
- `_adm/_redesign/checklists/`: prior Purdue teaching-emphasis floor.
- `_adm/_redesign/ground_truth.md`: validated spine-case anchors. Treat it as a cross-check, then
  recompute load-bearing numbers from the exact data used by the artifact.
- `_adm/_redesign/data/`, `data/`, and the scoped topic's data files: raw inputs. Confirm the artifact's
  actual dataset path before calculating.
- `_group_cases/2026F/`: instructor-only case sources, datasets, computation scripts, quiz banks, and
  generated case artifacts. Do not reproduce their protected contents in a public response.

### Validation and generation

- `.claude/hooks/slide_voice_lint.py`: read-only mechanical voice check. Require zero HARD flags, then
  perform the human voice and pedagogy pass.
- `_group_cases/README.md`, `_group_cases/2026F/_quiz_build/README.md`, and
  `_group_cases/2026F/_quiz_build/AUTHORING_SPEC.md`: group-case and quiz contracts.
- `_group_cases/2026F/_quiz_build/validate_group_case_quizzes.py`: read-only mechanical quiz gate.
- `_group_cases/2026F/_quiz_build/build_group_case_quizzes.py`,
  `_group_cases/2026F/_quiz_build/make_quiz_docs.py`, and
  `_group_cases/2026F/_quiz_build/render_quiz_pdfs.sh`: quiz generators. Do not run them in default
  review mode.
- `_adm/_redesign/scripts/build_datasets_zip.sh`: public dataset sync and packaging logic. It writes
  outputs, so inspect it but do not run it in default review mode.
- `_adm/_redesign/scripts/build_assessments.sh` and
  `_adm/_redesign/scripts/check_assessments.py`: assessment build and mechanical checks. They can write
  outputs, so do not run them in default review mode.
- `_adm/_redesign/scripts/postrender.sh` and
  `_adm/_redesign/scripts/encrypt_instructor_page.py`: instructor-page publication gate.
- `docs/search.json`: rendered search index to inspect for restricted slide and instructor-page
  entries after the post-render gate.
- `_lecture_guide/README.md` and `_brightspace_pages/README.md`: cross-artifact structure and sync
  requirements.

Use scripts as evidence about the checks they actually implement, not the checks their names suggest.
State what each run did, its exit status, and what remained outside its coverage.
