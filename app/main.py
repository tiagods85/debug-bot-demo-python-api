from __future__ import annotations

from fastapi import FastAPI, Query, status
from fastapi.middleware.cors import CORSMiddleware

from app.models import CreateItemRequest, Item, PagedResult
from app.store import ItemsStore

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
