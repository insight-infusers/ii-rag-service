import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stderr_handler.setFormatter(formatter)
    logging.basicConfig(level=level, handlers=[stderr_handler])
