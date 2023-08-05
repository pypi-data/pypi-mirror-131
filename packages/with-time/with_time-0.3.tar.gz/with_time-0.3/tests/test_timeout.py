import contextlib
import io
import logging
import time
import unittest
from unittest import TestCase

from with_time import LoggingTimer, PrintingTimer


class TestLoggingTimer(TestCase):
    def test_log_context_manager(self):
        with self.assertLogs(level="INFO") as log:
            with LoggingTimer("sleep"):
                time.sleep(0.01)
            self.assertEqual(len(log.records), 1)
            self.assertIn("sleep", log.output[0])

    @unittest.skip("assertNoLogs is in python > 3.10")
    def test_log_level(self):
        with self.assertNoLogs(level="INFO"):
            with LoggingTimer(log_level=logging.DEBUG):
                time.sleep(0.01)
        with self.assertLogs(level="DEBUG"):
            with LoggingTimer(log_level=logging.DEBUG):
                time.sleep(0.01)

    def test_log_decorator(self):
        @LoggingTimer("hello")
        def foo():
            time.sleep(0.01)

        with self.assertLogs(level="INFO") as log:
            foo()
            self.assertEqual(len(log.records), 1)
            self.assertIn("hello", log.output[0])

    def test_log_context_manager_process_time(self):
        with self.assertLogs(level="INFO") as log:
            with LoggingTimer(timer=time.process_time) as timer:
                time.sleep(0.01)
            self.assertEqual(len(log.records), 1)
            self.assertIn("Elapsed time", log.output[0])
            assert timer.elapsed_time <= 0.01


class TestPrintingTimer(TestCase):
    def test_log_context_manager(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            with PrintingTimer("sleep"):
                time.sleep(0.01)
        assert "sleep" in stdout.getvalue()
