 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/quantum_auth_secure/out_of_band.py b/quantum_auth_secure/out_of_band.py
new file mode 100644
index 0000000000000000000000000000000000000000..b208745dfb0704114a7d6fb1919a5747dcbd1bea
--- /dev/null
+++ b/quantum_auth_secure/out_of_band.py
@@ -0,0 +1,22 @@
+import secrets, time
+
+PENDING = {}
+
+def create_oob_request(username):
+    token = secrets.token_urlsafe(8)
+    PENDING[token] = {"user": username, "ts": time.time()}
+    print(f"[OOB] Approval link for {username}: http://127.0.0.1:8000/approve/{token}")
+    return token
+
+def approve_oob(token):
+    req = PENDING.pop(token, None)
+    if not req:
+        return False
+    if time.time() - req["ts"] > 120:
+        return False
+    return True
+
+
+def get_pending_requests():
+    """Return a shallow copy of the currently pending OOB approvals."""
+    return {token: data.copy() for token, data in PENDING.items()}
 
EOF
)
