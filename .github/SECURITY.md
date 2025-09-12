# Security Policy

## 🔒 Security First Philosophy

repo-digest is built with security as a core principle. We take the security of our users' code and data seriously.

## 🛡️ Built-in Security Features

- **Secret Detection**: Automatically blocks files matching sensitive patterns (`.env`, `*secret*`, `*.key`, `*.pem`)
- **Safe Defaults**: Excludes binary files, build artifacts, and common sensitive directories
- **Path Validation**: Prevents directory traversal attacks
- **Input Sanitization**: All file paths are validated and sanitized
- **No Code Execution**: Tool only reads files, never executes user code

## 🚨 Reporting Security Vulnerabilities

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them responsibly:

1. **Email**: Send details to `security@yourproject.com`
2. **Subject**: `[SECURITY] repo-digest vulnerability report`
3. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## ⏱️ Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 1-3 days
  - High: 1-2 weeks
  - Medium: 2-4 weeks
  - Low: Next release cycle

## 🏆 Security Hall of Fame

We recognize security researchers who help improve repo-digest:

*No reports yet - be the first!*

## 📋 Security Best Practices for Users

### ✅ Recommended Usage
```bash
# Safe default usage
repo-digest . -o output.txt

# Preview first to check what's included
repo-digest . --preview

# Set size limits for large repos
repo-digest . -o output.txt --max-bytes 5000000
```

### ⚠️ Use with Caution
```bash
# Only if you understand the risks
repo-digest . -o output.txt --allow-secrets

# Review .gitignore before using
repo-digest . -o output.txt --no-gitignore
```

### ❌ Never Do
- Don't use `--allow-secrets` on repositories with real credentials
- Don't ignore security warnings without understanding them
- Don't share output files containing sensitive information

## 🔍 Security Auditing

We regularly audit our code using:
- **Bandit**: Static security analysis
- **Safety**: Dependency vulnerability scanning
- **Manual Code Review**: Security-focused reviews
- **Community Reports**: User-reported issues

## 📚 Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.org/dev/security/)
- [Secure Coding Guidelines](https://wiki.sei.cmu.edu/confluence/display/seccode)

## 📄 Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

---

**Security is everyone's responsibility. Thank you for helping keep repo-digest secure! 🙏**
