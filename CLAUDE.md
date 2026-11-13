# Repository Instructions For Claude

## Goal
Make small, safe, reviewable changes that fit the existing project.

## General Rules
- Inspect the repository before proposing or applying changes.
- Keep diffs focused on the user's request.
- Do not refactor unrelated files.
- Preserve existing project conventions.
- Treat secrets, tokens, and credentials as sensitive. Never print them in full.
- Do not fabricate command, tool, Docker, Kubernetes, Azure, Claude, or CI output.

## Available Agent Modes
Use the matching mode when the task fits its domain:

- `python-developer`: Python and FastAPI application code, endpoints, Pydantic models, dependency injection, async code, error handling, software architecture (layered, hexagonal, clean architecture, SOLID), and test-driven development with pytest.
- `sre-engineer`: Docker, Kubernetes, Minikube, GitHub Actions, Makefiles, run scripts, Azure, deployment automation, reliability, and operational readiness.
- `ai-engineer`: Azure AI Services (formerly Cognitive Services) such as Computer Vision, OCR, Face, Custom Vision, Document Intelligence, Language, Speech, Translator, Content Safety, and Azure OpenAI, plus machine learning tooling such as Azure Machine Learning, Azure AI Foundry, ML.NET, ONNX Runtime, and MLflow.
- `data-engineer`: databases and queries, including relational and NoSQL data modeling, SQL authoring and optimization (PostgreSQL, MySQL, SQL Server / Azure SQL, SQLite), indexing, execution plans, transactions, Alembic migrations, SQLAlchemy / SQLModel persistence adapters, and ETL/ELT data pipelines.

## Claude Code Subagents
Subagents are defined in `.claude/agents`:

- `.claude/agents/python-developer.md`
- `.claude/agents/sre-engineer.md`
- `.claude/agents/ai-engineer.md`
- `.claude/agents/data-engineer.md`

Use `/agents` to confirm they are loaded, or ask Claude to delegate to one by name (for example, "use the sre-engineer agent to add a Dockerfile").

## Claude Code Skills
Matching skills are defined in `.claude/skills`:

- `.claude/skills/python-developer/SKILL.md`
- `.claude/skills/sre-engineer/SKILL.md`
- `.claude/skills/ai-engineer/SKILL.md`
- `.claude/skills/data-engineer/SKILL.md`

Invoke them with `/python-developer`, `/sre-engineer`, `/ai-engineer`, or `/data-engineer`, or let Claude load them automatically when the task matches their description.

## Validation
- Prefer repository-specific build and test commands when they exist.
- If validation cannot run because local tooling is unavailable, say exactly what was not run and why.

## Final Response
Include:
- Summary
- Files changed
- Commands run
- Verification result
