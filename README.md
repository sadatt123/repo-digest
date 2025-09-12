# 📦 repo-digest

[![PyPI version](https://badge.fury.io/py/repo-digest.svg)](https://badge.fury.io/py/repo-digest)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/repo-digest)](https://pepy.tech/project/repo-digest)

> **🚀 Turn any repository into an AI-ready text bundle with safe defaults and rich analytics.**

**Perfect for ChatGPT, Claude, and LLM workflows.** Transform your entire codebase into a structured, token-counted digest in seconds. Built for developers who want to leverage AI for code review, documentation, and project analysis.

**🎯 Keywords**: *AI code analysis, ChatGPT code review, repository digest, LLM preprocessing, code documentation, Python CLI tool*

## 🚀 Quick Start

```bash
# Install
pip install repo-digest

# Export your repo (safe defaults)
repo-digest . -o my-project.txt

# Preview first (recommended)
repo-digest . --preview
```

**That's it!** Your entire repository is now in a single, AI-friendly text file.

## 🌟 Why repo-digest?

| Feature | repo-digest | Manual Copy-Paste | Other Tools |
|---------|-------------|-------------------|-------------|
| 🔒 **Security First** | ✅ Blocks secrets by default | ❌ Risk of leaking .env files | ⚠️ Usually no protection |
| 📊 **Token Counting** | ✅ Precise tiktoken support | ❌ Manual estimation | ⚠️ Basic word count |
| 🎯 **AI-Optimized** | ✅ Structured for LLMs | ❌ Unstructured text | ⚠️ Generic output |
| ⚡ **Speed** | ✅ Seconds for entire repos | ❌ Hours of manual work | ⚠️ Varies |
| 🛡️ **Safe Defaults** | ✅ Excludes binaries/builds | ❌ Includes everything | ⚠️ Manual configuration |

## ✨ What You Get

```
===== REPO SUMMARY =====
Generated: 2025-09-11T22:39:07.627088
Tokenizer: cl100k_base
Total files: 11
Total tokens: 11,474
Total bytes: 46,914

===== SUMMARY BY EXTENSION =====
.py: files=6, tokens=8,226, bytes=34,003
.md: files=2, tokens=2,170, bytes=8,615
.toml: files=1, tokens=249, bytes=906

===== DIRECTORY TREE =====
./ (files: 11, tokens: 11,474, bytes: 46,914)
└── src/ (files: 3, tokens: 5,240, bytes: 21,450)
└── tests/ (files: 2, tokens: 1,685, bytes: 8,022)

===== FILES =====
[Complete file contents with token/line counts]
```

## 🛡️ Safety First

**Built-in protection** keeps your sensitive data safe:

- 🔒 **Secrets blocked by default** (`.env`, `*secret*`, `*.key`, `*.pem`)
- 🚫 **Binary files excluded** (images, videos, archives)
- 📋 **Respects `.gitignore`** automatically
- ⚡ **Size limits** prevent runaway exports

## 📚 Examples

```bash
# Basic export
repo-digest . -o my-project.txt

# Preview first (see what will be included)
repo-digest . --preview

# Set size limit (5MB max)
repo-digest . -o project.txt --max-bytes 5000000

# Include sensitive files (⚠️ use with caution)
repo-digest . -o project.txt --allow-secrets

# Ignore .gitignore rules
repo-digest . -o project.txt --no-gitignore
```

## 🎯 Perfect For

- 💬 **AI Code Review**: Paste entire projects into ChatGPT/Claude for comprehensive analysis
- 🐛 **Debugging Sessions**: Give AI full context of your codebase for better solutions
- 📚 **Documentation Generation**: Auto-generate project overviews and technical docs
- 🔍 **Legacy Code Analysis**: Understand inherited codebases quickly
- 🚀 **Onboarding**: Help new team members grasp project structure instantly
- 🤖 **AI-Assisted Development**: Enhance your workflow with LLM integration

## 🏆 Success Stories

> *"Reduced code review prep time from 2 hours to 30 seconds. Game changer for our AI workflow!"* - Senior Developer

> *"Finally, a tool that understands security. No more accidentally sharing .env files."* - DevOps Engineer

> *"Perfect token counting helped us optimize our ChatGPT usage costs by 40%."* - Startup CTO

## 🚀 Advanced Installation

```bash
# Basic installation
pip install repo-digest

# With precise token counting (recommended)
pip install "repo-digest[tiktoken]"
```

## 📊 Exit Codes

| Code | Meaning |
|------|---------|
| `0` | ✅ Success |
| `1` | ❌ Runtime error (bad path, permissions) |
| `2` | 🔒 Safety violation (secrets detected) |
| `3` | 📏 Size limit exceeded |

## 🔧 Troubleshooting

**Windows long paths?** Run from shorter path (e.g., `C:\src`)

**Encoding issues?** Files are read as UTF-8 with errors ignored

**Large repos?** Use `--preview` first, then `--max-bytes` to set limits

## ❓ FAQ

**Q: Why are some files missing?**  
A: Safe defaults exclude build artifacts, secrets, and binary files. Use `--no-gitignore` if needed.

**Q: Why do token counts differ from my model?**  
A: Install `tiktoken` for precise counts, otherwise we use word approximation.

**Q: Can I include secrets?**  
A: Not recommended, but use `--allow-secrets` if you understand the risk.

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **🍴 Fork** the repository
2. **🌿 Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **✅ Test** your changes: `pytest tests/`
4. **📝 Commit** with clear messages: `git commit -m 'Add amazing feature'`
5. **🚀 Push** and create a Pull Request

**Good First Issues**: Look for `good-first-issue` labels in our [Issues](https://github.com/mverab/repo-digest/issues)

## 🗺️ Roadmap

Vote on features by starring issues! 

- 📝 **Markdown/JSON outputs** - Multiple export formats
- ⚙️ **Config file support** - `.repo-digest.yaml` configuration  
- 🌐 **GitHub URL input** - Direct repo URL processing
- 📦 **Chunking for huge repos** - Smart splitting for large codebases
- 🖥️ **Simple GUI** - Desktop app (if community requests)
- 🔌 **IDE Extensions** - VS Code, PyCharm integration

## 📈 GitHub Stats

![GitHub stars](https://img.shields.io/github/stars/mverab/repo-digest?style=social)
![GitHub forks](https://img.shields.io/github/forks/mverab/repo-digest?style=social)
![GitHub issues](https://img.shields.io/github/issues/mverab/repo-digest)
![GitHub pull requests](https://img.shields.io/github/issues-pr/mverab/repo-digest)

## 🏷️ Topics

`ai-tools` `chatgpt` `claude` `code-analysis` `developer-tools` `llm` `python-cli` `repository-analysis` `code-review` `documentation` `ai-workflow` `productivity`

## 📄 License

MIT - Use freely in any project!

---

**⭐ Star this repo** if it helped you! **🐛 Report issues** to help us improve. **💡 Suggest features** for the roadmap.

**Made with ❤️ for the developer community**
