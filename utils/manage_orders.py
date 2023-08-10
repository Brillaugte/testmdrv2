

def manage_orders(exchange, symbols_and_quantities):
    open_positions = {}

    def handle_order(symbol, desired_qty):
        # Fetch order book
        orderbook = exchange.fetch_order_book(symbol)
        bids = orderbook['bids']
        asks = orderbook['asks']

        # Fetch historical trades and get the most recent trade's price
        historical_trades = exchange.fetch_trades(symbol, limit=1)
        last_filled_price = historical_trades[0]['price'] if historical_trades else None

        # Fetch current open orders for the symbol
        open_orders = exchange.fetch_open_orders(symbol)
        current_qty = sum(order['amount'] for order in open_orders if order['side'] == 'buy') - sum(order['amount'] for order in open_orders if order['side'] == 'sell')

        # Determine the quantity to buy or sell
        qty_to_trade = desired_qty - current_qty

        # If there's no need to trade, return
        if qty_to_trade == 0:
            return

        # Determine the price based on the bids or asks
        if qty_to_trade > 0:
            price = bids[0][0]  # Use the highest bid for a buy order
        else:
            if asks:
                price = asks[0][0]  # Use the lowest ask for a sell order
            else:
                # Fallback to using the bids or another method if asks are empty
                price = bids[-2][0]  # Example: use the second-to-last bid for a sell order

        # Cancel existing orders if they are out of the desired price range
        for order in open_orders:
            if (order['side'] == 'buy' and order['price'] < price) or (order['side'] == 'sell' and order['price'] > price):
                exchange.cancel_order(order['id'], symbol)

        # Create a limit order
        side = 'buy' if qty_to_trade > 0 else 'sell'
        exchange.create_limit_order(symbol, side, abs(qty_to_trade), price)

        # Update open positions
        open_positions[symbol] = {'desired_qty': desired_qty, 'last_filled_price': last_filled_price}

    # Handle each symbol and quantity
    for i in range(0, len(symbols_and_quantities), 2):
        handle_order(symbols_and_quantities[i], symbols_and_quantities[i + 1])

    return open_positions


#symbols_and_quantities = ['GRT/USDT:USDT', 50, 'KLAY/USDT:USDT', -30]
#open_positions = manage_orders(symbols_and_quantities)