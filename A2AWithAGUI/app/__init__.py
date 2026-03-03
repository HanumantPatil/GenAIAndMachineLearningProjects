# Copyright (c) Microsoft. All rights reserved.

"""Pizza Agent application package.

Refactored structure
--------------------
- ``app.config``       – Configuration constants and environment settings
- ``app.state``        – Shared runtime state (agent instance, semaphore)
- ``app.helpers``      – A2A protocol helper functions
- ``app.agent_card``   – A2A Agent Card definition
- ``app.agent``        – Agent factory (``PizzaAgentFactory``)
- ``app.tools``        – Pizza domain tools (menu, orders, @tool functions)
- ``app.routes``       – FastAPI route handlers (A2A, health)
- ``app.server``       – FastAPI application factory and lifespan
"""
