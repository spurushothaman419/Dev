 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/quantum_auth_secure/static/app.js b/quantum_auth_secure/static/app.js
new file mode 100644
index 0000000000000000000000000000000000000000..139710b1fbd8a3a1d6ebef0d144656e73f4d5694
--- /dev/null
+++ b/quantum_auth_secure/static/app.js
@@ -0,0 +1,13 @@
+async function registerWebAuthn() {
+    const username = prompt("Enter username for WebAuthn registration:");
+    const res = await fetch(`/webauthn/register/options?username=${username}`);
+    const opts = await res.json();
+    const credential = await navigator.credentials.create({ publicKey: opts });
+    const response = { id: credential.id, rawId: btoa(String.fromCharCode(...new Uint8Array(credential.rawId))) };
+    await fetch("/webauthn/register/verify", {
+        method: "POST",
+        headers: { "Content-Type": "application/json" },
+        body: JSON.stringify(response)
+    });
+    alert("WebAuthn registration complete!");
+}
 
EOF
)
