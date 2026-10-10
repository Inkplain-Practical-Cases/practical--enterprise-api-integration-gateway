"""STEP-3: Inject authentication configuration.
ICS layer: service. Called by: app.main.process.
Why it exists: isolates this teaching operation for direct tests.
Without it: the specific STEP-3 transformation is unavailable.
"""
def transform(value:str)->str:
    """Transform a synthetic string into an offline result."""
    import os
    return "auth:"+value if os.getenv("CRM_API_TOKEN","demo") else "configuration_missing"
