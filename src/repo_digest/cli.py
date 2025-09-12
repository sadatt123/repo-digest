import argparse
import os
import sys
from .core import export_repo_as_text

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="repo-digest",
        description="Turn any repository into an AI-ready text bundle with safe defaults and rich analytics.",
        epilog=(
            "Safety: By default, files matching sensitive patterns (e.g., .env, *secret*, *.key) are blocked. "
            "Use --allow-secrets only if you understand the risk."
        ),
    )
    parser.add_argument("path", nargs="?", default=".", help="Path to repository (default: current directory)")
    parser.add_argument("-o", "--output", default="repo_export.txt", help="Output file path (default: repo_export.txt)")
    parser.add_argument("--preview", action="store_true", help="Preview counts only; do not write output")
    parser.add_argument("--max-bytes", type=int, default=None, help="Fail if estimated total bytes exceed this limit")
    parser.add_argument("--allow-secrets", action="store_true", help="Allow files that match sensitive patterns (NOT recommended)")
    parser.add_argument("--no-gitignore", action="store_true", help="Do not respect .gitignore (default is to respect it)")

    args = parser.parse_args()

    path = os.path.abspath(args.path)
    if not os.path.exists(path):
        print(f"[error] Path does not exist: {path}")
        sys.exit(1)
    if not os.path.isdir(path):
        print(f"[error] Not a directory: {path}")
        sys.exit(1)

    code = export_repo_as_text(
        path,
        args.output,
        allow_secrets=args.allow_secrets,
        respect_gitignore=(not args.no_gitignore),
        max_bytes=args.max_bytes,
        preview=args.preview,
    )
    sys.exit(code)

if __name__ == "__main__":
    main()
