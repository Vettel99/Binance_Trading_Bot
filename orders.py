from .client import BinanceFuturesClient

def execute_order(client: BinanceFuturesClient, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity
    }
    
    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC" # Good Till Canceled is required for limit orders
        
    return client.place_order(params)