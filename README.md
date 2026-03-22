# Agent Arsenal

[繁體中文](README.zh-TW.md)

A Claude Code plugin marketplace containing custom skills and commands for AI-assisted development.

## Installation

Add this marketplace to your Claude Code settings:

```bash
claude mcp add-marketplace agent-arsenal https://github.com/allen-hsu/agent-arsenal
```

Or manually add to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": [
    {
      "name": "agent-arsenal",
      "source": "git:allen-hsu/agent-arsenal"
    }
  ]
}
```

Then install individual plugins:

```bash
claude plugins install agent-arsenal:product-planning
claude plugins install agent-arsenal:engineering-core
claude plugins install agent-arsenal:shipping
claude plugins install agent-arsenal:react-native-mobile
claude plugins install agent-arsenal:research
```

## Available Plugins

### product-planning

Product strategy and design thinking — brainstorm before you build.

**Skills:**
- `brainstorming-ideas` - YC-style office hours with forcing questions, premise challenges, and design doc output
- `reviewing-product-strategy` - CEO/founder perspective plan review with 4 scope modes and 10-section mega review
- `reviewing-product-design` - Designer's eye plan review with 7-pass audit and 0-10 scoring

### engineering-core

Core engineering practices — specs, review, and debugging.

**Skills:**
- `writing-tech-specs` - Create technical specification documents through interactive Q&A
- `reviewing-architecture` - Architecture review with data flow diagrams, failure modes, and test plans
- `reviewing-code` - Pre-landing PR review with two-pass methodology and fix-first approach
- `investigating-bugs` - Systematic root-cause debugging with Iron Law and 3-strike rule

### shipping

Testing, shipping, and retrospectives — from QA to production.

**Skills:**
- `testing-qa` - QA testing with Playwright, health scoring, atomic fix commits, and regression tests
- `shipping-code` - Automated ship workflow: merge base, run tests, bisectable commits, create PR
- `running-retro` - Weekly engineering retrospective with per-person analysis and trend tracking

**Commands:**
- `/commit` - Create a git commit with conventional commits format

### react-native-mobile

Complete React Native + Expo mobile development toolkit.

**Skills:**
- `creating-expo-apps` - Scaffold new Expo apps with best practices
- `developing-react-native` - App architecture, state management, navigation, and coding standards
- `designing-mobile-ui` - UI patterns, design systems, animations, and theming
- `deploying-mobile-apps` - EAS Build, Submit, Update, and CI/CD workflows
- `integrating-google-ads` - Google AdMob integration with consent management

**Commands:**
- `/eas-build` - Build your app with EAS
- `/eas-deploy` - Deploy your app to stores
- `/eas-workflow` - Manage EAS Workflows

### research

Research and content discovery.

**Skills:**
- `daily-tech-digest` - Aggregate trending content from ProductHunt, HackerNews, and Reddit
- `scanning-reddit-niches` - Find product opportunities by scanning subreddits for pain signals and tool complaints

**Requires (for scanning-reddit-niches):** [reddit-scanner CLI](https://github.com/allen-hsu/reddit-scanner) (`go install github.com/allen-hsu/reddit-scanner@latest`)

## Creating New Plugins

### Directory Structure

```
plugins/
└── your-plugin/
    ├── skills/
    │   └── your-skill/
    │       ├── SKILL.md
    │       └── references/
    │           └── guide.md
    └── commands/
        └── your-command.md
```

### Skill Format

Create `SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-name
description: Description including trigger conditions. Use when (1)..., (2)...
---

# Skill Content

Your skill instructions here...
```

### Command Format

Create a `.md` file with YAML frontmatter:

```yaml
---
description: What the command does
allowed-tools: Bash(git status:*), Bash(git diff:*)
---

# Command Instructions

Your command instructions here...
```

### Register in marketplace.json

Add your plugin to `.claude-plugin/marketplace.json`:

```json
{
  "name": "your-plugin",
  "description": "What your plugin does",
  "source": "./plugins/your-plugin",
  "skills": ["./skills/your-skill"],
  "commands": ["./commands/your-command.md"]
}
```

## License

MIT
