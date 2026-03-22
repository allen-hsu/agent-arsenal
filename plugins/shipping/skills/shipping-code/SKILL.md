---
name: shipping-code
description: >
  Fully automated ship workflow: detect and merge base branch, run tests, review diff
  for structural issues, split into bisectable commits, push, and create a PR with
  comprehensive body. Designed to be non-interactive -- the user says "ship" and the
  next thing they see is the PR URL. Use when (1) asked to "ship", "deploy", "push to
  main", "create a PR", or "merge and push", (2) code is described as ready or user
  asks about deploying, (3) a feature branch needs to be landed.
  Only stops for: merge conflicts, test failures, review findings needing judgment.
---

# Ship: Fully Automated Ship Workflow

You are running the `/ship` workflow. This is a **non-interactive, fully automated** workflow. Do NOT ask for confirmation at any step. The user said `/ship` which means DO IT. Run straight through and output the PR URL at the end.

**Only stop for:**
- On the base branch (abort)
- Merge conflicts that can't be auto-resolved (stop, show conflicts)
- Test failures (stop, show failures)
- Pre-landing review finds items that need user judgment

**Never stop for:**
- Uncommitted changes (always include them)
- Commit message approval (auto-commit)
- Multi-file changesets (auto-split into bisectable commits)
- Auto-fixable review findings (dead code, stale comments -- fixed automatically)
- Test coverage gaps (auto-generate and commit, or flag in PR body)

---

## Step 1: Pre-flight

1. **Detect the base branch:**
   ```bash
   gh repo view --json defaultBranchRef -q .defaultBranchRef.name
   ```
   If this fails, fall back to `main`.

2. Check the current branch. If on the base branch or the repo's default branch, **abort**: "You're on the base branch. Ship from a feature branch."

3. Run `git status` (never use `-uall`). Uncommitted changes are always included -- no need to ask.

4. Run `git diff <base>...HEAD --stat` and `git log <base>..HEAD --oneline` to understand what's being shipped.

---

## Step 2: Merge the Base Branch (BEFORE tests)

Fetch and merge the base branch into the feature branch so tests run against the merged state:

```bash
git fetch origin <base> && git merge origin/<base> --no-edit
```

**If there are merge conflicts:** Try to auto-resolve if they are simple. If conflicts are complex or ambiguous, **STOP** and show them.

**If already up to date:** Continue silently.

---

## Step 2.5: Test Framework Bootstrap

Check if the project has a test framework. Look for test config files (jest.config, vitest.config, pytest.ini, .rspec, Makefile with test target, etc.) and test directories. If no test framework is detected, suggest setting one up -- but do not block shipping.

---

## Step 3: Run Tests (on merged code)

Detect the project's test runner and run tests:

```bash
# Examples -- adapt to the project:
# npm test / yarn test / pnpm test
# pytest / python -m pytest
# bundle exec rspec / bin/rails test
# go test ./...
# cargo test
```

Run all available test suites. If multiple exist, run them in parallel where possible.

**If any test fails:** Show the failures and **STOP**. Do not proceed.

**If all pass:** Continue silently -- just note the counts briefly.

---

## Step 3.4: Test Coverage Audit

Evaluate what was ACTUALLY coded (from the diff), not what was planned.

1. **Trace every codepath changed** using `git diff origin/<base>...HEAD`:
   - Read every changed file. For each one, trace how data flows through the code.
   - Map every conditional branch, error path, and edge case.

2. **Check each branch against existing tests.** For each path, search for a test that exercises it.

3. **Output ASCII coverage diagram:**
   ```
   [+] src/services/billing.ts
       ├── processPayment()
       │   ├── [TESTED] Happy path -- billing.test.ts:42
       │   └── [GAP]    Network timeout -- NO TEST
       └── refundPayment()
           └── [TESTED] Full refund -- billing.test.ts:89

   COVERAGE: 2/3 paths tested (67%)
   GAPS: 1 path needs tests
   ```

4. **Generate tests for uncovered paths** if test framework is available:
   - Read 2-3 existing test files to match conventions exactly
   - Generate unit tests with real assertions (not just "it renders")
   - Run each test. Passes -> commit as `test: coverage for {feature}`
   - Fails -> fix once. Still fails -> revert, note gap in diagram.
   - Caps: 30 code paths max, 20 tests generated max, 2-min per-test cap.

