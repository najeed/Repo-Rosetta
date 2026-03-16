import pytest
import os
import tree_sitter
print(f"DEBUG: tree_sitter package path: {tree_sitter.__file__}")
from backend.parser.engine import ParserEngine

def test_parser_python_extraction():
    parser = ParserEngine()
    # Test on backend/main.py
    result = parser.parse_file("backend/main.py")
    assert result is not None
    assert result["language"] == "python"
    
    # Check if it found the 'root' function or imports
    entity_names = [e["name"] for e in result["entities"]]
    assert "root" in entity_names
    assert "fastapi" in entity_names

def test_parser_extension_mapping():
    parser = ParserEngine()
    # Test mapping for other languages (should return empty entities for now)
    assert parser.parse_file("test.js")["entities"] == []
    assert parser.parse_file("test.go")["entities"] == []

def test_parser_cleanup(tmp_path):
    parser = ParserEngine()
    test_file = tmp_path / "cleanup_test.txt"
    test_file.write_text("dummy content")
    
    assert os.path.exists(test_file)
    parser.cleanup(str(test_file))
    assert not os.path.exists(test_file)
