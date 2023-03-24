import fastapi
from psycopg2 import OperationalError
from retrying import retry
from secure import Secure

from app.api import healthcheck
from app.api.api_V1.api import api_router
from app.config.logger import init_logging
from app.db.session import SessionLocal
from app.utils.exceptions import DeployError

secure_headers = Secure()

app = fastapi.FastAPI(
    title="GBM Challenge",
    description="GBM Software Engineer Challenge",
    version="0.1.0",
)


# Detail logs for development purposes
app.add_event_handler("startup", init_logging)


@app.middleware("http")
@retry(
    retry_on_result=DeployError.db_starting_up,
    wait_fixed=10000,
    stop_max_attempt_number=3,
)
async def db_session_middleware(request: fastapi.Request, call_next):
    """
    Stablish DB sessions per request, it retries on DB starting up failure

    - **request**: http request
    - **call_next**: function that will receive the request as a parameter

    Return response
    """
    response = fastapi.Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    except OperationalError as e:
        DeployError.db_starting_up(e)
    finally:
        request.state.db.close()
    return response


@app.middleware("http")
async def set_secure_headers(request, call_next):
    """
    Secure headers middleware
    """
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response


app.include_router(healthcheck.router)
app.include_router(api_router, prefix="/api/v1")
