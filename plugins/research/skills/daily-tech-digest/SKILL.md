---
name: daily-tech-digest
description: Daily tech news aggregator. Use when (1) user asks for daily tech news digest, (2) user wants to aggregate news from ProductHunt, HackerNews, or Reddit, (3) user mentions "tech digest", "daily digest", "tech news summary", or (4) user wants to create content for tech podcast or newsletter.
---

# Daily Tech Digest Skill

This skill aggregates trending content from ProductHunt, HackerNews, and Reddit to create a comprehensive daily tech digest in Markdown format, suitable for conversion to podcast scripts or newsletters.

## Prerequisites

This skill requires the `agent-browser` CLI tool. Invoke the `agent-browser` skill first if you're unfamiliar with its commands.

## Workflow

### Step 1: Initialize

1. Create a working directory for today's digest
2. Note today's date for the digest header

### Step 2: Fetch ProductHunt Top 10

Use `agent-browser` CLI to scrape ProductHunt:

```bash
# Navigate to ProductHunt
agent-browser open https://www.producthunt.com/

# Wait for content to load
agent-browser wait 3000

# Get interactive snapshot to see the page structure
agent-browser snapshot -i

# Extract product information using snapshot refs
# Look for product cards and extract: name, tagline, votes, comments, URL
agent-browser get text @e1  # Example: get text from element ref
```

**Data to extract for each product** (top 10):
- Product name
- Tagline/description
- Upvote count
- Comment count
- Product URL

### Step 3: Fetch HackerNews Top 10

Use `agent-browser` CLI to scrape HackerNews:

```bash
# Navigate to HackerNews
agent-browser open https://news.ycombinator.com/

# Get snapshot (HN loads fast, minimal wait needed)
agent-browser snapshot -i

# Extract story information from the itemlist
# Each story has: title link, points, comments, time
agent-browser get text @e1  # Get story title
agent-browser get attr @e1 href  # Get story URL
```

**Data to extract for each story** (top 10):
- Title
- URL (external link)
- Points/score
- Comment count
- HN discussion URL

### Step 4: Fetch Reddit Hot Posts (3 Subreddits)

Use `agent-browser` CLI to scrape each subreddit:

```bash
# Navigate to r/technology
agent-browser open https://www.reddit.com/r/technology/hot/

# Wait for Reddit to load (may have loading spinners)
agent-browser wait 3000

# Get snapshot to analyze post structure
agent-browser snapshot -i

# Scroll if needed to load more posts
agent-browser scroll down 500

# Extract post data
# Skip pinned posts (usually first 1-2 with pin icon)
```

**Subreddits to scrape**:
- `https://www.reddit.com/r/technology/hot/`
- `https://www.reddit.com/r/programming/hot/`
- `https://www.reddit.com/r/startups/hot/`

**Data to extract for each post** (top 10 per subreddit, skip pinned):
- Title
- URL (external or Reddit self-post)
- Upvote count
- Comment count
- Flair/tag (if available)

### Step 5: Close Browser When Done

```bash
# Close the browser session
agent-browser close
```

### Step 6: Generate Summaries and Analysis

For each collected item, generate:

1. **Summary** (2-3 sentences): What is this? Why is it notable?
2. **Analysis** (1-2 sentences): What's the takeaway? What should readers/listeners do or consider?

Use WebSearch or WebFetch if needed to get more context about linked articles.

### Step 7: Identify Cross-Platform Trends

Analyze all collected items to identify:
- Common themes or technologies appearing across platforms
- Emerging trends worth watching
- Contrasting perspectives on the same topic

### Step 8: Generate Final Markdown

Use the template in `references/summary-template.md` to structure the output:

1. Write the opening summary highlighting top 3-5 stories
2. Organize items by platform
3. Include summaries and analysis for each item
4. Write the "Today's Insights" section with trend observations
5. Save as `daily-tech-digest-YYYY-MM-DD.md`

## agent-browser Quick Reference

```bash
# Navigation
agent-browser open <url>          # Go to URL
agent-browser close               # Close browser

# Page analysis
agent-browser snapshot -i         # Get interactive elements with refs
agent-browser wait <ms>           # Wait milliseconds
agent-browser wait --load networkidle  # Wait for network idle

# Interaction
agent-browser click @e1           # Click element by ref
agent-browser scroll down 500     # Scroll page

# Data extraction
agent-browser get text @e1        # Get element text
agent-browser get attr @e1 href   # Get attribute value
agent-browser get html @e1        # Get innerHTML

# Debugging
agent-browser screenshot          # Take screenshot
agent-browser console             # View console messages
```

## Output

The final output is a Markdown file named `daily-tech-digest-YYYY-MM-DD.md` containing:
- Opening hook for podcast/newsletter
- Platform-organized sections with detailed item coverage
- Closing insights and trend analysis

## Reference Files

- `references/sources.md` - Detailed scraping strategies for each platform
- `references/summary-template.md` - Markdown output format template

## Tips for Quality Output

1. **Be specific in summaries**: Avoid vague descriptions. Explain what makes each item newsworthy.
2. **Add context**: Reference related news, historical context, or industry implications.
3. **Vary the analysis**: Don't repeat the same takeaways. Each item should offer unique value.
4. **Time-sensitive framing**: Use language suitable for "today's news" format.
5. **Podcast-friendly language**: Write summaries that sound natural when read aloud.
