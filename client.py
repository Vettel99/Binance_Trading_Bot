from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .logging_config import logger

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str):
        # Initialize python-binance client with the testnet flag
        self.client = Client(api_key, api_secret, testnet=True)

    def place_order(self, params: dict) -> dict:
        logger.info(f"Preparing to send order via python-binance: {params}")
        
        try:
            # python-binance handles the base URL, timestamp, and HMAC signature automatically
            # We unpack the params dictionary directly into the method
            response = self.client.futures_create_order(**params)
            
            logger.info(f"API Response: {response}")
            return response
            
        except BinanceAPIException as e:
            # Catches exact Binance API rejections (like the -2015 error)
            logger.error(f"Binance API Exception: {e.status_code} - {e.message}")
            raise Exception(f"Binance API Error {e.status_code}: {e.message}")
            
        except BinanceRequestException as e:
            # Catches network-level timeouts or connection drops
            logger.error(f"Binance Request Exception: {e}")
            raise Exception(f"Network error: {e}")
            
        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            raise Exception(f"Unexpected error: {e}")