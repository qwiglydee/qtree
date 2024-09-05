"""Stateful webapp

General scheme of work

- app modules are preloaded
- browser opens runapp page and starts runapp handler
  - session/connection id is created
  - for a new session AppRoutine generator is created and stored into global app state
    - it creates Appscript generator from app module script function and stores it inside itself, in its locals
      - the generator starts app module script
    - it also creates page State tracking all changes, stored its locals
  - a html page with scripts is then generated
- page opens socket connection
  - the socket handler takes corresponding AppRoutine from global app state
- page sends 'READY' message
  - AppRoutine sends all current page state
- page sends some inputs (determined in its state) via socket
  - AppRoutine grabs the inputs and sends to AppScript
    - AppScript yields some outputs or requests some inputs
  - AppRoutine sends aggregates them into page state and sends to page via socket
- when AppScript is terminated, so is AppRoutine
  - AppRoutine is deleted from global webapp state along with all its locals and page states
  - websocket sends `TERMINATE` signal to page
  - page scripts post form to the runapp page
  - the handler deletes session/connection id
"""

from typing import Any, Generator, AsyncGenerator
import logging
from contextlib import asynccontextmanager
from pathlib import Path
import uuid

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.middleware import Middleware
from starlette.exceptions import HTTPException

from .types import Model, Data, AppScript, AppRoutine
from .apps import App, run
from .templates import templates

WORKDIR = Path(__file__).parent
FRONTDIR = WORKDIR.parent / "front"
APPSDIR = WORKDIR.parent / "apps"

APPS: dict[str, App] = App.importapps(WORKDIR.parent / "apps")  # { name: App instance { module } }

logger = logging.getLogger(__name__)


@asynccontextmanager  # type: ignore
async def lifespan(app):
    logger.debug("initializing")
    app.state.running = {}  # {sid: Running generator}
    yield  # run the asgi
    logger.debug("finalizing")
    for sid, app in app.state.running.items():
        # do something
        pass


async def index(request: Request) -> Response:
    sessions = {}
    for sid, running in request.app.state.running.items():
        app = running.ag_frame.f_locals["app"].name
        if app not in sessions:
            sessions[app] = []
        sessions[app].append(sid)

    filenames = {}
    for app in APPS.values():
        filenames[app.name] = "/".join(Path(app.module.__file__).parts[-2:])

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "apps": APPS.values(),
            "sessions": sessions,
            "filenames": filenames,
        },
    )


async def startapp(request: Request):
    appname = request.path_params["app"]
    app = APPS[appname]

    # creating new app session
    sid = str(uuid.uuid4())
    logger.debug(f"{appname} creating new running session {sid=}")
    running: AppRoutine = run(app)
    await running.asend(None)  # type: ignore # 0th iteration, yields None
    request.app.state.running[sid] = running

    return RedirectResponse(request.url_for("run", app=appname, sid=sid))


async def runapp(request: Request):
    appname = request.path_params["app"]
    app = APPS[appname]
    sid = request.path_params["sid"]

    if sid not in request.app.state.running:
        raise HTTPException(404)

    if request.method == "GET":
        return templates.TemplateResponse(
            request,
            "run.html",
            {
                "app": {"module": app.module.__name__, "name": app.name, "title": app.title, "descr": app.description},
                "sid": sid,
            },
        )

    if request.method == "POST":
        del request.app.state.running[sid]

        return templates.TemplateResponse(
            request,
            "fin.html",
            {
                "app": {"module": app.module.__name__, "name": app.name, "title": app.title, "descr": app.description},
                "sid": sid,
            },
        )


async def socket(websocket: WebSocket):
    appname = websocket.path_params["app"]
    app = APPS[appname]
    sid = websocket.path_params["sid"]

    assert sid in websocket.app.state.running
    running: AppRoutine = websocket.app.state.running[sid]

    logger.debug(f"{appname} connected")
    await websocket.accept()

    try:
        while True:
            inp: Data = await websocket.receive_json()
            out = {}
            logger.debug(f"{appname} websocket {inp=}")

            while not out.get("inputs"):
                out: Data = await running.asend(inp)
                logger.debug(f"{appname} websocket {out=}")
                await websocket.send_json(out)
                inp = {}
    except GeneratorExit as e:
        # normal session completion
        logger.debug(f"{appname} websocket terminated")
        await websocket.send_json(e.args[0])
        await websocket.close()
    except WebSocketDisconnect:
        # session interrupted, doing nothing in hope of reconnection
        logger.error(f"{appname} websocket disconnected")
        pass


app = Starlette(
    debug=True,
    lifespan=lifespan,
    routes=[
        Mount("/scripts", StaticFiles(directory=FRONTDIR / "scripts"), name="scripts"),
        Mount("/assets", StaticFiles(directory=FRONTDIR / "assets"), name="assets"),
        Route("/start/{app}", startapp, name="start"),
        Route("/run/{app}/{sid}", runapp, name="run", methods=["GET", "POST"]),
        WebSocketRoute("/run/{app}/{sid}/socket", socket, name="socket"),
        Mount("/code", StaticFiles(directory=APPSDIR), name="code"),
        Route("/", index),
    ],
)
