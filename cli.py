import os
import argparse
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from bot.client import BinanceFuturesClient
from bot.orders import execute_order
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.logging_config import logger

console = Console()

def print_summary(symbol, side, order_type, quantity, price):
    # Print clear order request summary
    table = Table(title="Order Request Summary", show_header=True, header_style="bold magenta")
    table.add_column("Symbol")
    table.add_column("Side")
    table.add_column("Type")
    table.add_column("Quantity")
    if order_type == "LIMIT":
        table.add_column("Price")
        table.add_row(symbol, side, order_type, str(quantity), str(price))
    else:
        table.add_row(symbol, side, order_type, str(quantity))
    console.print(table)

def main():
    # Force dotenv to override any cached environment variables with your .env file
    load_dotenv(override=True)
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        console.print("[bold red]Error:[/] API credentials not found in .env file.")
        return

    console.print(Panel.fit("Binance Futures Testnet Trading Bot", style="bold blue"))

    parser = argparse.ArgumentParser(description="Place orders on Binance Futures Testnet")
    parser.add_argument("--symbol", type=str, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, help="BUY or SELL")
    parser.add_argument("--type", type=str, help="MARKET or LIMIT")
    parser.add_argument("--qty", type=str, help="Quantity to trade")
    parser.add_argument("--price", type=str, help="Price (Required for LIMIT orders)")

    args = parser.parse_args()

    # Enhanced CLI UX: Interactive Prompts if arguments are missing
    try:
        symbol = validate_symbol(args.symbol or Prompt.ask("Enter Symbol", default="BTCUSDT"))
        side = validate_side(args.side or Prompt.ask("Enter Side", choices=["BUY", "SELL"]))
        order_type = validate_order_type(args.type or Prompt.ask("Enter Order Type", choices=["MARKET", "LIMIT"]))
        quantity = validate_quantity(args.qty or Prompt.ask("Enter Quantity"))
        
        price = 0.0
        if order_type == "LIMIT":
            price = validate_price(args.price or Prompt.ask("Enter Limit Price"), order_type)
            
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/] {e}")
        logger.warning(f"Validation Error: {e}")
        return

    print_summary(symbol, side, order_type, quantity, price)

    client = BinanceFuturesClient(api_key, api_secret)
    
    try:
        with console.status("[bold green]Placing order on Binance Testnet...[/]"):
            response = execute_order(client, symbol, side, order_type, quantity, price)
        
        # Print clear output: success message and order response details
        console.print("[bold green]✔ Order Executed Successfully![/]")
        
        res_table = Table(title="Order Response Details", show_header=True, header_style="bold green")
        res_table.add_column("Order ID")
        res_table.add_column("Status")
        res_table.add_column("Executed Qty")
        res_table.add_column("Avg Price")
        
        res_table.add_row(
            str(response.get("orderId", "N/A")),
            str(response.get("status", "N/A")),
            str(response.get("executedQty", "N/A")),
            str(response.get("avgPrice", "N/A"))
        )
        console.print(res_table)

    except Exception as e:
        console.print(f"[bold red]❌ Order Failed:[/] {e}")

if __name__ == "__main__":
    main()