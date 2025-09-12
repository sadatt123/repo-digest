import os
import fnmatch
from collections import defaultdict, Counter
from datetime import datetime
from typing import Iterable, Dict, Any, List, Tuple, Optional

try:
    import tiktoken  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    tiktoken = None

# Comprehensive list of directories and files to exclude
EXCLUDES = [
    # Version control
    '.git', '.svn', '.hg', '.bzr',
    
    # OS generated files
    '.DS_Store', 'Thumbs.db', 'desktop.ini',
    
    # Python
    '__pycache__', '*.pyc', '*.pyo', '*.pyd', '.Python',
    'pip-log.txt', 'pip-delete-this-directory.txt',
    '.venv', 'venv', 'ENV', 'env',
    '.pytest_cache', '.mypy_cache', '.tox',
    'htmlcov', '.coverage', '.coverage.*',
    '*.egg-info', 'dist', 'build', 'wheels',
    '.eggs', '*.egg',
    
    # Node.js / JavaScript
    'node_modules', 'npm-debug.log*', 'yarn-debug.log*', 'yarn-error.log*',
    '.npm', '.yarn', '.pnp', '.pnp.js',
    'bower_components', 'jspm_packages',
    
    # IDE and editors
    '.idea', '.vscode', '*.swp', '*.swo', '*~',
    '.project', '.classpath', '.settings',
    '*.sublime-project', '*.sublime-workspace',
    
    # Build outputs
    'target', 'out', 'bin', 'obj',
    '*.class', '*.jar', '*.war', '*.ear',
    '*.dll', '*.exe', '*.o', '*.so', '*.dylib',
    
    # Logs and databases
    '*.log', '*.sql', '*.sqlite', '*.db',
    'logs', 'log',
    
    # Temporary files
    '*.tmp', '*.temp', '*.bak', '*.backup', '*.cache',
    '.cache', 'tmp', 'temp',
    
    # Security sensitive files
    '*.key', '*.pem', '*.p12', '*.pfx',
    'secrets', 'credentials',
    
    # Documentation builds
    '_build', 'site', 'docs/_build',
    
    # Package manager locks (usually not needed for understanding code)
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    'Pipfile.lock', 'poetry.lock', 'composer.lock',
    
    # Other
    '.sass-cache', '.next', '.nuxt', '.turbo',
    '.docusaurus', '.cache-loader',
    'vendor', 'vendors',
]

# File extensions to exclude
EXCLUDE_EXTENSIONS = [
    # Binary files
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg',
    '.mp3', '.mp4', '.avi', '.mov', '.wmv', '.flv',
    '.zip', '.tar', '.gz', '.rar', '.7z',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    
    # Compiled files
    '.pyc', '.pyo', '.class', '.o', '.so', '.dll', '.exe',
    
    # Lock files
    '.lock',
    
    # Large data files
    '.csv', '.tsv', '.parquet', '.feather', '.h5', '.hdf5',
    
    # Font files
    '.ttf', '.otf', '.woff', '.woff2', '.eot',
    
    # Map files
    '.map', '.min.js.map', '.css.map',
]

# Patterns for files that might contain sensitive information
SENSITIVE_PATTERNS = [
    '*secret*', '*password*', '*token*', '*key*',
    '*.pem', '*.key', '*.cert', '*.crt',
    '.env*', '*.env',
]

GITIGNORE = '.gitignore'

def load_gitignore(root_dir: str) -> List[str]:
    patterns: List[str] = []
    gitignore_path = os.path.join(root_dir, GITIGNORE)
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    return patterns

def is_ignored(path: str, patterns: Iterable[str], check_sensitive: bool = True) -> bool:
    # Check against gitignore patterns
    for pat in patterns:
        if fnmatch.fnmatch(path, pat):
            return True
    
    # Check file extension
    _, ext = os.path.splitext(path)
    if ext.lower() in EXCLUDE_EXTENSIONS:
        return True
    
    # Check sensitive patterns (optional)
    if check_sensitive:
        for pat in SENSITIVE_PATTERNS:
            if fnmatch.fnmatch(path.lower(), pat.lower()):
                return True
    
    # Check if any part of the path contains excluded patterns
    path_parts = path.split(os.sep)
    for part in path_parts:
        for exclude in EXCLUDES:
            if fnmatch.fnmatch(part, exclude):
                return True
    
    return False

def count_tokens(text: str, encoder=None) -> int:
    if encoder:
        return len(encoder.encode(text))
    return len(text.split())

