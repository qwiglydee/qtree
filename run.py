from os import environ
from pathlib import Path
import logging
import uvicorn
import uvicorn.config

log_conf = uvicorn.config.LOGGING_CONFIG
log_conf["formatters"]["default"]["fmt"] = "%(levelprefix)s [%(name)s] %(message)s"
log_conf["loggers"]["root"] = {"handlers": ["default"], "level": "DEBUG"}

if __name__ == "__main__":
    uvicorn.run(
        "back.app:app",
        host=environ.get("HOST", "0.0.0.0"),
        port=int(environ.get("PORT", 8000)),
        root_path=environ.get("ROOT_PATH", ""),
    )
