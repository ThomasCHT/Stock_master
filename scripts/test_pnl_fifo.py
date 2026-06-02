from pathlib import Path
from tempfile import TemporaryDirectory
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import db.connection as db_connection
from services.pnl_service import get_realized_pnl_by_symbol
from services.trade_service import record_buy, record_sell


def main() -> None:
    original_db_path = db_connection.DB_PATH
    original_data_dir = db_connection.DATA_DIR

    with TemporaryDirectory() as tmpdir:
        temp_data_dir = Path(tmpdir)
        temp_db_path = temp_data_dir / "test_stock.db"

        db_connection.DATA_DIR = temp_data_dir
        db_connection.DB_PATH = temp_db_path

        try:
            print("=== FIFO Realized PnL Test (Temporary DB) ===")
            print("測試交易：")
            print("- 買 100 股 @ 10")
            print("- 買 100 股 @ 12")
            print("- 賣 150 股 @ 15")
            print()

            # FIFO check: (100@10 + 100@12), sell 150@15 => 650
            record_buy("TST1", 100, 10.0, "2026-06-01")
            record_buy("TST1", 100, 12.0, "2026-06-02")
            record_sell("TST1", 150, 15.0, "2026-06-03")

            results = {item.symbol: item.realized_pnl for item in get_realized_pnl_by_symbol()}
            expected = 650.0
            actual = results.get("TST1")

            print("FIFO 計算過程：")
            part1 = (15.0 - 10.0) * 100
            part2 = (15.0 - 12.0) * 50
            total = part1 + part2
            print(f"- 前 100 股成本 10，損益 = (15 - 10) * 100 = {part1:.0f}")
            print(f"- 後 50 股成本 12，損益 = (15 - 12) * 50 = {part2:.0f}")
            print(f"- 總已實現損益 = {total:.0f}")
            print()
            print(f"服務計算結果（TST1）= {actual:.0f}" if actual is not None else "服務計算結果（TST1）= N/A")

            if actual is None:
                raise AssertionError("TST1 result not found")
            if abs(actual - expected) > 1e-9:
                raise AssertionError(f"FIFO realized PnL mismatch: expected {expected}, got {actual}")
        finally:
            db_connection.DB_PATH = original_db_path
            db_connection.DATA_DIR = original_data_dir

    print("PASS: FIFO realized PnL test passed with temporary DB.")


if __name__ == "__main__":
    main()
