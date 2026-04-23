import json
from pathlib import Path
from typing import Iterable
import pandas as pd


def readJsonl(path: str | Path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    return rows
                            

def writeJsonl(path: str | Path, rows: Iterable[dict], mode: str ="w"):
    p = parentIsThere(path)
    with open(p, mode, encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def createParquet(path: str | Path, rows: list[dict]):
    p = parentIsThere(path)
    df = pd.DataFrame(rows)
    df.to_parquet(p, index=False)



def appendJsonl(path: str | Path, row: dict):
    writeJsonl(path, [row], mode="a")
    

def parentIsThere(path:str | Path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p