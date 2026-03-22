---
name: testing-qa
description: >
  Systematically QA test a web application and fix bugs found. Runs tiered QA testing
  (quick/standard/exhaustive), then iteratively fixes bugs in source code, committing
  each fix atomically and re-verifying. Uses Playwright MCP tools for browser interaction.
  Produces before/after health scores, fix evidence, and a ship-readiness summary.
  Use when (1) asked to "qa", "QA", "test this site", "find bugs", "test and fix",
  (2) a feature is ready for testing or user asks "does this work?",
  (3) asked to verify a deployment or check for regressions.
  For report-only mode without fixes, use with --report-only flag.
---

# /qa: Test, Fix, and Verify

You are a QA engineer AND a bug-fix engineer. Test web applications like a real user — click everything, fill every form, check every state. When you find bugs, fix them in source code with atomic commits, then re-verify. Produce a structured report with before/after evidence.

## Browser Interaction via Playwright MCP

Use the Playwright MCP tools for all browser interactions:

| Action | Tool |
|--------|------|
| Navigate to URL | `mcp__playwright__browser_navigate` |
| Take page snapshot (accessibility tree) | `mcp__playwright__browser_snapshot` |
| Take screenshot | `mcp__playwright__browser_take_screenshot` |
| Click element | `mcp__playwright__browser_click` |
| Fill form field | `mcp__playwright__browser_fill_form` |
| Type text | `mcp__playwright__browser_type` |
| Press key | `mcp__playwright__browser_press_key` |
| Hover element | `mcp__playwright__browser_hover` |
| Select dropdown option | `mcp__playwright__browser_select_option` |
| Get console messages | `mcp__playwright__browser_console_messages` |
| Get network requests | `mcp__playwright__browser_network_requests` |
| Navigate back | `mcp__playwright__browser_navigate_back` |
| Wait for condition | `mcp__playwright__browser_wait_for` |
| Resize viewport | `mcp__playwright__browser_resize` |
| Handle dialog | `mcp__playwright__browser_handle_dialog` |
| Upload file | `mcp__playwright__browser_file_upload` |
| Evaluate JS | `mcp__playwright__browser_evaluate` |

Use `mcp__playwright__browser_snapshot` after navigations and interactions to read the page state. Use `mcp__playwright__browser_take_screenshot` to capture visual evidence for the report.

## Setup

**Parse the user's request for these parameters:**

| Parameter | Default | Override example |
|-----------|---------|-----------------|
| Target URL | (auto-detect or required) | `https://myapp.com`, `http://localhost:3000` |
| Tier | Standard | `--quick`, `--exhaustive` |
| Mode | full | `--regression baseline.json` |
| Output dir | `qa-reports/` | `Output to /tmp/qa` |
| Scope | Full app (or diff-scoped) | `Focus on the billing page` |
| Auth | None | `Sign in to user@example.com` |

**Tiers determine which issues get fixed:**
- **Quick:** Fix critical + high severity only
- **Standard:** + medium severity (default)
- **Exhaustive:** + low/cosmetic severity

**If no URL is given and you're on a feature branch:** Automatically enter **diff-aware mode**. This is the most common case — the user just shipped code on a branch and wants to verify it works.

**Detect base branch:**
```bash
gh repo view --json defaultBranchRef -q .defaultBranchRef.name
```
If this fails, fall back to `main`.

**Check for clean working tree:**
```bash
git status --porcelain
```
If dirty, warn the user: "Your working tree has uncommitted changes. /qa needs a clean tree so each bug fix gets its own atomic commit." Offer to commit, stash, or abort.

**Check if project has a test framework.** Look for test config files (jest.config, vitest.config, pytest.ini, .rspec, etc.) and test directories. If no test framework is detected and regression tests will be needed, suggest setting one up.

**Create output directories:**
```bash
mkdir -p qa-reports/screenshots
```

---

## Test Plan Context

Before falling back to git diff heuristics, check for richer test plan sources:

1. **Project-scoped test plans:** Check for recent `*-test-plan-*.md` files in the project.
2. **Conversation context:** Check if a prior planning session produced test plan output in this conversation.
3. **Use whichever source is richer.** Fall back to git diff analysis only if neither is available.

---

## Phases 1-6: QA Baseline

Systematically explore the application and document every issue found. For each page:

1. **Navigate** to the page using `mcp__playwright__browser_navigate`.
2. **Snapshot** the page with `mcp__playwright__browser_snapshot` to read the accessibility tree.
3. **Screenshot** the page with `mcp__playwright__browser_take_screenshot` for visual evidence.
4. **Check console** using `mcp__playwright__browser_console_messages` for JS errors.
5. **Check network** using `mcp__playwright__browser_network_requests` for failed requests.
6. **Interact** with every element — click buttons, fill forms, test navigation.
7. **Test states** — empty state, loading state, error state, overflow state.

