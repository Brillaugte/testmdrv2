from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import os
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

rfqs = {}
quotes = {}
active_rfqs = set()


@app.route('/send_rfq', methods=['POST'])
def send_rfq():
  rfq_data = request.json
  rfq_id = f"{time.time()}_{rfq_data['address']}"
  rfqs[rfq_id] = rfq_data
  quotes[rfq_id] = []
  active_rfqs.add(rfq_id)
  socketio.emit('new_rfq', {
    'rfq_id': rfq_id,
    'rfq_data': rfq_data
  },
                broadcast=True)
  return jsonify({"rfq_id": rfq_id})


@app.route('/delete_rfq/<rfq_id>', methods=['DELETE'])
def delete_rfq(rfq_id):
  if rfq_id in rfqs:
    del rfqs[rfq_id]
    del quotes[rfq_id]
    active_rfqs.remove(rfq_id)
    socketio.emit('remove_rfq', {'rfq_id': rfq_id}, broadcast=True)
    return jsonify({"status": "deleted"})
  else:
    return jsonify({"status": "not_found"}), 404


@socketio.on('send_quote')
def handle_send_quote(json):
  rfq_id = json.get('rfq_id')
  quote_data = json.get('quote_data')
  if rfq_id in rfqs:
    quotes[rfq_id].append(quote_data)
    socketio.emit('new_quote', {
      'rfq_id': rfq_id,
      'quote_data': quote_data
    },
                  broadcast=True)


@app.route('/get_best_quote/<rfq_id>', methods=['GET'])
def get_best_quote(rfq_id):
  if rfq_id in quotes:
    if len(quotes[rfq_id]) == 0:
      return jsonify({"status": "no_quotes"})
    best_quote = max(quotes[rfq_id], key=lambda x: x['qty_at_price'])
    return jsonify({"best_quote": best_quote})
  else:
    return jsonify({"status": "rfq_not_found"}), 404


if __name__ == '__main__':
  port = int(os.environ.get("PORT", 8080))
  socketio.run(app, host='0.0.0.0', port=port)
  
'''
Goal is to make a RFQ system where there is multieple frontends and multiple liquidity provider, frontend user sends a rfq, and liquidity provider answer the rfq to the api, and frontend fetch the best one from the api.

# Do a JSON where peoples send their parameters and each hedging bot listen all orders and answer back their parameters, the query is based on the parameter. Parameter are spread instead of price.
# Have another replit that answer very basically to requests.
# Have the frontend where we can input parameters and dynamic pricing.
{address:"0x00", spread=1, isLong=True, bOracleId=3, price=123, qty=12, interesRate=-0.15} # use that as a key

answer 
{qty_at_price, full_qty_spread, interestRates = 120}


# methodm when first connect, if use dont have gaz token, send him some and some fake USD#spread ( 1 - price when posted / price aksed )
'''
