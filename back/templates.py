from pathlib import Path

from starlette.templating import Jinja2Templates
from jinja2 import Template, ChainableUndefined

WORKDIR = Path(__file__).parent
FRONTDIR = WORKDIR.parent / "front"
APPSDIR = WORKDIR.parent / "apps"


class MyUdefined(ChainableUndefined):
    def __str__(self):
        return "..."


templates = Jinja2Templates(directory=[FRONTDIR / "pages", APPSDIR], undefined=MyUdefined)
