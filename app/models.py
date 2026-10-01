from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Item(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    description: str | None = None
    created_at: datetime = Field(alias="createdAt")


class CreateItemRequest(BaseModel):
    name: str
    description: str | None = None


class PagedResult(BaseModel):
    items: list[Item]
    total: int
