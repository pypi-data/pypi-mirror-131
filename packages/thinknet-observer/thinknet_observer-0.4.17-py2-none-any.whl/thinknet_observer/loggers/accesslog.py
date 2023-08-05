import logging
import os
import time
from typing import IO, Optional, Union
from http import HTTPStatus


def _create_logger(
    name: str,
    target: Union[logging.Logger, str, None],
    level: Optional[str],
    sys_default: IO,
    *,
    propagate: bool = True,
) -> Optional[logging.Logger]:
    if isinstance(target, logging.Logger):
        return target

    if target:
        logger = logging.getLogger(name)
        logger.handlers = [
            logging.StreamHandler(sys_default)
            if target == "-"
            else logging.FileHandler(target)
        ]
        logger.propagate = propagate
        formatter = logging.Formatter(
            "%(message)s",
            "%Y-%m-%dT%H:%M:%S%zZ",
        )
        logger.handlers[0].setFormatter(formatter)
        if level is not None:
            logger.setLevel(logging.getLevelName(level.upper()))
        return logger
    else:
        return None


class AccessLogAtoms(dict):
    def __init__(
        self, request: "WWWScope", response: "ResponseSummary", request_time: float
    ) -> None:
        for name, value in request["headers"]:
            self[f"{{{name.decode('latin1').lower()}}}i"] = value.decode("latin1")
        for name, value in response.get("headers", []):
            self[f"{{{name.decode('latin1').lower()}}}o"] = value.decode("latin1")
        for name, value in os.environ.items():
            self[f"{{{name.lower()}}}e"] = value
        protocol = request.get("http_version", "ws")
        client = request.get("client")
        if client is None:
            remote_addr = None
        elif len(client) == 2:
            remote_addr = f"{client[0]}:{client[1]}"
        elif len(client) == 1:
            remote_addr = client[0]
        else:  # make sure not to throw UnboundLocalError
            remote_addr = f"<???{client}???>"
        if request["type"] == "http":
            method = request["method"]
        else:
            method = "GET"
        query_string = request["query_string"].decode()
        path_with_qs = request["path"] + ("?" + query_string if query_string else "")
        status_code = response["status"]
        try:
            status_phrase = HTTPStatus(status_code).phrase
        except ValueError:
            status_phrase = f"<???{status_code}???>"
        self.update(
            {
                "h": remote_addr,
                "l": "-",
                "t": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "r": f"{method} {request['path']} {protocol}",
                "R": f"{method} {path_with_qs} {protocol}",
                "s": response["status"],
                "st": status_phrase,
                "S": request["scheme"],
                "m": method,
                "U": request["path"],
                "Uq": path_with_qs,
                "q": query_string,
                "H": protocol,
                "b": self["{Content-Length}o"],
                "B": self["{Content-Length}o"],
                "f": self["{Referer}i"],
                "a": self["{User-Agent}i"],
                "T": int(request_time),
                "M": int(request_time * 1000),
                "D": int(request_time * 1_000_000),
                "L": f"{request_time:.6f}",
                "p": f"<{os.getpid()}>",
            }
        )

    def __getitem__(self, key: str) -> str:
        try:
            if key.startswith("{"):
                return super().__getitem__(key.lower())
            else:
                return super().__getitem__(key)
        except KeyError:
            return "-"
