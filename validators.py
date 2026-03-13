def validate_symbol(symbol: str) -> str:
    if not symbol or len(symbol) < 3:
        raise ValueError("Symbol must be a valid string (e.g., BTCUSDT).")
    return symbol.upper()

def validate_side(side: str) -> str:
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be either BUY or SELL.")
    return side

def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper()
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be MARKET or LIMIT.")
    return order_type

def validate_quantity(quantity: str) -> float:
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError()
        # Common Binance precision fix: truncate to 3 decimals for typical pairs
        return round(qty, 3)
    except ValueError:
        raise ValueError("Quantity must be a positive number.")

def validate_price(price: str, order_type: str) -> float:
    if order_type.upper() == "MARKET":
        return 0.0
    try:
        p = float(price)
        if p <= 0:
            raise ValueError()
        # Round price to 2 decimals for typical USDT pairs
        return round(p, 2)
    except ValueError:
        raise ValueError("Price is required and must be a positive number for LIMIT orders.")