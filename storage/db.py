from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DbC(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  p_A = db.Column(db.String)
  p_B = db.Column(db.String)
  oracle = db.Column(db.Float)
  referral = db.Column(db.String)
  initiator = db.Column(db.String)
  price = db.Column(db.Float)
  qty = db.Column(db.Float)
  im_A = db.Column(db.Float)
  im_B = db.Column(db.Float)
  df_A = db.Column(db.Float)
  df_B = db.Column(db.Float)
  ir = db.Column(db.Float)
  exp_A = db.Column(db.Float)
  exp_B = db.Column(db.Float)
  fee = db.Column(db.Float)
  t0 = db.Column(db.Float)
  state = db.Column(db.Integer)



class DbHedgerAccount(db.Model):
  address = db.Column(db.String, primary_key=True)
  onchain_collateral = db.Column(db.Float)
  balance_collateral = db.Column(db.Float)
  ratio_oi_max_drawdown = db.Column(db.Float) # for rebalancing
  max_OI = db.Column(db.Float)

class DbHedgerParameters(db.Model):
  oracle = db.Column(db.Float, primary_key=True)
  address = db.Column(db.String, primary_key=True)
  api_name = db.Column(db.String)
  pyth_address = db.Column(db.String)
  qty = db.Column(db.Float)
  im_A = db.Column(db.Float)
  im_B = db.Column(db.Float)
  df_A = db.Column(db.Float)
  df_B = db.Column(db.Float)
  ir = db.Column(db.Float)
  fee = db.Column(db.Float)
  max_OI = db.Column(db.Float)

ex : oracle = 1, address = "0xd0dDF915693f13Cf9B3b69dFF44eE77C901882f8", api_name = "KLAY/USDT:USDT",pyth_address = "0x73dc009953c83c944690037ea477df627657f45c14f16ad3a61089c5a3f9f4f2",im_A = 0.2,im_B = 0.3,df_A = 0.05,df_B = 0.05,ir = 0.20,fee = 0.0008,max_OI = 5000


def init_db(app):
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.init_app(app)
  with app.app_context():
    db.create_all()


