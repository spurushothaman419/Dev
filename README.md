# Quantum Auth Secure Demo

This repository hosts a FastAPI demo that layers multiple security mechanisms—SRP, Argon2id, Kyber512 key exchange, device fingerprinting, behavioral lockouts, WebAuthn enrollment, and out-of-band approvals—into a single sample application.

## Local development
1. Create and activate a Python 3.11 virtual environment.
2. Install dependencies:
   ```bash
   pip install -r quantum_auth_secure/requirements.txt
   ```
3. Run the FastAPI server:
   ```bash
   uvicorn quantum_auth_secure.main:app --reload
   ```
4. Open http://127.0.0.1:8000 to interact with the UI.

To see the scripted end-to-end flow locally, run:
```bash
python quantum_auth_secure/automated_demo.py
```

## Running inside GitHub
A GitHub Actions workflow (`Automated Demo Output`) is provided to execute the automated demo and capture its output whenever you push, open a pull request, or trigger it manually.

### Manual trigger via the GitHub UI
1. Navigate to **Actions ▸ Automated Demo Output** within your repository.
2. Click **Run workflow** and choose the branch to run.
3. After the run finishes, review the "Quantum Auth Automated Demo Output" section in the job summary or download the `automated-demo-output` artifact.

### Automatic execution on pushes / pull requests
- Pushes to `main` or `master` and all pull requests automatically run the demo.
- The workflow installs the Python requirements and executes `python quantum_auth_secure/automated_demo.py` to generate the same output as a local run.

This makes it easy to verify the recorded behavior directly from GitHub without setting up a local environment.
