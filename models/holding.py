from dataclasses import dataclass


@dataclass
class Holding:
    symbol: str
    quantity: int
