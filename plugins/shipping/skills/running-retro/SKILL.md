---
name: running-retro
description: >
  Weekly engineering retrospective that analyzes commit history, work patterns,
  and code quality metrics with persistent history and trend tracking. Team-aware:
  breaks down per-person contributions with specific praise and growth areas.
  Supports configurable time windows and comparison mode. Use when (1) asked for a
  "weekly retro", "what did we ship", or "engineering retrospective", (2) at the end
  of a work week or sprint, (3) asked to compare engineering velocity across periods.
---

# /retro -- Weekly Engineering Retrospective

Generates a comprehensive engineering retrospective analyzing commit history, work patterns, and code quality metrics. Team-aware: identifies the user running the command, then analyzes every contributor with per-person praise and growth opportunities. Designed for a senior IC/CTO-level builder using Claude Code as a force multiplier.

## Detect Default Branch

Before gathering data, detect the repo's default branch name:
```bash
gh repo view --json defaultBranchRef -q .defaultBranchRef.name
```
If this fails, fall back to `main`. Use the detected name wherever the instructions say `origin/<default>` below.

---

## Arguments

- `/retro` -- default: last 7 days
- `/retro 24h` -- last 24 hours
- `/retro 14d` -- last 14 days
- `/retro 30d` -- last 30 days
- `/retro compare` -- compare current window vs prior same-length window
- `/retro compare 14d` -- compare with explicit window

Parse the argument to determine the time window. Default to 7 days if no argument given. All times should be reported in the user's **local timezone** (use the system default -- do NOT set `TZ`).

**Midnight-aligned windows:** For day (`d`) and week (`w`) units, compute an absolute start date at local midnight, not a relative string. For example, if today is 2026-03-18 and the window is 7 days: the start date is 2026-03-11. Use `--since="2026-03-11T00:00:00"` for git log queries. For hour (`h`) units, use `--since="N hours ago"`.

**Argument validation:** If the argument doesn't match a number followed by `d`, `h`, or `w`, the word `compare`, or `compare` followed by a valid window, show usage and stop.

---

## Step 1: Gather Raw Data

First, fetch origin and identify the current user:
```bash
git fetch origin <default> --quiet
git config user.name
git config user.email
```

The name returned by `git config user.name` is **"you"** -- the person reading this retro. All other authors are teammates.

Run ALL of these git commands in parallel (they are independent):

```bash
# 1. All commits with timestamps, subject, hash, author, files changed
git log origin/<default> --since="<window>" --format="%H|%aN|%ae|%ai|%s" --shortstat

# 2. Per-commit test vs production LOC breakdown with author
git log origin/<default> --since="<window>" --format="COMMIT:%H|%aN" --numstat

# 3. Commit timestamps for session detection and hourly distribution
git log origin/<default> --since="<window>" --format="%at|%aN|%ai|%s" | sort -n

# 4. Files most frequently changed (hotspot analysis)
git log origin/<default> --since="<window>" --format="" --name-only | grep -v '^$' | sort | uniq -c | sort -rn

# 5. PR numbers from commit messages
git log origin/<default> --since="<window>" --format="%s" | grep -oE '#[0-9]+' | sed 's/^#//' | sort -n | uniq | sed 's/^/#/'

# 6. Per-author file hotspots
git log origin/<default> --since="<window>" --format="AUTHOR:%aN" --name-only

# 7. Per-author commit counts
git shortlog origin/<default> --since="<window>" -sn --no-merges

# 8. Test file count
find . -name '*.test.*' -o -name '*.spec.*' -o -name '*_test.*' -o -name '*_spec.*' 2>/dev/null | grep -v node_modules | wc -l

# 9. Test files changed in window
git log origin/<default> --since="<window>" --format="" --name-only | grep -E '\.(test|spec)\.' | sort -u | wc -l
```

---

## Step 2: Compute Metrics

Calculate and present these metrics in a summary table:

| Metric | Value |
|--------|-------|
| Commits to main | N |
| Contributors | N |
| PRs merged | N |
| Total insertions | N |
| Total deletions | N |
| Net LOC added | N |
| Test LOC (insertions) | N |
| Test LOC ratio | N% |
| Active days | N |
| Detected sessions | N |
| Avg LOC/session-hour | N |
| Test Health | N total tests, M added this period |

Then show a **per-author leaderboard** immediately below:

```
Contributor         Commits   +/-          Top area
You (name)               32   +2400/-300   src/
alice                    12   +800/-150    app/services/
bob                       3   +120/-40     tests/
```

