import os
import tempfile
import shutil
from pathlib import Path
import pytest
from src.repo_digest.core import (
    export_repo_as_text,
    is_ignored,
    load_gitignore,
    iter_files,
    SENSITIVE_PATTERNS,
    EXCLUDES
)


class TestRepoDigest:
    def setup_method(self):
        """Create a temporary directory for each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_repo = Path(self.temp_dir)
        
    def teardown_method(self):
        """Clean up temporary directory after each test"""
        shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, path: str, content: str = "test content"):
        """Helper to create test files"""
        file_path = self.test_repo / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return str(file_path.relative_to(self.test_repo))
    
    def test_basic_export(self):
        """Test basic repository export functionality"""
        # Create test files
        self.create_test_file("main.py", "print('hello world')")
        self.create_test_file("README.md", "# Test Project")
        self.create_test_file("src/utils.py", "def helper(): pass")
        
        output_file = self.test_repo / "output.txt"
        
        # Export repository
        result = export_repo_as_text(
            str(self.test_repo), 
            str(output_file),
            respect_gitignore=False
        )
        
        assert result == 0
        assert output_file.exists()
        
        content = output_file.read_text()
        assert "REPO SUMMARY" in content
        assert "main.py" in content
        assert "README.md" in content
        assert "src/utils.py" in content
        assert "print('hello world')" in content
    
    def test_secrets_blocking(self):
        """Test that sensitive files are blocked by default"""
        # Create sensitive files
        self.create_test_file(".env", "SECRET_KEY=abc123")
        self.create_test_file("config/password.txt", "admin123")
        self.create_test_file("main.py", "print('hello')")
        
        output_file = self.test_repo / "output.txt"
        
        # Should fail with secrets detected
        result = export_repo_as_text(
            str(self.test_repo),
            str(output_file),
            allow_secrets=False,
            respect_gitignore=False
        )
        
        assert result == 2  # Safety violation exit code
        assert not output_file.exists()
    
    def test_secrets_allowed(self):
        """Test that sensitive files are included when allow_secrets=True"""
        # Create sensitive files
        self.create_test_file(".env", "SECRET_KEY=abc123")
        self.create_test_file("main.py", "print('hello')")
        
        output_file = self.test_repo / "output.txt"
        
        # Should succeed with allow_secrets=True
        result = export_repo_as_text(
            str(self.test_repo),
            str(output_file),
            allow_secrets=True,
            respect_gitignore=False
        )
        
        assert result == 0
        assert output_file.exists()
        
        content = output_file.read_text()
        assert ".env" in content
        assert "SECRET_KEY=abc123" in content
    
    def test_gitignore_respect(self):
        """Test that .gitignore patterns are respected"""
        # Create .gitignore
        self.create_test_file(".gitignore", "*.log\ntemp/\n__pycache__/")
        
        # Create files that should be ignored
        self.create_test_file("debug.log", "log content")
        self.create_test_file("temp/cache.txt", "temp content")
        self.create_test_file("__pycache__/module.pyc", "compiled")
        
        # Create files that should be included
        self.create_test_file("main.py", "print('hello')")
        
        output_file = self.test_repo / "output.txt"
        
        result = export_repo_as_text(
            str(self.test_repo),
            str(output_file),
            respect_gitignore=True
        )
        
        assert result == 0
        content = output_file.read_text()
        
        # Should include main.py but not ignored files
        assert "main.py" in content
        assert "debug.log" not in content
        assert "temp/cache.txt" not in content
        assert "FILE: __pycache__/module.pyc" not in content
    
    def test_preview_mode(self):
        """Test preview mode functionality"""
        self.create_test_file("main.py", "print('hello world')")
        self.create_test_file("README.md", "# Test")
        
        output_file = self.test_repo / "output.txt"
        
        # Preview should not create output file
        result = export_repo_as_text(
            str(self.test_repo),
            str(output_file),
            preview=True,
            respect_gitignore=False
        )
        
        assert result == 0
        assert not output_file.exists()
    
    def test_max_bytes_limit(self):
        """Test max bytes limit enforcement"""
        # Create a file that will exceed the limit
        large_content = "x" * 1000
        self.create_test_file("large.txt", large_content)
        
        output_file = self.test_repo / "output.txt"
        
        # Should fail with size limit exceeded
        result = export_repo_as_text(
            str(self.test_repo),
            str(output_file),
            max_bytes=500,  # Set limit lower than file size
            respect_gitignore=False
        )
        
        assert result == 3  # Size limit exceeded
        assert not output_file.exists()
    
    def test_excluded_extensions(self):
        """Test that binary and excluded extensions are filtered out"""
        # Create files with excluded extensions
        self.create_test_file("image.jpg", "fake image data")
        self.create_test_file("video.mp4", "fake video data")
        self.create_test_file("archive.zip", "fake zip data")
        
        # Create files that should be included
        self.create_test_file("main.py", "print('hello')")
        
        output_file = self.test_repo / "output.txt"
        
        result = export_repo_as_text(
            str(self.test_repo),
            str(output_file),
            respect_gitignore=False
        )
        
        assert result == 0
        content = output_file.read_text()
        
        # Should include .py but not binary files
        assert "main.py" in content
        assert "image.jpg" not in content
        assert "video.mp4" not in content
        assert "archive.zip" not in content


class TestUtilityFunctions:
    def test_is_ignored_sensitive_patterns(self):
        """Test sensitive pattern detection"""
        assert is_ignored(".env", [])
        assert is_ignored("config/secret.txt", [])
        assert is_ignored("auth/password.conf", [])
        assert is_ignored("certs/private.key", [])
        assert not is_ignored("main.py", [])
        assert not is_ignored("README.md", [])
    
    def test_is_ignored_excluded_dirs(self):
        """Test excluded directory patterns"""
        assert is_ignored("node_modules/package.json", [])
        assert is_ignored("__pycache__/module.pyc", [])
        assert is_ignored(".git/config", [])
        assert is_ignored("dist/bundle.js", [])
        assert not is_ignored("src/main.py", [])
    
    def test_load_gitignore(self):
        """Test gitignore loading"""
        with tempfile.TemporaryDirectory() as temp_dir:
            gitignore_path = Path(temp_dir) / ".gitignore"
            gitignore_path.write_text("*.log\ntemp/\n# comment\n\n__pycache__/")
            
            patterns = load_gitignore(temp_dir)
            
            assert "*.log" in patterns
            assert "temp/" in patterns
            assert "__pycache__/" in patterns
            assert "# comment" not in patterns  # Comments should be filtered
            assert "" not in patterns  # Empty lines should be filtered


if __name__ == "__main__":
    pytest.main([__file__])
