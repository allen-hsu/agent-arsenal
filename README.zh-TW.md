# Agent Arsenal

[English](README.md)

一個 Claude Code 插件市集，包含自訂的 skills 和 commands，用於 AI 輔助開發。

## 安裝

將此市集加入 Claude Code 設定：

```bash
claude mcp add-marketplace agent-arsenal https://github.com/allen-hsu/agent-arsenal
```

或手動加入 `.claude/settings.json`：

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

接著安裝個別插件：

```bash
claude plugins install agent-arsenal:product-planning
claude plugins install agent-arsenal:engineering-core
claude plugins install agent-arsenal:shipping
claude plugins install agent-arsenal:reddit-scanner
claude plugins install agent-arsenal:react-native-mobile
claude plugins install agent-arsenal:research
```

## 可用插件

### product-planning

產品策略與設計思考 — 動手寫程式之前先想清楚。

**Skills：**
- `brainstorming-ideas` - YC 風格的 Office Hours，包含強制提問、前提挑戰和設計文件產出
- `reviewing-product-strategy` - CEO/創辦人視角的計畫審查，4 種範圍模式和 10 項審查
- `reviewing-product-design` - 設計師視角的計畫審查，7 項審計和 0-10 評分

### reddit-scanner

掃描 Reddit 利基社群，找出痛點和 App 機會。

**技能：**
- `scanning-reddit-niches` - 從 subreddit 的痛點信號和工具抱怨中發掘產品機會

**需要：** [reddit-scanner CLI](https://github.com/allen-hsu/reddit-scanner)（`go install github.com/allen-hsu/reddit-scanner@latest`）

### engineering-core

核心工程實踐 — 規格、審查、除錯。

**Skills：**
- `writing-tech-specs` - 透過互動式問答建立技術規格文件
- `reviewing-architecture` - 架構審查，含資料流程圖、故障模式和測試計畫
- `reviewing-code` - PR 預合併審查，兩階段方法論和修復優先策略
- `investigating-bugs` - 系統性根因除錯，Iron Law 和三振出局規則

### shipping

測試、發版與回顧 — 從 QA 到上線。

**Skills：**
- `testing-qa` - 使用 Playwright 進行 QA 測試，健康評分、原子化修復提交和迴歸測試
- `shipping-code` - 自動化發版流程：合併基礎分支、執行測試、可二分提交、建立 PR
- `running-retro` - 週工程回顧，含個人分析和趨勢追蹤

**Commands：**
- `/commit` - 使用 conventional commits 格式建立 git commit

### react-native-mobile

完整的 React Native + Expo 行動應用開發工具組。

**Skills：**
- `creating-expo-apps` - 使用最佳實踐建立新的 Expo 應用
- `developing-react-native` - 應用程式架構、狀態管理、導航和編碼規範
- `designing-mobile-ui` - UI 模式、設計系統、動畫和主題設定
- `deploying-mobile-apps` - EAS Build、Submit、Update 和 CI/CD 工作流程
- `integrating-google-ads` - Google AdMob 整合與同意管理

**Commands：**
- `/eas-build` - 使用 EAS 建置應用程式
- `/eas-deploy` - 部署應用程式到商店
- `/eas-workflow` - 管理 EAS Workflows

### research

研究與內容彙整。

**Skills：**
- `daily-tech-digest` - 彙整 ProductHunt、HackerNews 和 Reddit 的熱門內容

## 建立新插件

### 目錄結構

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

### Skill 格式

建立 `SKILL.md`，包含 YAML frontmatter：

```yaml
---
name: skill-name
description: 描述觸發條件。Use when (1)..., (2)...
---

# Skill 內容

你的 skill 指令...
```

### Command 格式

建立 `.md` 檔案，包含 YAML frontmatter：

```yaml
---
description: 這個指令做什麼
allowed-tools: Bash(git status:*), Bash(git diff:*)
---

# Command 指令

你的 command 指令...
```

### 註冊到 marketplace.json

將插件加入 `.claude-plugin/marketplace.json`：

```json
{
  "name": "your-plugin",
  "description": "你的插件功能描述",
  "source": "./plugins/your-plugin",
  "skills": ["./skills/your-skill"],
  "commands": ["./commands/your-command.md"]
}
```

## 授權

MIT
