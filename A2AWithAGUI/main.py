# Copyright (c) Microsoft. All rights reserved.

"""Pizza Agent server – thin entry point.

All application logic lives in the ``app`` package.  This module
exposes ``app`` for ``uvicorn main:app`` and provides a CLI entry point.

Endpoints
---------
- ``POST /ag-ui``                   AG-UI protocol (frontend / UI)
- ``POST /a2a``                     A2A JSON-RPC (agent-to-agent)
- ``GET  /.well-known/agent.json``  A2A agent card discovery
- ``GET  /health``                  Health check

Run
---
::

    # Development
    python main.py

    # Production (500 concurrent requests)
    uvicorn main:app --host 0.0.0.0 --port 8000 --limit-concurrency 500
"""

from __future__ import annotations

import logging

from app.server import app  # noqa: F401 – re-exported for ``uvicorn main:app``

logger = logging.getLogger(__name__)


def main() -> None:
    """CLI entry point – launch the pizza-agent server with uvicorn."""
    import uvicorn

    from app.config import HOST, MAX_CONCURRENT_REQUESTS, PORT, WORKERS

    logger.info("=" * 60)
    logger.info("  pizza-agent server")
    logger.info("=" * 60)
    logger.info("  AG-UI endpoint : POST http://%s:%s/ag-ui", HOST, PORT)
    logger.info("  A2A endpoint   : POST http://%s:%s/a2a", HOST, PORT)
    logger.info("  Agent Card     : GET  http://%s:%s/.well-known/agent.json", HOST, PORT)
    logger.info("  Health         : GET  http://%s:%s/health", HOST, PORT)
    logger.info("  Workers        : %s", WORKERS)
    logger.info("  Concurrency    : %s", MAX_CONCURRENT_REQUESTS)
    logger.info("=" * 60)

    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        workers=WORKERS,
        log_level="info",
        limit_concurrency=MAX_CONCURRENT_REQUESTS,
        timeout_keep_alive=30,
        access_log=True,
    )


if __name__ == "__main__":
    main()
