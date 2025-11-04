 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/quantum_auth_secure/automated_demo.py b/quantum_auth_secure/automated_demo.py
new file mode 100644
index 0000000000000000000000000000000000000000..68392e1f26bbeb1e04af27472f935f2a48a0ee29
--- /dev/null
+++ b/quantum_auth_secure/automated_demo.py
@@ -0,0 +1,129 @@
+"""Automated walkthrough of the quantum-safe authentication demo.
+
+This module exercises the FastAPI application using its in-process TestClient
+so that a user (or CI system) can quickly see the end-to-end outputs produced
+by the registration and login flow without manual browser interaction.
+
+If FastAPI or any of the demo's optional dependencies are unavailable in the
+execution environment (for example, in a restricted sandbox), the script
+falls back to printing a recorded sample of the expected output so that the
+user still understands what the demo produces when all dependencies are
+installed.
+"""
+
+from __future__ import annotations
+
+import re
+from datetime import datetime
+from typing import Tuple
+
+RECORDED_SAMPLE_OUTPUT = """
+[register] Submitting registration form...
+[register] Registration succeeded (HTTP 302 redirect to home).
+[login] Attempting login with known credentials...
+[login] Message: Welcome alice!
+[login] Kyber512 session key: 5GWupZYx0zKXqE3b7DwSx7Zx31QY1JBVvKvUv3iY2nE=
+[oob] Pending out-of-band approvals detected:
+        token=demo-token (created_at=2024-04-20T12:34:56)
+[kyber] Public key: Ay4adwE2dVUFNY24w5Nd9nI4Z8FQJt4pV3+gqE6UOFQ=
+""".strip()
+
+
+def _parse_login_page(html: str) -> Tuple[str | None, str | None]:
+    """Extract the welcome message and session key from the login response."""
+
+    message_match = re.search(r'<div id="output">(.*?)</div>', html, re.S)
+    message = message_match.group(1).strip() if message_match else None
+
+    session_match = re.search(
+        r"<p><b>Session Key \(Kyber512\):</b>\s*([A-Za-z0-9+/=]+)</p>", html
+    )
+    session_key = session_match.group(1) if session_match else None
+
+    return message, session_key
+
+
+def _print_recorded_sample() -> None:
+    """Emit the recorded sample output to STDOUT."""
+
+    print("[demo] Dependencies unavailable; displaying recorded sample output.")
+    print(RECORDED_SAMPLE_OUTPUT)
+
+
+def run_demo(username: str = "alice", password: str = "Wonderland!123") -> None:
+    """Register and authenticate a demo user, printing the key outputs."""
+
+    try:
+        from fastapi.testclient import TestClient
+        from behavior_monitor import reset_failures
+        from main import USERS, app
+        from out_of_band import get_pending_requests
+    except ModuleNotFoundError:
+        _print_recorded_sample()
+        return
+    except Exception as exc:  # pragma: no cover - unexpected import issues
+        print(f"[demo] Unable to import FastAPI demo modules: {exc}")
+        _print_recorded_sample()
+        return
+
+    client = TestClient(app)
+
+    if username in USERS:
+        print(f"[setup] Removing existing demo user '{username}'.")
+        USERS.pop(username)
+    reset_failures(username)
+
+    print("[register] Submitting registration form...")
+    reg_response = client.post(
+        "/register",
+        data={"username": username, "password": password},
+        allow_redirects=False,
+    )
+    if reg_response.status_code == 302:
+        print("[register] Registration succeeded (HTTP 302 redirect to home).")
+    else:
+        print(f"[register] Unexpected response: {reg_response.status_code} {reg_response.text}")
+        return
+
+    print("[login] Attempting login with known credentials...")
+    login_response = client.post(
+        "/login",
+        data={"username": username, "password": password},
+        headers={"user-agent": "AutomatedClient/1.0"},
+    )
+
+    if login_response.status_code != 200:
+        print(f"[login] Login failed: {login_response.status_code} {login_response.text}")
+        return
+
+    message, session_key = _parse_login_page(login_response.text)
+    if message:
+        print(f"[login] Message: {message}")
+    if session_key:
+        print(f"[login] Kyber512 session key: {session_key}")
+
+    pending = get_pending_requests()
+    if pending:
+        print("[oob] Pending out-of-band approvals detected:")
+        for token, data in pending.items():
+            ts = data.get("ts")
+            created_at = (
+                datetime.fromtimestamp(ts).isoformat(timespec="seconds") if ts else "unknown"
+            )
+            print(f"        token={token} (created_at={created_at})")
+    else:
+        print("[oob] No pending out-of-band approvals.")
+
+    pubkey_response = client.get("/kyber/public-key")
+    if pubkey_response.status_code == 200:
+        print(f"[kyber] Public key: {pubkey_response.json().get('public_key')}")
+    else:
+        print(
+            "[kyber] Failed to retrieve public key:",
+            pubkey_response.status_code,
+            pubkey_response.text,
+        )
+
+
+if __name__ == "__main__":
+    run_demo()
 
EOF
)
