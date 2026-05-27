# Keyboard Robustness Testing — Socratic Writer

**Goal**: Make every allowed keyboard input 100% reliable for forward-only writing, with zero visible changes to the writing experience.

**Core Principle**: All testing and debugging must be invisible to the normal user. No test UI, no on-screen indicators, no extra elements in the writing surface.

## How to Run Tests (Current Method)

1. Launch the app (`python3 ~/writer/launch.py` or Desktop icon).
2. Open Firefox DevTools Console (Ctrl+Shift+K).
3. In the console, type:

```js
SW.runKeyboardTests()
```

The entire suite runs with **zero visible changes** to the writing surface or any on-screen element. All results go to the console only.

Current harness creates an invisible off-screen test surface and drives real keyboard-style events through the core logic.

Run it as many times as you want — your actual writing is never touched.

## What "Basic Text Editor Keyboard Functions" Means Here

Allowed (must work perfectly):
- All printable characters from any keyboard layout (Latin, accented via dead keys, symbols, etc.)
- Enter / Return (creates paragraph breaks)
- Normal space character insertion (when not triggering the Socratic hold)
- The deliberate long-hold space (~650ms at end of text) as the single meta-action
- Shift + letters for uppercase
- Rapid, burst, and sustained typing

Explicitly forbidden (must remain completely blocked, no leakage):
- Backspace, Delete
- Arrow keys (all four)
- Home, End, PageUp, PageDown, Tab
- Ctrl/Cmd + A/C/V/X/Z/Y (and similar editing shortcuts)
- Any input that would move the caret or modify earlier text

## Current Test Coverage (in the harness)

- Basic insertion of letters, numbers, punctuation, and common symbols
- Multiple consecutive Enter presses
- Normal space insertion at end
- Long-hold space detection (time-controlled simulation)
- Forbidden key blocking (no text mutation)
- Rapid typing burst (50+ characters in quick succession)
- Shifted characters
- Modifier key combinations that should be ignored
- Attempted editing while a Socratic reflection is visible
- Edge case: typing immediately after a reflection is triggered

## How to Extend Tests

The test code lives inside `app/socratic-writer.html` near the bottom (search for `KeyboardTestHarness`).

To add a new case:
1. Add a method `testYourNewCase()` on the harness.
2. Call it from `runAll()`.
3. It should return `{ pass: boolean, message?: string }` or throw on failure.
4. The runner will aggregate results.

For even more rigorous external testing (future):
- Use Playwright or Puppeteer to drive the real page and inject real `KeyboardEvent`s.
- The harness is designed so the same test cases can later be ported to that environment.

**Self-contained iteration process (used by the maintainer):**
The single source of truth for keyboard logic is `tests/keyboard_simulator.py`.  
Run it with `python3 tests/keyboard_simulator.py [--verbose]`. It must report 100% pass before any JS change is considered complete.

This file now supports `--verbose` for detailed failure output during heavy iteration cycles.

The browser harness (`SW.runKeyboardTests()`) is a secondary smoke test that exercises real DOM events. It follows the same rules as the Python simulator.

## Iteration Rule

Do not declare the keyboard input "robust" until:
- 100% of the automated tests pass on the target browser (Firefox on Linux for this project).
- Manual testing with real international keyboard layouts + dead keys succeeds.
- Rapid typing never drops characters or inserts in the wrong place.
- The long-press space never accidentally inserts a space *or* fails to trigger when intended.

Only then move on to other work (real LLM, multiple threads, etc.).

## Philosophy Reminder

The visual surface must remain completely unchanged during this entire phase. All robustness work happens under the hood and in the console.
