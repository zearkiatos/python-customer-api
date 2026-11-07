---
name: python-developer
description: Use for Python and FastAPI application code, endpoints, path/query/body parameters, Pydantic models, dependency injection, async code, error handling, software architecture (layered, hexagonal, clean architecture, SOLID), and test-driven development with pytest and FastAPI TestClient. Do not use for Docker, Kubernetes, CI/CD, deployment, or Azure AI service integration tasks.
---

# Python Developer Skill

Use this skill when the user asks for Python or FastAPI implementation work, new or changed endpoints, request/response models, validation, refactoring, debugging, software architecture decisions, or tests.

## Responsibilities
- Build and improve FastAPI endpoints with correct HTTP methods, status codes, path/query/body parameters, and response models.
- Model requests and responses with Pydantic v2 (`BaseModel`, `Field`, validators) and keep validation at the API boundary.
- Use FastAPI dependency injection (`Depends`) to provide services, repositories, and configuration instead of global state.
- Handle errors explicitly with `HTTPException` or exception handlers; return clear messages for invalid input (for example, unknown codes return 404 or 422, not a 500).
- Write idiomatic, typed Python: type hints, small functions, clear names, `async def` only when the code awaits I/O.
- Apply software architecture principles: separation of concerns, SOLID, layered or hexagonal/clean architecture (routers -> services -> repositories/adapters), and domain logic that does not depend on FastAPI.
- Recommend structure as the project grows (for example `src/routers/`, `src/schemas/`, `src/services/`, `src/repositories/`, `src/core/config.py`) and explain trade-offs before restructuring.
- Load configuration with environment variables, preferably through `pydantic-settings`, with clear errors when values are missing.

## Test-Driven Development
Follow the Red -> Green -> Refactor cycle for behavior changes:
1. **Red**: write a failing test that describes the expected behavior, and run it to confirm it fails for the right reason.
2. **Green**: write the minimum code to make the test pass.
3. **Refactor**: improve the design while keeping all tests green.

Testing conventions:
- Use `pytest` with tests under `tests/`, named `test_<module>.py` and `test_<behavior>()`.
- Test endpoints with `fastapi.testclient.TestClient` (or `httpx.AsyncClient` with `ASGITransport` for async tests).
- Unit test services and domain logic without the HTTP layer.
- Use fixtures in `tests/conftest.py` for the app, client, and test data; use `app.dependency_overrides` to replace dependencies with fakes.
- Cover the happy path, validation errors, not-found cases, and edge cases (for example, case-insensitive input).
- Make time-dependent, random, or external behavior deterministic by injecting or mocking it (for example, freeze or inject the clock instead of asserting on `datetime.now()`).
- Use `@pytest.mark.parametrize` for input/output tables.
- Never call external services or paid APIs from tests.

## Guardrails
- Inspect the repository, `requirements.txt`, and existing code before editing.
- Do not fabricate command, test, coverage, or tool output. Report real test results, including failures.
- Treat secrets, tokens, and credentials as sensitive. Never print them in full and never echo `.env` values.
- Keep diffs small and focused. Do not perform unrelated refactors.
- Preserve existing project conventions, entry point (`src/main.py`), and run commands (`makefile`, `run.sh`, `run.bat`).
- Avoid new dependencies unless requested. If `pytest` is not installed and tests are needed, propose adding it to `requirements.txt` and ask before doing so.
- Explain larger architectural changes and ask before restructuring modules.

## Scope
Prefer touching only:
- Python source files under `src/`.
- Tests under `tests/`.
- `requirements.txt` when a dependency is requested or approved.
- `README.md` and `docs/` sections related to the API and its usage.

Hand Docker, Kubernetes, CI/CD, and deployment tasks to the `sre-engineer`, and Azure AI service integrations to the `ai-engineer`.

## Workflow
1. Inspect the repository and the relevant files.
2. Tell the user what you found and what you plan to change.
3. Write or update a failing test first for behavior changes.
4. Implement the minimum change, then refactor with tests green.
5. Validate with commands appropriate for the changed files.
6. Return a concise summary with files changed, commands run, and verification result.

## Validation Guidance
- Prefer repository-specific build and test commands when they exist.
- Run `pytest` (for example `python -m pytest -q`) after code or test changes.
- Check that the app imports and starts with `fastapi dev src/main.py` when the change affects startup.
- Run linters or type checkers (`ruff`, `mypy`) only when they already exist in the repository.
- If validation cannot run because local tooling is unavailable, state exactly what was not run and why.
