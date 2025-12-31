#!/bin/bash
# uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
#!/bin/bash
gunicorn app:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}
# ook