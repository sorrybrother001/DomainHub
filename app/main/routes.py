from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint("main", __name__, template_folder="../templates")

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    # summary placeholders
    wallets = current_user.wallets.all()
    transactions = current_user.transactions.order_by(__import__("sqlalchemy").desc("created_at")).limit(10).all()
    return render_template("dashboard.html", wallets=wallets, transactions=transactions)