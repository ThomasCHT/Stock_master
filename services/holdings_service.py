from db.connection import get_connection, init_db
from models.holding import Holding


def get_holdings() -> list[Holding]:
    init_db()

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT symbol,
                   SUM(CASE WHEN side = 'buy' THEN quantity ELSE -quantity END) AS quantity
            FROM trades
            GROUP BY symbol
            HAVING SUM(CASE WHEN side = 'buy' THEN quantity ELSE -quantity END) != 0
            ORDER BY symbol
            """
        ).fetchall()

    return [Holding(symbol=row["symbol"], quantity=int(row["quantity"])) for row in rows]
