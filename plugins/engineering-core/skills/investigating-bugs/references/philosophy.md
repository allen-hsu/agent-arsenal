# Engineering Philosophy

Core principles for systematic debugging and investigation. Extracted from
battle-tested engineering practices.

---

## Boil the Lake

AI-assisted coding makes the marginal cost of completeness near-zero. When
the complete implementation costs minutes more than the shortcut -- do the
complete thing. Every time.

**Lake vs. ocean:** A "lake" is boilable -- 100% test coverage for a module,
full feature implementation, all edge cases, complete error paths. An "ocean"
is not -- rewriting an entire system from scratch, multi-quarter platform
migrations. Boil lakes. Flag oceans as out of scope.

**Completeness is cheap.** When evaluating "approach A (full, ~150 LOC) vs
approach B (90%, ~80 LOC)" -- always prefer A. The 70-line delta costs
seconds with AI coding.

**Anti-patterns:**
- "Choose B -- it covers 90% with less code." (If A is 70 lines more, choose A.)
- "Let's defer tests to a follow-up PR." (Tests are the cheapest lake to boil.)
- "This would take 2 weeks." (Say: "2 weeks human / ~1 hour AI-assisted.")

---

## Search Before Building

The first instinct should be "has someone already solved this?" not "let me
design it from scratch." Before building anything involving unfamiliar
patterns, infrastructure, or runtime capabilities -- stop and search first.
The cost of checking is near-zero. The cost of not checking is reinventing
something worse.

### Three Layers of Knowledge

**Layer 1: Tried and true.** Standard patterns, battle-tested approaches.
The risk is not that you don't know -- it's that you assume the obvious
answer is right when occasionally it isn't.

**Layer 2: New and popular.** Current best practices, blog posts, ecosystem
trends. Search for these. But scrutinize what you find -- the crowd can be
wrong about new things just as easily as old things.

**Layer 3: First principles.** Original observations derived from reasoning
about the specific problem at hand. These are the most valuable of all.
Prize them above everything else.

### The Eureka Moment

The most valuable outcome of searching is not finding a solution to copy. It is:

1. Understanding what everyone is doing and WHY (Layers 1 + 2)
2. Applying first-principles reasoning to their assumptions (Layer 3)
3. Discovering a clear reason why the conventional approach is wrong

---

## The Completeness Principle

Together: search first, then build the complete version of the right thing.
The worst outcome is building a complete version of something that already
exists as a one-liner. The best outcome is building a complete version of
something nobody has thought of yet -- because you searched, understood the
landscape, and saw what everyone else missed.

**Applied to debugging:** Don't just fix the symptom. Search for the root
cause, understand the full failure mode, write the regression test, and
verify the fix. The complete investigation costs minutes more than the
quick patch -- and prevents the bug from recurring.
