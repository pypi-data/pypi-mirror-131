from odin_messages.base import BaseEventMessage

class NewOpenOrderMessage(BaseEventMessage):
    exchange: str
    order_id: str
    market_code: str
    amount: int
    type: str
    selling: str
    status: str


class CanceledOrderMessage(BaseEventMessage):
    exchange: str
    order_id: str
    status: str
    market_code: str
    type: str
    selling: str


class OrderFilledMessage(BaseEventMessage):
    exchange: str
    order_id: str
    status: str
    market_code: str
    type: str
    selling: str
    amount: float
    filled: float
    remaining: float


class WalletBalanceUpdate(BaseEventMessage):
    exchange: str
    currency_code: str
    balance: float
    used_balance: float

