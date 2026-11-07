# Copilot Agents

This repository defines custom Copilot agents in `.github/agents`.

## Available Agents
- `python-developer`: Python and FastAPI developer for endpoints, Pydantic models, software architecture, and test-driven development with pytest.
- `sre-engineer`: SRE and Azure specialist for Docker, Kubernetes, GitHub Actions, Makefile, and deployment automation.
- `ai-engineer`: AI engineer for Azure AI Services (Computer Vision, OCR, Language, Speech, Azure OpenAI) and machine learning tooling (Azure Machine Learning, ML.NET, ONNX Runtime, MLflow).

## Usage
- In Copilot custom agents, select `python-developer`, `sre-engineer`, or `ai-engineer`.
- For reusable prompts, use `.github/prompts/python-developer.prompt.md`, `.github/prompts/sre-engineer.prompt.md`, or `.github/prompts/ai-engineer.prompt.md`.

## Notes
- Custom agents must be Markdown files ending in `.agent.md`.
- Agent files need YAML frontmatter with at least a `description`.
- `AGENTS.md` files are instructions, not selectable custom agent profiles.
