---
name: designing-mobile-ui
description: "Mobile UI/UX design intelligence for React Native. Searchable database of color palettes, UI styles, typography, and UX guidelines. Actions: design, build, create, implement, review, fix, improve, optimize, enhance mobile UI. Projects: mobile app, iOS app, Android app, React Native app, Expo app. Elements: button, card, modal, bottom sheet, tab bar, list, form, input. Styles: iOS native, Material Design, glassmorphism, neumorphism, minimal, bold, luxury, dark mode. Topics: color palette, typography, font pairing, animation, gesture, haptics, safe area, touch target, accessibility."
---

# Mobile Design (React Native) - Design Intelligence

Searchable database of mobile UI styles, color palettes, font pairings, UX guidelines, and product recommendations for React Native apps.

## Prerequisites

Check if Python is installed:

```bash
python3 --version || python --version
```

If Python is not installed, install it based on your OS:

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

---

## How to Use This Skill

When user requests mobile UI/UX work (design, build, create, implement, review, fix, improve), follow this workflow:

### Step 1: Analyze User Requirements

Extract key information from user request:
- **App type**: Social, fintech, e-commerce, health, etc.
- **Style keywords**: minimal, bold, luxury, playful, dark mode, etc.
- **Platform focus**: iOS-first, Android-first, cross-platform
- **Target audience**: Teens, professionals, seniors, kids, etc.

### Step 2: Search Design Database

Use `search.py` multiple times to gather comprehensive design information.

```bash
# Run from the skill's directory:
python3 ./scripts/search.py "<keywords>" --domain <domain> [-n <max_results>]
```

**Recommended search order:**

1. **Products** - Get style/color/typography recommendations for app type
2. **Colors** - Get color palette with hex values
3. **Styles** - Get detailed style guide (radius, shadows, animations)
4. **Typography** - Get font pairings with Expo installation
5. **UX** - Get mobile-specific UX guidelines

### Step 3: Apply Design Patterns

After gathering design data:
1. Use the recommended color palette in `tailwind.config.js`
2. Apply the recommended style characteristics
3. Load fonts via `expo-google-fonts`
4. Follow UX guidelines for interactions

---

## Search Reference

### Available Domains

| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `products` | App type recommendations | social, fintech, health, e-commerce, gaming |
| `colors` | Color palettes by category | bold, minimal, luxury, playful, dark |
| `styles` | UI styles and characteristics | ios, material, glassmorphism, minimal, bold |
| `typography` | Font pairings | modern, elegant, playful, tech, minimal |
| `ux` | Mobile UX guidelines | touch, keyboard, haptics, animation, loading |
| `all` | Search everything | (any keywords) |

### Example Workflow

**User request:** "Build a banking app with premium feel"

```bash
# 1. Search product type
python3 ./scripts/search.py "banking fintech" --domain products

# 2. Search recommended colors
python3 ./scripts/search.py "luxury gold premium" --domain colors

# 3. Search style
python3 ./scripts/search.py "luxury refined elegant" --domain styles

# 4. Search typography
python3 ./scripts/search.py "modern professional" --domain typography

# 5. Search relevant UX guidelines
python3 ./scripts/search.py "touch keyboard" --domain ux
python3 ./scripts/search.py "haptics" --domain ux
```

---

## Common Rules for Professional Mobile UI

These are frequently overlooked issues that make mobile UI look unprofessional:

### Touch & Interaction

| Rule | Do | Don't |
|------|----|----|
| **44pt minimum** | Use `min-h-[44px] min-w-[44px]` for all buttons | Make touch targets smaller than 44pt |
| **Touch feedback** | Add scale animation (0.95) on press | No visual feedback on press |
| **Haptic feedback** | Use `Haptics.impactAsync()` on important actions | Silent interactions |
| **Extended hit area** | Use `hitSlop={12}` for small icons | Leave small icons without hitSlop |

### Safe Areas & Layout

| Rule | Do | Don't |
|------|----|----|
| **Safe area insets** | Use `useSafeAreaInsets()` for padding | Ignore notches and home indicators |
| **Bottom sheet padding** | Add extra bottom padding for home indicator | Let content overlap home indicator |
| **Keyboard avoiding** | Use `KeyboardAvoidingView` with correct behavior | Let keyboard cover inputs |
| **Tab bar visibility** | Keep tabs visible on main screens | Hide tabs unnecessarily |

