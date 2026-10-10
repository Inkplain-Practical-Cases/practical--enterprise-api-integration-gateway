# STEP-2 — Call mock CRM provider

Install: `python -m pip install -r requirements.txt`; test: `python -m pytest -q`.

Use only synthetic inputs. The `httpx.MockTransport` adapter performs a real HTTP client call in-memory, never calls an outside CRM. Inbound Pydantic validation precedes outbound requests. All responses and errors are explicitly mapped; review the CRD and Python source.
