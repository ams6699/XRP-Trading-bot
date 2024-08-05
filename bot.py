from pybit.unified_trading import HTTP
from config import API_KEY, API_SECRET, SYMBOL, TARGET_PRICE, QTY, TIME_CHECK
import time

# Initialize Bybit client with unified trading endpoint
client = HTTP(api_key=API_KEY, api_secret=API_SECRET)

def get_xrp_price():
    try:
        response = client.get_tickers(symbol=SYMBOL, category='spot')
        if response['retCode'] == 0 and 'list' in response['result']:
            return float(response['result']['list'][0]['lastPrice'])
        else:
            print("Error or no data returned.")
            return None
    except Exception as e:
        print(f"Error getting XRP price: {e}")
        return None

def get_wallet_balance():
    try:
        response = client.get_wallet_balance(accountType='UNIFIED')
        if response['retCode'] == 0:
            print(response['result']['list'][0]['totalMarginBalance'])
            return response['result']['list'][0]['totalMarginBalance']
        else:
            print(f"Error getting wallet balance: {response['retMsg']} (ErrCode: {response['retCode']})")
            return None
    except Exception as e:
        print(f"Error getting wallet balance: {e}")
        return None

def header():
    print("\n")
    print("="*50)
    print("          Welcome To Simpsons XRP Bot")
    print("="*50)
    print("\n")
    

def place_order(Price,Qty):
    try:
        Price=str(Price)
        order_params = {
            'category': 'spot',
            'symbol': 'XRPUSDT',
            'side': 'Sell',
            'orderType': 'Market',
            'qty': str(Qty),
        }
        # Place the order with the API
        response = client.place_order(**order_params)
        
        return response
    except Exception as e:
        print(f"Error placing order: {e}")
        return None

def trading_bot(target_price):
    header()
    while True:
        try:
            current_price = get_xrp_price()
            if current_price is None:
                print("Failed to get current price, retrying...")
                time.sleep(TIME_CHECK)
                continue
            print(f'Current {SYMBOL} price: {current_price}')
            if current_price >= target_price:
                print(f'Price condition satisfied')
                print(f'Placing sell order at: {current_price}')
                order_response = place_order(current_price, QTY)
                if order_response is None:
                    print("Failed to place order, retrying...")
                    time.sleep(TIME_CHECK)
                    continue
                print(order_response)
                print("Successfull!")
                break
            time.sleep(TIME_CHECK)  # wait for 60 seconds before checking the price again
        except Exception as e:
            print(f'An unexpected error occurred: {e}')
            time.sleep(TIME_CHECK)

# Start the bot
# get_wallet_balance()
trading_bot(TARGET_PRICE)
