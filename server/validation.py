import json
from typing import Protocol, TypeVar, overload

from litestar.dto import DTOData
from litestar.exceptions import ClientException
from litestar.status_codes import HTTP_400_BAD_REQUEST
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


class Validation(Protocol):
    @overload
    def __call__(self, data: DTOData[T]) -> T:
        ...

    @overload
    def __call__(self, data: DTOData[T], raise_400: bool) -> T | None:
        ...

    def __call__(self, data: DTOData[T], raise_400: bool = True) -> T | None:
        """
        Perform a validation of the input and convert it to the given Pydantic model.
        By default, raises HTTP 400 when validation fails.
        """
        ...


def validate(data: DTOData[T], raise_400: bool = True) -> T | None:
    try:
        result = data.create_instance()
    except ValidationError as err:
        if raise_400:
            raise ClientException(
                "Validation error while processing body",
                status_code=HTTP_400_BAD_REQUEST,
                extra=json.loads(err.json(include_context=False, include_url=False)),
            ) from err
        return None
    return result


async def provide_validation() -> Validation:
    return validate  # type: ignore
