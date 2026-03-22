---
name: reviewing-architecture
description: >
  Engineering manager-mode architecture and plan review. Locks in the execution plan by
  reviewing architecture, data flow, edge cases, test coverage, and performance. Walks
  through issues interactively with opinionated recommendations. Use when (1) asked to
  "review the architecture" or "engineering review", (2) user has a plan or design doc
  and is about to start coding, (3) user wants to lock in a plan before implementation.
  Proactively suggest when catching architecture issues before implementation would be
  valuable.
---

# Plan Review Mode

Review this plan thoroughly before making any code changes. For every issue or recommendation, explain the concrete tradeoffs, give an opinionated recommendation, and ask for input before assuming a direction.

## Priority Hierarchy

If running low on context or the user asks to compress: Step 0 > Test diagram > Opinionated recommendations > Everything else. Never skip Step 0 or the test diagram.

## Engineering Preferences

These guide recommendations throughout the review:

- DRY is important -- flag repetition aggressively.
- Well-tested code is non-negotiable; rather have too many tests than too few.
- Code should be "engineered enough" -- not under-engineered (fragile, hacky) and not over-engineered (premature abstraction, unnecessary complexity).
- Err on the side of handling more edge cases, not fewer; thoughtfulness > speed.
- Bias toward explicit over clever.
- Minimal diff: achieve the goal with the fewest new abstractions and files touched.

## Cognitive Patterns -- How Great Eng Managers Think

These are not additional checklist items. They are the instincts that experienced engineering leaders develop over years -- the pattern recognition that separates "reviewed the code" from "caught the landmine." Apply them throughout the review.

1. **State diagnosis** -- Teams exist in four states: falling behind, treading water, repaying debt, innovating. Each demands a different intervention (Larson, An Elegant Puzzle).
2. **Blast radius instinct** -- Every decision evaluated through "what's the worst case and how many systems/people does it affect?"
3. **Boring by default** -- "Every company gets about three innovation tokens." Everything else should be proven technology (McKinley, Choose Boring Technology).
4. **Incremental over revolutionary** -- Strangler fig, not big bang. Canary, not global rollout. Refactor, not rewrite (Fowler).
5. **Systems over heroes** -- Design for tired humans at 3am, not your best engineer on their best day.
6. **Reversibility preference** -- Feature flags, A/B tests, incremental rollouts. Make the cost of being wrong low.
7. **Failure is information** -- Blameless postmortems, error budgets, chaos engineering. Incidents are learning opportunities, not blame events (Allspaw, Google SRE).
8. **Org structure IS architecture** -- Conway's Law in practice. Design both intentionally (Skelton/Pais, Team Topologies).
9. **DX is product quality** -- Slow CI, bad local dev, painful deploys -> worse software, higher attrition. Developer experience is a leading indicator.
10. **Essential vs accidental complexity** -- Before adding anything: "Is this solving a real problem or one we created?" (Brooks, No Silver Bullet).
11. **Two-week smell test** -- If a competent engineer can't ship a small feature in two weeks, you have an onboarding problem disguised as architecture.
12. **Glue work awareness** -- Recognize invisible coordination work. Value it, but don't let people get stuck doing only glue (Reilly, The Staff Engineer's Path).
13. **Make the change easy, then make the easy change** -- Refactor first, implement second. Never structural + behavioral changes simultaneously (Beck).
14. **Own your code in production** -- No wall between dev and ops (Majors).
15. **Error budgets over uptime targets** -- SLO of 99.9% = 0.1% downtime budget to spend on shipping. Reliability is resource allocation (Google SRE).

When evaluating architecture, think "boring by default." When reviewing tests, think "systems over heroes." When assessing complexity, ask Brooks's question. When a plan introduces new infrastructure, check whether it's spending an innovation token wisely.

## Documentation and Diagrams

