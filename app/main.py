from __future__ import annotations

import os
import subprocess
import time

import sentry_sdk
from fastapi import FastAPI, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app.models import CreateItemRequest, Item, PagedResult
from app.store import ItemsStore

_sentry_dsn = os.environ.get("SENTRY_DSN")
if _sentry_dsn:
    try:
        _release = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, timeout=5, check=True
        ).stdout.strip()
    except Exception:
        _release = None
    sentry_sdk.init(
        dsn=_sentry_dsn,
        integrations=[FastApiIntegration()],
        traces_sample_rate=1.0,
        environment="demo",
        release=_release,
    )

app = FastAPI(title="DebugBotDemo Python API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

store = ItemsStore()


@app.get("/api/items", response_model=PagedResult, response_model_exclude_none=True)
def get_items(page: int = 1, page_size: int = Query(10, alias="pageSize")) -> PagedResult:
    return store.get_page(page, page_size)


@app.post("/api/items", response_model=Item, status_code=status.HTTP_201_CREATED, response_model_exclude_none=True)
def create_item(request: CreateItemRequest) -> Item:
    return store.add(request)


@app.get("/api/debug/crash")
def debug_crash() -> None:
    raise RuntimeError("deliberate crash for the Sentry PoC's own backend-exception scenario")


@app.get("/api/debug/slow")
def debug_slow() -> dict[str, str]:
    time.sleep(3)
    return {"status": "finally done"}
