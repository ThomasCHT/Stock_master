from collections import deque
from dataclasses import dataclass

from db.connection import get_connection, init_db
from models.realized_pnl import RealizedPnL
from models.trade import Trade


@dataclass
class _BuyLot:
    quantity: int
    unit_cost: float


def _fetch_trades_ordered() -> list[Trade]:
    init_db()
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM trades
            ORDER BY trade_date, id
            """
        ).fetchall()
    return [Trade.from_row(row) for row in rows]


def get_realized_pnl_by_symbol() -> list[RealizedPnL]:
    trades = _fetch_trades_ordered()

    lots_by_symbol: dict[str, deque[_BuyLot]] = {}
    realized_by_symbol: dict[str, float] = {}

    for trade in trades:
        symbol = trade.symbol
        lots_by_symbol.setdefault(symbol, deque())
        realized_by_symbol.setdefault(symbol, 0.0)

        if trade.side == "buy":
            total_cost = (trade.price * trade.quantity) + trade.fee + trade.tax
            unit_cost = total_cost / trade.quantity
            lots_by_symbol[symbol].append(_BuyLot(quantity=trade.quantity, unit_cost=unit_cost))
            continue

        remaining_sell_qty = trade.quantity
        sell_total_proceeds = (trade.price * trade.quantity) - trade.fee - trade.tax
        sell_unit_proceeds = sell_total_proceeds / trade.quantity

        matched_cost = 0.0
        lots = lots_by_symbol[symbol]
        while remaining_sell_qty > 0 and lots:
            buy_lot = lots[0]
            matched_qty = min(remaining_sell_qty, buy_lot.quantity)
            matched_cost += matched_qty * buy_lot.unit_cost

            buy_lot.quantity -= matched_qty
            remaining_sell_qty -= matched_qty
            if buy_lot.quantity == 0:
                lots.popleft()

        matched_proceeds = (trade.quantity - remaining_sell_qty) * sell_unit_proceeds
        realized_by_symbol[symbol] += matched_proceeds - matched_cost

    results = [
        RealizedPnL(symbol=symbol, realized_pnl=realized_pnl)
        for symbol, realized_pnl in sorted(realized_by_symbol.items())
        if abs(realized_pnl) > 1e-12
    ]
    return results