def iter_files(root_dir: str, patterns: Iterable[str]) -> Iterable[str]:
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter out excluded directories
        dirnames[:] = [d for d in dirnames if not any(fnmatch.fnmatch(d, exc) for exc in EXCLUDES)]
        
        for filename in sorted(filenames):
            # Skip files matching exclude patterns
            if any(fnmatch.fnmatch(filename, exc) for exc in EXCLUDES):
                continue
            
            rel_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
            
            # Skip if ignored by any rule (but don't check sensitive patterns here)
            if is_ignored(rel_path, patterns, check_sensitive=False):
                continue
            
            # Skip minified files
            if '.min.' in filename or filename.endswith('.min.js') or filename.endswith('.min.css'):
                continue
            
            yield rel_path

def build_dir_aggregates(file_infos: Iterable[Dict[str, Any]]) -> Tuple[Dict[str, Dict[str, int]], Dict[str, List[str]]]:
    aggregates: Dict[str, Dict[str, int]] = defaultdict(lambda: {"files": 0, "tokens": 0, "bytes": 0})
    children_map: Dict[str, set] = defaultdict(set)
    for info in file_infos:
        rel_path = info["path"]
        tokens = int(info["tokens"])  # ensure ints
        size = int(info["bytes"])
        # accumulate for this file's directory and all ancestors
        dir_path = os.path.dirname(rel_path) or "."
        parts = [] if dir_path == "." else dir_path.split(os.sep)
        for i in range(len(parts) + 1):
            d = "." if i == 0 else os.sep.join(parts[:i])
            # Count file for all ancestor directories including root (represents total files under dir)
            aggregates[d]["files"] += 1
            aggregates[d]["tokens"] += tokens
            aggregates[d]["bytes"] += size
        # children map
        if dir_path != ".":
            parent = os.path.dirname(dir_path) or "."
            children_map[parent].add(dir_path)
        else:
            children_map["."].add(".")  # ensure root exists
    # ensure sets converted to sorted lists
    children = {k: sorted(v - {k}) for k, v in children_map.items()}
    return aggregates, children

def print_dir_tree(out, aggregates: Dict[str, Dict[str, int]], children: Dict[str, List[str]], current: str = ".", prefix: str = "") -> None:
    # Print current directory line (skip printing for root at first call)
    if prefix == "":
        # root header printed separately by caller
        pass
    else:
        data = aggregates.get(current, {"files": 0, "tokens": 0, "bytes": 0})
        out.write(f"{prefix}{os.path.basename(current) or '.'}/ (files: {data['files']}, tokens: {data['tokens']}, bytes: {data['bytes']})\n")
    # children dirs
    dirs = sorted([d for d in children.get(current, []) if d != current])
    for idx, child in enumerate(dirs):
        is_last = idx == len(dirs) - 1
        branch = "└── " if is_last else "├── "
        next_prefix = (prefix.replace("└── ", "    ").replace("├── ", "│   ") if prefix else "") + branch
        print_dir_tree(out, aggregates, children, child, next_prefix)


