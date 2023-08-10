from flask import Flask
from thirdweb import ThirdwebSDK
from thirdweb.types import SDKOptions
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

private_key = os.environ['PRIVATE_KEY']
secret_key = os.environ['SECRET_KEY']
address = "0xd0dDF915693f13Cf9B3b69dFF44eE77C901882f8"#owner address

sdk = ThirdwebSDK.from_private_key(private_key, "mumbai", SDKOptions(secret_key=secret_key))


app = Flask(__name__)
init_db(app)
for id in ccxt.exchanges:
    exchange = getattr(ccxt, id)
    exchanges[id] = exchange()



@app.route('/')
def index():
    return ' https://www.youtube.com/watch?v=WEMCYBPUR00 '


# case where user need parameters to open a trade

# case where hedger acccept automatically a quote
data = contract.call("acceptQuote", _id)




# triger liquidation on a position ( later )
# settle a transaction ( later )



def update_db_hedges (c_db_id):
  # fetch from exchange position # for frontend

def update_db_hedger_account():


def db_hedger_parameters():

    
def get_open_positions(oracle)
  //scan 
  return list

def get_open_positions("address"):
  // scan into the db each open positions open for an address




app.run(host='0.0.0.0', port=81)


@app.route('/api/open-trade', methods=['GET'])
def get_open_trade():
    symbol = request.args.get('symbol')
    # Retrieve the open trade data based on the symbol from your database
    open_trade_data = retrieve_open_trade_data(symbol)
    return jsonify(open_trade_data)

def retrieve_open_trade_data(symbol):
    # This function should query your database to get the open trade data
    # for the given symbol
    return {
        'symbol': symbol,
        'data': 'Example data for symbol ' + symbol
    }

if __name__ == '__main__':
    app.run()