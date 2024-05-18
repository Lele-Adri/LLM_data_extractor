# import os
# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from pyinstrument import Profiler
# import app
# from app.app_constants import ENABLE_PROFILING_ENVIRONMENT_VARIABLE_NAME

# PROFILING = float(os.getenv(ENABLE_PROFILING_ENVIRONMENT_VARIABLE_NAME, 0))

# if PROFILING:
#     @app.middleware("http")
#     async def profile_request(request: Request, call_next):
#         profiling = request.query_params.get("profile", False)
#         if profiling:
#             profiler = Profiler(interval=0.001, async_mode="enabled")
#             profiler.start()
#             response = await call_next(request)
#             profiler.stop()
#             return HTMLResponse(profiler.output_html())
#         else:
#             return await call_next(request)
