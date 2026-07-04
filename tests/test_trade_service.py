from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import db.connection as db_connection
from services.holdings_service import get_holdings
from services.trade_service import record_buy, record_sell


class TradeServiceTest(unittest.TestCase):
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

    def test_record_sell_rejects_oversold_quantity(self) -> None:
        record_buy("TST1", 100, 10.0, "2026-06-01")

        with self.assertRaisesRegex(ValueError, "not enough holdings"):
            record_sell("TST1", 101, 12.0, "2026-06-02")

        holdings = {item.symbol: item.quantity for item in get_holdings()}
        self.assertEqual(holdings["TST1"], 100)

    def test_record_sell_allows_available_quantity(self) -> None:
        record_buy("TST2", 100, 10.0, "2026-06-01")

        trade = record_sell("TST2", 40, 12.0, "2026-06-02")

        self.assertEqual(trade.symbol, "TST2")
        self.assertEqual(trade.side, "sell")
        holdings = {item.symbol: item.quantity for item in get_holdings()}
        self.assertEqual(holdings["TST2"], 60)


if __name__ == "__main__":
    unittest.main()
