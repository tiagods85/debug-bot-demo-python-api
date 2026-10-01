from __future__ import annotations

from datetime import datetime, timezone

from app.models import CreateItemRequest, Item, PagedResult


class ItemsStore:
    def __init__(self) -> None:
        self._items: list[Item] = []
        self._next_id = 1
        self.add(CreateItemRequest(name="Widget A", description="The first seeded widget"))
        self.add(CreateItemRequest(name="Widget B", description="The second seeded widget"))
        self.add(CreateItemRequest(name="Widget C", description=None))

    def add(self, request: CreateItemRequest) -> Item:
        item = Item(
            id=self._next_id,
            name=request.name,
            description=request.description,
            created_at=datetime.now(timezone.utc),
        )
        self._next_id += 1
        self._items.append(item)
        return item

    def get_page(self, page: int, page_size: int) -> PagedResult:
        start = (page - 1) * page_size
        items = self._items[start : start + page_size]
        return PagedResult(items=items, total=len(self._items))
