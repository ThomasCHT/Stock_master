from dataclasses import dataclass


@dataclass
class RealizedPnL:
    symbol: str
    realized_pnl: float
