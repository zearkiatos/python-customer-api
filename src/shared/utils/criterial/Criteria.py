from .Filter import Filter


class Criteria:
    def __init__(self, limit: int, offset: int, sort: str, filters: list[Filter]):
        self.limit = limit
        self.offset = offset
        self.sort = sort
        self.filters = filters

    def has_filters(self):
        return bool(self.filters)

    def has_sort(self):
        return bool(self.sort)

    def plain_filters(self) -> list[Filter]:
        return self.filters

    def to_dict(self):
        return {
            "limit": self.limit,
            "offset": self.offset,
            "sort": self.sort,
            "filters": [f.to_dict() for f in self.filters]
        }

    def _filter_serialization(self) -> str:
        return ' AND '.join([f.serialization() for f in self.filters])

    def serialization(self):
        serialized = ''
        if self.has_filters():
            serialized = ' AND '.join([f.serialization() for f in self.filters])

        if self.has_sort():
            if serialized:
                serialized += ' AND '
            serialized += f"sort:{self.sort}"

        if self.offset:
            if serialized:
                serialized += ' AND '
            serialized += f"offset:{self.offset}"

        if self.limit:
            if serialized:
                serialized += ' AND '
            serialized += f"limit:{self.limit}"
        
        return serialized