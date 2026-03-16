import pytest
import os
from backend.parser.engine import ParserEngine

def test_parser_extension_mapping():
    parser = ParserEngine()
    
    # Mocking different extensions to test mapping
    assert parser.parse_file("test.py") is not None
    assert parser.parse_file("test.js") is not None
    assert parser.parse_file("test.tsx") is not None
    assert parser.parse_file("test.go") is not None
    assert parser.parse_file("test.rs") is not None
    assert parser.parse_file("test.cpp") is not None
    assert parser.parse_file("test.txt") is None

def test_parser_cleanup(tmp_path):
    parser = ParserEngine()
    test_file = tmp_path / "cleanup_test.txt"
    test_file.write_text("dummy content")
    
    assert os.path.exists(test_file)
    parser.cleanup(str(test_file))
    assert not os.path.exists(test_file)
