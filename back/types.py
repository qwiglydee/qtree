from typing import Literal, Any, Generator, AsyncGenerator

Model = dict[str, type]  # to be replaced by pydantic or something

EffAct = Literal["T"] | Literal["V"] | Literal["I"]  # template, values, inputs
Effect = dict[EffAct, dict]

Data = dict[str, Any]  # json serializable

AppScript = Generator[Effect, Data, None]  # user-side script
AppRoutine = AsyncGenerator[Data, Data]  # core-side wrapper
