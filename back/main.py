import logging
from contextlib import asynccontextmanager
from pathlib import Path
import uuid

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from .apps import importapps

WORKDIR = Path(__file__).parent
FRONTDIR = WORKDIR.parent / "front"

SESSION_COOKIE = "SID"
SECRET_KEY = "xxxx"


APPS = importapps(WORKDIR.parent / "apps")  # { name: App instance }

logger = logging.getLogger(__name__)


@asynccontextmanager  # type: ignore
async def lifespan(app):
    logger.debug("initializing")
    yield
    logger.debug("finalizing")


templates = Jinja2Templates(directory=FRONTDIR / "pages")


async def index(request: Request) -> Response:
    return templates.TemplateResponse(
        request,
        "index.html",
        {"apps": APPS.keys()},
    )


async def run(request: Request):
    appname = request.path_params["app"]
    app = APPS[appname]
    cid = request.session.get("cid", None)
    if not cid:
        cid = str(uuid.uuid4())
        request.session["cid"] = cid
    return templates.TemplateResponse(
        request,
        "main.html",
        {
            "app": {"name": appname, "title": app.title, "descr": app.descr},
            "cid": cid,
        },
    )


async def socket(websocket: WebSocket):
    app = websocket.path_params["app"]
    cid = websocket.session["cid"]
    await websocket.accept()
    await websocket.send_json({"msg": f"Hello, {cid}"})
    await websocket.close()


app = Starlette(
    debug=True,
    lifespan=lifespan,
    middleware=[
        Middleware(SessionMiddleware, secret_key="xxx", https_only=True, session_cookie=SESSION_COOKIE),
    ],
    routes=[
        Mount("/scripts", StaticFiles(directory=FRONTDIR / "scripts"), name="scripts"),
        Route("/run/{app}", run, name="app"),
        WebSocketRoute("/{app}/socket", socket, name="socket"),
        Route("/", index),
    ],
)
