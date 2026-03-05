import json
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_PATH = Path("products.json")


def save_products_to_json(products: List[Dict[str, Any]], path: Path = DEFAULT_PATH) -> None:
    path.write_text(
        json.dumps(products, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def load_products_from_json(path: Path = DEFAULT_PATH) -> List[Dict[str, Any]]:
    if not path.exists():
        return []

    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []