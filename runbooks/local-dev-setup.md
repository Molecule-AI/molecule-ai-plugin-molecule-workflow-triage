# Runbook: Local Development Setup — github-app-auth Plugin

This runbook covers setting up a local development environment for the
`github-app-auth` plugin (GitHub App installation-token injection). It is a Go
plugin, not a standard molecule plugin — there is no Python validate-plugin.py
step.

---

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Go | 1.25+ | Must match `go.mod` |
| Git | 2.40+ | |
| GitHub App | Installed on org | Requires App ID, installation ID, private key PEM |
| `gh` CLI | 2.40+ | Optional — for manual verification |
| molecule-monorepo | Local checkout | Required for `cmd/` and `pluginloader/` packages to compile |

---

## Step 1 — Clone

```bash
git clone https://github.com/Molecule-AI/molecule-ai-plugin-github-app-auth.git
cd molecule-ai-plugin-github-app-auth
```

---

## Step 2 — Private Key

Generate or retrieve the GitHub App private key PEM file:

```bash
# Downloaded from: GitHub App Settings → Keys → Generate a private key
# Save as:
cp ~/Downloads/molecule-ai.private-key.pem /secrets/github-app.pem
chmod 600 /secrets/github-app.pem
```

Required env vars for local development:

```bash
export GITHUB_APP_ID=3398844          # Your App's numeric ID
export GITHUB_APP_INSTALLATION_ID=...  # Shown on the installation page
export GITHUB_APP_PRIVATE_KEY_FILE=/secrets/github-app.pem
```

> **Security:** Never commit the PEM file. It is gitignored. Keep it on a
> tmpfs or an encrypted volume.

---

## Step 3 — Local Platform Replace Directive

The `go.mod` includes a `replace` directive pointing at a local platform checkout
(`../molecule-monorepo/platform`). For local development:

```bash
# If you have molecule-monorepo checked out adjacent to this repo:
ls ../molecule-monorepo/platform  # verify it exists

# If not, remove the replace directive (needed for CI):
go mod edit -dropreplace github.com/Molecule-AI/molecule-monorepo/platform
go mod tidy
```

---

## Step 4 — Build and Test

```bash
# Test the self-contained internal package (no platform dependency):
go test ./internal/... -race -count=1

# Vet:
go vet ./internal/...

# Build the server example (requires the platform replace directive):
go build ./cmd/server-with-github-app/ -o /tmp/test-server
```

The `cmd/` and `pluginloader/` packages require the `molecule-monorepo/platform`
module — they are integration territory, validated by the platform's own CI
when the plugin is pulled in as a dependency.

---

## Step 5 — Integration Test

If running in a local platform instance:

```bash
# Start the platform with the plugin loaded
docker compose up -d --build platform

# Verify the token is injected into a workspace container
docker exec ws-test printenv GITHUB_TOKEN
# Expected: ghs_...

# Verify gh auth works inside the workspace
docker exec ws-test gh auth status
# Expected: Logged in to github.com as app/molecule-ai[bot]
```

---

## Common Issues

| Symptom | Likely Cause | Fix |
|---|---|---|
| `go: module not found: github.com/Molecule-AI/molecule-monorepo/platform` | Local platform not checked out | `go mod edit -dropreplace ...` then `go mod tidy` |
| `githubapp: AppID is required` at boot | `GITHUB_APP_ID` not set | Set the env var; confirm the App ID from the GitHub App settings page |
| `crypto/rsa: key too small` error | Private key < 2048-bit | Re-generate the key (GitHub requires ≥ 2048-bit RSA keys) |
| `401 Unauthorized` in workspace | Installation token expired or App not installed | Check `ghs_` prefix in `GITHUB_TOKEN`; verify App is installed with correct permissions |
| `GraphQL` errors even though `gh auth status` OK | App lacks required OAuth scopes | Verify App has Contents: Write, Issues: Write, PRs: Write, Metadata: Read |
| `jwt: signature is invalid` | Clock skew > 60s | Sync system clock: `timedatectl set-ntp true` |
| Platform crashes on first workspace boot | PEM file missing or unreadable at startup | Verify: `test -r $GITHUB_APP_PRIVATE_KEY_FILE && echo OK` |