**Fast path:** All paths covered -> "Step 3.4: All new code paths have test coverage." Continue.

See `references/philosophy.md` for the Completeness Principle -- tests are the cheapest lake to boil.

---

## Step 3.5: Pre-Landing Review

Review the diff for structural issues that tests don't catch.

1. Run `git diff origin/<base>` to get the full diff.

2. Review for:
   - **SQL & data safety:** Raw SQL, missing transactions, N+1 queries, unindexed lookups
   - **Security:** Hardcoded secrets, missing auth checks, unvalidated input, XSS vectors
   - **Dead code:** Unused imports, unreachable branches, commented-out code
   - **Error handling:** Swallowed exceptions, missing error boundaries, silent failures
   - **Performance:** Unnecessary re-renders, missing memoization, large payloads
   - **Style:** Stale comments, inconsistent naming, TODO without issue reference

3. **Classify each finding as AUTO-FIX or ASK.**
   - AUTO-FIX: Dead code removal, stale comment cleanup, obvious style fixes
   - ASK: Security concerns, data safety issues, architectural decisions

4. **Auto-fix all AUTO-FIX items.** Output one line per fix:
   `[AUTO-FIXED] [file:line] Problem -> what you did`

5. **If ASK items remain,** present them to the user with recommended actions.

6. **After all fixes:** If any fixes were applied, commit and tell the user to run `/ship` again to re-test. If no fixes, continue.

---

## Step 4: Commit (Bisectable Chunks)

**Goal:** Create small, logical commits that work well with `git bisect`.

1. Analyze the diff and group changes into logical commits. Each commit should represent **one coherent change**.

2. **Commit ordering** (earlier commits first):
   - **Infrastructure:** migrations, config changes, route additions
   - **Models & services:** new models, services, concerns (with their tests)
   - **Controllers & views:** controllers, views, JS/React components (with their tests)

3. **Rules for splitting:**
   - A model and its test file go in the same commit
   - A service and its test file go in the same commit
   - Migrations are their own commit (or grouped with the model they support)
   - If the total diff is small (< 50 lines across < 4 files), a single commit is fine

4. **Each commit must be independently valid** -- no broken imports, no references to code that doesn't exist yet.

5. Compose each commit message: `<type>: <summary>` (type = feat/fix/chore/refactor/docs)

---

## Step 5: Verification Gate

**No completion claims without fresh verification evidence.**

Before pushing, re-verify if code changed during Steps 3.4-4:

1. **Test verification:** If ANY code changed after Step 3's test run, re-run the test suite. Stale output from Step 3 is NOT acceptable.
2. **Build verification:** If the project has a build step, run it.
3. **Rationalization prevention:**
   - "Should work now" -> RUN IT.
   - "I'm confident" -> Confidence is not evidence.
   - "It's a trivial change" -> Trivial changes break production.

**If tests fail here:** STOP. Do not push. Fix the issue and return to Step 3.

---

## Step 6: Push

Push to the remote with upstream tracking:

```bash
git push -u origin <branch-name>
```

---

## Step 7: Create PR

Create a pull request using `gh`:

```bash
gh pr create --base <base> --title "<type>: <summary>" --body "$(cat <<'EOF'
## Summary
<bullet points describing what changed and why>

## Test Coverage
<coverage diagram from Step 3.4, or "All new code paths have test coverage.">

## Pre-Landing Review
<findings from Step 3.5, or "No issues found.">

## Test plan
- [x] All tests pass (N tests, 0 failures)

Generated with Claude Code
EOF
)"
```

**Output the PR URL.**

---

## Rules

- **Never skip tests.** If tests fail, stop.
- **Never force push.** Use regular `git push` only.
- **Never ask for trivial confirmations** (e.g., "ready to push?", "create PR?").
- **Split commits for bisectability** -- each commit = one logical change.
- **Never push without fresh verification evidence.** If code changed after Step 3 tests, re-run before pushing.
- **The goal is: user says `/ship`, next thing they see is the PR URL.**

---

## Next Steps

After shipping, consider:
- **running-retro** to analyze what was shipped and engineering patterns
- **testing-qa** if the shipped code needs QA verification
