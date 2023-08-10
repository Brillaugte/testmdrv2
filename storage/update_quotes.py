from db import db, DbC, DbPrice, DbHedges, DbHedgerAccount, DbHedgerParameters


def get_latest_c_id():
  latest_c = DbC.query.order_by(DbC.id.desc()).first()
  if latest_c is not None:
    return latest_c.id
  else:
    return 0


def update_db_c(contract):
  c_id = get_latest_c_id()
  cL = contract.call("get_cL")
  for i in range(c_id, cL):
    (_id, p_A, p_B, oracle, referral, initiator, price, qty, im_A,
     im_B) = contract.call("get_cM", i)

    (df_A, df_B, ir, exp_A, exp_B, t0, state) = contract.call("get_cM2", i)

    # Create and add the record to the database
    record = DbC(id=_id,
                 p_A=str(p_A),
                 p_B=str(p_B),
                 oracle=float(oracle),
                 referral=str(referral),
                 initiator=str(initiator),
                 price=float(price),
                 qty=float(qty),
                 im_A=float(im_A),
                 im_B=float(im_B),
                 df_A=float(df_A),
                 df_B=float(df_B),
                 ir=float(ir),
                 exp_A=float(exp_A),
                 exp_B=float(exp_B),
                 t0=float(t0),
                 state=int(state))
    db.session.add(record)
    db.session.commit()

    c_id = i + 1
