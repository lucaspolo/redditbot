# AGENTS.md - AI Agent Instructions

This document provides comprehensive instructions for AI agents working on the RedditBot codebase.

## Project Overview

RedditBot is a Telegram bot that fetches and shares trending posts from Reddit. Built with:

- **Python 3.12+**
- **uv** as the package manager
- **python-telegram-bot** for Telegram integration
- **httpx** for async HTTP requests
- **Click** for CLI interface
- **Dynaconf** for configuration management

## Setup & Dependencies

Install all project dependencies:

```bash
make dependencies
```

This runs `uv sync` to install dependencies from `pyproject.toml`.

---

## Linting

**Command:**

```bash
make lint
```

This runs `uv run flake8 redditbot` to check code style.

### Linting Tools

- **flake8** - PEP 8 style checker
- **flake8-quotes** - Enforces consistent quote style

### Common Lint Issues and How to Fix Them

| Error Code | Issue | Fix |
|------------|-------|-----|
| `Q000` | Wrong quote style | Use **single quotes** `'string'` instead of double quotes |
| `E501` | Line too long | Keep lines **under 79 characters**; break long lines |
| `E302` | Expected 2 blank lines | Add **2 blank lines** before top-level function/class definitions |
| `E303` | Too many blank lines | Remove extra blank lines |
| `E401` | Multiple imports on one line | Use **separate import statements** for each module |
| `E711` | Comparison to None | Use `is None` or `is not None` instead of `== None` |
| `W291` | Trailing whitespace | Remove **trailing whitespace** at end of lines |
| `W292` | No newline at end of file | Add a **newline** at the end of the file |
| `F401` | Imported but unused | Remove **unused imports** |
| `F841` | Variable assigned but never used | Remove or use the **unused variable** |

### Quote Style Convention

This project uses **single quotes** for all strings:

```python
# Correct
message = 'Hello, world!'
name = 'RedditBot'

# Incorrect - will fail lint
message = "Hello, world!"
name = "RedditBot"
```

### Import Order

Follow this import order (PEP 8):

```python
# 1. Standard library imports
import asyncio
from http import HTTPStatus

# 2. Third-party imports
import httpx
from telegram import Update

# 3. Local application imports
from redditbot.crawlers.reddit_crawler import get_subreddits
```

---

## Testing

### Test Commands

**Run tests (stop on first failure):**

```bash
make test
```

This runs `uv run pytest -x`.

**Run tests with coverage:**

```bash
make test-cov
```

This runs `uv run pytest --cov redditbot` and generates coverage reports.

### Test Structure

The test directory mirrors the source code structure:

```
tests/
├── __init__.py
├── conftest.py              # Global fixtures (HTTP mocks)
├── crawlers/
│   ├── __init__.py
│   ├── conftest.py          # Crawler-specific fixtures
│   └── test_crawler.py      # Crawler unit tests
└── ui/
    ├── __init__.py
    ├── test_bot.py          # Telegram bot handler tests (async)
    └── test_nadaparafazer.py # CLI tests (Click CliRunner)
```

### Key Testing Patterns

#### 1. Async Tests

Async tests run automatically without decorators (configured via `asyncio_mode = 'auto'`):

```python
async def test_get_subreddits_should_return_threads(mock_request_dog):
    threads = await get_subreddits(['dogs'])
    assert len(threads) == 1
```

#### 2. HTTP Mocking with pytest-httpx

Use `httpx_mock` fixture to mock HTTP requests:

```python
@pytest.fixture
def mock_request_dog(httpx_mock):
    httpx_mock.add_response(
        method='GET',
        url='https://www.reddit.com/r/dogs/top.json?sort=new',
        json={
            'data': {
                'children': [
                    {'data': {'subreddit': 'dogs', 'title': 'Cute Dogs', 'ups': 9999}}
                ]
            }
        },
    )
```

#### 3. Mocking with unittest.mock

Use `mock.patch` for patching dependencies:

```python
from unittest import mock

@mock.patch('redditbot.ui.bot.ApplicationBuilder')
def test_main_should_register_handlers(self, application_builder_mock):
    # Test implementation
```

#### 4. Async Mock Objects

For async methods, use `mock.AsyncMock()`:

```python
update = mock.MagicMock()
update.message.reply_text = mock.AsyncMock()
```

#### 5. CLI Testing with Click

Use `CliRunner` for testing Click commands:

```python
from click.testing import CliRunner

def test_cli_command():
    runner = CliRunner()
    result = runner.invoke(main, ['-s', 'fake'])
    assert result.exit_code == 0
```

### Fixtures Location

- **Global fixtures** → `tests/conftest.py` (available to all tests)
- **Module-specific fixtures** → `tests/<module>/conftest.py` (e.g., `tests/crawlers/conftest.py`)

### Coverage Configuration

Coverage is configured in `pyproject.toml`:

- Branch coverage enabled
- Excludes `if __name__ == "__main__":` blocks
- Reports: terminal with missing lines + XML

---

## ⚠️ MANDATORY: Verification After Changes

**IMPORTANT: After ANY code change, you MUST run both linter and tests before considering the work complete.**

### Verification Workflow

After making changes, execute these steps in order:

```bash
# Step 1: Run linter - fix ALL errors before proceeding
make lint

# Step 2: Run tests - ensure ALL tests pass
make test
```

### Rules

1. **No code is complete until both `make lint` and `make test` pass**
2. **If lint fails**: Fix all style issues before running tests
3. **If tests fail**: Fix failing tests before making additional changes
4. **Do not skip this step** - always verify before committing or reporting completion

### Quick Verification Command

Run both in sequence:

```bash
make lint && make test
```

If this command completes without errors, the changes are ready.

---

## Running the Bot

**Command:**

```bash
make run-bot
```

**Prerequisite:** Set the Telegram token environment variable:

```bash
export TELEGRAM_TOKEN='your-telegram-bot-token'
```

---

## Project Structure

```
redditbot/
├── __init__.py
├── config/              # Configuration (Dynaconf)
│   └── __init__.py
├── crawlers/            # Reddit API interaction
│   ├── __init__.py
│   └── reddit_crawler.py
└── ui/                  # User interfaces
    ├── __init__.py
    ├── bot.py           # Telegram bot interface
    └── nadaparafazer.py # CLI interface
```

### Module Responsibilities

| Module | Purpose |
|--------|---------|
| `redditbot/crawlers/reddit_crawler.py` | Fetches and processes Reddit posts via API |
| `redditbot/ui/bot.py` | Telegram bot handlers (`/start`, `/nadaparafazer`) |
| `redditbot/ui/nadaparafazer.py` | CLI tool for fetching Reddit posts |
| `redditbot/config/` | Configuration management with Dynaconf |

---

## Summary of Make Commands

| Command | Description |
|---------|-------------|
| `make dependencies` | Install project dependencies with uv |
| `make lint` | Run flake8 linter |
| `make test` | Run tests (stop on first failure) |
| `make test-cov` | Run tests with coverage report |
| `make run-bot` | Start the Telegram bot |
