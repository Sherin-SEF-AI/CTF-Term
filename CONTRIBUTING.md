# Contributing to CTF Terminal

Thank you for your interest in contributing to CTF Terminal! This document provides guidelines and instructions for contributing.

## Author

**Sherin Joseph Roy**  
Co-Founder & Head of Products at [DeepMost AI](https://deepmost.ai)

- 🌐 [Portfolio](https://sherinjosephroy.link)
- 💼 [LinkedIn](https://www.linkedin.com/in/sherin-roy-deepmost)
- 🐦 [X/Twitter](https://x.com/SherinSEF)
- 💻 [GitHub](https://github.com/Sherin-SEF-AI)

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version)
- Relevant logs or error messages

### Suggesting Features

Feature suggestions are welcome! Please:
- Describe the feature clearly
- Explain why it would be useful
- Provide use cases or examples

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Add tests** for new functionality
5. **Run tests** (`pytest`)
6. **Commit changes** with clear messages
7. **Push to your fork** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

### Code Style

- Follow PEP 8 style guidelines
- Use type hints
- Format with `black`
- Lint with `ruff`
- Write docstrings for all functions

### Writing Tests

- Add tests for new features
- Maintain test coverage above 90%
- Use pytest conventions
- Test edge cases

### Documentation

- Update README.md for user-facing changes
- Update docstrings for code changes
- Keep examples up to date

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ctf-term.git
cd ctf-term

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/

# Lint code
ruff check src/ tests/
```

## Commit Message Guidelines

- Use clear, descriptive messages
- Start with a verb in imperative mood
- Example: "Add challenge validation command"
- Reference issues when applicable

## Pull Request Process

1. Update README.md if needed
2. Add/update tests
3. Ensure all tests pass
4. Update documentation
5. Request review

## Questions?

Feel free to reach out:
- Open an issue for questions
- Contact the author via [sherinjosephroy.link/contact](https://sherinjosephroy.link/contact)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

