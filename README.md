
# Educational Research

## Overview

AI-driven agent designed to explore the academic landscape surrounding seminal research works. The agent accepts a seminal paper (as a PDF/file, DOI, or URL), analyzes its core contributions, discovers recent works that cite it, and synthesizes findings to propose potential future research directions.

1. Identify and retrieve recent academic publications that cite the supplied seminal paper (via web search tools).
2. Synthesize analysis of the original paper with the recent citing literature and propose next-step research avenues.

## Agent Details

| Feature              | Description                       |
| -------------------- | --------------------------------- |
| **Interaction Type** | Conversational                    |
| **Complexity**       | Easy                              |
| **Agent Type**       | Multi-Agent                       |
| **Components**       | Tools: built-in web/Google Search |
| **Vertical**         | Education                         |

### Agent architecture

This diagram shows the agent tools and flow (add/replace the image as needed):

<img src="docs/academic-research.svg" alt="academic researcher" width="800"/>

---

## Setup and Installation

1. **Prerequisites**

* Python 3.10+ (recommend 3.11/3.12)
* **uv** for dependency management (or use `pip`)

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
* (Optional) Google Cloud account + CLI if you plan to deploy to Vertex AI Agent Engine

2. **Installation**

```bash
# Clone this repository
git clone https://github.com/vijayarulmuthu/educational-research.git
cd educational-research

# Create virtual env and install project deps
uv venv
source .venv/bin/activate   # macOS/Linux
# Windows PowerShell: .\.venv\Scripts\Activate.ps1

# Install deps (editable mode)
uv pip install -e .
# or: uv sync        # uses pyproject + uv.lock
```

3. **Configuration**

Create and populate your environment file:

```bash
cp .env.example .env   # if .env.example is present; otherwise create .env
```

> If you intend to deploy on Vertex AI Agent Engine, set the following as well:

```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT=<your-project-id>
export GOOGLE_CLOUD_LOCATION=<your-project-location>
export GOOGLE_CLOUD_STORAGE_BUCKET=<your-storage-bucket>  # only for Agent Engine deployment
```

Authenticate with Google Cloud (for deployment paths):

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project $GOOGLE_CLOUD_PROJECT
```

---

## Local Web Testing with ADK (`adk web`)

The quickest way to try the agent end-to-end is with the ADK web playground.

### 1) Install the CLI

```bash
# Prefer pipx (isolated)
pipx install adk

# or with pip (inside your virtualenv)
pip install adk
```

> Check it’s installed:

```bash
adk --version
```

### 2) Environment & auth (local)

Create/populate `.env` as usual (see Setup). For **local** testing, you typically don’t need Vertex; if you do, keep the same Google auth steps from the deployment section.

* Local only (no Vertex): set `GOOGLE_GENAI_USE_VERTEXAI=false` (or leave unset).
* If using Vertex-backed tools locally, make sure you’ve run:

  ```bash
  gcloud auth application-default login
  gcloud auth application-default set-quota-project $GOOGLE_CLOUD_PROJECT
  ```

### 3) Start the playground

From the project root:

```bash
# If your project has an ADK manifest (e.g., adk.yaml) in the root:
adk web

# If your manifest or entry is elsewhere, point to it explicitly, for example:
adk web --entry deployment/adk_app.py

# Optional flags
adk web --port 5173              # default is usually fine
adk web --host 0.0.0.0           # bind for LAN access
adk web --log-level INFO         # DEBUG for deeper troubleshooting
```

This will launch a local UI at something like:

```
http://localhost:5173
```

Use the UI to:

* Provide a PDF/DOI/URL of a seminal paper,
* Ask the agent to summarize, find recent citing works, and propose research directions.

### 4) Troubleshooting

* **“No manifest/entry found”**: pass `--entry` to the agent’s Python entry (e.g., an `app.py` that builds/starts the agent) or place an `adk.yaml` in the repo root.
* **Import errors**: ensure the virtualenv is active and the package is installed in editable mode:

  ```bash
  source .venv/bin/activate
  uv pip install -e .
  ```
* **Credential/permission errors (Vertex)**: verify `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, and that `gcloud auth application-default login` succeeded.
* **Port in use**: pick another port, e.g., `adk web --port 5174`.

---

## Running Tests & Evaluation

Install dev dependencies:

```bash
uv sync --dev
```

Run tests and evaluation:

```bash
uv run pytest tests
uv run pytest eval
```

* `tests/` ensures components are functional.
* `eval/` can hold evaluation flows (e.g., verifying agent responses against expected outputs).

---

## Packaging

```bash
uv build
# or:
pip install build
python -m build
```

Artifacts appear in `dist/`.

---

## Deployment

### Vertex AI Agent Engine (optional)

If your repo’s `deployment/` folder includes Agent Engine scripts:

```bash
uv sync --group deployment
uv run deployment/deploy.py --create
```

When deployment finishes, you’ll see something like:

```
Created remote agent: projects/<PROJECT_NUMBER>/locations/<PROJECT_LOCATION>/reasoningEngines/<AGENT_ENGINE_ID>
```

List agents:

```bash
uv run deployment/deploy.py --list
```

Interact with a remote agent (example):

```bash
export USER_ID=<any string>
uv run deployment/test_deployment.py --resource_id=${AGENT_ENGINE_ID} --user_id=${USER_ID}
```

Delete the remote agent:

```bash
uv run deployment/deploy.py --delete --resource_id=${AGENT_ENGINE_ID}
```

### Container image (alternative)

If you prefer Docker and a `deployment/Dockerfile` exists:

```bash
docker build -t educational-research:latest -f deployment/Dockerfile .
docker run --rm --env-file .env educational-research:latest
```

Push to GHCR (optional):

```bash
echo $GH_TOKEN | docker login ghcr.io -u <YOUR_GH_USERNAME> --password-stdin
docker tag educational-research:latest ghcr.io/vijayarulmuthu/educational-research:latest
docker push ghcr.io/vijayarulmuthu/educational-research:latest
```

---

## Customization

* **Specialized academic search**: Add tools for arXiv, Crossref, or Semantic Scholar.
* **Visualization**: Graph the citation network or future-work map.
* **Prompting/agent roles**: Tune sub-agent prompts for deeper citation analysis or interdisciplinary emphasis.
* **Paper retrieval**: Add DOI/URL PDF retrieval + reference manager integration.

---

## Security Notes

* Never commit secrets. Keep `.env` local and add `.env.example` for placeholders.
* If a secret was ever committed, rotate it immediately and purge from git history:

  ```bash
  brew install git-filter-repo  # or: pipx install git-filter-repo
  git filter-repo --path .env --invert-paths --force
  git push --force origin main
  ```

---

## License

Choose a license (e.g., MIT) and add `LICENSE` to the repo.

---

If you want, I can also open a PR that adds this `README.md`, a `.env.example`, and optional CI (tests/build).
