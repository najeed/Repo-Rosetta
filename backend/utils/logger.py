import os
import time
import logging
from typing import Optional

class RosettaLogger:
    """Centralized logging utility for Repo Rosetta."""
    
    _initialized = False
    
    @classmethod
    def setup(cls):
        if cls._initialized:
            return
            
        debug_mode = os.getenv("ROSETTA_DEBUG", "false").lower() == "true"
        log_level = logging.DEBUG if debug_mode else logging.INFO
        
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S"
        )
        cls._initialized = True
        
    @staticmethod
    def log_trace(component: str, message: str, provider: Optional[str] = None, model: Optional[str] = None, latency: Optional[float] = None):
        """Standardized trace logging for LLM and internal operations."""
        RosettaLogger.setup()
        logger = logging.getLogger(component)
        
        trace_parts = [message]
        if provider: trace_parts.append(f"Provider={provider}")
        if model: trace_parts.append(f"Model={model}")
        if latency is not None: trace_parts.append(f"Latency={latency:.2f}s")
        
        logger.debug(" | ".join(trace_parts))
        
    @staticmethod
    def debug(component: str, message: str):
        RosettaLogger.setup()
        logging.getLogger(component).debug(message)

    @staticmethod
    def info(component: str, message: str):
        RosettaLogger.setup()
        logging.getLogger(component).info(message)

    @staticmethod
    def warning(component: str, message: str):
        RosettaLogger.setup()
        logging.getLogger(component).warning(message)

    @staticmethod
    def error(component: str, message: str):
        RosettaLogger.setup()
        logging.getLogger(component).error(message)

# Global Instance
logger = RosettaLogger
