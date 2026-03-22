---
name: creating-expo-apps
description: Scaffold new React Native apps with create-expo-stack (rn.new). Use when (1) user wants to create a new React Native or Expo app, (2) user mentions "scaffold", "initialize", "new app", or "rn.new", (3) user asks about create-expo-stack CLI options.
---

# Creating Expo Apps

Scaffold new React Native apps using **create-expo-stack** (rn.new) with your preferred configuration.

## Quick Start (Recommended)

Interactive CLI that lets you choose your tech stack:

```bash
# Simplest way
npx rn-new@latest

# Or with package managers
pnpm create expo-stack
npm create expo-stack
yarn create expo-stack
bun create expo-stack
```

The CLI will prompt you to select:
- Navigation framework (Expo Router / React Navigation)
- Navigation type (Stack / Tabs / Drawer)
- Styling solution (NativeWind / Unistyles / Tamagui / Restyle / StyleSheet)
- Backend services (Firebase / Supabase / None)
- Additional features (i18n, import aliases, etc.)

## One-liner with Preset Options

For production-ready setup matching our tech stack:

```bash
# Full production setup with Expo Router + NativeWind + i18n
pnpm create expo-stack MyApp --expo-router --tabs --nativewind --i18next --import-alias

cd MyApp
pnpm ios      # iOS simulator
pnpm android  # Android emulator
```

## Available Options

| Category | Options |
|----------|---------|
| **Package Manager** | `--npm`, `--yarn`, `--pnpm`, `--bun` |
| **Navigation** | `--expo-router`, `--react-navigation` |
| **Nav Type** | `--tabs`, `--drawer` (default: stack) |
| **Styling** | `--nativewind`, `--unistyles`, `--tamagui`, `--restyle`, `--stylesheet` |
| **Backend** | `--firebase`, `--supabase` |
| **Features** | `--i18next`, `--import-alias` |
| **Other** | `-d/--default`, `--no-git`, `--no-install` |

## Prerequisites

- Node.js LTS
- pnpm (`npm install -g pnpm`)
- Watchman (macOS/Linux)
- Xcode (iOS) / Android Studio (Android)

## Post-setup

1. Open project in VS Code/Cursor and install recommended extensions (ESLint, Prettier, Tailwind CSS IntelliSense)
2. Update `app.config.ts` with your app name, bundle ID, etc.
3. Configure environment variables in `.env`
4. Run `eas init` to set up EAS Build

> **Docs:** https://docs.rn.new/ | **GitHub:** https://github.com/roninoss/create-expo-stack

## Default Tech Stack

Based on create-expo-stack (Expo SDK 54):

| Category         | Technology                                         |
| ---------------- | -------------------------------------------------- |
| Framework        | React Native 0.81 + React 19 + Expo SDK 54         |
| Navigation       | Expo Router 6 (file-based routing with typed routes) |
| Styling          | NativeWind 4 (Tailwind CSS) or Unistyles 3         |
| State Management | Zustand (add manually)                             |
| Data Fetching    | TanStack Query (React Query) + Axios (add manually) |
| Forms            | React Hook Form + Zod (add manually)               |
| Storage          | MMKV (recommended) or AsyncStorage                 |
| i18n             | i18next + react-i18next (use `--i18next` flag)     |
| Offline Support  | NetInfo + Custom Queue (add manually)              |
| Authentication   | Supabase or Firebase (optional flags)              |
| Testing          | Jest + React Native Testing Library                |

> For architecture and development patterns, see the `developing-react-native` skill.
