from flask import current_app
def register_domain(name, provider, **kwargs):
    current_app.logger.info("Register domain placeholder: %s via %s", name, provider)
    return {"status": "ok", "order_id": "order_placeholder"}