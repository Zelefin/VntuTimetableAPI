import inspect
import logging
import os
from pathlib import Path

from loguru import logger


base_dir = Path(__file__).resolve(strict=True).parent
production_log = base_dir / "logs/production.log"
DEBUG = False


class InterceptHandler(logging.Handler):
    """Intercept standard logging messages toward your Loguru sinks."""

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


if PRODUCTION := not DEBUG:
    # Remove default handler or previously added custom handler
    # Avoids logs to be printed x2 on the terminal
    # or if we want to add new and overwrite previous handler.
    # Note: If we want to see logs on the terminal
    # alongside the log file - don't remove default handler.
    # logger.remove()

    def opener(file, flags):
        """
        Only root user or owner can open the file.
        Ref.: https://chmod-calculator.com/

        r (read): 4 | (write): 2 | x (execute): 1
        Owner:  rw- = 4+2+0 = 6
        Group:  --- = 0+0+0 = 0
        Others: --- = 0+0+0 = 0
        """
        return os.open(file, flags, 0o600)

    FORMATTER = (
        "{time:YYYY-MM-DD at HH:mm:ss} | {level: <8} | {name: ^15} | "
        "{function: ^15} | {line: >3} | {message}"
    )

    # Note:
    # 1.If `serialize=True` - creates very detailed messages
    # by converting the logging record to a valid JSON string
    # It is useful for easier parsing of logs, e.g. analytics or real-time monitoring
    # 2. If we need short logs - remove this argument or set it to `False`.
    logger.add(
        production_log,
        format=FORMATTER,
        serialize=True,
        diagnose=False,
        rotation="50 MB",
        compression="zip",
        opener=opener,
    )

# logger.debug("loggind started.")
# logger.info("loggind started.")
