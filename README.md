# PHX Common Modules

A shared Python library containing common utilities, data models, and response structures for Phoenix projects.

## Features

- **API Response DTO**: Standardized API response structure with pagination support
- **Pagination**: Pagination data model for paginated responses
- **Date Utils**: Date and datetime utilities with Mexico timezone support
- **Logging**: Integrated with Loguru for structured logging

## Requirements

- Python >= 3.11
- [uv](https://github.com/astral-sh/uv) package manager

## Setup

### 1. Install Python 3.11 using uv

```bash
uv python install 3.11
uv python pin 3.11
```

### 2. Initialize and Create Virtual Environment

```bash
uv venv --python 3.11
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install main dependencies
uv pip install .

# Install development dependencies (includes pytest)
uv pip install -e ".[dev]"
```

## Project Structure

```
phx-common-modules/
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   └── pagination.py          # Pagination data model
│   ├── response/
│   │   ├── __init__.py
│   │   └── api_response_dto.py    # API response DTO
│   └── utils/
│       ├── __init__.py
│       └── date_utils.py          # Date utilities with Mexico timezone
├── tests/
│   ├── __init__.py
│   └── test_date_utils.py         # Test suite
├── pyproject.toml                 # Project configuration
└── README.md
```

## Usage

### API Response DTO

```python
from src.response import ApiResponseDto
from src.data import Pagination

# Simple response
response = ApiResponseDto.ok({"message": "Success"})

# Paginated response
pagination = Pagination(page=0, size=10)
response = ApiResponseDto.ok_with_pagination([1, 2, 3], pagination)

# Paginated response with total elements
response = ApiResponseDto.ok_from_page(
    [1, 2, 3], 
    pagination, 
    total_elements=100
)
```

### Date Utils

```python
from src.utils import DateUtils

# Get current Mexico time
now = DateUtils.now()  # datetime with Mexico timezone

# Get current Mexico date
today = DateUtils.today()  # date object

# Convert to Mexico timezone
from datetime import datetime
from zoneinfo import ZoneInfo

utc_dt = datetime(2024, 1, 15, 18, 0, 0, tzinfo=ZoneInfo("UTC"))
mexico_dt = DateUtils.to_mexico_timezone(utc_dt)

# Convert from Mexico timezone to UTC
utc_dt = DateUtils.from_mexico_timezone(mexico_dt, ZoneInfo("UTC"))
```

## Testing

### Run All Tests

```bash
pytest
```

### Run Tests with Verbose Output

```bash
pytest -vv
```

### Run Tests with Coverage Report

```bash
pytest --cov=src --cov-report=term-missing
```

### Run Tests with HTML Coverage Report

```bash
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in your browser
```

### Run Specific Test File

```bash
pytest tests/test_date_utils.py
```

### Run Specific Test Class or Method

```bash
pytest tests/test_date_utils.py::TestDateUtils
pytest tests/test_date_utils.py::TestDateUtils::test_now_returns_datetime_with_mexico_timezone
```

## Adding New Implementations

When adding new features to this shared library, follow these best practices:

### 1. Code Organization

- Place new modules in the appropriate directory under `src/`:
  - `src/data/` - Data models and DTOs
  - `src/response/` - Response structures
  - `src/utils/` - Utility functions and helper classes
  - Create new directories as needed (e.g., `src/exceptions/`, `src/validators/`)

### 2. Package Structure

- Always create `__init__.py` files in each package directory
- Export public classes/functions in `__init__.py` using `__all__`
- Use absolute imports: `from src.module import Class` (not relative imports)

### 3. Type Hints

- Use type hints for all function parameters and return types
- Use `Generic[T]` for generic classes
- Import types from `typing` module when needed

### 4. Documentation

- Add docstrings to all public classes and methods
- Use Google-style or NumPy-style docstrings
- Include examples in docstrings for complex functions

### 5. Testing

- Write tests for all new functionality
- Place tests in `tests/` directory
- Follow naming convention: `test_<module_name>.py`
- Use descriptive test method names: `test_<functionality>_<expected_behavior>`
- Aim for high test coverage (ideally >80%)

### 6. Dependencies

- Add new dependencies to `pyproject.toml` in the `dependencies` section
- Add test-only dependencies to `[project.optional-dependencies].dev`
- Specify minimum versions (e.g., `"package>=1.0.0"`)

### 7. Example: Adding a New Utility

```python
# src/utils/new_util.py
"""New utility module."""

from loguru import logger


class NewUtil:
    """Utility class for new functionality."""

    @staticmethod
    def do_something(param: str) -> str:
        """
        Do something useful.

        Args:
            param: Input parameter

        Returns:
            Result string
        """
        logger.debug(f"Processing: {param}")
        return f"Processed: {param}"
```

```python
# src/utils/__init__.py
"""Utility modules for common operations."""

from .date_utils import DateUtils
from .new_util import NewUtil

__all__ = ["DateUtils", "NewUtil"]
```

```python
# tests/test_new_util.py
"""Tests for NewUtil class."""

import pytest
from src.utils import NewUtil


class TestNewUtil:
    """Test cases for NewUtil."""

    def test_do_something_returns_processed_string(self):
        """Test that do_something processes the input correctly."""
        result = NewUtil.do_something("test")
        assert result == "Processed: test"
```

## Using in Other Python Projects

This shared library can be installed in other Python projects directly from GitHub.

### For Public Repositories

If the repository is public, you can install it directly:

```bash
# Using uv
uv pip install git+https://github.com/your-org/phx-common-modules.git

# Using pip
pip install git+https://github.com/your-org/phx-common-modules.git

# Install specific branch or tag
uv pip install git+https://github.com/your-org/phx-common-modules.git@main
uv pip install git+https://github.com/your-org/phx-common-modules.git@v0.1.0
```

### For Private Repositories

For private repositories, you have several options:

#### Option 1: Using SSH (Recommended)

```bash
# Using uv - install latest from main branch
uv pip install git+ssh://git@github.com/your-org/phx-common-modules.git

# Install from specific tag
uv pip install git+ssh://git@github.com/your-org/phx-common-modules.git@v0.1.0

# Install from specific branch
uv pip install git+ssh://git@github.com/your-org/phx-common-modules.git@main

# Using pip
pip install git+ssh://git@github.com/your-org/phx-common-modules.git
pip install git+ssh://git@github.com/your-org/phx-common-modules.git@v0.1.0
```

**Setup SSH key:**
1. Generate SSH key if you don't have one: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Add SSH key to your GitHub account: Settings → SSH and GPG keys → New SSH key
3. Test connection: `ssh -T git@github.com`

#### Option 2: Using HTTPS with Personal Access Token

```bash
# Using uv - install latest from main branch
uv pip install git+https://<TOKEN>@github.com/your-org/phx-common-modules.git

# Install from specific tag
uv pip install git+https://<TOKEN>@github.com/your-org/phx-common-modules.git@v0.1.0

# Install from specific branch
uv pip install git+https://<TOKEN>@github.com/your-org/phx-common-modules.git@main

# Using pip
pip install git+https://<TOKEN>@github.com/your-org/phx-common-modules.git
pip install git+https://<TOKEN>@github.com/your-org/phx-common-modules.git@v0.1.0
```

**Create Personal Access Token:**
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. Use token in the URL (replace `<TOKEN>`)

#### Option 3: Using Git Credentials

Configure Git to use credentials:

```bash
# Store credentials
git config --global credential.helper store

# Then install
uv pip install git+https://github.com/your-org/phx-common-modules.git
# Enter your GitHub username and Personal Access Token when prompted
```

#### Option 4: Add to requirements.txt or pyproject.toml

**In requirements.txt:**
```
# Install from main branch (latest)
git+ssh://git@github.com/your-org/phx-common-modules.git
# or
git+https://<TOKEN>@github.com/your-org/phx-common-modules.git

# Install from specific tag (recommended for production)
git+ssh://git@github.com/your-org/phx-common-modules.git@v0.1.0
# or
git+https://<TOKEN>@github.com/your-org/phx-common-modules.git@v0.1.0

# Install from specific branch
git+ssh://git@github.com/your-org/phx-common-modules.git@develop
```

**In pyproject.toml:**
```toml
[project]
dependencies = [
    # Install from main branch (latest)
    "phx-common-modules @ git+ssh://git@github.com/your-org/phx-common-modules.git",
    # or
    "phx-common-modules @ git+https://<TOKEN>@github.com/your-org/phx-common-modules.git",
    
    # Install from specific tag (recommended for production)
    "phx-common-modules @ git+ssh://git@github.com/your-org/phx-common-modules.git@v0.1.0",
    # or
    "phx-common-modules @ git+https://<TOKEN>@github.com/your-org/phx-common-modules.git@v0.1.0",
    
    # Install from specific branch
    "phx-common-modules @ git+ssh://git@github.com/your-org/phx-common-modules.git@develop",
]
```

**Note:** When using tags, replace `v0.1.0` with your actual tag name (e.g., `v1.0.0`, `v2.3.1`, etc.). Using tags is recommended for production environments to ensure version stability.

Then install:
```bash
uv pip install -r requirements.txt
# or
uv pip install .
```

### Working with Tags

Tags are recommended for production use as they provide version stability. Here's how to work with them:

**Create a new tag:**
```bash
# Create an annotated tag (recommended)
git tag -a v0.1.0 -m "Release version 0.1.0"

# Push tag to remote
git push origin v0.1.0

# Push all tags
git push origin --tags
```

**List available tags:**
```bash
# List all tags
git tag

# List tags matching a pattern
git tag -l "v0.*"

# Show tag details
git show v0.1.0
```

**Install from a tag:**
```bash
# Using uv
uv pip install git+ssh://git@github.com/your-org/phx-common-modules.git@v0.1.0

# Using pip
pip install git+ssh://git@github.com/your-org/phx-common-modules.git@v0.1.0
```

### Installing in Editable Mode (Development)

If you're actively developing and want changes to reflect immediately:

```bash
# Clone the repository first
git clone git@github.com/your-org/phx-common-modules.git
cd phx-common-modules

# Install in editable mode
uv pip install -e .

# In your project, install from local path
uv pip install -e /path/to/phx-common-modules
```

### Using in Your Project

Once installed, import and use the modules:

```python
from src.response import ApiResponseDto
from src.data import Pagination
from src.utils import DateUtils

# Your code here
response = ApiResponseDto.ok({"data": "example"})
now = DateUtils.now()
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

### Code Quality

This project uses:
- **Pydantic** for data validation
- **Loguru** for logging
- **pytest** for testing
- **pytest-cov** for coverage reporting

## License


## Contributing

