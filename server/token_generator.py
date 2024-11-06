import json
import secrets

# This is absolutely unsafe way how to create aliasing between token and client name.
# Don't use it for normal code

def generate_token(length=32):
    """Generate random token"""
    return secrets.token_urlsafe(length)

clients_tokens = dict()

clients_tokens["Alice"] = generate_token()
clients_tokens["Bob"] = generate_token()
clients_tokens["Eva"] = generate_token()

json_data = json.dumps(clients_tokens)

# write token data into json file
with open("clients_tokens.json", "w") as f:
    f.write(json_data)
