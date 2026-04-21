from typing import Iterable, Any
import yaml
from pathlib import Path

def build_message(specification: Any):
    return [{"role": "system", "content": loadSysPrompt}]

def loadSysPrompt():
    path = Path(__file__).parent.parent.parent / "config" / "sys_prompt.yaml"
    with open(path, "r", encoding="utf-8") as f:
        #print(yaml.safe_load(f))
        return yaml.safe_load(f)