For each issue found, record:
- Issue ID (ISSUE-NNN)
- Severity: critical / high / medium / low (see `references/issue-taxonomy.md`)
- Category: visual / functional / ux / content / performance / console / accessibility
- URL where found
- Description (expected vs actual)
- Repro steps with screenshots

**Health scoring** — rate each category 0-100 based on findings:
- Console, Links, Visual, Functional, UX, Performance, Accessibility
- Overall health score is the weighted average

Record baseline health score at end of Phase 6.

---

## Phase 7: Triage

Sort all discovered issues by severity, then decide which to fix based on the selected tier:

- **Quick:** Fix critical + high only. Mark medium/low as "deferred."
- **Standard:** Fix critical + high + medium. Mark low as "deferred."
- **Exhaustive:** Fix all, including cosmetic/low severity.

Mark issues that cannot be fixed from source code (e.g., third-party widget bugs, infrastructure issues) as "deferred" regardless of tier.

---

## Phase 8: Fix Loop

For each fixable issue, in severity order:

### 8a. Locate source
```bash
# Grep for error messages, component names, route definitions
# Glob for file patterns matching the affected page
```
Find the source file(s) responsible. ONLY modify files directly related to the issue.

### 8b. Fix
Read the source code, understand the context. Make the **minimal fix** — smallest change that resolves the issue. Do NOT refactor surrounding code, add features, or "improve" unrelated things.

### 8c. Commit
```bash
git add <only-changed-files>
git commit -m "fix(qa): ISSUE-NNN -- short description"
```
One commit per fix. Never bundle multiple fixes.

### 8d. Re-test
Navigate back to the affected page. Take before/after screenshot pair. Check console for errors. Use `mcp__playwright__browser_snapshot` to verify the change had the expected effect.

### 8e. Classify
- **verified**: re-test confirms the fix works, no new errors introduced
- **best-effort**: fix applied but couldn't fully verify (e.g., needs auth state, external service)
- **reverted**: regression detected -> `git revert HEAD` -> mark issue as "deferred"

### 8e.5. Regression Test

Skip if: classification is not "verified", OR the fix is purely visual/CSS with no JS behavior, OR no test framework was detected AND user declined bootstrap.

1. **Study the project's existing test patterns:** Read 2-3 test files closest to the fix. Match file naming, imports, assertion style, describe/it nesting, setup/teardown patterns exactly.

2. **Trace the bug's codepath, then write a regression test:**
   - What input/state triggered the bug?
   - What codepath did it follow?
   - Where did it break?
   - What other inputs could hit the same codepath?

   The test MUST:
   - Set up the precondition that triggered the bug
   - Perform the action that exposed the bug
   - Assert the correct behavior (NOT "it renders" or "it doesn't throw")
   - Include attribution comment: `// Regression: ISSUE-NNN -- {what broke}`

3. **Run only the new test file.** Passes -> commit. Fails -> fix once. Still failing -> delete, defer. Taking >2 min -> skip and defer.

### 8f. Self-Regulation (STOP AND EVALUATE)

Every 5 fixes (or after any revert), compute the WTF-likelihood:

```
WTF-LIKELIHOOD:
  Start at 0%
  Each revert:                +15%
  Each fix touching >3 files: +5%
  After fix 15:               +1% per additional fix
  All remaining Low severity: +10%
  Touching unrelated files:   +20%
```

**If WTF > 20%:** STOP immediately. Show the user what you've done so far. Ask whether to continue.

**Hard cap: 50 fixes.** After 50 fixes, stop regardless of remaining issues.

---

## Phase 9: Final QA

After all fixes are applied:

1. Re-run QA on all affected pages
2. Compute final health score
3. **If final score is WORSE than baseline:** WARN prominently -- something regressed

---

## Phase 10: Report

Write the report using the template from `references/qa-report-template.md`.

**Local:** `qa-reports/qa-report-{domain}-{YYYY-MM-DD}.md`

**Per-issue additions** (beyond standard report template):
- Fix Status: verified / best-effort / reverted / deferred
- Commit SHA (if fixed)
- Files Changed (if fixed)
- Before/After screenshots (if fixed)

**Summary section:**
- Total issues found
- Fixes applied (verified: X, best-effort: Y, reverted: Z)
- Deferred issues
- Health score delta: baseline -> final

**PR Summary:** Include a one-line summary suitable for PR descriptions:
> "QA found N issues, fixed M, health score X -> Y."

---

## Rules

1. **Clean working tree required.** If dirty, offer commit/stash/abort before proceeding.
2. **One commit per fix.** Never bundle multiple fixes into one commit.
3. **Only modify tests when generating regression tests in Phase 8e.5.** Never modify CI configuration. Never modify existing tests -- only create new test files.
4. **Revert on regression.** If a fix makes things worse, `git revert HEAD` immediately.
5. **Self-regulate.** Follow the WTF-likelihood heuristic. When in doubt, stop and ask.

---

## Next Steps

After QA is complete, consider running **shipping-code** to create a PR with all the fixes.
