from typing import Literal, NamedTuple, Any, Generator, AsyncGenerator
from jinja2 import Template

Model = dict[str, type]  # to be replaced by pydantic or something
Data = dict[str, Any]  # json serializable


class Effect(NamedTuple):
    T: Template | str | None = None
    V: Data | None = None
    I: Model | None = None


AppScript = Generator[Effect, Data, None]  # user-side script
AppRoutine = AsyncGenerator[Data, Data]  # core-side wrapper
