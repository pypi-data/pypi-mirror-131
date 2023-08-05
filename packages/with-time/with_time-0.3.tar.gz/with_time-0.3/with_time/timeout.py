import logging
import signal
import time
from contextlib import ContextDecorator

from with_time.exceptions import TimeoutError

logger = logging.getLogger(__name__)


class SignalTimeout(ContextDecorator):
    def __init__(self, seconds: float, *, exception=None):
        self.seconds = seconds
        self.old_handler = None
        self.old_interval = None
        self.old_seconds = None
        self.exception = exception or TimeoutError("Timed out")
        self.start_time = None

    def _handler(self, *_, **__):
        raise self.exception

    def __enter__(self):
        self.old_handler = signal.signal(signal.SIGALRM, self._handler)
        self.old_seconds, self.old_interval = signal.setitimer(
            signal.ITIMER_REAL, self.seconds
        )
        if self.old_seconds > 0 and self.old_seconds < self.seconds:
            logger.warning("Existing (outer) timer may be delayed.")
        self.start_time = time.time()

    def __exit__(self, *_):
        elapsed = time.time() - self.start_time
        signal.signal(signal.SIGALRM, self.old_handler)
        if self.old_seconds != 0.0:
            signal.setitimer(
                signal.ITIMER_REAL,
                max(self.old_seconds - elapsed, 0.0),
                self.old_interval,
            )