Sort by commits descending. The current user always appears first, labeled "You (name)".

---

## Step 3: Commit Time Distribution

Show hourly histogram in local time using bar chart:

```
Hour  Commits  ----------------
 00:    4      ####
 07:    5      #####
 ...
```

Identify and call out:
- Peak hours
- Dead zones
- Whether pattern is bimodal (morning/evening) or continuous
- Late-night coding clusters (after 10pm)

---

## Step 4: Work Session Detection

Detect sessions using **45-minute gap** threshold between consecutive commits. For each session report:
- Start/end time (local)
- Number of commits
- Duration in minutes

Classify sessions:
- **Deep sessions** (50+ min)
- **Medium sessions** (20-50 min)
- **Micro sessions** (<20 min, typically single-commit)

Calculate:
- Total active coding time (sum of session durations)
- Average session length
- LOC per hour of active time

---

## Step 5: Commit Type Breakdown

Categorize by conventional commit prefix (feat/fix/refactor/test/chore/docs). Show as percentage bar:

```
feat:     20  (40%)  ####################
fix:      27  (54%)  ###########################
refactor:  2  ( 4%)  ##
```

Flag if fix ratio exceeds 50% -- this signals a "ship fast, fix fast" pattern that may indicate review gaps.

---

## Step 6: Hotspot Analysis

Show top 10 most-changed files. Flag:
- Files changed 5+ times (churn hotspots)
- Test files vs production files in the hotspot list

---

## Step 7: PR Size Distribution

From commit diffs, estimate PR sizes and bucket them:
- **Small** (<100 LOC)
- **Medium** (100-500 LOC)
- **Large** (500-1500 LOC)
- **XL** (1500+ LOC)

---

## Step 8: Focus Score + Ship of the Week

**Focus score:** Percentage of commits touching the single most-changed top-level directory. Higher = deeper focused work. Lower = scattered context-switching. Report as: "Focus score: 62% (app/services/)"

**Ship of the week:** Auto-identify the single highest-LOC PR in the window. Highlight PR number, title, LOC changed, and why it matters (infer from commit messages and files touched).

---

## Step 9: Team Member Analysis

For each contributor (including the current user), compute:

1. **Commits and LOC** -- total commits, insertions, deletions, net LOC
2. **Areas of focus** -- which directories/files they touched most (top 3)
3. **Commit type mix** -- their personal feat/fix/refactor/test breakdown
4. **Session patterns** -- when they code (peak hours), session count
5. **Test discipline** -- their personal test LOC ratio
6. **Biggest ship** -- their single highest-impact commit or PR in the window

**For the current user ("You"):** Deepest treatment. Include session analysis, time patterns, focus score. Frame in first person.

**For each teammate:** Write 2-3 sentences covering what they worked on. Then:
- **Praise** (1-2 specific things): Anchor in actual commits. Not "great work" -- say exactly what was good.
- **Opportunity for growth** (1 specific thing): Frame as a leveling-up suggestion, not criticism. Anchor in data.

**If only one contributor (solo repo):** Skip team breakdown. The retro is personal.

**If there are Co-Authored-By trailers:** Parse them. Credit those authors alongside the primary author. Note AI co-authors (e.g., `noreply@anthropic.com`) but track as "AI-assisted commits" metric, not as team members.

---

## Step 10: Week-over-Week Trends (if window >= 14d)

If the time window is 14 days or more, split into weekly buckets and show trends:
- Commits per week (total and per-author)
- LOC per week
- Test ratio per week
- Fix ratio per week
- Session count per week

---

## Step 11: Streak Tracking

Count consecutive days with at least 1 commit to origin/<default>, going back from today:

```bash
# Team streak
git log origin/<default> --format="%ad" --date=format:"%Y-%m-%d" | sort -u

# Personal streak
git log origin/<default> --author="<user_name>" --format="%ad" --date=format:"%Y-%m-%d" | sort -u
```

Count backward from today -- how many consecutive days have at least one commit? Display both:
- "Team shipping streak: 47 consecutive days"
- "Your shipping streak: 32 consecutive days"

---

## Step 12: Load History and Compare

Before saving the new snapshot, check for prior retro history:

```bash
ls -t .context/retros/*.json 2>/dev/null
```

**If prior retros exist:** Load the most recent one. Calculate deltas:
```
                    Last        Now         Delta
Test ratio:         22%    ->   41%         +19pp
Sessions:           10     ->   14          +4
LOC/hour:           200    ->   350         +75%
Fix ratio:          54%    ->   30%         -24pp (improving)
```

