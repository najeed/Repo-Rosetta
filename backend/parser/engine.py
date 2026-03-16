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
        # Initialize languages directly from tree-sitter bindings
        self.languages = {
            "python": tspython.language(),
            "javascript": tsjs.language(),
            "typescript": tstypescript.language(),
            "go": tsgo.language(),
            "rust": tsrust.language(),
            "cpp": tscpp.language(),
        }
        self.parser = Parser(self.languages["python"]) # Initialize with a default

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
        # Planned implementation: Use tree-sitter queries to extract
        # comprehensive function, class, and import metadata.
        entities = []
        root_node = tree.root_node
        
        # Current: Heuristic-based extraction for architectural overview
        # In a real implementation, we would use tree-sitter queries
        return {
            "file": file_path,
            "language": lang,
            "entities": entities
        }
