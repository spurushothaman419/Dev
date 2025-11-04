 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/quantum_auth_secure/security_headers.py b/quantum_auth_secure/security_headers.py
new file mode 100644
index 0000000000000000000000000000000000000000..208f173f1ecb954fa7bebbb56e92c731630f5be9
--- /dev/null
+++ b/quantum_auth_secure/security_headers.py
@@ -0,0 +1,13 @@
+from fastapi import Request
+from fastapi.responses import Response, JSONResponse
+
+ALLOWED_ORIGINS = {"https://auth.yourdomain.com", "http://127.0.0.1:8000"}
+
+async def add_security_headers(request: Request, call_next):
+    origin = request.headers.get("origin")
+    if origin and origin not in ALLOWED_ORIGINS:
+        return JSONResponse(status_code=400, content={"error": "Invalid origin"})
+    response: Response = await call_next(request)
+    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
+    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self';"
+    return response
 
EOF
)
