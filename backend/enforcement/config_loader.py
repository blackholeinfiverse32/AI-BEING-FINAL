import yaml
from pathlib import Path
import os

# Use absolute path relative to this file
CURRENT_DIR = Path(__file__).parent
CONFIG_DIR = CURRENT_DIR / "config"

def load_yaml(name: str):
    path = CONFIG_DIR / name
    if not path.exists():
        # Return safe defaults if config missing
        if name == "enforcement.yaml":
            return {"kill_switch": False, "strict_mode": True}
        elif name == "runtime.yaml":
            return {"environment": "production", "debug": False}
        raise FileNotFoundError(f"Missing config: {name}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

ENFORCEMENT_CONFIG = load_yaml("enforcement.yaml")
RUNTIME_CONFIG = load_yaml("runtime.yaml")
