# Contributing to repo-digest

🎉 Thanks for your interest in contributing to repo-digest! We welcome contributions from developers of all skill levels.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/yourusername/repo-digest.git`
3. **Install** in development mode: `pip install -e ".[dev]"`
4. **Run tests**: `pytest tests/`

## 🐛 Reporting Issues

**Before creating an issue**, please:
- Search existing issues to avoid duplicates
- Use our issue templates
- Provide clear reproduction steps
- Include system information (OS, Python version)

## 💡 Feature Requests

We love new ideas! Please:
- Check the [roadmap](README.md#roadmap) first
- Open a discussion before large features
- Explain the use case and benefits
- Consider implementation complexity

## 🔧 Development Setup

```bash
# Clone and setup
git clone https://github.com/mverab/repo-digest.git
cd repo-digest

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run security checks
bandit -r src/

# Check code style
black --check src/ tests/
```

## 📝 Code Guidelines

- **Python 3.8+** compatibility
- **Type hints** for all functions
- **Docstrings** for public APIs
- **Tests** for new features
- **Security first** mindset

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/

# Test specific functionality
pytest tests/test_core.py::TestRepoDigest::test_secrets_blocking
```

## 📋 Pull Request Process

1. **Create branch**: `git checkout -b feature/your-feature`
2. **Write tests** for your changes
3. **Update documentation** if needed
4. **Run full test suite**: `pytest tests/`
5. **Submit PR** with clear description

### PR Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Security considerations addressed
- [ ] Backwards compatibility maintained

## 🏷️ Good First Issues

Look for issues labeled:
- `good-first-issue` - Perfect for newcomers
- `help-wanted` - Community contributions welcome
- `documentation` - Improve docs and examples

## 🎯 Areas We Need Help

- **Documentation**: Examples, tutorials, API docs
- **Testing**: Edge cases, platform compatibility
- **Features**: See roadmap for priorities
- **Performance**: Optimization opportunities
- **Security**: Code review, vulnerability research

## 💬 Community

- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Bug reports and feature requests
- **Security**: Email security@yourproject.com for vulnerabilities

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making repo-digest better! 🙏**
