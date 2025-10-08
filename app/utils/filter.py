from fastapi.params import Query


class Filter:
    def __init__(
        self,
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        order_by: str = Query("id"),
        sort: str = Query("asc"),
    ):
        self.limit = limit
        self.offset = offset
        self.order_by = f"{'-' if sort == 'desc' else ''}{order_by}"
        self.sort = sort
        self.query_by = {}
