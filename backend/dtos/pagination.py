from pydantic import BaseModel


class PaginationResponse[T](BaseModel):
    count: int
    results: list[T]