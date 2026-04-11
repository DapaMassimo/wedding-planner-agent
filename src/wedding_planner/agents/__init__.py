from .travel import TRAVEL_AGENT
from .venue import VENUE_AGENT
from .dj import DJ_AGENT
from .coordinator import COORDINATOR_AGENT
from .base import Agent


AGENTS = {
    TRAVEL_AGENT.name: TRAVEL_AGENT,
    VENUE_AGENT.name: VENUE_AGENT,
    DJ_AGENT.name: DJ_AGENT,
    COORDINATOR_AGENT.name: COORDINATOR_AGENT
}

__all__ = [
    "Agent",
    "AGENTS",
    "TRAVEL_AGENT", 
    "VENUE_AGENT", 
    "DJ_AGENT", 
    "COORDINATOR_AGENT"
]