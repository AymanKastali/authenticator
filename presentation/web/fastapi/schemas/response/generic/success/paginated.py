from typing import TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class PaginationModel(BaseModel):
    total_items: int | None = Field(
        default=None, description="Total number of items"
    )
    page: int | None = Field(default=None, description="Current page number")
    per_page: int | None = Field(default=None, description="Items per page")
    total_pages: int | None = Field(
        default=None, description="Total pages available"
    )


class PaginatedResponseModel[T](BaseModel):
    status_code: int = 200
    message: str | None = None
    data: list[T] | None = None
    pagination: PaginationModel | None = None

    @classmethod
    def build(
        cls,
        data: list[T] | None = None,
        message: str | None = None,
        status_code: int = 200,
        page: int = 1,
        per_page: int = 10,
    ) -> "PaginatedResponseModel[T]":
        total_items = len(data) if data else 0
        total_pages = (
            (total_items + per_page - 1) // per_page if per_page else 1
        )

        paginated_data = []
        if data:
            start_idx = max((page - 1) * per_page, 0)
            end_idx = start_idx + per_page
            paginated_data = data[start_idx:end_idx]

        pagination = PaginationModel(
            page=page,
            per_page=per_page,
            total_items=total_items,
            total_pages=total_pages,
        )

        return cls(
            data=paginated_data,
            message=message,
            status_code=status_code,
            pagination=pagination,
        )
