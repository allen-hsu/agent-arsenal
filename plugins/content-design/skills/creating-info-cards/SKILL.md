---
name: creating-info-cards
description: "Creates editorial-quality HTML info cards with modern magazine aesthetics. Transforms complex information into visually striking, self-contained HTML cards with Swiss International typography, noise textures, and adaptive layouts. Use when the user asks to create an info card, visual summary card, data card, knowledge card, social media card, quote card, or any single-page HTML visual that presents information in a magazine-style editorial layout. Also triggers when the user says 'make this look like a magazine', 'create a visual card', 'design an info graphic card', or wants to turn text content into a polished visual."
---

# Editorial Info Card Designer

Create visually striking, self-contained HTML info cards that combine Swiss International typography with modern magazine aesthetics. Each card is a single HTML file with embedded CSS — no external dependencies except Google Fonts.

## Design Philosophy

The goal is the intersection of Swiss International Style's rigorous structure and modern magazine visual impact. Every card should feel like a page torn from a premium editorial publication — precise grids, bold typography, intentional whitespace, and restrained color.

## Workflow

### Step 1: Analyze Content Density

Before writing any code, assess the input in one sentence and pick the best layout:

| Content shape | Recommended layout |
|--------------|-------------------|
| Single quote, stat, or headline | **Big Typography** |
| 3-5 key points, short summary | **Single Column** |
| 7+ items, dense editorial text | **Multi-Column Grid** |
| Technical specs, code, directory structures | **Modular Panels** |
| Sequential process, roadmap, changelog | **Timeline / Steps** |
| A vs B, before/after, pricing tiers | **Comparison** |
| Product launch, event, person profile | **Hero + Details** |

Content may combine layouts — e.g., a Hero header with Modular Panels below, or a Timeline inside a Single Column card.

### Step 2: Choose Layout Strategy

Pick the layout that best matches the content structure, not just density.

**1. Big Typography** — for quotes, single stats, headlines
- Title fills the card at 80-120px
- Core data enlarged to 120px+ as a visual anchor
- Generous whitespace — the emptiness IS the design
- Best when you have one powerful number or sentence

**2. Single Column** — for short summaries, 3-5 key points
- Standard editorial flow with clear hierarchy
- Accent bars and pull quotes break up content
- Strong vertical rhythm, one reading path

**3. Multi-Column Grid** — for dense editorial content
- Newspaper-inspired 2-3 column layout
- Vertical divider lines between columns
- Sidebar panels for metadata and secondary info
- Best for 7+ items that benefit from parallel scanning

**4. Modular Panels** — for technical specs, structured data, architecture
- Card-in-card layout with bordered containers
- Each topic gets its own panel with subtle border or background
- Supports code blocks, directory trees, and spec tables inside panels
- Mix monospace (`font-family: 'SF Mono', 'Fira Code', monospace; font-size: 14px`) with editorial fonts
- Best for developer-facing content: API docs, architecture overviews, config references
- Panel CSS pattern:
  ```css
  .panel {
    border: 1.5px solid rgba(0,0,0,0.12);
    padding: 24px 28px;
    background: #fff;
  }
  .panel-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
  }
  .panel code, .panel pre {
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 14px;
    background: rgba(0,0,0,0.04);
    padding: 2px 6px;
    border-radius: 3px;
  }
  ```

**5. Timeline / Steps** — for roadmaps, processes, version history, changelogs
- Vertical flow with connected nodes or numbered steps
- Each step gets a number/date, title, and description
- A vertical line or dots connect the steps visually
- Alternating left/right placement adds visual interest for 4+ steps
- Best for sequential information: product roadmaps, onboarding flows, historical events
- Node CSS pattern:
  ```css
  .timeline {
    position: relative;
    padding-left: 40px;
  }
  .timeline::before {
    content: '';
    position: absolute;
    left: 12px;
    top: 0;
    bottom: 0;
    width: 3px;
    background: var(--accent);
  }
  .step {
    position: relative;
    margin-bottom: 28px;
  }
  .step::before {
    content: '';
    position: absolute;
    left: -34px;
    top: 6px;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: var(--accent);
    border: 3px solid #f5f3ed;
  }
  ```

