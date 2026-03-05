import json
from pathlib import Path
from typing import List, Dict, Any

DEFAULT_PATH = Path("products.json")


def save_products_to_json(products: List[Dict[str, Any]], path: Path = DEFAULT_PATH) -> None:
    """Guarda una lista de dicts (productos) a JSON."""
    path.write_text(
        json.dumps(products, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def load_products_from_json(path: Path = DEFAULT_PATH) -> List[Dict[str, Any]]:
    """Carga una lista de dicts desde JSON. Si no existe, devuelve []."""
    if not path.exists():
        return []

    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        # Archivo corrupto o no legible -> arrancamos vacío
        return []