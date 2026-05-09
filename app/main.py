from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import Base, engine
from app.routers import auth
from app.stats import stats
from app.logger import logger

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def tracking_middleware(request: Request, call_next):
    response = await call_next(request)
    stats.record_request(response.status_code)
    logger.info(json_log(request, response.status_code))
    return response


def json_log(request: Request, status_code: int) -> str:
    import json
    return json.dumps({
        "method": request.method,
        "path": request.url.path,
        "status_code": status_code,
    }, ensure_ascii=False)


@app.get("/stats", tags=["service"])
def get_stats():
    return JSONResponse(content=stats.get_stats())


app.include_router(auth.router)