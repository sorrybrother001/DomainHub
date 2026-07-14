from flask import current_app
def create_stripe_charge(amount, currency="usd", source=None):
    # Placeholder: integrate stripe SDK here with current_app.config["STRIPE_API_KEY"]
    current_app.logger.info("Stripe charge placeholder: %s %s", amount, currency)
    return {"id": "ch_placeholder", "status": "succeeded"}