**6. Comparison** — for A vs B, before/after, pros/cons, plan tiers
- Two (or three) symmetrical columns with clear visual separation
- Highlight differences with color coding: green for advantage, red/grey for disadvantage
- A shared header row labels each column
- Optional "winner" indicator or recommendation badge
- Best for decision-making content: pricing tiers, tech stack comparisons, before/after results
- Split CSS pattern:
  ```css
  .comparison {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
  }
  .side {
    padding: 28px;
  }
  .side:first-child {
    border-right: 3px solid var(--accent);
  }
  .side-label {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 16px;
  }
  ```

**7. Hero + Details** — for product launches, event announcements, profiles
- Large color-block header area (full-width accent background or image placeholder)
- Hero element: oversized date, product name, or person name
- Details section below with structured metadata
- Best for announcements, conference talks, product releases, team member profiles
- Hero CSS pattern:
  ```css
  .hero-block {
    background: var(--accent);
    color: #fff;
    padding: 40px;
    margin: -50px -50px 0 -50px; /* bleed to card edges */
  }
  .hero-block .overline {
    font-size: 13px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    opacity: 0.7;
    margin-bottom: 12px;
  }
  .hero-block h1 {
    font-size: 56px;
    font-weight: 900;
    line-height: 1.05;
  }
  ```

### Step 3: Build the HTML

Produce a single, self-contained HTML file with all CSS inlined in a `<style>` block.

#### Font Stack

For Latin-only content:
```html
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
```

