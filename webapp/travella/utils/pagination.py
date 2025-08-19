from typing import Callable, Generic, TypeVar
from django.core.paginator import Paginator, Page

ITEM = TypeVar('ITEM')
DTO = TypeVar('DTO')

class PaginationResult(Generic[DTO, ITEM]):
    items:list[DTO] = []
    has_prev:bool
    prev_page:int = 0
    has_next:bool
    next_page:int = 0
    total_pages:int
    current_page:int

    def pages(self) -> list[int]:
        return [i+1 for i in range(self.total_pages)]

    def __init__(self, page_number:int, pagination:Paginator, mapFunc:Callable[[ITEM], DTO]):
        page = pagination.get_page(page_number)
        self.items = [mapFunc(p) for p in page.object_list]

        self.has_prev = page.has_previous()
        if self.has_prev:
            self.prev_page = page.previous_page_number()

        self.has_next = page.has_next()
        if self.has_next:
            self.next_page = page.next_page_number()

        self.total_pages = pagination.num_pages
        self.current_page = page.number