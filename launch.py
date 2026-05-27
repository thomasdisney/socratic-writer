#!/usr/bin/env python3
"""
Socratic Writer — Launcher
Serves the app locally and opens it in a clean browser window.
This is the official way to start the writing tool.
"""

import http.server
import socketserver
import threading
import webbrowser
import socket
import os
import sys
import subprocess
import time
import json
import shlex
from pathlib import Path

# Configuration
APP_DIR = Path(__file__).parent / "app"
PORT = 0  # 0 = auto-assign free port
BROWSER = "firefox"  # We know firefox is available on this machine

class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Serve files quietly. Only log errors.
    Provides a same-origin proxy that invokes the local Grok Build CLI
    (`grok --single`) for Socratic question generation. Falls back to the
    built-in heuristic in the browser when the CLI is unavailable.
    """

    def log_message(self, format, *args):
        # Only log real problems
        if args and len(args) > 0 and "404" in str(args[0]):
            super().log_message(format, *args)

    def end_headers(self):
        # Strong no-cache headers so we always get the latest version during development
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    GROK_CLI = "/home/demo/.grok/bin/grok"

    def do_POST(self):
        if self.path != "/api/reflect":
            self.send_error(404, "Not found")
            return

        try:
            content_len = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_len).decode('utf-8')
            payload = json.loads(body)

            # We ignore the "model" field — Grok Build CLI uses the environment's default (grok-build)
            system_prompt = payload.get("system", "").strip()
            recent_text = payload.get("text", "").strip()

            if not recent_text:
                self._send_json({"questions": [], "error": "empty text"}, 400)
                return

            # Build a single strong prompt for the Grok CLI.
            # The CLI with --single is our "LLM" now. No local models.
            full_prompt = (
                "You are a strict Socratic mirror for a writer. "
                "Your ONLY output must be 0-3 short, penetrating questions (one per line). "
                "Never add any other text, numbers, bullets, explanations, or pleasantries.\n\n"
                f"{system_prompt}\n\n"
                f"=== RECENT TEXT ===\n{recent_text}\n=== END TEXT ===\n\n"
                "Output ONLY the questions now, one per line."
            )

            # Call the Grok Build CLI in fully headless single-turn mode.
            # This replaces any local model (Ollama etc.).
            cmd = [
                self.GROK_CLI,
                "--single", full_prompt,
                "--output-format", "plain",
                "--no-memory",
                "--no-plan",
                "--no-subagents",
                "--permission-mode", "bypassPermissions",
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=45,
                cwd="/home/demo/Desktop/Writer",  # stable cwd
            )

            if result.returncode != 0:
                raise RuntimeError(f"grok CLI exited {result.returncode}: {result.stderr[:300]}")

            raw = (result.stdout or "").strip()

            # Parse into clean questions (one per line, max 3). Very defensive.
            lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
            questions = []
            for ln in lines:
                if 8 <= len(ln) <= 280 and ln.endswith("?"):
                    questions.append(ln)
                if len(questions) >= 3:
                    break

            self._send_json({
                "questions": questions,
                "source": "grok-cli",
            })

        except subprocess.TimeoutExpired:
            self._send_json({
                "questions": [],
                "error": "grok_cli_timeout",
            }, 504)
        except FileNotFoundError:
            self._send_json({
                "questions": [],
                "error": "grok_cli_not_found",
            }, 503)
        except Exception as e:
            self._send_json({
                "questions": [],
                "error": "grok_cli_error",
                "detail": str(e)[:200],
            }, 503)

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

def launch_browser(url: str):
    """Try to open a clean, distraction-free browser window."""
    try:
        # Firefox with a new instance + new window (cleaner than default)
        subprocess.Popen(
            [BROWSER, "--new-instance", "--new-window", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        print(f"→ Opened in Firefox: {url}")
        print("   (Press F11 in the browser for true fullscreen writing mode)")
    except FileNotFoundError:
        print("Firefox not found. Falling back to system default browser...")
        webbrowser.open(url, new=1)
    except Exception as e:
        print(f"Could not launch browser cleanly: {e}")
        webbrowser.open(url, new=1)

def main():
    if not APP_DIR.exists():
        print(f"ERROR: app directory not found at {APP_DIR}")
        sys.exit(1)

    port = find_free_port()
    
    # Change to the app directory so index-like serving works
    os.chdir(APP_DIR)

    handler = QuietHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        url = f"http://127.0.0.1:{port}/socratic-writer.html"
        
        print("\n" + "=" * 54)
        print("  SOCRATIC WRITER")
        print("  Ultra-minimalist writing surface")
        print("=" * 54)
        print(f"\n  Serving from: {APP_DIR}")
        print(f"  Local URL:    {url}")
        print("\n  Rules active in this session:")
        print("    • Only forward typing is possible")
        print("    • Backspace, arrows, delete — disabled")
        print("    • Hold SPACE (650ms) at end of a thought → Socratic questions")
        print("    • Type 'sample1' then hold space for a demo text")
        print("    • Type 'export' then hold space to save your writing")
        print("\n  LLM (powered by Grok via the Build CLI):")
        print("    • When the grok CLI is available and authenticated, holding space")
        print("      calls Grok for high-quality Socratic questions.")
        print("    • If the CLI is not reachable it instantly falls back to the")
        print("      excellent local heuristic engine (no change in experience).")
        print("\n  Close this terminal window or press Ctrl+C to stop the app.\n")

        # Launch browser in a background thread so the server starts immediately
        threading.Thread(target=launch_browser, args=(url,), daemon=True).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nSocratic Writer stopped.")
            sys.exit(0)

if __name__ == "__main__":
    main()
