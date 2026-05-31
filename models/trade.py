from dataclasses import dataclass
from typing import Optional


@dataclass
class Trade:
    symbol: str
    side: str
    quantity: int
    price: float
    trade_date: str
    id: Optional[int] = None
    fee: float = 0.0
    tax: float = 0.0
    note: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "Trade":
        return cls(
            id=row["id"],
            symbol=row["symbol"],
            side=row["side"],
            quantity=row["quantity"],
            price=row["price"],
            fee=row["fee"],
            tax=row["tax"],
            trade_date=row["trade_date"],
            note=row["note"],
            created_at=row["created_at"],
        )
