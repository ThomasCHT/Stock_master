from typing import Iterable, Optional

from models.holding import Holding


def _format_note(note: Optional[str]) -> str:
    return note or ""


def print_trades(rows: Iterable) -> None:
    rows = list(rows)
    if not rows:
        print("\n目前沒有交易紀錄。\n")
        return

    headers = ("ID", "代號", "方向", "股數", "單價", "日期", "手續費", "交易稅", "備註")
    side_labels = {"buy": "買", "sell": "賣"}

    table_rows = []
    for row in rows:
        table_rows.append(
            (
                str(row["id"]),
                row["symbol"],
                side_labels.get(row["side"], row["side"]),
                str(row["quantity"]),
                str(row["price"]),
                row["trade_date"],
                str(row["fee"]),
                str(row["tax"]),
                _format_note(row["note"]),
            )
        )

    widths = [
        max(len(headers[i]), *(len(r[i]) for r in table_rows))
        for i in range(len(headers))
    ]

    def format_row(cells):
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells))

    print()
    print(format_row(headers))
    print(format_row(["-" * w for w in widths]))
    for row in table_rows:
        print(format_row(row))
    print()


def print_holdings(holdings: list[Holding]) -> None:
    if not holdings:
        print("\n目前沒有持股。\n")
        return

    headers = ("代號", "持有股數", "狀態")
    table_rows = []
    for holding in holdings:
        status = "異常（超賣）" if holding.quantity < 0 else ""
        table_rows.append((holding.symbol, str(holding.quantity), status))

    widths = [
        max(len(headers[i]), *(len(r[i]) for r in table_rows))
        for i in range(len(headers))
    ]

    def format_row(cells):
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells))

    print()
    print(format_row(headers))
    print(format_row(["-" * w for w in widths]))
    for row in table_rows:
        print(format_row(row))
    print()
