"""Services package."""
from .gemini_service import GeminiService
from .image_optimizer import ImageOptimizer
from .graph_generator import GraphGenerator

# For backward compatibility, no cost tracker needed (Gemini is free)
class CostTracker:
    async def track_cost(self, *args, **kwargs):
        pass  # Gemini is free!

cost_tracker = CostTracker()

__all__ = [
    "GeminiService",
    "ImageOptimizer",
    "GraphGenerator",
    "CostTracker",
    "cost_tracker",
]
