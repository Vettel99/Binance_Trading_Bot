
# Binance Futures Testnet Trading Bot

A Python 3.x application designed to place orders on the Binance Futures Testnet (USDT-M). This project features a modular architecture with a clear separation between the API client layer and the CLI layer. It supports both Market and Limit orders for Buy and Sell sides with integrated logging and input validation.

## Setup Steps

Follow these instructions to configure and run the bot locally:

1.  **Clone the Repository**
    
    Bash
    
    ```
    git clone <repository-url>
    cd trading_bot
    ```
    
2.  **Create a Virtual Environment**
    
    Bash
    
    ```
    python -m venv venv
    # Activate on Windows:
    venv\Scripts\activate
    # Activate on macOS/Linux:
    source venv/bin/activate
    ```
    
3.  **Install Dependencies** The project requires `python-binance`, `rich`, and `python-dotenv`.
    
    Bash
    
    ```
    pip install -r requirements.txt
    ```
    
4.  **Configure Environment Variables** Create a `.env` file in the root directory and add your Binance Futures Testnet credentials:
    
    Code snippet
    
    ```
    BINANCE_API_KEY=your_testnet_api_key
    BINANCE_API_SECRET=your_testnet_api_secret
    ```
    

----------

## How to Run (Examples)

The bot accepts user input via CLI arguments or an interactive prompt system.

### 1. Market Order Example

To place a MARKET BUY order for a specific quantity:

Bash

```
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.002

```

### 2. Limit Order Example

To place a LIMIT SELL order, you must provide a price:

Bash

```
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.001 --price 95000.00

```

### 3. Interactive Mode (Enhanced CLI UX)

If arguments are omitted, the bot launches an interactive menu for user input:

Bash

```
python cli.py

```

----------

## Assumptions

The following assumptions were made during development:

-   **Testnet Environment**: The application is hardcoded to use the Binance Futures Testnet base URL: `https://testnet.binancefuture.com`.
    
-   **Asset Margin**: It is assumed the Testnet account has a sufficient USDT balance to meet margin requirements for the requested trades.
    
-   **Time in Force**: For all LIMIT orders, the `TimeInForce` is set to `GTC` (Good Till Cancelled) by default to ensure successful placement.
    
-   **Precision Handling**: The bot rounds quantities to 3 decimal places to comply with standard Binance contract filters and prevent API rejection.
    

----------

## Project Structure

The project follows a modular structure for maintainability and reuse:

-   `cli.py`: The entry point for command-line interaction and input parsing.
    
-   `bot/client.py`: A wrapper for the Binance API client using `python-binance`.
    
-   `bot/orders.py`: Contains the logic for constructing and executing order requests.
    
-   `bot/validators.py`: Handles validation for symbols, sides, order types, and numerical inputs.
    
-   `bot/logging_config.py`: Configures structured logging of requests, responses, and errors to `trading_bot.log`.
    

----------

## Logging

All API interactions are logged to `trading_bot.log`. This includes:

-   **Full Request Summary**: Symbol, side, type, and quantity.
    
-   **Full API Response**: Order ID, status, executed quantity, and average price.
    
-   **Error Details**: Specific Binance API exceptions and network failures.
    

----------
