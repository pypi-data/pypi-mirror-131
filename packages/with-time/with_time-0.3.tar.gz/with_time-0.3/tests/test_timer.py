import time
from unittest import TestCase

from with_time import SignalTimeout, TimeoutError


class OuterError(TimeoutError):
    pass


class InnerError(TimeoutError):
    pass


class TestSignalTimeout(TestCase):
    def test_context_manager(self):
        with self.assertRaises(TimeoutError):
            with SignalTimeout(0.1):
                time.sleep(1)

    def test_decorator(self):
        @SignalTimeout(0.1)
        def foo():
            time.sleep(1)

        with self.assertRaises(TimeoutError):
            foo()

    def test_nested_timeout_outer(self):
        start = time.time()
        with self.assertRaises(OuterError):
            with SignalTimeout(0.3, exception=OuterError()):
                try:
                    with SignalTimeout(0.2, exception=InnerError()):
                        time.sleep(1)
                except InnerError:
                    pass
                time.sleep(1)
        elapsed = time.time() - start
        assert elapsed < 0.31
        assert elapsed > 0.29

    def test_nested_delay_outer(self):
        start = time.time()
        with self.assertRaises(OuterError):
            with SignalTimeout(0.2, exception=OuterError()):
                with self.assertLogs(level="WARN") as log:
                    try:
                        with SignalTimeout(0.3, exception=InnerError()):
                            pass
                    except InnerError:
                        pass
                self.assertIn("delayed", log.output[0])
                time.sleep(1)
        elapsed = time.time() - start
        assert elapsed < 0.21
        assert elapsed > 0.19

    def test_custom_exception(self):
        with self.assertRaises(RuntimeError):
            with SignalTimeout(0.1, exception=RuntimeError("foo")):
                time.sleep(1)
