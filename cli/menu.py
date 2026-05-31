from db.connection import get_connection, init_db
from cli.display import print_holdings, print_trades
from cli.prompts import (
    prompt_float,
    prompt_int,
    prompt_optional_float,
    prompt_text,
    prompt_trade_date,
)
from services.holdings_service import get_holdings
from services.trade_service import record_buy, record_sell


def _handle_buy() -> None:
    print("\n--- 新增買進 ---")
    symbol = prompt_text("股票代號")
    quantity = prompt_int("股數")
    price = prompt_float("單價")
    trade_date = prompt_trade_date()
    fee = prompt_optional_float("手續費")
    note = prompt_text("備註", required=False) or None

    try:
        trade = record_buy(symbol, quantity, price, trade_date, fee=fee, note=note)
    except ValueError as exc:
        print(f"\n新增失敗：{exc}\n")
        return

    print(f"\n買進成功：{trade.symbol} {trade.quantity} 股，單價 {trade.price}。\n")


def _handle_sell() -> None:
    print("\n--- 新增賣出 ---")
    symbol = prompt_text("股票代號")
    quantity = prompt_int("股數")
    price = prompt_float("單價")
    trade_date = prompt_trade_date()
    fee = prompt_optional_float("手續費")
    tax = prompt_optional_float("交易稅")
    note = prompt_text("備註", required=False) or None

    try:
        trade = record_sell(
            symbol, quantity, price, trade_date, fee=fee, tax=tax, note=note
        )
    except ValueError as exc:
        print(f"\n新增失敗：{exc}\n")
        return

    print(f"\n賣出成功：{trade.symbol} {trade.quantity} 股，單價 {trade.price}。\n")


def _handle_list_trades() -> None:
    init_db()
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, symbol, side, quantity, price, trade_date, fee, tax, note
            FROM trades
            ORDER BY trade_date, id
            """
        ).fetchall()

    print_trades(rows)


def _handle_list_holdings() -> None:
    print_holdings(get_holdings())


def run() -> None:
    init_db()

    actions = {
        "1": ("新增買進", _handle_buy),
        "2": ("新增賣出", _handle_sell),
        "3": ("查看所有交易紀錄", _handle_list_trades),
        "4": ("查看目前持股", _handle_list_holdings),
    }

    while True:
        print("=== 股票交易紀錄系統 ===")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print("0. 離開")

        choice = input("請選擇：").strip()

        if choice == "0":
            print("再見。")
            break

        action = actions.get(choice)
        if action is None:
            print("無效的選項，請重新輸入。\n")
            continue

        action[1]()
