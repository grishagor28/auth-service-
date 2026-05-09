import logging
import json
import socket
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "service": "auth-service",
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry, ensure_ascii=False)


class TCPLogstashHandler(logging.Handler):
    def __init__(self, host: str, port: int):
        super().__init__()
        self.host = host
        self.port = port

    def emit(self, record: logging.LogRecord):
        try:
            message = self.format(record) + "\n"
            with socket.create_connection((self.host, self.port), timeout=2) as sock:
                sock.sendall(message.encode("utf-8"))
        except Exception:
            pass


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("auth-service")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(JsonFormatter())
        logger.addHandler(console_handler)

        logstash_handler = TCPLogstashHandler(host="logstash", port=5044)
        logstash_handler.setFormatter(JsonFormatter())
        logger.addHandler(logstash_handler)

    return logger


logger = setup_logger()