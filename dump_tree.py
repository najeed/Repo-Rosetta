import tree_sitter
import tree_sitter_python
from tree_sitter import Language, Parser

def dump_tree(node, level=0):
    indent = "  " * level
    print(f"{indent}{node.type} ({node.start_point}-{node.end_point})")
    for child in node.children:
        dump_tree(child, level + 1)

def main():
    capsule = tree_sitter_python.language()
    lang = Language(capsule)
    parser = Parser(lang)
    
    with open("backend/main.py", "rb") as f:
        code = f.read()
    
    tree = parser.parse(code)
    print("TREE DUMP:")
    dump_tree(tree.root_node)

if __name__ == "__main__":
    main()
