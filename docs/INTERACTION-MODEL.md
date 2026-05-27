# Interaction Model — Socratic Writer

This document defines the **exact** user experience. It is the most important design artifact because the constraints are so extreme.

## The Fundamental State

The application has exactly **one primary state** for writing:

> A completely blank, full-screen (or full-window) surface containing only the writer's text, rendered in a single, beautiful, highly readable serif or humanist sans typeface. Nothing else is visible.

There is no cursor in the traditional blinking sense if we can avoid it — or it is extremely subtle. The text simply grows downward as the writer types. The view auto-scrolls smoothly so the current line is always comfortably in the lower third of the screen.

## Typing Behavior

- Every printable character the user types is appended to the end of the text buffer.
- The writer never sees a "cursor" they can move. There is only the growing end of the text.
- Backspace, delete, arrow keys, home, end, page up/down — **all are disabled or produce no effect**.
- Enter/Return may be treated as a paragraph break (two newlines) or simply as another character, depending on later typographic decisions. The key point: it does not "execute" anything.

The writer experiences pure **forward momentum**. The only way to "fix" something is to keep writing and let the new thought supersede the old one.

## The Space Bar — The Only Deliberate Meta-Action

This is the single most important design decision we will make.

### Requirements for the Space Bar Trigger

1. It must be **extremely unlikely to trigger accidentally** during normal typing.
2. It must feel **deliberate and slightly ceremonial** — a conscious choice to step back and think.
3. It must be **reversible / ignorable** — pressing it by mistake must not pollute the writing or force the writer to deal with an unwanted AI response.
4. It should feel different from the space that occurs between words.

### Current Leading Candidate: "Committed Paragraph + Space"

- The writer types normally.
- When they finish a paragraph (two consecutive newlines or a deliberate double-enter), the paragraph is considered "committed."
- If the writer then presses **Space** while at the very end of the document (no characters after the last committed paragraph), this triggers the Socratic reflection on the most recent 1–3 paragraphs.

Alternative candidates to evaluate:

- **Double-space at end of line** (two rapid spaces when the cursor is at a natural break)
- **Long-press space** (hold for 600–800ms) — feels very intentional
- **Space on an otherwise empty line** after a paragraph
- **Three spaces** in a row (rare in normal prose)
- **Space + Enter** combination (but we want to avoid multi-key thinking)

**Open question**: Do we allow the space bar to produce a visible space character in the text at all, or is space *only* ever the trigger? (Strong argument for the latter given the constraints.)

## What Happens When the Space Bar Is Triggered

1. The system immediately acknowledges the request with **zero visual fanfare** — perhaps a single, very subtle line or a change in background warmth for 200ms, nothing more.
2. The LLM is called (asynchronously) with:
   - The full current text (or a smart window of recent committed paragraphs)
   - A carefully engineered system prompt that enforces strict Socratic behavior
3. While the LLM thinks, the writer **continues typing completely normally**. There is no spinner, no "generating..." text, no frozen interface. The AI response is a background event.
4. When the response is ready, it appears in one of two ways (to be prototyped and tested):

   **Option A — Quiet Margin Notes**
   - 1 to 3 short questions appear in a very narrow, extremely low-contrast right margin or bottom pane.
   - They use a smaller, lighter weight of the same typeface.
   - They do not push the main text or cause reflow.
   - They fade in over 800ms.

   **Option B — After-Current-Paragraph Overlay**
   - The questions appear as a single, elegant block right after the paragraph the writer was working on when they summoned.
   - The writer can simply keep typing and the questions scroll up and out of view naturally.

5. The writer may:
   - Completely ignore the questions and keep writing (they will eventually scroll away or be minimized).
   - Let one question influence the next things they type.
   - (In a future review mode) explicitly "answer" a question by writing in response to it.

**Critical rule**: The appearance of Socratic content must **never** stop the writer from continuing to type. Keystrokes must always go to the main text buffer.

## Text Rendering & Typography

- Single font family, two weights maximum (regular + light for AI questions).
- Excellent line length (ideally 70–85 characters).
- Generous, but not wasteful, line spacing.
- Very high contrast text on warm off-white or true paper background. No pure white.
- Subtle, almost invisible vertical rhythm lines or none at all.
- No syntax highlighting, no markdown rendering while writing. Plain text only.

Later we may add an extremely minimal "review" mode where the text is re-rendered with light structural markup (headings detected, etc.), but this is never the writing view.

## Session Model

- The tool opens to a single, infinite writing surface.
- There is no "new document" action. You are always writing.
- Sessions are saved automatically and continuously (local plain text + optional metadata).
- The writer can have multiple named "threads" or "notebooks" but switching between them is a deliberate, separate action — not something done mid-flow.
- On launch, the writer is immediately returned to where they left off, with the last few paragraphs visible.

## What "Feedback" Actually Means

The user said: "space bar is the only input for extra controll for must have feedback."

"Feedback" here is interpreted as **Socratic reflection / structural insight**, not:
- Spell check
- Word count
- "How am I doing?"
- Generic encouragement

The only thing the system ever "tells" the writer is a small number of high-signal questions derived from the writer's own words.

## Edge Cases to Resolve

- What happens if the writer presses space in the middle of a sentence?
- What if they trigger it 40 times in a row?
- How do we handle very long sessions (10k+ words)? Does the LLM get the whole thing or a sliding window?
- Can the writer ever delete or edit in a later "reflection" phase, or is editing always a separate, heavier tool?
- Is there a way to "dismiss" AI questions without answering them, or do they just naturally age out?

These will be answered through rapid prototyping and real use, not upfront speculation.

---

## Summary Table (For Quick Reference)

| Action                    | Result                              | Allowed? |
|---------------------------|-------------------------------------|----------|
| Type letters/punctuation  | Appended to text                    | Yes      |
| Space (normal)            | TBD — either space char or trigger  | Special  |
| Backspace / Delete        | No effect                           | No       |
| Arrow keys / navigation   | No effect                           | No       |
| Enter                     | Paragraph break (likely)            | Yes      |
| Mouse movement / clicks   | Ignored or hidden cursor            | No       |
| Any modifier + key        | No effect                           | No       |
| Space bar (deliberate)    | Summon Socratic reflection          | Only meta action |

This model will be validated and refined only by building and using it.
