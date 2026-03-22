---
name: reviewing-code
description: >
  Pre-landing PR code review. Analyzes the diff against the base branch for SQL safety,
  LLM trust boundary violations, race conditions, conditional side effects, and other
  structural issues that tests do not catch. Uses a two-pass review (critical then
  informational) with fix-first methodology. Use when (1) asked to "review this PR",
  "code review", or "pre-landing review", (2) user is about to merge or land code changes,
  (3) user wants a structural check of their diff before shipping.
---

# Pre-Landing PR Review

Analyze the current branch's diff against the base branch for structural issues that tests don't catch.

## Detect Base Branch

Detect the base branch for comparison:

```bash
gh repo view --json defaultBranchRef -q .defaultBranchRef.name
```

Fallback to `main` if the command fails or no remote is configured.

---

## Step 1: Check Branch

1. Run `git branch --show-current` to get the current branch.
2. If on the base branch, output: **"Nothing to review -- you're on the base branch or have no changes against it."** and stop.
3. Run `git fetch origin <base> --quiet && git diff origin/<base> --stat` to check if there's a diff. If no diff, output the same message and stop.

---

## Step 1.5: Scope Drift Detection

Before reviewing code quality, check: **did they build what was requested -- nothing more, nothing less?**

1. Read `TODOS.md` (if it exists). Read PR description (`gh pr view --json body --jq .body 2>/dev/null || true`).
   Read commit messages (`git log origin/<base>..HEAD --oneline`).
   **If no PR exists:** rely on commit messages and TODOS.md for stated intent.
2. Identify the **stated intent** -- what was this branch supposed to accomplish?
3. Run `git diff origin/<base> --stat` and compare the files changed against the stated intent.
4. Evaluate with skepticism:

   **SCOPE CREEP detection:**
   - Files changed that are unrelated to the stated intent
   - New features or refactors not mentioned in the plan
   - "While I was in there..." changes that expand blast radius

   **MISSING REQUIREMENTS detection:**
   - Requirements from TODOS.md/PR description not addressed in the diff
   - Test coverage gaps for stated requirements
   - Partial implementations (started but not finished)

5. Output:
   ```
   Scope Check: [CLEAN / DRIFT DETECTED / REQUIREMENTS MISSING]
   Intent: <1-line summary of what was requested>
   Delivered: <1-line summary of what the diff actually does>
   [If drift: list each out-of-scope change]
   [If missing: list each unaddressed requirement]
   ```

6. This is **INFORMATIONAL** -- does not block the review. Proceed to Step 2.

---

## Step 2: Read the Checklist

Read [references/review-checklist.md](references/review-checklist.md).

**If the file cannot be read, STOP and report the error.** Do not proceed without the checklist.

---

## Step 3: Get the Diff

Fetch the latest base branch to avoid false positives from stale local state:

```bash
git fetch origin <base> --quiet
```

Run `git diff origin/<base>` to get the full diff. This includes both committed and uncommitted changes against the latest base branch.

---

## Step 4: Two-Pass Review

Apply the checklist against the diff in two passes:

1. **Pass 1 (CRITICAL):** SQL & Data Safety, Race Conditions & Concurrency, LLM Output Trust Boundary, Enum & Value Completeness
2. **Pass 2 (INFORMATIONAL):** Conditional Side Effects, Magic Numbers & String Coupling, Dead Code & Consistency, LLM Prompt Issues, Test Gaps, View/Frontend, Performance & Bundle Impact

**Enum & Value Completeness requires reading code OUTSIDE the diff.** When the diff introduces a new enum value, status, tier, or type constant, use Grep to find all files that reference sibling values, then Read those files to check if the new value is handled. This is the one category where within-diff review is insufficient.

**Search-before-recommending:** When recommending a fix pattern (especially for concurrency, caching, auth, or framework-specific behavior):
- Verify the pattern is current best practice for the framework version in use
- Check if a built-in solution exists in newer versions before recommending a workaround
- Verify API signatures against current docs (APIs change between versions)

