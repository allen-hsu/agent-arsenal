# Consent & Privacy Setup

How to implement GDPR consent (UMP SDK) and iOS App Tracking Transparency (ATT) for AdMob.

## Required Flow

```
App Launch
  → Request UMP consent info
  → Show consent form (if required)
  → Request ATT permission (iOS)
  → Initialize mobile ads SDK
  → Load ads
```

**This order matters.** Consent must be obtained before initializing ads.

## 1. UMP SDK (Google's User Messaging Platform)

Built into `react-native-google-mobile-ads` — no extra install needed.

### Basic Consent Flow

```tsx
import mobileAds, { AdsConsent, AdsConsentStatus } from "react-native-google-mobile-ads";

async function initializeAdsWithConsent() {
  // 1. Request consent info update
  const consentInfo = await AdsConsent.requestInfoUpdate();

  // 2. Show consent form if required
  if (consentInfo.isConsentFormAvailable && consentInfo.status === AdsConsentStatus.REQUIRED) {
    await AdsConsent.loadAndShowConsentFormIfRequired();
  }

  // 3. Check if ads can be shown
  const { canRequestAds } = await AdsConsent.getConsentInfo();

  if (canRequestAds) {
    // 4. Initialize ads SDK
    await mobileAds().initialize();
  }
}
```

### Consent Status Values

| Status | Meaning |
|---|---|
| `AdsConsentStatus.UNKNOWN` | Consent not yet requested |
| `AdsConsentStatus.NOT_REQUIRED` | User is not in EEA/UK — no consent needed |
| `AdsConsentStatus.REQUIRED` | Consent required but not yet obtained |
| `AdsConsentStatus.OBTAINED` | User has given or refused consent |

### Testing Consent in Development

UMP consent forms only appear in EEA/UK by default. To test outside those regions:

```tsx
const consentInfo = await AdsConsent.requestInfoUpdate({
  debugGeography: AdsConsentDebugGeography.EEA,
  testDeviceIdentifiers: ["YOUR_TEST_DEVICE_HASHED_ID"],
});
```

Import `AdsConsentDebugGeography` from `react-native-google-mobile-ads`.

### Resetting Consent (Dev Only)

```tsx
await AdsConsent.reset();
```

### Showing Privacy Options

For users who want to change their consent after initial choice:

```tsx
import { AdsConsent, AdsConsentPrivacyOptionsRequirementStatus } from "react-native-google-mobile-ads";

async function showPrivacyOptions() {
  const { privacyOptionsRequirementStatus } = await AdsConsent.getConsentInfo();

  if (privacyOptionsRequirementStatus === AdsConsentPrivacyOptionsRequirementStatus.REQUIRED) {
    await AdsConsent.showPrivacyOptionsForm();
  }
}
```

Add a "Privacy Settings" button in your app's settings screen that calls this function.

## 2. App Tracking Transparency (iOS)

Required on iOS 14+ to request permission to track users across apps.

### Install

```bash
npx expo install expo-tracking-transparency
```

### Configure app.config.ts

```ts
export default {
  expo: {
    plugins: [
      [
        "expo-tracking-transparency",
        {
          userTrackingPermission:
            "This identifier will be used to deliver personalized ads to you.",
        },
      ],
    ],
  },
};
```

### Request Permission

```tsx
import { requestTrackingPermissionsAsync } from "expo-tracking-transparency";
import { Platform } from "react-native";

async function requestATT() {
  if (Platform.OS !== "ios") return true;

  const { status } = await requestTrackingPermissionsAsync();
  return status === "granted";
}
```

### ATT Status Values

| Status | Meaning |
|---|---|
| `"granted"` | User allows tracking — full personalized ads |
| `"denied"` | User denied tracking — limited ad personalization |
| `"undetermined"` | Not yet asked |
| `"restricted"` | Device-level restriction (e.g., parental controls) |

> Even if denied, ads still show — they're just less targeted (lower eCPM).

## 3. Complete Integration

Putting it all together in your app entry point:

```tsx
import { useEffect, useState } from "react";
import { Platform } from "react-native";
import mobileAds, { AdsConsent, AdsConsentStatus } from "react-native-google-mobile-ads";
import { requestTrackingPermissionsAsync } from "expo-tracking-transparency";

export function useAdsInitialization() {
  const [adsReady, setAdsReady] = useState(false);

  useEffect(() => {
    async function initialize() {
      try {
        // Step 1: UMP consent
        const consentInfo = await AdsConsent.requestInfoUpdate();

        if (consentInfo.isConsentFormAvailable && consentInfo.status === AdsConsentStatus.REQUIRED) {
          await AdsConsent.loadAndShowConsentFormIfRequired();
        }

        // Step 2: ATT (iOS only)
        if (Platform.OS === "ios") {
          await requestTrackingPermissionsAsync();
        }

        // Step 3: Initialize ads
        const { canRequestAds } = await AdsConsent.getConsentInfo();

        if (canRequestAds) {
          await mobileAds().initialize();
          setAdsReady(true);
        }
      } catch (error) {
        console.warn("Ads initialization failed:", error);
        // Don't block app on ad init failure
      }
    }

    initialize();
  }, []);

  return adsReady;
}
```

### Usage in App Root

```tsx
function App() {
  const adsReady = useAdsInitialization();

  // App renders normally regardless of ad state
  return <MainNavigator />;
}
```

## 4. Full app.config.ts Example

All ad-related config in one place:

```ts
export default {
  expo: {
    plugins: [
      [
        "react-native-google-mobile-ads",
        {
          androidAppId: "ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy",
          iosAppId: "ca-app-pub-xxxxxxxxxxxxxxxx~zzzzzzzzzz",
          skAdNetworkItems: [
            "cstr6suwn9.skadnetwork", // Google
            // Add other ad network SKAdNetwork IDs as needed
          ],
        },
      ],
      [
        "expo-tracking-transparency",
        {
          userTrackingPermission:
            "This identifier will be used to deliver personalized ads to you.",
        },
      ],
    ],
  },
};
```

The `skAdNetworkItems` enable attribution tracking on iOS 14+ without user-level tracking. Google provides a [full list of SKAdNetwork IDs](https://developers.google.com/admob/ios/3p-skadnetworks) for their ad partners.
