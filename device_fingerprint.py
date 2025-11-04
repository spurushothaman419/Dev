 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/quantum_auth_secure/device_fingerprint.py b/quantum_auth_secure/device_fingerprint.py
new file mode 100644
index 0000000000000000000000000000000000000000..5f196177694a3d759137d901d4bd45a1acd54bbb
--- /dev/null
+++ b/quantum_auth_secure/device_fingerprint.py
@@ -0,0 +1,10 @@
+import hashlib, json
+from fastapi import Request
+
+def get_device_fingerprint(request: Request):
+    info = {
+        "ua": request.headers.get("user-agent"),
+        "ip": request.client.host,
+    }
+    raw = json.dumps(info, sort_keys=True).encode()
+    return hashlib.sha256(raw).hexdigest()
 
EOF
)
