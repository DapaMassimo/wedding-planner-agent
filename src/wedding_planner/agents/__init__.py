from .flight import FLIGHT_AGENT
from .venue import VENUE_AGENT
from .dj import DJ_AGENT
from .coordinator import COORDINATOR_AGENT
from .base import Agent


AGENTS = {
    FLIGHT_AGENT.name: FLIGHT_AGENT,
    VENUE_AGENT.name: VENUE_AGENT,
    DJ_AGENT.name: DJ_AGENT,
    COORDINATOR_AGENT.name: COORDINATOR_AGENT,
}

__all__ = [
    "Agent",
    "AGENTS",
    "FLIGHT_AGENT",
    "VENUE_AGENT",
    "DJ_AGENT",
    "COORDINATOR_AGENT",
]