### Lists & Performance

| Rule | Do | Don't |
|------|----|----|
| **Virtualized lists** | Use `FlashList` or `FlatList` for lists | Use `ScrollView` with `map()` for long lists |
| **Pull to refresh** | Add `RefreshControl` to data lists | Force users to tap refresh button |
| **Skeleton loading** | Show skeleton placeholders while loading | Show only spinner or blank screen |
| **Optimistic updates** | Update UI immediately, sync later | Wait for server response to update UI |

### Animations

| Rule | Do | Don't |
|------|----|----|
| **Spring physics** | Use `withSpring()` for natural feel | Use `withTiming()` with linear easing |
| **Duration limits** | Keep UI animations 200-400ms | Use animations > 500ms for feedback |
| **Reduced motion** | Respect `prefers-reduced-motion` | Ignore accessibility preferences |
| **Layout animations** | Use `Layout.springify()` for list reordering | Instant layout changes |

### Typography & Text

| Rule | Do | Don't |
|------|----|----|
| **Dynamic Type** | Support iOS Dynamic Type for accessibility | Use only fixed font sizes |
| **Line height** | Use `leading-relaxed` for body text | Use tight line height for paragraphs |
| **Custom fonts** | Load via `expo-font` or `expo-google-fonts` | Rely only on system fonts |
| **Text truncation** | Use `numberOfLines` with ellipsis | Let text overflow containers |

### Images & Media

| Rule | Do | Don't |
|------|----|----|
| **Placeholder** | Use blurhash or solid color placeholder | Show broken image or spinner |
| **Aspect ratio** | Maintain consistent ratios in lists | Random aspect ratios |
| **Optimized loading** | Use `expo-image` with caching | Use `Image` without optimization |
| **Lazy loading** | Load images as they enter viewport | Load all images at once |

---

## Pre-Delivery Checklist

Before delivering mobile UI code, verify these items:

### Touch & Interaction
- [ ] All buttons have min 44pt touch target
- [ ] Press states provide visual feedback (scale/opacity)
- [ ] Important actions have haptic feedback
- [ ] Small icons have `hitSlop` extended

### Layout & Safe Areas
- [ ] Content respects safe area insets
- [ ] Keyboard doesn't cover input fields
- [ ] Bottom sheets have home indicator padding
- [ ] Fixed elements don't overlap content

### Lists & Data
- [ ] Long lists use virtualized components
- [ ] Data lists have pull to refresh
- [ ] Loading states show skeletons
- [ ] Empty states are designed

### Animations
- [ ] Animations use spring physics
- [ ] Durations are 200-400ms for feedback
- [ ] `prefers-reduced-motion` is respected
- [ ] No janky or dropped frames

### Typography
- [ ] Custom fonts are loaded correctly
- [ ] Body text has proper line height
- [ ] Text truncates with ellipsis
- [ ] Font weights are consistent

### Accessibility
- [ ] Touch targets are accessible size
- [ ] Color contrast meets WCAG AA
- [ ] Screen readers can navigate
- [ ] Dynamic Type is supported

### Platform Specific
- [ ] iOS: Swipe back gesture works
- [ ] iOS: Home indicator doesn't overlap UI
- [ ] Android: Back button works correctly
- [ ] Android: Status bar styled appropriately

---

## Tech Stack Reference

| Tool | Purpose |
|------|---------|
| NativeWind | Tailwind CSS for React Native |
| tailwind-variants | Type-safe component variants |
| react-native-reanimated | Performant animations |
| react-native-gesture-handler | Touch interactions |
| expo-image | Optimized images with blur hash |
| @gorhom/bottom-sheet | Beautiful bottom sheets |
| expo-haptics | Haptic feedback |
| expo-font / expo-google-fonts | Custom fonts |

---

## Resources

- **Color Palettes**: [references/color-palettes.md](references/color-palettes.md)
- **Animation Patterns**: [references/animations.md](references/animations.md)
- **Component Gallery**: [references/components.md](references/components.md)
