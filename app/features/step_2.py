"""Offline CRM integration teaching adapter."""
def transform(message: str) -> str:
    """Return a deterministic simulated CRM record."""
    return "crm:" + message.strip()
