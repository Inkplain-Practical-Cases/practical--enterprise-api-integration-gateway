"""STEP-2: Call mock CRM provider.
ICS layer: service. Called by: app.main.process.
Why it exists: isolates this teaching operation for direct tests.
Without it: the specific STEP-2 transformation is unavailable.
"""
def transform(value:str)->str:
    """Transform a synthetic string into an offline result."""
    return "crm:"+value.strip()