**If no prior retros exist:** Skip comparison. Append: "First retro recorded -- run again next week to see trends."

---

## Step 13: Save Retro History

Save a JSON snapshot:

```bash
mkdir -p .context/retros
```

Determine the next sequence number for today:
```bash
today=$(date +%Y-%m-%d)
existing=$(ls .context/retros/${today}-*.json 2>/dev/null | wc -l | tr -d ' ')
next=$((existing + 1))
```

Use the Write tool to save `.context/retros/${today}-${next}.json` with this schema:
```json
{
  "date": "2026-03-08",
  "window": "7d",
  "metrics": {
    "commits": 47,
    "contributors": 3,
    "prs_merged": 12,
    "insertions": 3200,
    "deletions": 800,
    "net_loc": 2400,
    "test_loc": 1300,
    "test_ratio": 0.41,
    "active_days": 6,
    "sessions": 14,
    "deep_sessions": 5,
    "avg_session_minutes": 42,
    "loc_per_session_hour": 350,
    "feat_pct": 0.40,
    "fix_pct": 0.30,
    "peak_hour": 22,
    "ai_assisted_commits": 32
  },
  "authors": {
    "Name": { "commits": 32, "insertions": 2400, "deletions": 300, "test_ratio": 0.41, "top_area": "src/" }
  },
  "streak_days": 47,
  "tweetable": "Week of Mar 1: 47 commits, 3.2k LOC, 38% tests, 12 PRs, peak: 10pm"
}
```

Include `test_health` if test files exist. Omit optional fields when data is unavailable.

---

## Step 14: Write the Narrative

Structure the output as:

**Tweetable summary** (first line):
```
Week of Mar 1: 47 commits (3 contributors), 3.2k LOC, 38% tests, 12 PRs, peak: 10pm | Streak: 47d
```

Then sections:

1. **Summary Table** (from Step 2)
2. **Trends vs Last Retro** (from Step 12, skip if first retro)
3. **Time and Session Patterns** (from Steps 3-4) -- narrative interpreting patterns
4. **Shipping Velocity** (from Steps 5-7) -- commit type mix, PR size distribution, fix-chain detection
5. **Code Quality Signals** -- test LOC ratio trend, hotspot analysis
6. **Test Health** -- total test files, tests added, regression test commits
7. **Focus and Highlights** (from Step 8) -- focus score, ship of the week
8. **Your Week** (personal deep-dive from Step 9) -- the section the user cares most about
9. **Team Breakdown** (from Step 9, skip if solo repo) -- per-teammate sections
10. **Top 3 Team Wins** -- highest-impact things shipped
11. **3 Things to Improve** -- specific, actionable, anchored in actual commits
12. **3 Habits for Next Week** -- small, practical, realistic (<5 min to adopt)
13. **Week-over-Week Trends** (if applicable, from Step 10)

---

## Compare Mode

When the user runs `/retro compare` (or `/retro compare 14d`):

1. Compute metrics for the current window
2. Compute metrics for the immediately prior same-length window (using `--since` and `--until` to avoid overlap)
3. Show a side-by-side comparison table with deltas and arrows
4. Write a brief narrative highlighting biggest improvements and regressions
5. Save only the current-window snapshot

---

## Tone

- Encouraging but candid, no coddling
- Specific and concrete -- always anchor in actual commits/code
- Skip generic praise ("great job!") -- say exactly what was good and why
- Frame improvements as leveling up, not criticism
- Praise should feel like something you'd actually say in a 1:1 -- specific, earned, genuine
- Growth suggestions should feel like investment advice -- "worth your time because..." not "you failed at..."
- Never compare teammates against each other negatively
- Keep total output around 3000-4500 words
- Use markdown tables and code blocks for data, prose for narrative
- Output directly to the conversation -- do NOT write to filesystem (except the JSON snapshot)

---

## Rules

- ALL narrative output goes directly to the user in the conversation. The ONLY file written is the `.context/retros/` JSON snapshot.
- Use `origin/<default>` for all git queries (not local main which may be stale)
- Display all timestamps in the user's local timezone
- If the window has zero commits, say so and suggest a different window
- Round LOC/hour to nearest 50
- Treat merge commits as PR boundaries
- Do not read CLAUDE.md or other docs -- this skill is self-contained
- On first run (no prior retros), skip comparison sections gracefully

---

## Next Steps

After the retro, consider **brainstorming-ideas** for the next sprint to channel insights into action.
