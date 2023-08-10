from flask import Flask, request, jsonify
import threading
import asyncio
from utils.manage_orders import *

app = Flask(__name__)

# Global variable to control the loop
running = False

# Function to run the loop
def run_loop():
    global running
    running = True
    while running:
        # Call the manage_orders function
        symbols_and_quantities = [] 
        manage_orders(symbols_and_quantities)

        # Call the process_quotes function
        quotes = [{'symbol': 'BTC/USDT', 'quantity': 5, 'price': 40000}, {'symbol': 'ETH/USDT', 'quantity': -3, 'price': 2500}] # Example input
        accepted, rejected = asyncio.run(process_quotes(quotes))
        print("Accepted quotes:", accepted)
        print("Rejected quotes:", rejected)

        # Sleep for a while before the next iteration
        asyncio.sleep(5)

# Endpoint to start the loop
@app.route('/start', methods=['POST'])
def start():
    global running
    if not running:
        thread = threading.Thread(target=run_loop)
        thread.start()
        return jsonify(status='started')
    else:
        return jsonify(status='already running')

# Endpoint to stop the loop
@app.route('/stop', methods=['POST'])
def stop():
    global running
    running = False
    return jsonify(status='stopped')

if __name__ == '__main__':
    app.run(port=5000)
