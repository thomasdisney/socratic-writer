# Product Spike 001: Minimal Backend for Hosted Socratic Writer (LLM Proxy + Stripe)

**Branch**: agent/product-hosted-v1-stripe-llm-spike
**Date**: 2026-05
**Status**: Initial design (post-ceremony). No code yet.

## Goals for this spike
- Thinnest possible backend that can:
  - Accept Socratic reflection requests from the writing surface (with auth token).
  - Proxy to a remote LLM (product pays) with the exact same strict Socratic system prompt and post-filtering.
  - Handle basic Stripe webhooks for subscription status / usage recording.
  - Return questions or graceful heuristic fallback signal.
- Zero impact on the existing writing surface code (isolated).
- Can be run locally for testing against the current 9876 surface (via proxy or env var endpoint).

## Non-Goals (for spike)
- Full auth system (use a simple shared secret or magic token for now).
- Full subscription UI or customer portal.
- Usage dashboard.
- Production deployment.
- Changing the core HTML/JS writing surface at all.

## Recommended Tech for Spike (to be confirmed by stack choice)
- Python (FastAPI or Flask) to stay close to the existing launcher.py culture, or Hono/Cloudflare Workers for edge.
- SQLite or in-memory for initial user/entitlement store.
- Stripe Python library for webhooks.
- LLM provider SDK (to be chosen).

## High-Level API Design (minimal)

POST /api/reflect
  Headers: Authorization: Bearer <token>
  Body: { "text": "...", "recent": "..." }
  Response: { "questions": ["...", ...], "source": "remote-llm" | "heuristic" }

POST /api/stripe/webhook (Stripe signed)
  Handles subscription events and usage recording.

GET /api/entitlement?token=...
  For the client to know if paid tier is active (for future UI hints outside writing flow).

## Open Decisions (need user input to proceed)
- Stack: Tauri desktop app + thin backend, or pure web (Next.js/SvelteKit)?
- LLM provider for paid tier (Grok/xAI, Claude, OpenAI, or other)?
- Rough pricing tiers and reflection limits?
- Domain name for the product?
- Does the pure local 9876 version need to stay a first-class, maintained, free/offline artifact forever, or can it be deprecated over time?

## Next after spike design approved
- Choose stack.
- Implement the spike in isolation (new directory, not touching app/).
- Test against the current writing surface by pointing LLM_ENDPOINT to the spike.
- Add basic Stripe test mode webhook handling.

This spike must remain completely isolated from the writing surface until the core invariants are re-verified with the simulator + harness.
