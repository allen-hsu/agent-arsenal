---
name: integrating-google-ads
description: Integrate Google AdMob ads into React Native/Expo apps. Use when (1) user wants to add ads or monetize their mobile app, (2) user mentions "AdMob", "Google Ads", "banner ad", "interstitial", or "rewarded ad", (3) user asks about ad integration, ad placement, or ad revenue in a React Native app.
---

# Google AdMob Integration for React Native/Expo

Uses [`react-native-google-mobile-ads`](https://github.com/invertase/react-native-google-mobile-ads) by Invertase.

> **Expo Go is NOT supported.** You must use a development build (`npx expo run:ios` / `npx expo run:android` or EAS Build).

## Quick Setup

### 1. Install

```bash
npx expo install react-native-google-mobile-ads
```

### 2. Configure app.config.ts

Add the plugin with your AdMob app IDs (get these from the [AdMob console](https://apps.admob.com)):

```ts
export default {
  expo: {
    plugins: [
      [
        "react-native-google-mobile-ads",
        {
          androidAppId: "ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy",
          iosAppId: "ca-app-pub-xxxxxxxxxxxxxxxx~zzzzzzzzzz",
        },
      ],
    ],
  },
};
```

### 3. Initialize the SDK

Call once at app startup, **before** loading any ads:

```tsx
import mobileAds from "react-native-google-mobile-ads";

// In your app entry point (e.g., App.tsx or _layout.tsx)
mobileAds()
  .initialize()
  .then((adapterStatuses) => {
    // Ads can now be loaded
  });
```

### 4. Rebuild

```bash
npx expo prebuild --clean
npx expo run:ios   # or run:android
```

## Test Ad Unit IDs

**Always use test IDs during development.** Real ad IDs in dev can get your account suspended.

```ts
import { TestIds } from "react-native-google-mobile-ads";
```

| Format | `TestIds` constant |
|---|---|
| Banner | `TestIds.BANNER` |
| Interstitial | `TestIds.INTERSTITIAL` |
| Rewarded | `TestIds.REWARDED` |
| Rewarded Interstitial | `TestIds.REWARDED_INTERSTITIAL` |
| App Open | `TestIds.APP_OPEN` |

In production, swap to your real ad unit IDs:

```ts
const adUnitId = __DEV__ ? TestIds.BANNER : "ca-app-pub-xxxxx/yyyyy";
```

## Ad Formats Overview

| Format | Type | Best For | Complexity |
|---|---|---|---|
| **Banner** | Inline | Persistent visibility, low friction | Simple |
| **Interstitial** | Full-screen | Natural transitions | Medium |
| **Rewarded** | Full-screen | In-app currency, premium unlocks | Medium |
| **Rewarded Interstitial** | Full-screen | Rewards without opt-in prompt | Medium |
| **App Open** | Full-screen | Cold start monetization | Medium |

See **[references/ad-formats.md](./references/ad-formats.md)** for complete code examples of each format.

## Banner Ad Quick Start

Banners are the most common ad format — here's a ready-to-use component:

```tsx
import { BannerAd, BannerAdSize, TestIds } from "react-native-google-mobile-ads";

const adUnitId = __DEV__ ? TestIds.BANNER : "ca-app-pub-xxxxx/yyyyy";

export function AdBanner() {
  return (
    <BannerAd
      unitId={adUnitId}
      size={BannerAdSize.ANCHORED_ADAPTIVE_BANNER}
      requestOptions={{
        networkExtras: {
          collapsible: "bottom", // collapsible banner (optional)
        },
      }}
    />
  );
}
```

Common banner sizes: `BANNER` (320x50), `LARGE_BANNER` (320x100), `MEDIUM_RECTANGLE` (300x250), `FULL_BANNER` (468x60), `LEADERBOARD` (728x90), `ANCHORED_ADAPTIVE_BANNER` (adaptive width).

## Full-Screen Ads Pattern

All full-screen ad types follow the same lifecycle:

```
createForAdRequest() → load event → show() → closed event → load next
```

1. Create the ad instance with your ad unit ID
2. Register event listeners (loaded, error, closed, earned_reward)
3. Call `.load()` to fetch the ad
4. Call `.show()` when the ad is ready and the moment is right
5. Preload the next ad in the `closed` handler

See **[references/ad-formats.md](./references/ad-formats.md)** for full implementations.

## Consent & Privacy

Before showing ads, you must handle user consent (required for GDPR in EEA and for App Tracking Transparency on iOS):

1. **UMP SDK** — Built into `react-native-google-mobile-ads` via `AdsConsent`
2. **ATT (iOS)** — Use `expo-tracking-transparency` to request tracking permission

The correct flow: **Request consent → Request ATT → Initialize ads → Load ads**

See **[references/consent-setup.md](./references/consent-setup.md)** for full implementation.

## Ad Placement Best Practices

| Guideline | Details |
|---|---|
| **Banner placement** | Bottom of screen (anchored), or inline between content sections |
| **Interstitial timing** | Between levels, after completing a flow, on screen transitions — NOT on app launch or mid-action |
| **Rewarded trigger** | User-initiated only (e.g., "Watch ad for 50 coins" button) |
| **Frequency cap** | Max 1 interstitial per 60s; don't show back-to-back full-screen ads |
| **Don't stack ads** | Never show banner + full-screen simultaneously |
| **Loading indicator** | Show a loading state while full-screen ads load to avoid UI jank |
| **Preload early** | Load full-screen ads well before you need them (e.g., at screen mount) |
| **Handle failures** | If an ad fails to load, proceed normally — never block the user |

## Common Pitfalls

| Issue | Solution |
|---|---|
| Ads not showing in Expo Go | Use a development build — Expo Go does not support native modules |
| Account suspended | Use `TestIds` during development, never real ad unit IDs |
| Ads not loading | Call `mobileAds().initialize()` before any ad load; check network |
| Blank banner space | Handle `onAdFailedToLoad` — hide the container when no fill |
| Low fill rate in dev | Normal with test IDs; production IDs will have better fill |
| iOS ads not loading | Check ATT consent — denied tracking reduces personalized ad fill |
| Android crash on launch | Verify `androidAppId` in app.config.ts matches your AdMob console |
| Consent form not showing | UMP only shows in EEA/UK; test with `debugGeography` option |

## Resources

- **[Ad Format Examples](./references/ad-formats.md)** — Complete code for all 5 ad types
- **[Consent & Privacy Setup](./references/consent-setup.md)** — UMP SDK + ATT implementation
- [react-native-google-mobile-ads docs](https://docs.page/invertase/react-native-google-mobile-ads)
- [AdMob Console](https://apps.admob.com)
- [AdMob Policies](https://support.google.com/admob/answer/6128543)
