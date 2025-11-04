 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/quantum_auth_secure/behavior_monitor.py b/quantum_auth_secure/behavior_monitor.py
new file mode 100644
index 0000000000000000000000000000000000000000..8a16a8d01788a571bfa0408d0020afdc49ef24ae
--- /dev/null
+++ b/quantum_auth_secure/behavior_monitor.py
@@ -0,0 +1,14 @@
+from collections import defaultdict
+import time
+
+FAILED_LOGINS = defaultdict(list)
+
+def record_failed(username):
+    now = time.time()
+    FAILED_LOGINS[username].append(now)
+    recent = [t for t in FAILED_LOGINS[username] if now - t < 300]
+    if len(recent) > 5:
+        raise Exception("Too many failed attempts, account locked")
+
+def reset_failures(username):
+    FAILED_LOGINS[username] = []
 
EOF
)
