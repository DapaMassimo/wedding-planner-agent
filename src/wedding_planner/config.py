import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def _required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}."
            f"Set it into the .env file or shell!"
        )
    return value
    

# --- API keys ---
OPENAI_API_KEY = _required('OPENAI_API_KEY')
TAVILY_API_KEY = _required('TAVILY_API_KEY')

# --- Defaults ---
DEFAULT_MODEL = "o3-mini"
ROUTER_MODEL = "o3-mini"

# --- Default model params ---
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 1.0

# --- Paths ---
PACKAGE_ROOT = Path(__file__).parent
PROMPTS_DIR = PACKAGE_ROOT / "prompts"