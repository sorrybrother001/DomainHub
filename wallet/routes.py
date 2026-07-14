from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from ..extensions import db
from ..models.wallet import Wallet, Transaction
from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

wallet_bp = Blueprint("wallet", __name__, template_folder="../templates/wallet")

class TransferForm(FlaskForm):
    currency = SelectField("Currency", choices=[("USD","USD"),("EUR","EUR"),("BTC","BTC"),("ETH","ETH"),("USDT-TRC20","USDT-TRC20"),("USDT-BEP20","USDT-BEP20"),("TON","TON")])
    amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=0.0001)])
    to_address = StringField("Destination Address", validators=[DataRequired()])
    submit = SubmitField("Send")

@wallet_bp.route("/")
@login_required
def wallet_index():
    wallets = current_user.wallets.all()
    return render_template("wallet/index.html", wallets=wallets)

@wallet_bp.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    form = TransferForm()
    if form.validate_on_submit():
        # Simple local transfer implementation (internal transfer)
        currency = form.currency.data
        amount = Decimal(str(form.amount.data))
        to_address = form.to_address.data.strip()
        # find user's wallet
        src = current_user.wallets.filter_by(currency=currency).first()
        if not src or src.balance < amount:
            flash("Insufficient balance", "danger")
            return redirect(url_for("wallet.wallet_index"))
        # Create a pending transaction; external processing is required
        tx = Transaction(wallet=src, user=current_user, tx_type="transfer", amount=amount, currency=currency, status="pending", external_ref=to_address)
        src.balance = src.balance - amount
        db.session.add(tx)
        db.session.commit()
        current_app.logger.info("Created transfer tx %s -> %s %s", current_user.email, to_address, amount)
        flash("Transfer initiated. Pending confirmation.", "success")
        return redirect(url_for("wallet.wallet_index"))
    return render_template("wallet/transfer.html", form=form)

@wallet_bp.route("/transactions")
@login_required
def transactions():
    txs = current_user.transactions.order_by(__import__("sqlalchemy").desc("created_at")).all()
    return render_template("wallet/transactions.html", transactions=txs)