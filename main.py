(cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/quantum_auth_secure/main.py b/quantum_auth_secure/main.py
new file mode 100644
index 0000000000000000000000000000000000000000..9bac308a1f09d1ea1dacc6e9846187859314fb53
--- /dev/null
+++ b/quantum_auth_secure/main.py
@@ -0,0 +1,86 @@
+from fastapi import FastAPI, Request, Form, HTTPException
+from fastapi.responses import HTMLResponse, RedirectResponse
+from fastapi.staticfiles import StaticFiles
+from fastapi.templating import Jinja2Templates
+from argon2 import PasswordHasher
+from pqcrypto.kem.kyber512 import generate_keypair, encapsulate, decapsulate
+from srptools import SRPContext, SRPServerSession
+from device_fingerprint import get_device_fingerprint
+from behavior_monitor import record_failed, reset_failures
+from out_of_band import create_oob_request, approve_oob
+from security_headers import add_security_headers
+from webauthn_routes import router as webauthn_router
+import secrets, base64, os
+
+app = FastAPI(title="Quantum-Safe Secure Auth")
+app.include_router(webauthn_router)
+
+# Static + templates
+app.mount("/static", StaticFiles(directory="static"), name="static")
+templates = Jinja2Templates(directory="templates")
+
+# Apply security headers middleware
+app.middleware("http")(add_security_headers)
+
+ph = PasswordHasher()
+USERS = {}
+kyber_public_key, kyber_secret_key = generate_keypair()
+
+@app.get("/", response_class=HTMLResponse)
+def home(request: Request):
+    return templates.TemplateResponse("index.html", {"request": request})
+
+@app.post("/register")
+async def register(request: Request, username: str = Form(...), password: str = Form(...)):
+    if username in USERS:
+        raise HTTPException(400, "User already exists")
+    ctx = SRPContext(username, password)
+    salt = secrets.token_hex(16)
+    verifier = ctx.get_verifier()
+    USERS[username] = {
+        "salt": salt,
+        "verifier": verifier,
+        "password_hash": ph.hash(password),
+        "known_devices": [],
+    }
+    return RedirectResponse("/", 302)
+
+@app.post("/login")
+async def login(request: Request, username: str = Form(...), password: str = Form(...)):
+    user = USERS.get(username)
+    if not user:
+        record_failed(username)
+        raise HTTPException(404, "User not found")
+
+    try:
+        ph.verify(user["password_hash"], password)
+    except Exception:
+        record_failed(username)
+        raise HTTPException(401, "Invalid password")
+
+    reset_failures(username)
+
+    # Device fingerprint check
+    fp = get_device_fingerprint(request)
+    if fp not in user["known_devices"]:
+        user["known_devices"].append(fp)
+        create_oob_request(username)
+
+    # Quantum-safe session
+    ciphertext, shared_secret = encapsulate(kyber_public_key)
+    user["session_key"] = base64.b64encode(shared_secret).decode()
+
+    return templates.TemplateResponse(
+        "index.html",
+        {"request": request, "message": f"Welcome {username}!", "session": user["session_key"]}
+    )
+
+@app.get("/approve/{token}")
+def approve(token: str):
+    if approve_oob(token):
+        return {"status": "Approved"}
+    return {"status": "Invalid or expired token"}
+
+@app.get("/kyber/public-key")
+def get_pubkey():
+    return {"public_key": base64.b64encode(kyber_public_key).decode()}
 
EOF
)