Follow the output format specified in the checklist. Respect the suppressions -- do NOT flag items listed in the "DO NOT flag" section.

---

## Step 4.5: Design Review (Conditional)

If the diff touches frontend files, apply [references/design-checklist.md](references/design-checklist.md).

Include any design findings alongside the findings from Step 4. They follow the same Fix-First flow in Step 5 -- AUTO-FIX for mechanical CSS fixes, ASK for everything else.

---

## Step 5: Fix-First Review

**Every finding gets action -- not just critical ones.**

Output a summary header: `Pre-Landing Review: N issues (X critical, Y informational)`

### Step 5a: Classify Each Finding

For each finding, classify as AUTO-FIX or ASK per the Fix-First Heuristic in the review checklist. Critical findings lean toward ASK; informational findings lean toward AUTO-FIX.

### Step 5b: Auto-Fix All AUTO-FIX Items

Apply each fix directly. For each one, output a one-line summary:
`[AUTO-FIXED] [file:line] Problem -> what you did`

### Step 5c: Batch-Ask About ASK Items

If there are ASK items remaining, present them together:

- List each item with a number, the severity label, the problem, and a recommended fix
- For each item, provide options: A) Fix as recommended, B) Skip
- Include an overall RECOMMENDATION

Example format:
```
I auto-fixed 5 issues. 2 need your input:

1. [CRITICAL] app/models/post.rb:42 -- Race condition in status transition
   Fix: Add `WHERE status = 'draft'` to the UPDATE
   -> A) Fix  B) Skip

2. [INFORMATIONAL] app/services/generator.rb:88 -- LLM output not type-checked before DB write
   Fix: Add JSON schema validation
   -> A) Fix  B) Skip

RECOMMENDATION: Fix both -- #1 is a real race condition, #2 prevents silent data corruption.
```

If 3 or fewer ASK items, you may use individual questions instead of batching.

### Step 5d: Apply User-Approved Fixes

Apply fixes for items where the user chose "Fix." Output what was fixed.

If no ASK items exist (everything was AUTO-FIX), skip the question entirely.

### Verification of Claims

Before producing the final review output:
- If you claim "this pattern is safe" -> cite the specific line proving safety
- If you claim "this is handled elsewhere" -> read and cite the handling code
- If you claim "tests cover this" -> name the test file and method
- Never say "likely handled" or "probably tested" -- verify or flag as unknown

---

## Step 5.5: TODOS Cross-Reference

Read `TODOS.md` in the repository root (if it exists). Cross-reference the PR against open TODOs:

- **Does this PR close any open TODOs?** If yes, note which items: "This PR addresses TODO: <title>"
- **Does this PR create work that should become a TODO?** If yes, flag it as an informational finding.
- **Are there related TODOs that provide context for this review?** If yes, reference them.

If TODOS.md doesn't exist, skip this step silently.

---

## Step 5.6: Documentation Staleness Check

Cross-reference the diff against documentation files. For each `.md` file in the repo root (README.md, ARCHITECTURE.md, CONTRIBUTING.md, CLAUDE.md, etc.):

1. Check if code changes in the diff affect features, components, or workflows described in that doc file.
2. If the doc file was NOT updated in this branch but the code it describes WAS changed, flag it as an INFORMATIONAL finding:
   "Documentation may be stale: [file] describes [feature/component] but code changed in this branch."

This is informational only -- never critical. If no documentation files exist, skip this step silently.

---

## Important Rules

- **Read the FULL diff before commenting.** Do not flag issues already addressed in the diff.
- **Fix-first, not read-only.** AUTO-FIX items are applied directly. ASK items are only applied after user approval. Never commit, push, or create PRs -- that is a separate workflow.
- **Be terse.** One line problem, one line fix. No preamble.
- **Only flag real problems.** Skip anything that's fine.

---

## Next Steps

After completing the code review:

- Run the **shipping-code** workflow to create the PR and land the changes.
- Run the **investigating-bugs** skill if the review surfaces bugs that need root cause analysis.
