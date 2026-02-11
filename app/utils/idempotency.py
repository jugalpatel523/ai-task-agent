import secrets

def new_run_id() -> str:
    return secrets.token_hex(16)
