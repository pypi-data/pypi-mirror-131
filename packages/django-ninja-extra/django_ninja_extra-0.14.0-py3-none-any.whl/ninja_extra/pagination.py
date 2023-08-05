import inspect
import logging
from collections import OrderedDict
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Optional, Type, Union, cast, overload

from django.core.paginator import InvalidPage, Page, Paginator
from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Schema
from ninja.constants import NOT_SET
from ninja.pagination import LimitOffsetPagination, PageNumberPagination, PaginationBase
from ninja.signature import has_kwargs
from ninja.types import DictStrAny
from pydantic import Field

from ninja_extra.conf import settings
from ninja_extra.exceptions import NotFound
from ninja_extra.schemas import PaginatedResponseSchema
from ninja_extra.urls import remove_query_param, replace_query_param

logger = logging.getLogger()

if TYPE_CHECKING:
    from .controllers import ControllerBase  # pragma: no cover

__all__ = [
    "PageNumberPagination",
    "PageNumberPaginationExtra",
    "PaginationBase",
    "LimitOffsetPagination",
    "paginate",
    "PaginatedResponseSchema",
]


def _positive_int(
    integer_string: Union[str, int], strict: bool = False, cutoff: Optional[int] = None
) -> int:
    """
    Cast a string to a strictly positive integer.
    """
    ret = int(integer_string)
    if ret < 0 or (ret == 0 and strict):
        raise ValueError()
    if cutoff:
        return min(ret, cutoff)
    return ret


class PageNumberPaginationExtra(PaginationBase):
    class Input(Schema):
        page: int = Field(1, gt=0)
        page_size: int = Field(100, lt=200)

    page_query_param = "page"
    page_size_query_param = "page_size"

    max_page_size = 200
    paginator_class = Paginator

    def __init__(
        self,
        page_size: int = settings.PAGINATION_PER_PAGE,
        max_page_size: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.page_size = page_size
        self.max_page_size = max_page_size or 200
        self.Input = self.create_input()  # type:ignore

    def create_input(self) -> Type[Input]:
        class DynamicInput(PageNumberPaginationExtra.Input):
            page: int = Field(1, gt=0)
            page_size: int = Field(self.page_size, lt=self.max_page_size)

        return DynamicInput

    def paginate_queryset(
        self, items: QuerySet, request: HttpRequest, **params: Any
    ) -> Any:

        pagination_input = cast(PageNumberPaginationExtra.Input, params["pagination"])
        page_size = self.get_page_size(pagination_input.page_size)
        current_page_number = pagination_input.page
        paginator = self.paginator_class(items, page_size)
        try:
            url = request.build_absolute_uri()
            page: Page = paginator.page(current_page_number)
            return self.get_paginated_response(base_url=url, page=page)
        except InvalidPage as exc:
            msg = "Invalid page. {page_number} {message}".format(
                page_number=current_page_number, message=str(exc)
            )
            raise NotFound(msg)

    def get_paginated_response(self, *, base_url: str, page: Page) -> DictStrAny:
        return OrderedDict(
            [
                ("count", page.paginator.count),
                ("next", self.get_next_link(base_url, page=page)),
                ("previous", self.get_previous_link(base_url, page=page)),
                ("results", list(page)),
            ]
        )

    @classmethod
    def get_response_schema(
        cls, response_schema: Union[Schema, Type[Schema], Any]
    ) -> Any:
        return PaginatedResponseSchema[response_schema]

    def get_next_link(self, url: str, page: Page) -> Optional[str]:
        if not page.has_next():
            return None
        page_number = page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self, url: str, page: Page) -> Optional[str]:
        if not page.has_previous():
            return None
        page_number = page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_page_size(self, page_size: int) -> int:
        if page_size:
            try:
                return _positive_int(page_size, strict=True, cutoff=self.max_page_size)
            except (KeyError, ValueError):
                pass

        return self.page_size


@overload
def paginate() -> Callable[..., Any]:
    ...


@overload
def paginate(
    func_or_pgn_class: Any = NOT_SET, **paginator_params: Any
) -> Callable[..., Any]:
    ...


def paginate(
    func_or_pgn_class: Any = NOT_SET, **paginator_params: Any
) -> Callable[..., Any]:
    isfunction = inspect.isfunction(func_or_pgn_class)
    isnotset = func_or_pgn_class == NOT_SET

    pagination_class: Type[PaginationBase] = settings.PAGINATION_CLASS

    if isfunction:
        return _inject_pagination(func_or_pgn_class, pagination_class)

    if not isnotset:
        pagination_class = func_or_pgn_class

    def wrapper(func: Callable[..., Any]) -> Any:
        return _inject_pagination(func, pagination_class, **paginator_params)

    return wrapper


def _inject_pagination(
    func: Callable[..., Any],
    paginator_class: Type[PaginationBase],
    **paginator_params: Any,
) -> Callable[..., Any]:
    func.has_kwargs = True  # type: ignore
    if not has_kwargs(func):
        func.has_kwargs = False  # type: ignore
        logger.debug(
            f"function {func.__name__} should have **kwargs if you want to use pagination parameters"
        )

    paginator: PaginationBase = paginator_class(**paginator_params)
    paginator_kwargs_name = "pagination"

    @wraps(func)
    def view_with_pagination(
        controller: "ControllerBase", *args: Any, **kw: Any
    ) -> Any:
        func_kwargs = dict(kw)
        if not func.has_kwargs:  # type: ignore
            func_kwargs.pop(paginator_kwargs_name)

        items = func(controller, *args, **func_kwargs)
        assert (
            controller.context and controller.context.request
        ), "Request object is None"
        return paginator.paginate_queryset(items, controller.context.request, **kw)

    view_with_pagination._ninja_contribute_args = [  # type: ignore
        (
            paginator_kwargs_name,
            paginator.Input,
            paginator.InputSource,
        ),
    ]

    return view_with_pagination
