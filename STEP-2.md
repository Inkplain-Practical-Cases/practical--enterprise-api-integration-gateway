# STEP-2 — Call mock CRM provider

Run `pip install -r requirements.txt && pytest -q`.

The FastAPI door delegates to a deterministic provider adapter. A missing message is rejected by the schema. This branch is an offline simulation, not a real CRM integration.