def export_repo_as_text(root_dir: str, output_file: str, *, allow_secrets: bool = False, respect_gitignore: bool = True, max_bytes: Optional[int] = None, preview: bool = False) -> int:
    """
    Export repository at root_dir into a single text file with summaries.

    Returns an exit code:
      0 success
      2 safety violation (secrets detected and not allowed)
      3 exceeded size/limits in preview
    """
    patterns = load_gitignore(root_dir) if respect_gitignore else []
    encoder = tiktoken.get_encoding('cl100k_base') if tiktoken else None
    tokenizer_name = 'cl100k_base' if encoder else 'words_approx'

    file_infos: List[Dict[str, Any]] = []
    total_tokens = 0
    total_bytes = 0
    by_ext_tokens: Counter = Counter()
    by_ext_bytes: Counter = Counter()
    by_ext_files: Counter = Counter()

    # Pre-scan to detect secrets and size
    blocked_sensitive: List[str] = []

    for rel_path in iter_files(root_dir, patterns):
        # sensitive check by pattern (path-level)
        is_sensitive = any(fnmatch.fnmatch(rel_path.lower(), pat.lower()) for pat in SENSITIVE_PATTERNS)
        if is_sensitive and not allow_secrets:
            blocked_sensitive.append(rel_path)
            continue

        abs_path = os.path.join(root_dir, rel_path)
        try:
            with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            tokens = count_tokens(content, encoder)
            lines = content.count('\n') + (1 if content and not content.endswith('\n') else 0)
            size = os.path.getsize(abs_path)
            file_infos.append({"path": rel_path, "tokens": tokens, "lines": lines, "bytes": size, "content": content})
            total_tokens += tokens
            total_bytes += size
            ext = os.path.splitext(rel_path)[1].lower() or "<no-ext>"
            by_ext_tokens[ext] += tokens
            by_ext_bytes[ext] += size
            by_ext_files[ext] += 1
        except Exception as e:
            print(f"[skip] {rel_path}: {e}")

    # Safety: secrets check
    if blocked_sensitive and not allow_secrets:
        print("[SAFETY] Sensitive-looking files were blocked by default:")
        for p in blocked_sensitive[:20]:
            print(f" - {p}")
        if len(blocked_sensitive) > 20:
            print(f" ... and {len(blocked_sensitive) - 20} more")
        print("Re-run with --allow-secrets if you know what you're doing.")
        return 2
    
    # Warning when secrets are allowed
    if allow_secrets:
        sensitive_included = [info["path"] for info in file_infos if any(fnmatch.fnmatch(info["path"].lower(), pat.lower()) for pat in SENSITIVE_PATTERNS)]
        if sensitive_included:
            print(f"[WARNING] Including {len(sensitive_included)} sensitive files (--allow-secrets enabled)")
            for p in sensitive_included[:5]:
                print(f" - {p}")
            if len(sensitive_included) > 5:
                print(f" ... and {len(sensitive_included) - 5} more")

    # Preview mode
    if preview:
        print("===== PREVIEW =====")
        print(f"Tokenizer: {tokenizer_name}")
        print(f"Total candidate files: {len(file_infos)}")
        print(f"Estimated total tokens: {total_tokens}")
        print(f"Estimated total bytes: {total_bytes}")
        print("Top extensions:")
        for ext in sorted(by_ext_files.keys())[:10]:
            print(f" {ext}: files={by_ext_files[ext]}, tokens={by_ext_tokens[ext]}, bytes={by_ext_bytes[ext]}")
        if max_bytes is not None and total_bytes > max_bytes:
            print(f"[LIMIT] Estimated bytes {total_bytes} exceed --max-bytes={max_bytes}")
            return 3
        return 0

    # Max bytes enforcement (write path)
    if max_bytes is not None and total_bytes > max_bytes:
        print(f"[LIMIT] Total bytes {total_bytes} exceed --max-bytes={max_bytes}. Use --preview first or raise the limit.")
        return 3

    # Build aggregates and tree
    aggregates, children = build_dir_aggregates(file_infos)

    with open(output_file, 'w', encoding='utf-8') as out:
        # Summary
        out.write('===== REPO SUMMARY =====\n')
        out.write(f"Generated: {datetime.now().isoformat()}\n")
        out.write(f"Tokenizer: {tokenizer_name}\n")
        out.write(f"Total files: {len(file_infos)}\n")
        out.write(f"Total tokens: {total_tokens}\n")
        out.write(f"Total bytes: {total_bytes}\n")

        # Extension breakdown
        out.write('\n===== SUMMARY BY EXTENSION =====\n')
        for ext in sorted(by_ext_files.keys()):
            out.write(f"{ext}: files={by_ext_files[ext]}, tokens={by_ext_tokens[ext]}, bytes={by_ext_bytes[ext]}\n")

        # Directory tree
        out.write('\n===== DIRECTORY TREE =====\n')
        root_data = aggregates.get('.', {"files": 0, "tokens": 0, "bytes": 0})
        out.write(f"./ (files: {root_data['files']}, tokens: {root_data['tokens']}, bytes: {root_data['bytes']})\n")
        print_dir_tree(out, aggregates, children, current='.', prefix='')

        # Files
        out.write('\n===== FILES =====\n')
        for info in sorted(file_infos, key=lambda x: x["path"]):
            out.write(f"\n===== FILE: {info['path']} =====\n")
            out.write(f"[TOKENS: {info['tokens']} | LINES: {info['lines']} | BYTES: {info['bytes']}]\n")
            out.write(info['content'])
            out.write('\n')

        # Detailed summary by file
        out.write(f"\n===== SUMMARY BY FILE =====\n")
        for info in sorted(file_infos, key=lambda x: x['tokens'], reverse=True):
            out.write(f"{info['path']} : {info['tokens']} tokens, {info['lines']} lines, {info['bytes']} bytes\n")

        # Top files
        out.write(f"\n===== TOP 20 BY TOKENS =====\n")
        for info in sorted(file_infos, key=lambda x: x['tokens'], reverse=True)[:20]:
            out.write(f"{info['path']} : {info['tokens']} tokens\n")
        out.write(f"\n===== TOP 20 BY BYTES =====\n")
        for info in sorted(file_infos, key=lambda x: x['bytes'], reverse=True)[:20]:
            out.write(f"{info['path']} : {info['bytes']} bytes\n")

    return 0
