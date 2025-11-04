 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/quantum_auth_secure/webauthn_routes.py b/quantum_auth_secure/webauthn_routes.py
new file mode 100644
index 0000000000000000000000000000000000000000..539777090041e0fcbf2691b87d16f273038f274e
--- /dev/null
+++ b/quantum_auth_secure/webauthn_routes.py
@@ -0,0 +1,14 @@
+from fastapi import APIRouter
+from webauthn import generate_registration_options, options_to_json, verify_registration_response
+
+router = APIRouter(prefix="/webauthn")
+
+@router.get("/register/options")
+def get_options(username: str):
+    opts = generate_registration_options(user_id=username.encode(), user_name=username)
+    return options_to_json(opts)
+
+@router.post("/register/verify")
+def verify(response: dict):
+    verified = verify_registration_response(response)
+    return {"verified": verified}
 
EOF
)
