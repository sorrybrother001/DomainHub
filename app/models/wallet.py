from ..extensions import db
from datetime import datetime
from decimal import Decimal

class Wallet(db.Model):
    __tablename__ = "wallets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    currency = db.Column(db.String(20), nullable=False)  # USD, EUR, TON, BTC, ETH, USDT-TRC20 etc.
    balance = db.Column(db.Numeric(20, 8), default=0)
    address = db.Column(db.String(255), nullable=True)  # placeholder for external address
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship("Transaction", backref="wallet", lazy="dynamic")

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey("wallets.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    tx_type = db.Column(db.String(20))  # deposit, withdraw, transfer
    amount = db.Column(db.Numeric(20, 8), nullable=False)
    currency = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending, completed, failed
    external_ref = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)