from django.core.paginator import Paginator
from typing import Dict, Any, Union, Optional, Tuple
from django.db.models import Q, QuerySet, Model

from social_network.constants.default_values import SortingOrder


class GetData:
    """
    Class to handle query modifications for search, sort, filter, and pagination with method chaining.

    data = (
        GetData(Model_OR_query)
        .search(search_text="sample", "field_1", "field_2", "field_n")
        .filter(category="Category A")
        .sort(sort_by="name", order="asc")
        .paginate(page=1, limit=10)
        .execute()
    )
    """

    def __init__(self, query_or_model: Union[QuerySet, type[Model]]):
        """
        Initialize with a QuerySet or a Model.
        """
        if hasattr(query_or_model, "objects"):
            # If a model is passed, get its QuerySet
            self.queryset: QuerySet = query_or_model.objects.all()
        else:
            # If a QuerySet is passed, use it directly
            self.queryset: QuerySet = query_or_model

        # Store applied options for debugging or returning later
        self.applied_options: Dict[str, Any] = {
            "search": dict(),
            "sort": dict(),
            "filter": dict(),
            "pagination": dict(),
        }

    def search(self, search_text: Optional[str] = None, *fields: str) -> "GetData":
        """
        Filter queryset based on a search text across multiple fields.

        Args:
            search_text: Text to search for.
            fields: Fields to include in the search.

        Returns:
            self: Allows method chaining.
        """
        if search_text and fields:
            query = Q()
            for field in fields:
                query |= Q(**{f"{field}__icontains": search_text})
            self.queryset = self.queryset.filter(query)
            self.applied_options["search"] = {"text": search_text, "fields": fields}
        return self

    def sort(self, sort_by: Optional[str] = None, order: str = SortingOrder.ASC.value) -> "GetData":
        """
        Sort the queryset by a given field in ascending or descending order.

        Args:
            sort_by: Field name to sort by.
            order: Sorting order, either 'asc' for ascending or 'desc' for descending.

        Returns:
            self: Allows method chaining.
        """
        if sort_by:
            field_name = sort_by
            if order == SortingOrder.DESC.value:
                sort_by = f"-{sort_by}"
            self.queryset = self.queryset.order_by(sort_by)
            self.applied_options["sort"] = {"field": field_name, "order": order}
        return self

    def filter(self, **filters: Any) -> "GetData":
        """
        Apply filtering to the queryset based on the given keyword arguments.

        Args:
            **filters: Filter conditions.

        Returns:
            self: Allows method chaining.
        """
        if filters:
            self.queryset = self.queryset.filter(**filters)
            self.applied_options["filter"] = filters
        return self

    def paginate(self, page: int = 1, limit: int = 10) -> "GetData":
        """
        Paginate the queryset.

        Args:
            page: Page number.
            limit: Number of items per page.

        Returns:
            self: Updates queryset and allows method chaining.
        """
        paginator = Paginator(self.queryset, limit)
        self.page_obj = paginator.get_page(page)
        self.queryset = self.page_obj.object_list
        self.pagination_meta: Dict[str, Any] = {
            "total": paginator.count,
            "total_page": paginator.num_pages,
            "current_page": self.page_obj.number,
            "next_page": (
                self.page_obj.next_page_number() if self.page_obj.has_next() else None
            ),
        }
        self.applied_options["pagination"] = {
            "page": page,
            "limit": limit,
        }
        return self        

    def execute(self, *fields: str) -> Dict[str, Any]:
        """
        Return the final processed queryset, pagination metadata, and applied options.

        Returns:
            dict: Contains the results, pagination metadata, and applied options.
        """
        return {
            "data": list(self.queryset.values(*fields)),
            "pagination": self.pagination_meta,
            "applied_options": self.applied_options,
        }
