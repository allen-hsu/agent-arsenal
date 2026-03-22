# Shipping Philosophy

Principles that shape how code should be shipped. These reflect what we believe
about building software in the AI-assisted era.

---

## 1. Boil the Lake

AI-assisted coding makes the marginal cost of completeness near-zero. When
the complete implementation costs minutes more than the shortcut -- do the
complete thing. Every time.

**Lake vs. ocean:** A "lake" is boilable -- 100% test coverage for a module,
full feature implementation, all edge cases, complete error paths. An "ocean"
is not -- rewriting an entire system from scratch, multi-quarter platform
migrations. Boil lakes. Flag oceans as out of scope.

**Completeness is cheap.** When evaluating "approach A (full, ~150 LOC) vs
approach B (90%, ~80 LOC)" -- always prefer A. The 70-line delta costs
seconds with AI coding. "Ship the shortcut" is legacy thinking from when
human engineering time was the bottleneck.

**Anti-patterns:**
- "Choose B -- it covers 90% with less code." (If A is 70 lines more, choose A.)
- "Let's defer tests to a follow-up PR." (Tests are the cheapest lake to boil.)
- "This would take 2 weeks." (Say: "2 weeks human / ~1 hour AI-assisted.")

---

## 2. Search Before Building

The first instinct should be "has someone already solved this?" not
"let me design it from scratch." Before building anything involving unfamiliar
patterns, infrastructure, or runtime capabilities -- stop and search first.
The cost of checking is near-zero. The cost of not checking is reinventing
something worse.

### Three Layers of Knowledge

**Layer 1: Tried and true.** Standard patterns, battle-tested approaches.
The risk is assuming the obvious answer is right when occasionally it isn't.

**Layer 2: New and popular.** Current best practices, ecosystem trends.
Search for these. But scrutinize -- the crowd can be wrong about new things.

**Layer 3: First principles.** Original observations derived from reasoning
about the specific problem. The most valuable of all. Prize them above
everything else.

**Anti-patterns:**
- Rolling a custom solution when the runtime has a built-in. (Layer 1 miss)
- Accepting blog posts uncritically in novel territory. (Layer 2 mania)
- Assuming tried-and-true is right without questioning premises. (Layer 3 blindness)

---

## 3. The Completeness Principle

**Search first, then build the complete version of the right thing.**

The worst outcome is building a complete version of something that already
exists as a one-liner. The best outcome is building a complete version of
something nobody has thought of yet -- because you searched, understood the
landscape, and saw what everyone else missed.

Together these principles mean:
- Never skip tests -- they are the cheapest lake to boil
- Never ship a shortcut when the complete version costs minutes more
- Never build from scratch without checking what exists
- Always prefer the thorough approach over the expedient one
