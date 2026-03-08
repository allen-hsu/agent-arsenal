---
name: scanning-reddit-niches
description: Scan Reddit subreddits for pain points, tool complaints, and app opportunities using the reddit-scanner CLI. Use when users want to find product ideas, validate market needs, discover underserved niches, or analyze Reddit communities for business signals. Triggers on "scan Reddit", "Reddit pain points", "find app ideas", "niche research", "subreddit analysis", "product opportunity", or "what are people complaining about".
---

# Scanning Reddit Niches

Find real product opportunities by scanning Reddit for pain signals and tool complaints from niche communities.

## Prerequisites

Install the CLI:

```bash
go install github.com/allen-hsu/reddit-scanner@latest
```

Or build from source:

```bash
git clone https://github.com/allen-hsu/reddit-scanner.git
cd reddit-scanner && go build -o reddit-scanner .
```

## Core Workflow

### 1. Browse niche categories

```bash
reddit-scanner suggest
```

Lists 25 niche categories (trades, healthcare, beauty, events, etc.) with specific subreddit recommendations.

### 2. Scan subreddits

```bash
# Basic scan — top posts from the past week
reddit-scanner scan r/bartenders r/HVAC r/Locksmith --plain

# Search with keywords
reddit-scanner scan r/bartenders -q "checklist OR routine OR software"

# Only pain-signal posts + fetch comments for workaround analysis
reddit-scanner scan r/hairstylist r/Barber --plain --pain-only --comments -p month
```

### 3. Interactive TUI mode

```bash
reddit-scanner scan r/bartenders r/KitchenConfidential
```

Controls: `↑↓`/`jk` navigate, `Enter` expand comments, `o` open in browser, `p` toggle pain-only, `q` quit.

## CLI Reference

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--query` | `-q` | | Search query within subreddits |
| `--period` | `-p` | `week` | Time period: day/week/month/year |
| `--min-ups` | | `5` | Minimum upvotes |
| `--limit` | | `20` | Posts per subreddit |
| `--pain-only` | | `false` | Only posts with pain signals |
| `--comments` | | `false` | Fetch top comments (plain mode) |
| `--plain` | | `false` | Plain text output, no TUI |

## Signal Detection

Posts are scored by two signal types:

- **Pain signals** (🔴 PAIN): hate, frustrated, spreadsheet, nightmare, alternative, expensive, overkill, "someone should build", "would pay for"...
- **Tool signals** (🔧 TOOL): software, app, CRM, booking, scheduling, invoice, workflow, automation, SaaS...

Posts with both signals rank highest — they indicate someone already paying for tools and unhappy with them.

## Analysis Pattern

After scanning, analyze high-signal posts by:

1. Read the post and top comments for real workarounds people are using
2. Identify the gap between current workaround and ideal solution
3. Assess: pain intensity, willingness to pay, existing competition, MVP complexity
4. Document findings with source links, quotes, and opportunity scoring

## Suggested Niche Categories

Trades (HVAC, Electricians, Plumbing), Beauty (hairstylist, Barber, NailTech), Pet Services (doggrooming, dogtraining), Events (weddingplanning, catering), Food & Beverage (bartenders, KitchenConfidential, TheBrewery), Healthcare (VetTech, optometry, PhysicalTherapy), Education (Teachers, Tutors, homeschool), Property (PropertyManagement, Landlord, AirBnB), Creative (TattooArtists, weddingphotography, livesound), Field Service (Handyman, pestcontrol, Truckers).

Run `reddit-scanner suggest` for the full list.