For CJK (Chinese/Japanese/Korean) content, add Noto fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&family=Noto+Sans+SC:wght@400;500;700&family=Oswald:wght@500;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
```

Use this font hierarchy:
- **Display/titles**: `'Oswald', sans-serif` (Latin) or `'Noto Serif SC', serif` (CJK) — for visual impact
- **Body text**: `'Inter', sans-serif` (Latin) or `'Inter', 'Noto Sans SC', sans-serif` (CJK) — for readability
- **Metadata/labels**: `'Inter', sans-serif` with `letter-spacing: 0.15em; text-transform: uppercase`

#### Type Scale

| Level | Size | Properties | Purpose |
|-------|------|------------|---------|
| Hero title | 72-84px | line-height: 1.0, weight: 900, letter-spacing: -0.04em | Primary visual hook |
| Section title | 56px | line-height: 1.1, weight: 700 | Major section headers |
| Subheading | 32px | line-height: 1.2 | Secondary headers |
| Body | 18-20px | line-height: 1.6, color: #1a1a1a | Main content |
| Caption | 15-16px | line-height: 1.5, color: #555 | Supporting text |
| Tag/meta | 13px | letter-spacing: 0.15em, weight: 700, uppercase | Category labels |

#### Unit & Symbol Treatment

When displaying statistics, size the number large (100-120px) and the unit/symbol at roughly 40% of that size (40-50px). The number is the visual anchor; the unit provides context without competing for attention.

```css
.stat-number { font-size: 110px; font-weight: 700; line-height: 1.0; }
.stat-unit   { font-size: 42px;  font-weight: 500; color: var(--accent); }
```

**Example:** `$500K` → `$` at 42px, `500` at 110px, `K` at 42px. The eye reads "five hundred" first, then registers "dollars, thousands." This pattern is standard in The Economist, Bloomberg Businessweek, and similar editorial infographics.

Place units inline with numbers — prefix symbols (`$`, `€`) before the number, suffix symbols (`%`, `K`, `M`, `B`) after. Use the accent color on units to further differentiate them from the number.

#### Spacing System

- Container padding: 40-50px
- Paragraph spacing: ≤ 1.5em
- Component gap: 30-40px
- Line height: 1.5-1.6 for body text

#### Visual Texture

Apply these subtle details to elevate from "web page" to "editorial":

- **Noise overlay**: A subtle grain texture at 4% opacity for paper-like feel. Use CSS:
  ```css
  .card::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 1;
  }
  /* All direct children must sit above the noise layer */
  .card > * {
    position: relative;
    z-index: 2;
  }
  ```
- **Heavy dividers**: 4-6px solid lines in the accent color for section breaks
- **Tinted panels**: `rgba(0,0,0,0.03)` background blocks to define spatial zones

#### Base Card Structure

```css
.card {
  width: 900px;
  max-width: 100%; /* responsive fallback for mobile preview */
  background: #f5f3ed;
  padding: 50px;
  box-sizing: border-box;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 30px;
  font-family: 'Inter', 'Noto Sans SC', sans-serif;
}
```

Let the card height grow naturally to fit content — do not set a fixed height. The aspect ratio guidance (3:4, 4:5, 16:9) is a visual target, not a hard constraint.

#### Color Approach

Choose an accent color. If the content has a brand color, use it. Otherwise pick from these defaults. These are calibrated to pop on the warm paper background (#f5f3ed) while maintaining editorial restraint:

| Content domain | Accent | Hex |
|---------------|--------|-----|
| News / tech | Royal blue | #2d5faa |
| Finance | Emerald or gold | #1a7a4a / #c49a2a |
| Health | Vivid teal | #0f8a7a |
| Culture / arts | Vermillion | #c44536 |
| Startup / energy | Burnt orange | #e85d26 |
| Neutral | Charcoal | #333333 |

Keep it to 2-3 colors max: background (#f5f3ed), text (#0a0a0a), and one accent. The accent should feel vibrant on the warm paper — avoid overly dark or desaturated colors that look muddy.

### Step 4: Self-Check

Before delivering, verify:

1. **Readability**: Body text at 18-20px is legible on mobile screens
2. **Hierarchy**: Squint test — can you identify the visual hierarchy from 2 feet away?
3. **Density**: No large empty voids. If sparse, make the typography bigger. If cramped, add columns.
4. **Texture**: Noise overlay and accent bars are present
5. **Self-contained**: The HTML file works when opened directly — no broken external dependencies (except Google Fonts CDN)
6. **Aspect ratio**: Card proportions feel editorial (roughly 3:4 or 4:5 for portrait, 16:9 for landscape)

## Output Format

Always output:

1. **One-line density assessment** (e.g., "Medium density — 4 key statistics with supporting text")
2. **Complete HTML file** with embedded `<style>` block
3. **Design note** — one sentence explaining the key design decision made (e.g., "Used 2-column grid because the 6 data points needed parallel comparison")

## Examples of Good Design Decisions

- Single powerful quote → **Big Typography** — 72px centered text, generous margins
- Three competing statistics → **Multi-Column Grid** — oversized numbers (120px) with small labels
- Long article summary → **Multi-Column Grid** — newspaper 2-column with a pull quote
- API / SDK overview → **Modular Panels** — bordered boxes with code blocks and directory trees
- Product roadmap → **Timeline** — vertical nodes with dates and milestones
- Pricing plans → **Comparison** — side-by-side columns with feature checkmarks
- Conference talk announcement → **Hero + Details** — full-bleed color header with speaker name, details below
- Before/after redesign → **Comparison** — old vs new screenshots with callout annotations

## Anti-Patterns to Avoid

- Generic Bootstrap/Tailwind card look — this should feel editorial, not like a UI component
- Tiny text (under 16px for body) — defeats the purpose of a visual card
- Rainbow colors — restrain to 2-3 colors
- Centered everything — use left alignment for body text, reserve centering for hero elements
- Stock photo backgrounds — use typography and color as the visual interest

## Next Steps

- If the user wants to iterate on the design, adjust based on their feedback
- For multiple cards in a series, maintain consistent typography and color palette across cards
- For print-ready output, suggest increasing the card width to 1200px and adjusting for print margins
