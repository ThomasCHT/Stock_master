from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import db.connection as db_connection
from services.pnl_service import get_realized_pnl_by_symbol
from services.trade_service import record_buy, record_sell


class RealizedPnLServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self._original_data_dir = db_connection.DATA_DIR
        self._original_db_path = db_connection.DB_PATH

        temp_data_dir = Path(self._tmpdir.name)
        db_connection.DATA_DIR = temp_data_dir
        db_connection.DB_PATH = temp_data_dir / "test_stock.db"

    def tearDown(self) -> None:
        db_connection.DATA_DIR = self._original_data_dir
        db_connection.DB_PATH = self._original_db_path
        self._tmpdir.cleanup()

    def test_fifo_realized_pnl_uses_oldest_buy_lots_first(self) -> None:
        record_buy("TST1", 100, 10.0, "2026-06-01")
        record_buy("TST1", 100, 12.0, "2026-06-02")
        record_sell("TST1", 150, 15.0, "2026-06-03")

        results = {
            item.symbol: item.realized_pnl
            for item in get_realized_pnl_by_symbol()
        }

        self.assertAlmostEqual(results["TST1"], 650.0)

    def test_realized_pnl_includes_buy_fee_and_sell_fee_tax(self) -> None:
        record_buy("TST2", 100, 10.0, "2026-06-01", fee=20.0)
        record_sell("TST2", 100, 12.0, "2026-06-02", fee=10.0, tax=5.0)

        results = {
            item.symbol: item.realized_pnl
            for item in get_realized_pnl_by_symbol()
        }

        self.assertAlmostEqual(results["TST2"], 165.0)


if __name__ == "__main__":
    unittest.main()
