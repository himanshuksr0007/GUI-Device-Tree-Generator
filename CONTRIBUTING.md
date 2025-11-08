# Contributing to GUI Device Tree Generator

First off, thank you for considering contributing to GUI Device Tree Generator! It's people like you that make this tool better for the entire Android ROM development community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When filing a bug report, include:**
- **Clear title and description**
- **Steps to reproduce** the problem
- **Expected behavior** vs **actual behavior**
- **Screenshots** if applicable
- **System information**:
  - OS and version
  - Python version
  - Application version
- **Log files** from the `logs/` directory
- **Boot image details** (size, source device) if relevant

**Example bug report:**

```markdown
**Title:** Application crashes when selecting .tar boot images

**Description:**
The application crashes immediately after selecting a .tar format boot image.

**Steps to Reproduce:**
1. Launch the application
2. Click "Select Image"
3. Choose a .tar file (e.g., boot.tar from Samsung device)
4. Application crashes

**Expected Behavior:**
Application should process the .tar file or show appropriate error message

**Actual Behavior:**
Application crashes with no error dialog

**Environment:**
- OS: Windows 11 22H2
- Python: 3.9.7
- App Version: 1.0.0

**Additional Info:**
- Attached crash log from logs/ directory
- The .tar file is 45MB from a Samsung Galaxy S21
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Clear description** of the enhancement
- **Use case** - why is this useful?
- **Mockups or examples** if applicable
- **Potential implementation approach** (if you have ideas)

### Code Contributions

#### Good First Issues

Look for issues labeled `good-first-issue` - these are great for newcomers!

#### Areas That Need Help

1. **LineageOS device tree support** - Major feature planned for v1.1
2. **Batch processing** - Process multiple images at once
3. **Device tree comparison** - Diff tool for device trees
4. **GUI improvements** - Better error messages, progress indicators
5. **Documentation** - More examples, translations
6. **Testing** - Unit tests, integration tests

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/GUI-Device-Tree-Generator.git
cd GUI-Device-Tree-Generator

# Add upstream remote
git remote add upstream https://github.com/himanshuksr0007/GUI-Device-Tree-Generator.git
```

### 2. Create Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

### 3. Install System Dependencies

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install cpio lz4 device-tree-compiler abootimg
```

**macOS:**
```bash
brew install cpio lz4 dtc
```

**Windows:**
- Dependencies will be bundled in the executable
- For development, use WSL or Docker

### 4. Run the Application

```bash
python src/main.py
```

### 5. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_validator.py
```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces (no tabs)
- **String quotes**: Double quotes for user-facing strings, single quotes for internal

### Code Formatting

We use `black` for automatic formatting:

```bash
# Format all Python files
black src/

# Check what would be formatted
black --check src/
```

### Linting

```bash
# Run flake8
flake8 src/

# Run mypy for type checking
mypy src/
```

### Documentation

All functions and classes should have docstrings:

```python
def process_image(self, image_path: str, output_dir: str) -> Dict[str, Any]:
    """
    Process boot image and generate device tree.
    
    Args:
        image_path: Path to boot/recovery image
        output_dir: Directory for output files
    
    Returns:
        Dict containing success status and output path
    
    Raises:
        FileNotFoundError: If image_path doesn't exist
        ValueError: If image format is unsupported
    """
    pass
```

### Type Hints

Use type hints for all function signatures:

```python
from typing import Dict, List, Optional, Any

def get_device_info(filepath: str) -> Optional[Dict[str, str]]:
    pass
```

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```
feat(gui): add drag-and-drop support for boot images

- Implement drag-and-drop event handling
- Add visual feedback when dragging over drop zone
- Validate dropped files before processing

Closes #42
```

```
fix(core): handle corrupted boot images gracefully

- Add try-catch around image extraction
- Show user-friendly error message
- Log detailed error information

Fixes #38
```

### Commit Best Practices

1. **Make atomic commits** - One logical change per commit
2. **Write meaningful messages** - Explain what and why, not how
3. **Reference issues** - Use "Fixes #123" or "Closes #456"
4. **Keep commits focused** - Don't mix unrelated changes

## Pull Request Process

### Before Submitting

- [ ] Code follows the project's style guide
- [ ] All tests pass locally
- [ ] Added tests for new functionality
- [ ] Updated documentation if needed
- [ ] Commits are clean and well-described
- [ ] No merge conflicts with main branch

### Submitting a PR

1. **Update your fork:**
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes and commit:**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

4. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request on GitHub**

### PR Template

When creating a PR, include:

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issues
Closes #issue_number

## Testing
Describe the tests you ran and how to reproduce them

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated and passing
- [ ] No new warnings introduced
```

### PR Review Process

1. **Automated checks** must pass (CI/CD pipeline)
2. **Code review** by maintainer(s)
3. **Requested changes** must be addressed
4. **Approval** from at least one maintainer
5. **Merge** by maintainer

### After Your PR is Merged

1. Delete your feature branch
2. Update your local main:
   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

## Development Guidelines

### Project Structure

```
src/
├── main.py           # Entry point
├── gui/              # GUI components
│   ├── main_window.py  # Main application window
│   └── components.py   # Reusable UI components
├── core/             # Core logic
│   ├── processor.py    # Image processing
│   └── validator.py    # Validation logic
└── utils/            # Utilities
    └── logger.py       # Logging system
```

### Adding New Features

1. **Discuss first** - Open an issue to discuss major features
2. **Start small** - Break large features into smaller PRs
3. **Write tests** - Test-driven development is encouraged
4. **Update docs** - Keep documentation in sync with code

### Testing Guidelines

Write tests for:
- All new functions
- Bug fixes
- Edge cases

Example test:

```python
import pytest
from src.core.validator import ImageValidator

def test_valid_boot_image():
    validator = ImageValidator()
    result = validator.validate_image("tests/fixtures/valid_boot.img")
    assert result['valid'] is True
    assert result['type'] == 'Android Boot Image'

def test_invalid_file_size():
    validator = ImageValidator()
    result = validator.validate_image("tests/fixtures/tiny_file.img")
    assert result['valid'] is False
    assert 'too small' in result['message'].lower()
```

## Questions?

If you have questions:

- **Check existing issues** - Someone may have asked already
- **Open a discussion** - Use GitHub Discussions for general questions
- **Open an issue** - For specific problems or feature requests

## Recognition

All contributors will be:
- Listed in the project README
- Credited in release notes
- Appreciated immensely! 🙏

---

**Thank you for contributing to GUI Device Tree Generator!**

*Together, we're making Android ROM development more accessible to everyone.*
