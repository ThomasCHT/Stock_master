import re
from typing import Optional

from db.connection import get_connection, init_db
from models.trade import Trade

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _normalize_symbol(symbol: str) -> str:
    normalized = symbol.strip().upper()
    if not normalized:
        raise ValueError("symbol must not be empty")
    return normalized


def _validate_trade_inputs(
    symbol: str,
    quantity: int,
    price: float,
    trade_date: str,
    fee: float,
    tax: float,
) -> str:
    normalized_symbol = _normalize_symbol(symbol)

    if quantity <= 0:
        raise ValueError("quantity must be greater than 0")
    if price <= 0:
        raise ValueError("price must be greater than 0")
    if fee < 0:
        raise ValueError("fee must not be negative")
    if tax < 0:
        raise ValueError("tax must not be negative")
    if not DATE_PATTERN.match(trade_date):
        raise ValueError("trade_date must be in YYYY-MM-DD format")

    return normalized_symbol


def _insert_trade(
    symbol: str,
    side: str,
    quantity: int,
    price: float,
    trade_date: str,
    fee: float,
    tax: float,
    note: Optional[str],
) -> Trade:
    init_db()

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO trades (symbol, side, quantity, price, fee, tax, trade_date, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (symbol, side, quantity, price, fee, tax, trade_date, note),
        )
        conn.commit()
        trade_id = cursor.lastrowid

        row = conn.execute("SELECT * FROM trades WHERE id = ?", (trade_id,)).fetchone()

    return Trade.from_row(row)


def _get_current_quantity(symbol: str) -> int:
    init_db()

    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT COALESCE(
                SUM(CASE WHEN side = 'buy' THEN quantity ELSE -quantity END),
                0
            ) AS quantity
            FROM trades
            WHERE symbol = ?
            """,
            (symbol,),
        ).fetchone()

    return int(row["quantity"])


def record_buy(
    symbol: str,
    quantity: int,
    price: float,
    trade_date: str,
    fee: float = 0.0,
    tax: float = 0.0,
    note: Optional[str] = None,
) -> Trade:
    normalized_symbol = _validate_trade_inputs(
        symbol, quantity, price, trade_date, fee, tax
    )
    return _insert_trade(
        normalized_symbol, "buy", quantity, price, trade_date, fee, tax, note
    )


def record_sell(
    symbol: str,
    quantity: int,
    price: float,
    trade_date: str,
    fee: float = 0.0,
    tax: float = 0.0,
    note: Optional[str] = None,
) -> Trade:
    normalized_symbol = _validate_trade_inputs(
        symbol, quantity, price, trade_date, fee, tax
    )

    current_quantity = _get_current_quantity(normalized_symbol)
    if quantity > current_quantity:
        raise ValueError(
            f"not enough holdings for {normalized_symbol}: "
            f"available {current_quantity}, requested {quantity}"
        )

    return _insert_trade(
        normalized_symbol, "sell", quantity, price, trade_date, fee, tax, note
    )
