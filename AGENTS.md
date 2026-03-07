# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Retail management system (sistema de gestión para comercios) for a clothing store. It is a CLI menu-driven application written in Python 3.14 with **zero external dependencies** (stdlib only). The UI is in Spanish; code and docstrings are a mix of English and Spanish.

## Running the Application

```
python main.py
```

This launches an interactive menu loop. Product data is loaded from `products.json` at startup and saved back on clean exit (option "0").

## Build & Dependencies

There is no `requirements.txt`, `pyproject.toml`, or virtual environment setup. The project uses only the Python standard library. No build step is needed.

## Tests & Linting

No test framework or linter is currently configured. There are no existing tests.

## Architecture

The codebase follows a two-layer pattern:

**Presentation layer** — `cli_handlers.py` owns all user-facing I/O (menus, input prompts, print output). Every module menu follows the same pattern: a `show_*_menu()` display function paired with a `handle_*_menu()` loop function.

**Domain layer** — Plain Python classes (no dataclasses/Pydantic) that hold business state in-memory:

- `Inventory` (`inventory.py`) is the central aggregate. It holds a `products: dict[int, Product]` keyed by product ID, and a `transfers: list[Transfer]` log. Most operations flow through it.
- `Product` (`product.py`) is the richest model — supports `to_dict()` / `from_dict()` for JSON round-tripping. Has many optional retail-specific fields (brand_code, season, liquidation, sizes, etc.).
- `Sales` (`sale.py`) records sale objects; `SalesAnalysis` (`sales_analysis.py`) independently tracks product-name/quantity pairs for analytics. Both must be updated when recording a sale (see `handle_register_sale` in `cli_handlers.py`).
- `Pettycash` (`petty_cash.py`) manages cash register balance and a list of `Transaction` objects.
- `Transfer` (`transfer.py`) is a simple value object for stock movements between locations.

**Persistence** — `data_managment.py` reads/writes `products.json`. Only product data is persisted; sales, petty cash, and transfers are in-memory only and reset on restart.

**Not yet integrated into the main flow:** `Employee` (`employee.py`), `Supllier` (`supplier.py`, note the typo in the class name), `PaymentMethod` (`paymethod.py`). These models exist but are not wired into menus or persistence.

## Key Patterns & Gotchas

- **Dual sales tracking**: When recording a sale, you must update both `Sales.record_sale()` (full sale object) and `SalesAnalysis.record_sale()` (name + quantity only), plus call `product.remove_stock()`. These three steps are manually coordinated in `cli_handlers.py`, not encapsulated in a single method.
- **Serialization**: Only `Product` has `to_dict()`/`from_dict()`. If adding persistence for other entities, follow the same pattern.
- **ID assignment**: Product IDs are user-supplied via input. Sale IDs are auto-incremented from `len(sales.sales_data) + 1`.
- **The `seed()` function** in `main.py` is a placeholder (currently `pass`) intended for loading test/demo data.
- **Class name typo**: `Supllier` in `supplier.py` — preserve this unless intentionally refactoring.
- **`products.json`** is committed to the repo and contains sample product data.