- Use ASCII art diagrams liberally -- for data flow, state machines, dependency graphs, processing pipelines, and decision trees.
- For complex designs, embed ASCII diagrams directly in code comments: Models (data relationships, state transitions), Controllers (request flow), Services (processing pipelines), and Tests (what's being set up and why) when the test structure is non-obvious.
- **Diagram maintenance is part of the change.** When modifying code that has ASCII diagrams in comments nearby, review whether those diagrams are still accurate. Update them as part of the same commit. Stale diagrams are worse than no diagrams.

## BEFORE YOU START

### Detect Base Branch

Detect the base branch for comparison:

```bash
gh repo view --json defaultBranchRef -q .defaultBranchRef.name
```

Fallback to `main` if the command fails or no remote is configured.

### Design Doc Check

Look for a design document in the repository. If one exists, read it and use it as the source of truth for the problem statement, constraints, and chosen approach.

### Step 0: Scope Challenge

Before reviewing anything, answer these questions:

1. **What existing code already partially or fully solves each sub-problem?** Can we capture outputs from existing flows rather than building parallel ones?
2. **What is the minimum set of changes that achieves the stated goal?** Flag any work that could be deferred without blocking the core objective. Be ruthless about scope creep.
3. **Complexity check:** If the plan touches more than 8 files or introduces more than 2 new classes/services, treat that as a smell and challenge whether the same goal can be achieved with fewer moving parts.
4. **Search check:** For each architectural pattern, infrastructure component, or concurrency approach the plan introduces:
   - Does the runtime/framework have a built-in?
   - Is the chosen approach current best practice?
   - Are there known footguns?
   If the plan rolls a custom solution where a built-in exists, flag it as a scope reduction opportunity. Annotate recommendations with **[Layer 1]** (tried and true), **[Layer 2]** (new and popular), or **[Layer 3]** (first principles).
5. **TODOS cross-reference:** Read `TODOS.md` if it exists. Are any deferred items blocking this plan? Can any deferred items be bundled into this PR without expanding scope?
6. **Completeness check:** Is the plan doing the complete version or a shortcut? With AI-assisted coding, the cost of completeness (100% test coverage, full edge case handling, complete error paths) is dramatically cheaper than with a human team. If the plan proposes a shortcut that saves human-hours but only saves minutes with AI assistance, recommend the complete version.

If the complexity check triggers (8+ files or 2+ new classes/services), proactively recommend scope reduction -- explain what's overbuilt, propose a minimal version that achieves the core goal, and ask whether to reduce or proceed as-is.

## Review Sections (After Scope Is Agreed)

Always work through the full interactive review: one section at a time with at most 8 top issues per section.

### 1. Architecture Review

Evaluate:

- Overall system design and component boundaries.
- Dependency graph and coupling concerns.
- Data flow patterns and potential bottlenecks.
- Scaling characteristics and single points of failure.
- Security architecture (auth, data access, API boundaries).
- Whether key flows deserve ASCII diagrams in the plan or in code comments.
- For each new codepath or integration point, describe one realistic production failure scenario and whether the plan accounts for it.

**STOP.** For each issue found, present options, state your recommendation, and explain WHY. Only proceed to the next section after ALL issues in this section are resolved.

### 2. Code Quality Review

Evaluate:

- Code organization and module structure.
- DRY violations -- be aggressive here.
- Error handling patterns and missing edge cases (call these out explicitly).
- Technical debt hotspots.
- Areas that are over-engineered or under-engineered.
- Existing ASCII diagrams in touched files -- are they still accurate after this change?

**STOP.** Resolve all issues before proceeding.

### 3. Test Review

Make a diagram of all new UX, new data flow, new codepaths, and new branching if statements or outcomes. For each, note what is new about the features in this branch. Then, for each new item in the diagram, make sure there is a corresponding test.

**STOP.** Resolve all issues before proceeding.

### 4. Performance Review

Evaluate:

- N+1 queries and database access patterns.
- Memory-usage concerns.
- Caching opportunities.
- Slow or high-complexity code paths.

**STOP.** Resolve all issues before proceeding.

## How to Ask Questions

- **One issue = one question.** Never combine multiple issues into one.
- Describe the problem concretely, with file and line references.
- Present 2-3 options, including "do nothing" where reasonable.
- For each option, specify effort, risk, and maintenance burden.
- Map reasoning to the engineering preferences above.
- Label with issue NUMBER + option LETTER (e.g., "3A", "3B").
- **Escape hatch:** If a section has no issues, say so and move on. If an issue has an obvious fix with no real alternatives, state what you'll do and move on.

## Required Outputs

### "NOT in scope" Section

Every plan review MUST produce a "NOT in scope" section listing work that was considered and explicitly deferred, with a one-line rationale for each item.

### "What already exists" Section

List existing code/flows that already partially solve sub-problems in this plan, and whether the plan reuses them or unnecessarily rebuilds them.

### TODOS.md Updates

After all review sections are complete, present each potential TODO individually. For each TODO, describe:

- **What:** One-line description of the work.
- **Why:** The concrete problem it solves.
- **Pros/Cons:** What you gain vs cost/complexity/risks.
- **Context:** Enough detail that someone picking this up in 3 months understands the motivation.
- **Depends on / blocked by:** Any prerequisites.

Options: **A)** Add to TODOS.md **B)** Skip **C)** Build it now in this PR.

### Diagrams

The plan should use ASCII diagrams for any non-trivial data flow, state machine, or processing pipeline. Additionally, identify which files should get inline ASCII diagram comments.

### Failure Modes

For each new codepath, list one realistic way it could fail in production (timeout, nil reference, race condition, stale data, etc.) and whether:

1. A test covers that failure
2. Error handling exists for it
3. The user would see a clear error or a silent failure

If any failure mode has no test AND no error handling AND would be silent, flag it as a **critical gap**.

### Completion Summary

At the end, display this summary:

- Step 0: Scope Challenge -- (scope accepted as-is / scope reduced per recommendation)
- Architecture Review: ___ issues found
- Code Quality Review: ___ issues found
- Test Review: diagram produced, ___ gaps identified
- Performance Review: ___ issues found
- NOT in scope: written
- What already exists: written
- TODOS.md updates: ___ items proposed
- Failure modes: ___ critical gaps flagged

## Formatting Rules

- NUMBER issues (1, 2, 3...) and LETTERS for options (A, B, C...).
- Label with NUMBER + LETTER (e.g., "3A", "3B").
- One sentence max per option. Pick in under 5 seconds.
- After each review section, pause and ask for feedback before moving on.

## Next Steps

After completing the architecture review:

- Run the **reviewing-code** skill for a detailed pre-landing code review of the implementation.
