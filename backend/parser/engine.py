import tree_sitter_python as tspython
import tree_sitter_javascript as tsjs
import tree_sitter_typescript as tstypescript
import tree_sitter_go as tsgo
import tree_sitter_rust as tsrust
import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser
from typing import List, Dict, Any
import os

class ParserEngine:
    def __init__(self):
        self.languages = {
            "python": Language(tspython.language()),
            "javascript": Language(tsjs.language()),
            "typescript": Language(tstypescript.language()),
            "go": Language(tsgo.language()),
            "rust": Language(tsrust.language()),
            "cpp": Language(tscpp.language()),
        }
        self.parser = Parser()

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".py":
            lang = "python"
        elif ext == ".js":
            lang = "javascript"
        elif ext in [".ts", ".tsx"]:
            lang = "typescript"
        elif ext == ".go":
            lang = "go"
        elif ext == ".rs":
            lang = "rust"
        elif ext in [".cpp", ".h", ".hpp", ".cc", ".cxx"]:
            lang = "cpp"
        else:
            return None

        self.parser.set_language(self.languages[lang])
        with open(file_path, "rb") as f:
            tree = self.parser.parse(f.read())

        return self._extract_entities(tree, lang, file_path)

    def cleanup(self, path: str):
        # Securely delete raw code files after Knowledge Graph construction
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            import shutil
            shutil.rmtree(path)
        print(f"[*] Securely deleted raw code at: {path}")

    def _extract_entities(self, tree, lang: str, file_path: str) -> Dict[str, Any]:
        # This is a placeholder for actual extraction logic which will use queries
        # to find functions, classes, and imports.
        entities = []
        root_node = tree.root_node
        
        # Simple extraction logic for demonstration
        # In a real implementation, we would use tree-sitter queries
        return {
            "file": file_path,
            "language": lang,
            "entities": entities
        }
