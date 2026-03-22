# Data Sources and Scraping Strategies

This document details the scraping strategies for each platform in the Daily Tech Digest.

## ProductHunt

### URL
```
https://www.producthunt.com/
```

### Target Content
The daily product leaderboard showing today's top launches.

### Data Points to Extract (per product)

| Field | Description | Example |
|-------|-------------|---------|
| name | Product name | "Notion AI" |
| tagline | One-line description | "Your AI-powered workspace assistant" |
| upvotes | Number of upvotes | 1,234 |
| comments | Number of comments | 89 |
| url | Product page URL | "https://www.producthunt.com/posts/notion-ai" |
| topics | Product categories | ["Productivity", "AI"] |
| maker | Creator name (if visible) | "Notion Team" |

### Scraping Notes

1. **Daily Reset**: ProductHunt resets rankings at midnight PT. Scrape after ~9am PT for meaningful data.
2. **Sticky Products**: Featured or sponsored products may appear at top - note if they're marked as such.
3. **Authentication**: No login required for basic data. Logged-in users may see personalized content.
4. **Rate Limiting**: Use reasonable delays between page loads.

### Browser Steps

```
1. Navigate to https://www.producthunt.com/
2. Wait for the product list to fully load (look for vote buttons)
3. Locate the main product feed/leaderboard section
4. For each of the first 10 products:
   a. Extract the product name (usually <h3> or prominent text)
   b. Extract the tagline (usually smaller text below name)
   c. Extract upvote count (number near upvote button)
   d. Extract comment count (number near comment icon)
   e. Extract the product URL from the link
   f. Extract topic tags if displayed
5. Compile into structured data
```

---

## HackerNews

### URL
```
https://news.ycombinator.com/
```

### Target Content
Front page stories ranked by the HN algorithm (combination of votes, time, and other factors).

### Data Points to Extract (per story)

| Field | Description | Example |
|-------|-------------|---------|
| title | Story headline | "Show HN: I built a faster SQLite" |
| url | External article link | "https://example.com/article" |
| points | Upvote score | 423 |
| comments | Number of comments | 156 |
| hn_url | HN discussion page | "https://news.ycombinator.com/item?id=12345" |
| submitted_by | Username | "dang" |
| time_ago | Relative time | "3 hours ago" |

### Scraping Notes

1. **Simple HTML**: HN uses minimal, table-based HTML. Very scraping-friendly.
2. **No JavaScript Required**: Content loads without JS, but `agent-browser` handles this anyway.
3. **Story Types**: Mix of external links, Ask HN, Show HN, and job posts. Note the type.
4. **30 Stories Per Page**: First page shows 30 stories; we only need 10.

### Browser Steps

```
1. Navigate to https://news.ycombinator.com/
2. The page loads immediately with content
3. Locate the story table (class "itemlist")
4. For each of the first 10 stories:
   a. Extract title from the "titleline" link
   b. Extract external URL from the title link
   c. Extract points from the "score" span
   d. Extract comment count from the "subtext" links
   e. Construct HN discussion URL from item ID
   f. Extract username and time from subtext
5. Compile into structured data
```

### HN URL Patterns

- Story page: `https://news.ycombinator.com/item?id={ID}`
- User page: `https://news.ycombinator.com/user?id={USERNAME}`

---

## Reddit

### URLs
```
https://www.reddit.com/r/technology/hot/
https://www.reddit.com/r/programming/hot/
https://www.reddit.com/r/startups/hot/
```

### Target Content
Hot posts from each subreddit (trending content based on recent activity and votes).

### Data Points to Extract (per post)

| Field | Description | Example |
|-------|-------------|---------|
| title | Post title | "Apple announces new M4 chip" |
| url | Link (external or Reddit) | "https://apple.com/..." |
| upvotes | Net upvote count | 5,432 |
| comments | Number of comments | 892 |
| subreddit | Source subreddit | "r/technology" |
| flair | Post flair/tag | "Hardware" |
| post_type | Link, text, image, video | "link" |
| reddit_url | Reddit discussion URL | "https://reddit.com/r/..." |

### Scraping Notes

1. **Old Reddit Option**: `old.reddit.com` has simpler HTML but may have different content.
2. **Pinned Posts**: Skip posts marked as "pinned" or "stickied" (usually mod announcements).
3. **NSFW Filter**: These subreddits are SFW, but check for NSFW tags just in case.
4. **Login Wall**: Reddit may show login prompts - these can usually be dismissed or bypassed.
5. **Rate Limiting**: Add delays between subreddit requests.

### Browser Steps (per subreddit)

```
1. Navigate to the subreddit hot page (e.g., https://www.reddit.com/r/technology/hot/)
2. Wait for posts to load
3. Dismiss any login/cookie prompts if they appear
4. Locate the post feed
5. Skip any pinned/stickied posts (usually marked with a pin icon)
6. For each of the first 10 non-pinned posts:
   a. Extract post title
   b. Extract URL (may be external link or Reddit self-post)
   c. Extract upvote count
   d. Extract comment count
   e. Extract flair if present
   f. Note if it's a text post, link, image, or video
   g. Construct Reddit discussion URL
7. Compile into structured data
8. Repeat for next subreddit
```

### Subreddit Descriptions

| Subreddit | Focus | Typical Content |
|-----------|-------|-----------------|
| r/technology | General tech news | Industry news, product launches, policy |
| r/programming | Software development | Languages, tools, practices, career |
| r/startups | Entrepreneurship | Fundraising, growth, founder stories |

---

## Data Collection Summary

| Platform | URL | Items | Key Metrics |
|----------|-----|-------|-------------|
| ProductHunt | producthunt.com | 10 | Upvotes, Comments |
| HackerNews | news.ycombinator.com | 10 | Points, Comments |
| r/technology | reddit.com/r/technology/hot | 10 | Upvotes, Comments |
| r/programming | reddit.com/r/programming/hot | 10 | Upvotes, Comments |
| r/startups | reddit.com/r/startups/hot | 10 | Upvotes, Comments |

**Total Items**: 50 items per digest

---

## Error Handling

### Common Issues

1. **Page Not Loading**: Retry with increased timeout
2. **Login Wall**: Try old.reddit.com or dismiss modal
3. **Rate Limited**: Wait and retry with exponential backoff
4. **Content Layout Changed**: Fall back to text extraction
5. **Missing Data Points**: Record as "N/A" and continue

### Fallback Strategy

If browser scraping fails for a platform:
1. Note the failure in the digest
2. Try alternative URL (e.g., old.reddit.com)
3. Use WebSearch to find recent news about the platform's trending content
4. Mark the section as "Limited Data" in the output
