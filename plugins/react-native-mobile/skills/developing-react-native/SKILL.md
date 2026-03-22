---
name: developing-react-native
description: React Native architecture and development patterns for production apps. Use when (1) user is building features in a React Native app, (2) user asks about mobile architecture, components, state management, or data fetching, (3) user needs help with navigation, forms, or testing patterns, (4) user mentions "mobile", "React Native", "Expo", "RN", "iOS app", or "Android app".
---

# Developing React Native Apps

Architecture patterns and conventions for building production-ready React Native + Expo applications.

## Project Structure

Follow the recommended structure from [references/project-structure.md](references/project-structure.md).

```
├── app/                    # Expo Router screens and layouts
├── src/
│   ├── core/               # Core infrastructure (base layer)
│   │   ├── config/         # Environment variables, constants
│   │   ├── services/       # API client, storage, network, logger
│   │   │   ├── api/        # HTTP client, interceptors, error handler
│   │   │   ├── network/    # NetInfo monitor, offline queue, sync
│   │   │   └── storage/    # MMKV wrapper
│   │   ├── i18n/           # i18next config, RTL support
│   │   └── providers/      # Theme, Query, i18n, Network providers
│   ├── features/           # Feature modules (self-contained)
│   │   └── [feature]/      # screens/, widgets/, api/, hooks/, store/
│   ├── shared/             # Shared components, hooks, utils
│   │   ├── components/     # ui/, forms/, layout/, feedback/
│   │   └── hooks/          # useDebounce, useMounted, etc.
│   ├── store/              # Global state (auth, theme, network)
│   └── __tests__/          # Test setup, mocks, utilities
├── assets/                 # Static assets (images, fonts)
└── locales/                # i18n JSON files (common, errors, features)
```

### Architecture Layers

```
app/      → features/, shared/, core/, store/
features/ → shared/, core/, store/ (NO cross-feature imports)
shared/   → core/ only
core/     → No dependencies (base layer)
store/    → core/, shared/
```

## Coding Standards

Refer to [references/coding-standards.md](references/coding-standards.md) for detailed conventions.

### Key Rules

1. **File naming**: Use `kebab-case` for all files and folders (e.g., `login-form.tsx`)
2. **Imports**: Use `@/` alias for absolute imports (configure with `--import-alias`)
3. **Type imports**: Use `import type` for type-only imports
4. **Function limits**: Max 3 parameters, max 70 lines per function
5. **Exports**: Prefer named exports over default exports

## Components

Use NativeWind (Tailwind CSS) for styling. For complex variants, use `tailwind-variants`. See [references/component-patterns.md](references/component-patterns.md) for patterns including forms with React Hook Form + Zod.

## State Management

Use Zustand with `createSelectors` for optimized re-renders. Export actions separately for use outside React. See [references/data-layer.md](references/data-layer.md) for store patterns and data fetching.

## Data Fetching

Use TanStack Query (React Query) with Axios. See [references/data-layer.md](references/data-layer.md) for query/mutation patterns and cache management.

## Navigation (Expo Router)

### File-based Routing

```
app/
├── _layout.tsx        # Root layout
├── index.tsx          # Home screen (/)
├── login.tsx          # Login screen (/login)
├── (tabs)/            # Tab group
│   ├── _layout.tsx    # Tab layout
│   ├── home.tsx       # /home tab
│   └── profile.tsx    # /profile tab
└── [id].tsx           # Dynamic route (/:id)
```

### Protected Routes

```tsx
// app/_layout.tsx
import { useAuth } from "@/lib/auth";
import { Redirect, Stack } from "expo-router";

export default function RootLayout() {
  const status = useAuth.use.status();

  if (status === "signOut") {
    return <Redirect href="/login" />;
  }

  return <Stack />;
}
```

## Environment Variables

Use Zod for validation in `env.js`:

```javascript
const client = z.object({
  APP_ENV: z.enum(["development", "staging", "production"]),
  API_URL: z.string().url(),
  VERSION: z.string(),
});

// Access via @env alias
import Env from "@env";
console.log(Env.API_URL);
```

## Testing

See [references/testing.md](references/testing.md) for component testing, mocking, and test utilities.

## Quick Commands

```bash
# Development
pnpm start                    # Start Expo dev server
pnpm ios                      # Run on iOS simulator
pnpm android                  # Run on Android emulator

# Testing
pnpm test                     # Run tests
pnpm lint                     # Run ESLint
pnpm typecheck               # Run TypeScript check

# Building
APP_ENV=staging pnpm build:ios      # Build iOS (staging)
APP_ENV=production pnpm build:android  # Build Android (production)
```

## Resources

### Architecture & Patterns
- **Project Structure**: [references/project-structure.md](references/project-structure.md)
- **Coding Standards**: [references/coding-standards.md](references/coding-standards.md)
- **Component Patterns**: [references/component-patterns.md](references/component-patterns.md)

### Data & Services
- **Data Layer**: [references/data-layer.md](references/data-layer.md)
- **Offline Support**: [references/offline.md](references/offline.md)

### Internationalization & Testing
- **i18n Guide**: [references/i18n.md](references/i18n.md)
- **Testing Guide**: [references/testing.md](references/testing.md)
