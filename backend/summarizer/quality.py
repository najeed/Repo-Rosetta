from typing import List, Set
import re

class QualityScorer:
    """
    Analyzes generated summaries for uniqueness, density, and semantic value.
    """
    @staticmethod
    def calculate_score(summary: str, previous_summaries: List[str], symbols: List[str], is_heuristic: bool = False) -> int:
        if not summary: return 0
        
        # 0. Heuristic Penalty (CRITICAL)
        # If explicitly marked or detects base template "rationales"
        template_boilerplate = [
            "contributes to the overall system coherence",
            "standard structural wrapper",
            "facilitates system interactions",
            "supports feature stability",
            "traffic router",
            "performs discrete operations",
            "serves as a traffic router",
            "central orchestrator",
            "defines the data contract",
            "bridges external requests",
            "discrete operations",
            "outside the main service loop"
        ]
        
        is_detected_heuristic = is_heuristic or any(b in summary.lower() for b in template_boilerplate)
        
        # 1. Uniqueness (40%)
        uniqueness_score = 100
        words = set(re.findall(r'\w+', summary.lower()))
        for prev in previous_summaries:
            prev_words = set(re.findall(r'\w+', prev.lower()))
            overlap = words.intersection(prev_words)
            if len(words) > 0:
                similarity = len(overlap) / len(words)
                if similarity > 0.7:
                    uniqueness_score -= 60
        
        # 2. Information Density (30%)
        density_score = 0
        if symbols:
            found_symbols = [s for s in symbols if s.lower() in summary.lower()]
            density_score = min(100, (len(found_symbols) / max(1, len(symbols))) * 200)
        
        # 3. Contextual Richness (30%)
        richness_score = 0
        # If it's a heuristic, we cap the richness score at 10 regardless of content
        if is_detected_heuristic:
            richness_score = 5
            uniqueness_score = min(uniqueness_score, 20)
        else:
            keywords = ["dependency", "encapsulate", "interface", "governs", "logic", "module", "relation"]
            found_keywords = [k for k in keywords if k in summary.lower()]
            richness_score = (len(found_keywords) / len(keywords)) * 100

        final_score = (uniqueness_score * 0.4) + (density_score * 0.3) + (richness_score * 0.3)
        
        # Final cap for heuristics
        if is_detected_heuristic:
            return int(min(30, max(0, final_score)))
            
        return int(min(100, max(0, final_score)))

    @staticmethod
    def get_critique(score: int) -> str:
        if score < 40: return "Low Fidelity (Repetitive/Generic)"
        if score < 70: return "Functional (Template-heavy)"
        return "High Fidelity (Contextual)"
