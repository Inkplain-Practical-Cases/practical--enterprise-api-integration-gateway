"""STEP-4: Map CRM responses and failures.
ICS layer: service. Called by: app.main.process.
Why it exists: isolates this teaching operation for direct tests.
Without it: the specific STEP-4 transformation is unavailable.
"""
def transform(value:str)->str:
    """Transform a synthetic string into an offline result."""
    return "record:"+value.strip().lower()
