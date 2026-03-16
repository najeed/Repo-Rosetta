import tree_sitter_python as tspython
import tree_sitter_javascript as tsjs
import tree_sitter_typescript as tstypescript
import tree_sitter_go as tsgo
import tree_sitter_rust as tsrust
import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser, Query, QueryCursor
from typing import List, Dict, Any
import os
class ParserEngine:
    MAX_FILE_SIZE = 1024 * 1024 * 2 # 2MB limit for semantic analysis

    def __init__(self):
        # Initialize languages from tree_sitter 0.25+ bindings
        self.languages = {}
        for lang_name, module in [
            ("python", tspython), ("javascript", tsjs), ("typescript", tstypescript),
            ("tsx", tstypescript), ("go", tsgo), ("rust", tsrust), ("cpp", tscpp)
        ]:
            try:
                self.languages[lang_name] = self._get_lang(module, lang_name)
            except Exception as e:
                print(f"[*] Warning: Could not initialize {lang_name}: {e}")

    def _get_lang(self, module, name):
        # Standard tree-sitter 0.25 language getter
        if hasattr(module, "language"):
            return Language(module.language())
        # Fallback for older or variant bindings
        if hasattr(module, f"language_{name}"):
            return Language(getattr(module, f"language_{name}")())
        raise AttributeError(f"Binding for {name} does not export a language() getter.")

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
            
            if os.path.getsize(file_path) > self.MAX_FILE_SIZE:
                return {"file": file_path, "language": lang, "entities": [], "error": "File too large"}
            
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
                
                result = self._extract_entities(tree, lang, file_path)
                result["line_count"] = tree.root_node.end_point[0] + 1
                return result
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

        # Multi-Language SCM Queries
        queries = {
            "python": """
                (class_definition name: (identifier) @class.name)
                (function_definition name: (identifier) @function.name)
                (import_from_statement module_name: (dotted_name) @import.name)
                (import_statement name: (dotted_name) @import.name)
            """,
            "javascript": """
                (class_declaration name: (identifier) @class.name)
                (function_declaration name: (identifier) @function.name)
                (method_definition name: (property_identifier) @function.name)
                (import_statement source: (string) @import.name)
                (variable_declarator name: (identifier) @function.name value: (arrow_function))
                (variable_declarator name: (identifier) @function.name value: (function_expression))
            """,
            "typescript": """
                (class_declaration name: (type_identifier) @class.name)
                (function_declaration name: (identifier) @function.name)
                (method_definition name: (property_identifier) @function.name)
                (import_statement source: (string) @import.name)
                (interface_declaration name: (type_identifier) @class.name)
                (variable_declarator name: (identifier) @function.name value: (arrow_function))
            """,
            "tsx": """
                (class_declaration name: (type_identifier) @class.name)
                (function_declaration name: (identifier) @function.name)
                (method_definition name: (property_identifier) @function.name)
                (import_statement source: (string) @import.name)
                (interface_declaration name: (type_identifier) @class.name)
                (variable_declarator name: (identifier) @function.name value: (arrow_function))
            """,
            "go": """
                (type_spec name: (type_identifier) @class.name)
                (func_declaration name: (identifier) @function.name)
                (method_declaration name: (field_identifier) @function.name)
                (import_spec path: (string_literal) @import.name)
            """,
            "rust": """
                (struct_item name: (type_identifier) @class.name)
                (enum_item name: (type_identifier) @class.name)
                (function_item name: (identifier) @function.name)
                (use_declaration argument: (_) @import.name)
                (impl_item type: (type_identifier) @class.name)
                (trait_item name: (type_identifier) @class.name)
            """,
            "cpp": """
                (class_specifier name: (type_identifier) @class.name)
                (function_definition declarator: (function_declarator declarator: (identifier) @function.name))
                (preproc_include path: (string_literal) @import.name)
            """
        }

        query_scm = queries.get(lang)
        if not query_scm:
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
                node_type = "unknown"
                if "class" in tag: node_type = "class"
                elif "function" in tag: node_type = "function"
                elif "import" in tag: node_type = "import"

                entities.append({
                    "name": node.text.decode("utf-8") if isinstance(node.text, bytes) else node.text,
                    "type": node_type,
                    "path": file_path,
                    "line_start": node.start_point[0] + 1,
                    "line_end": node.end_point[0] + 1,
                })

        return {
            "file": file_path,
            "language": lang,
            "entities": entities
        }
