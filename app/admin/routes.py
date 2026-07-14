from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models.user import User
from ..extensions import db

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Simple admin check placeholder: email equals configured ADMIN_EMAIL
        from flask import current_app
        if not current_user.is_authenticated or current_user.email != current_app.config.get("ADMIN_EMAIL"):
            flash("Admin access required", "danger")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)
    return wrapper

@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    users = User.query.order_by(User.created_at.desc()).limit(50).all()
    return render_template("admin/dashboard.html", users=users)