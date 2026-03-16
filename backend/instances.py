from backend.graph.manager import GraphManager
from backend.summarizer.engine import SummarizerEngine
from backend.parser.engine import ParserEngine

# Shared singleton instances
graph_manager = GraphManager()
summarizer = SummarizerEngine()
parser_engine = ParserEngine()
