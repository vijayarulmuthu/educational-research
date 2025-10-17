Here’s a drop-in `README.md` for your repo, structured to match your attached template and tailored to your repository layout (`deployment/`, `educational_research/`, `eval/`, `tests/`, `pyproject.toml`, `uv.lock`). This README follows your template. 

---

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

## Running the Agent (Local)

**CLI / module entry**

If your package exposes a module entrypoint:

```bash
python -m educational_research --help
```

Common patterns:

```bash
# Example: run the agent with a local PDF
python -m educational_research --paper path/to/seminal.pdf

# Example: run with a DOI/URL
python -m educational_research --doi 10.48550/arXiv.1706.03762
# or
python -m educational_research --url https://arxiv.org/abs/1706.03762
```

**Web interface (if included in the project):**

If your project provides a simple web UI script (e.g., `eval/web.py`), run:

```bash
uv run python eval/web.py
```

> Adjust the command to whatever UI runner your repo includes. If not available, you can skip this section.

### Example prompts to try

```
Who are you?
Analyze this paper (attached PDF) and summarize the core contributions.
Find recent papers citing it and propose 3 future research directions.
```

---

## Debugging Locally (macOS-focused)

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Module: educational_research",
      "type": "python",
      "request": "launch",
      "module": "educational_research",
      "justMyCode": true,
      "envFile": "${workspaceFolder}/.env",
      "console": "integratedTerminal"
    },
    {
      "name": "Script: eval/run_experiment.py",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/eval/run_experiment.py",
      "args": [],
      "justMyCode": true,
      "envFile": "${workspaceFolder}/.env",
      "console": "integratedTerminal"
    },
    {
      "name": "Pytest current file",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-q", "${file}"],
      "envFile": "${workspaceFolder}/.env",
      "console": "integratedTerminal"
    }
  ]
}
```

Tips:

* Set breakpoints in `educational_research/` files.
* Use the “Pytest current file” configuration to debug tests.

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
