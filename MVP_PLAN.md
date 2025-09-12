# repo-digest MVP Plan

## Project Overview
Transform the existing `export_repo_as_text.py` script into a professional, beginner-friendly PyPI package called `repo-digest`.

**Goal**: Create a dead-simple tool for anyone to turn a local repository into an AI-ready text bundle with sensible defaults and safety guardrails.

**Target Users**: 
- Absolute beginners using ChatGPT/Claude who want to "paste" their repo context
- Developers who want a quick repo digest

## Core Value Proposition
- **One-liner**: Turn any repository into a safe, structured text export ready for LLMs
- **Differentiators**:
  - Sensible, safe defaults (strong excludes, secret patterns blocked by default)
  - Accurate token counting with optional tiktoken (fallback to words if not installed)
  - Clean summary and directory tree for quick repo understanding
  - Works out-of-the-box on macOS/Linux/Windows

## MVP Scope (No Overengineering)

### ✅ COMPLETED
- [x] **Project Structure**: Created professional package structure with `src/repo_digest/`
- [x] **PyPI Package Setup**: `pyproject.toml` with metadata, optional tiktoken extra, console script
- [x] **Core Module**: Ported original script to `src/repo_digest/core.py` with type hints
- [x] **CLI Interface**: Basic argparse CLI in `src/repo_digest/cli.py` with MVP flags
- [x] **Documentation**: Beginner-friendly README.md with quickstart, safety, examples
- [x] **License**: MIT license for maximum adoption
- [x] **Package Structure**:
  ```
  repo-digest/
  ├── pyproject.toml
  ├── README.md
  ├── LICENSE
  ├── src/
  │   └── repo_digest/
  │       ├── __init__.py
  │       ├── core.py
  │       └── cli.py
  ```

### 🔧 IN PROGRESS
- [ ] **Safety Logic Fix**: Complete allow_secrets implementation in core.py
- [ ] **CLI Testing**: Verify all flags work correctly

### 📋 PENDING (MVP Deliverables)
- [ ] **Testing**: Basic functionality tests
- [ ] **CI/CD**: GitHub Actions for lint + build
- [ ] **Package Build**: Test local build and installation
- [ ] **PyPI Release**: Publish v0.1.0 to PyPI
- [ ] **Demo Content**: Create GIF/screenshots for README

## CLI Design (MVP)

### Commands
```bash
# Basic usage
repo-digest . -o repo.txt

# With options
repo-digest ~/project -o export.txt --preview
repo-digest . -o repo.txt --max-bytes 5000000
repo-digest . -o repo.txt --allow-secrets --no-gitignore
```

### Flags
- `--preview`: Show counts only; don't write output
- `--max-bytes N`: Fail if estimated total bytes exceed limit
- `--allow-secrets`: Allow files matching sensitive patterns (off by default)
- `--no-gitignore`: Ignore .gitignore (default respects it)

### Exit Codes
- `0`: Success
- `1`: Runtime error (bad path, permission)
- `2`: Safety violation (secrets detected and not allowed)
- `3`: Exceeded size/limits

## Safety and Guardrails

### ✅ Implemented
- Comprehensive exclusion patterns (build dirs, node_modules, etc.)
- Binary file exclusions
- Gitignore respect by default
- Sensitive pattern detection

### 🔧 Needs Fix
- Secret blocking logic (currently has implementation issue)
- Clear safety banners in output

### Safety Features
- **Secrets blocked by default**: `.env`, `*secret*`, `*password*`, `*token*`, `*key*`, `*.pem`, etc.
- **Binary exclusions**: Images, videos, archives, compiled files
- **Build artifact exclusions**: `node_modules`, `__pycache__`, `dist`, `build`, etc.
- **Large data exclusions**: `.csv`, `.h5`, `.parquet`, etc.

## Installation and Distribution

### Package Details
- **Name**: `repo-digest`
- **PyPI**: `pip install repo-digest`
- **Optional tiktoken**: `pip install "repo-digest[tiktoken]"`
- **Entry point**: `repo-digest` console script
- **Python support**: >=3.8

### Distribution Channels (MVP)
- [x] PyPI package
- [ ] GitHub releases
- [ ] Basic documentation

### Future Distribution (Post-MVP)
- Homebrew formula for macOS
- Snap package for Linux
- Chocolatey for Windows

## Launch Plan (7-10 days)

### Phase 1: Complete MVP (Days 1-2)
- [ ] Fix safety logic in core.py
- [ ] Add basic tests
- [ ] Set up GitHub Actions (lint + build)
- [ ] Test local installation
- [ ] Release v0.1.0 to PyPI

### Phase 2: Demo and Launch (Days 3-4)
- [ ] Create demo GIF showing: run CLI → open output → highlight tree and summary
- [ ] Polish README with demo
- [ ] Create GitHub repository with good README and tags

### Phase 3: Promotion (Days 5-10)
- [ ] Launch on Reddit: r/Python, r/learnprogramming, r/programming
- [ ] Twitter/X thread with GIF demo
- [ ] Position as: "Paste your repo into ChatGPT/Claude in one go"
- [ ] Add "Good First Issues" and "Help Wanted" labels
- [ ] Respond quickly to feedback

## Success Metrics (MVP)

### Technical Metrics
- **Installation friction**: Time-to-first-export < 2 minutes
- **Functionality**: Users can export without reading more than Quickstart

### Community Metrics
- **GitHub**: 50-100 stars in first 2 weeks
- **PyPI**: 200-500 downloads in first month
- **Feedback**: At least 5 real user issues/requests (validation signal)

## Roadmap After MVP (Only When Demand Validated)

### Phase 2 Features
- Output formats: Markdown and JSON
- Config file support (repo-to-text.yaml)
- Platform integrations (GitHub repo URL)

### Phase 3 Features
- Chunking large repos into multiple files with manifest
- Simple GUI (only if users ask)
- Advanced filtering options

### Phase 4 Ecosystem
- Plugin system for custom processors
- Integration with popular AI tools
- Enterprise features

## Technical Decisions Made

### Core Choices
- **Language**: Python (matches original script)
- **CLI Framework**: argparse (simple, no dependencies)
- **Package Manager**: pip/PyPI (standard Python distribution)
- **License**: MIT (maximum adoption)
- **Limit Flag**: `--max-bytes` (simple and predictable vs `--max-tokens`)

### Architecture Decisions
- **Module Structure**: Clean separation of core logic and CLI
- **Type Hints**: Added for better code quality
- **Error Handling**: Structured exit codes for automation
- **Safety First**: Secrets blocked by default, explicit override required

## Current Status Summary

**✅ Foundation Complete**: Package structure, core functionality, CLI interface, documentation
**🔧 Minor Fixes Needed**: Safety logic implementation, testing
**📋 Ready for Launch**: Once fixes complete, ready for PyPI release and promotion

**Next Immediate Steps**:
1. Fix allow_secrets logic in core.py
2. Add basic tests
3. Test local installation
4. Release to PyPI
5. Create demo content
6. Launch promotion campaign

The MVP is 90% complete and ready for launch within 1-2 days of completing the remaining technical fixes.