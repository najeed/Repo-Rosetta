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
        # Initialize languages from tree-sitter bindings with fallbacks for naming variations
        self.languages = {
            "python": self._get_lang(tspython, "python"),
            "javascript": self._get_lang(tsjs, "javascript"),
            "typescript": self._get_lang(tstypescript, "typescript"),
            "tsx": self._get_lang(tstypescript, "tsx"),
            "go": self._get_lang(tsgo, "go"),
            "rust": self._get_lang(tsrust, "rust"),
            "cpp": self._get_lang(tscpp, "cpp"),
        }
        self.parser = Parser(self.languages["python"])

    def _get_lang(self, module, name):
        # Handle variations where some libs use module.language() and others module.language_name()
        capsule = None
        if hasattr(module, "language"):
            capsule = module.language()
        elif hasattr(module, f"language_{name}"):
            capsule = getattr(module, f"language_{name}")()
        
        if capsule:
            from tree_sitter import Language
            return Language(capsule)
        raise AttributeError(f"Could not find language getter in tree-sitter-{name}")

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".py":
            lang = "python"
        elif ext == ".js":
            lang = "javascript"
        elif ext == ".ts":
            lang = "typescript"
        elif ext == ".tsx":
            lang = "tsx"
        elif ext == ".go":
            lang = "go"
        elif ext == ".rs":
            lang = "rust"
        elif ext in [".cpp", ".h", ".hpp", ".cc", ".cxx"]:
            lang = "cpp"
        else:
            lang = None

        if lang and lang in self.languages:
            if not os.path.exists(file_path):
                return None
            
            try:
                with open(file_path, "rb") as f:
                    code_bytes = f.read()
                
                # Use a fresh parser instance for every call to avoid state issues in some C-extensions
                from tree_sitter import Parser
                parser = Parser(self.languages[lang])
                tree = parser.parse(code_bytes)
                
                if tree.root_node.type == "ERROR":
                    # Fallback or diagnostic for failed parse
                    return {"file": file_path, "language": lang, "entities": [], "error": "Syntax Error or Version Mismatch"}
                
                return self._extract_entities(tree, lang, file_path)
            except Exception as e:
                # Log but don't crash
                print(f"[*] Parser failure for {file_path}: {e}")
                return None
        return None

    def cleanup(self, path: str):
        # Securely delete raw code files after Knowledge Graph construction
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            import shutil
            shutil.rmtree(path)
        print(f"[*] Securely deleted raw code at: {path}")

    def _extract_entities(self, tree, lang: str, file_path: str) -> Dict[str, Any]:
        if lang not in self.languages:
            return {"file": file_path, "language": lang, "entities": []}

        # Python SCM Queries
        if lang == "python":
            query_scm = """
            (class_definition
                name: (identifier) @class.name) @class.def
            (function_definition
                name: (identifier) @function.name) @function.def
            (import_from_statement
                module_name: (dotted_name) @import.from) @import.stmt
            (import_statement
                name: (dotted_name) @import.name) @import.stmt
            """
        else:
            # Placeholder for other languages, for now return empty
            return {"file": file_path, "language": lang, "entities": []}
        
        try:
            query = self.languages[lang].query(query_scm)
            cursor = QueryCursor(query)
            captures = cursor.captures(tree.root_node)
        except Exception as e:
            print(f"DEBUG: Query error for {lang}: {e}")
            return {"file": file_path, "language": lang, "entities": []}
        
        entities = []
        # In tree-sitter 0.25, captures is a dict: { "tag.name": [Node, ...] }
        for tag, nodes in captures.items():
            for node in nodes:
                if tag in ["class.name", "function.name"]:
                    entities.append({
                        "name": node.text.decode("utf-8"),
                        "type": "class" if "class" in tag else "function",
                        "path": file_path,
                        "line_start": node.start_point[0] + 1,
                        "line_end": node.end_point[0] + 1,
                    })
                elif tag in ["import.from", "import.name"]:
                    entities.append({
                        "name": node.text.decode("utf-8"),
                        "type": "import",
                        "path": file_path,
                        "line_start": node.start_point[0] + 1,
                        "line_end": node.end_point[0] + 1,
                    })

        return {
            "file": file_path,
            "language": lang,
            "entities": entities
        }
