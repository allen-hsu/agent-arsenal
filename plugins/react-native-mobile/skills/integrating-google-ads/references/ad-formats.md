# Ad Format Reference

Complete code examples for all Google AdMob ad types in React Native.

## Banner Ads

The simplest ad format — displays inline within your UI.

### Basic Banner

```tsx
import { BannerAd, BannerAdSize, TestIds } from "react-native-google-mobile-ads";

const adUnitId = __DEV__ ? TestIds.BANNER : "ca-app-pub-xxxxx/yyyyy";

export function AdBanner() {
  return (
    <BannerAd
      unitId={adUnitId}
      size={BannerAdSize.ANCHORED_ADAPTIVE_BANNER}
    />
  );
}
```

### Banner with Error Handling

Hide the ad container when no fill is available:

```tsx
import { useState } from "react";
import { View } from "react-native";
import { BannerAd, BannerAdSize, TestIds } from "react-native-google-mobile-ads";

const adUnitId = __DEV__ ? TestIds.BANNER : "ca-app-pub-xxxxx/yyyyy";

export function AdBanner() {
  const [adLoaded, setAdLoaded] = useState(false);
  const [adError, setAdError] = useState(false);

  if (adError) return null;

  return (
    <View style={{ opacity: adLoaded ? 1 : 0 }}>
      <BannerAd
        unitId={adUnitId}
        size={BannerAdSize.ANCHORED_ADAPTIVE_BANNER}
        onAdLoaded={() => setAdLoaded(true)}
        onAdFailedToLoad={() => setAdError(true)}
      />
    </View>
  );
}
```

### Banner Sizes

| Constant | Size | Description |
|---|---|---|
| `BANNER` | 320x50 | Standard banner |
| `LARGE_BANNER` | 320x100 | Large banner |
| `MEDIUM_RECTANGLE` | 300x250 | Medium rectangle (in-feed) |
| `FULL_BANNER` | 468x60 | Full-size banner (tablet) |
| `LEADERBOARD` | 728x90 | Leaderboard (tablet) |
| `ANCHORED_ADAPTIVE_BANNER` | Adaptive | Adapts to screen width (recommended) |
| `INLINE_ADAPTIVE_BANNER` | Adaptive | For ScrollView / FlatList |

### Collapsible Banners

Collapsible banners start expanded and can be collapsed by the user:

```tsx
<BannerAd
  unitId={adUnitId}
  size={BannerAdSize.ANCHORED_ADAPTIVE_BANNER}
  requestOptions={{
    networkExtras: {
      collapsible: "bottom", // "top" or "bottom"
    },
  }}
/>
```

### iOS useForeground Hook

On iOS, banner ads pause when the app backgrounds. Use `useForeground` to resume:

```tsx
import { useForeground } from "react-native-google-mobile-ads";
import { useRef } from "react";
import { Platform } from "react-native";

export function AdBanner() {
  const bannerRef = useRef<BannerAd>(null);

  if (Platform.OS === "ios") {
    useForeground(() => {
      bannerRef.current?.load();
    });
  }

  return (
    <BannerAd
      ref={bannerRef}
      unitId={adUnitId}
      size={BannerAdSize.ANCHORED_ADAPTIVE_BANNER}
    />
  );
}
```

## Interstitial Ads

Full-screen ads shown at natural transition points.

```tsx
import { useEffect, useState } from "react";
import {
  InterstitialAd,
  AdEventType,
  TestIds,
} from "react-native-google-mobile-ads";

const adUnitId = __DEV__ ? TestIds.INTERSTITIAL : "ca-app-pub-xxxxx/yyyyy";
const interstitial = InterstitialAd.createForAdRequest(adUnitId);

export function useInterstitialAd() {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const unsubLoaded = interstitial.addAdEventListener(
      AdEventType.LOADED,
      () => setLoaded(true)
    );
    const unsubClosed = interstitial.addAdEventListener(
      AdEventType.CLOSED,
      () => {
        setLoaded(false);
        interstitial.load(); // preload next
      }
    );

    interstitial.load();

    return () => {
      unsubLoaded();
      unsubClosed();
    };
  }, []);

  const show = () => {
    if (loaded) {
      interstitial.show();
    }
  };

  return { loaded, show };
}
```

### Usage

```tsx
function GameScreen() {
  const { loaded, show } = useInterstitialAd();

  const onLevelComplete = () => {
    // Show interstitial between levels
    if (loaded) show();
    navigateToNextLevel();
  };

  return <Button title="Next Level" onPress={onLevelComplete} />;
}
```

### iOS StatusBar Issue

On iOS, the status bar may hide after closing an interstitial. Fix:

```tsx
import { StatusBar, Platform } from "react-native";

interstitial.addAdEventListener(AdEventType.CLOSED, () => {
  if (Platform.OS === "ios") {
    StatusBar.setHidden(false);
  }
});
```

## Rewarded Ads

Users opt in to watch an ad in exchange for a reward.

