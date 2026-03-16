import tree_sitter
import tree_sitter_python
from tree_sitter import Language

def debug_versions():
    try:
        capsule = tree_sitter_python.language()
        lang = Language(capsule)
        
        print(f"tree_sitter.LANGUAGE_VERSION: {tree_sitter.LANGUAGE_VERSION}")
        print(f"tree_sitter.MIN_COMPATIBLE_LANGUAGE_VERSION: {tree_sitter.MIN_COMPATIBLE_LANGUAGE_VERSION}")
        # pyo3 bindings Language object might have version?
        if hasattr(lang, "version"):
            print(f"Language version: {lang.version}")
            
    except Exception as e:
        print(f"CAUGHT ERROR: {e}")

if __name__ == "__main__":
    debug_versions()