```tsx
import { useEffect, useState } from "react";
import {
  RewardedAd,
  RewardedAdEventType,
  TestIds,
} from "react-native-google-mobile-ads";

const adUnitId = __DEV__ ? TestIds.REWARDED : "ca-app-pub-xxxxx/yyyyy";
const rewarded = RewardedAd.createForAdRequest(adUnitId);

export function useRewardedAd() {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const unsubLoaded = rewarded.addAdEventListener(
      RewardedAdEventType.LOADED,
      () => setLoaded(true)
    );
    const unsubEarned = rewarded.addAdEventListener(
      RewardedAdEventType.EARNED_REWARD,
      (reward) => {
        console.log(`User earned: ${reward.amount} ${reward.type}`);
        // Grant reward to user here
      }
    );
    const unsubClosed = rewarded.addAdEventListener(
      RewardedAdEventType.CLOSED,
      () => {
        setLoaded(false);
        rewarded.load();
      }
    );

    rewarded.load();

    return () => {
      unsubLoaded();
      unsubEarned();
      unsubClosed();
    };
  }, []);

  const show = () => {
    if (loaded) rewarded.show();
  };

  return { loaded, show };
}
```

### Server-Side Verification (SSV)

For high-value rewards, verify on your server to prevent fraud:

```tsx
const rewarded = RewardedAd.createForAdRequest(adUnitId, {
  serverSideVerificationOptions: {
    userId: "user-123",
    customData: "extra-data",
  },
});
```

Google sends a callback to your server URL (configured in AdMob console) when the user earns a reward.

## Rewarded Interstitial Ads

Like rewarded ads, but shown without requiring a user opt-in prompt. The user still earns a reward.

```tsx
import { useEffect, useState } from "react";
import {
  RewardedInterstitialAd,
  RewardedAdEventType,
  TestIds,
} from "react-native-google-mobile-ads";

const adUnitId = __DEV__
  ? TestIds.REWARDED_INTERSTITIAL
  : "ca-app-pub-xxxxx/yyyyy";
const rewardedInterstitial =
  RewardedInterstitialAd.createForAdRequest(adUnitId);

export function useRewardedInterstitialAd() {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const unsubLoaded = rewardedInterstitial.addAdEventListener(
      RewardedAdEventType.LOADED,
      () => setLoaded(true)
    );
    const unsubEarned = rewardedInterstitial.addAdEventListener(
      RewardedAdEventType.EARNED_REWARD,
      (reward) => {
        console.log(`User earned: ${reward.amount} ${reward.type}`);
      }
    );
    const unsubClosed = rewardedInterstitial.addAdEventListener(
      RewardedAdEventType.CLOSED,
      () => {
        setLoaded(false);
        rewardedInterstitial.load();
      }
    );

    rewardedInterstitial.load();

    return () => {
      unsubLoaded();
      unsubEarned();
      unsubClosed();
    };
  }, []);

  const show = () => {
    if (loaded) rewardedInterstitial.show();
  };

  return { loaded, show };
}
```

## App Open Ads

Shown when users bring your app to the foreground. Best for monetizing the cold start experience.

```tsx
import { useEffect, useRef, useState } from "react";
import { AppState, AppStateStatus } from "react-native";
import {
  AppOpenAd,
  AdEventType,
  TestIds,
} from "react-native-google-mobile-ads";

const adUnitId = __DEV__ ? TestIds.APP_OPEN : "ca-app-pub-xxxxx/yyyyy";

const EXPIRY_MS = 4 * 60 * 60 * 1000; // 4 hours — ads expire after this

export function useAppOpenAd() {
  const appOpenAd = useRef<AppOpenAd | null>(null);
  const loadTime = useRef<number>(0);
  const appState = useRef(AppState.currentState);

  const loadAd = () => {
    const ad = AppOpenAd.createForAdRequest(adUnitId);

    ad.addAdEventListener(AdEventType.LOADED, () => {
      loadTime.current = Date.now();
    });
    ad.addAdEventListener(AdEventType.CLOSED, () => {
      loadAd(); // preload next
    });

    ad.load();
    appOpenAd.current = ad;
  };

  const showIfReady = () => {
    const ad = appOpenAd.current;
    if (!ad?.loaded) return;

    // Don't show expired ads
    if (Date.now() - loadTime.current > EXPIRY_MS) {
      loadAd();
      return;
    }

    ad.show();
  };

  useEffect(() => {
    loadAd();

    const subscription = AppState.addEventListener(
      "change",
      (nextAppState: AppStateStatus) => {
        if (
          appState.current.match(/inactive|background/) &&
          nextAppState === "active"
        ) {
          showIfReady();
        }
        appState.current = nextAppState;
      }
    );

    return () => subscription.remove();
  }, []);
}
```

**Important:** App Open Ads have a **4-hour expiry**. Always check the load time before showing.

## Ad Lifecycle Events

All ad types emit these events:

| Event | Constant | When |
|---|---|---|
| Loaded | `AdEventType.LOADED` | Ad is ready to display |
| Error | `AdEventType.ERROR` | Ad failed to load (includes error code) |
| Opened | `AdEventType.OPENED` | Full-screen ad is now visible |
| Closed | `AdEventType.CLOSED` | User closed the ad |
| Clicked | `AdEventType.CLICKED` | User tapped the ad |
| Impression | `AdEventType.IMPRESSION` | Ad recorded an impression |
| Paid | `AdEventType.PAID` | Revenue event (for analytics) |

Rewarded ads also have:

| Event | Constant | When |
|---|---|---|
| Earned Reward | `RewardedAdEventType.EARNED_REWARD` | User completed the rewarded action |

### PAID Event for Revenue Tracking

```tsx
import { AdEventType } from "react-native-google-mobile-ads";

ad.addAdEventListener(AdEventType.PAID, (event) => {
  // Send to your analytics (Firebase, Adjust, AppsFlyer, etc.)
  analytics.logAdRevenue({
    value: event.value,
    currency: event.currency,
    precision: event.precision, // "estimated", "publisher_provided", "precise"
  });
});
```
