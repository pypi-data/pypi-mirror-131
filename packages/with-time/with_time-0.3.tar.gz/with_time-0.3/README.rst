===============================
With Time
===============================


.. image:: https://img.shields.io/pypi/v/with_time.svg
        :target: https://pypi.python.org/pypi/with_time


Context Managers and Decorator for common time operations 

Quick start
============

Installation
------------

.. code-block:: shell

    pip intall with-time

Usage
-----

Measuring duration, with PrintingTimer or LoggingTimer

with_timer.PrintingTimer(label: str = None, timer: Callable[[], float] = time.time)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prints out how long context operation or function took. Message is prepended with
*label*. By default elapsed running time will be measured but other `time`_ methods can be
utilized such as *time.process_time*, *time.monotomic*, and so on.

.. code-block:: python

    >>> import time
    >>> from with_time import PrintingTimer
    >>>
    >>> # Context Manager Example
    >>> with PrintingTimer("Example"):
    ...     time.sleep(.1337)
    ... 
    Example: 0.13398265838623047 seconds
    >>> 
    >>> # Decorator Example
    >>> @PrintingTimer("Decorator Example")
    ... def foo():
    ...     time.sleep(.1337)
    ... 
    >>> foo()
    Decorator Example: 0.13398265838623047 seconds


with_timer.LoggingTimer(label: str = None, log_level: int = None, timer: Callable[[], float] = time.time)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

LoggingTimer works just the same way as PrintinTimer except duration is logged
rather than printed. Log level can be customized using `logging.debug, logging.warning...`_

.. code-block:: python

    >>> import time
    >>> import logging
    >>> from with_time import LoggingTimer
    >>> logging.basicConfig(force=True)
    >>>
    >>> # Context Manager Example
    >>> with LoggingTimer("Example"):
    ...     time.sleep(.1337)
    ... 
    INFO:with_time.timer:Example: 0.13399600982666016 seconds
    >>> 
    >>> # Decorator Example
    >>> @LoggingTimer("Decorator Example")
    ... def foo():
    ...     time.sleep(.1337)
    ... 
    >>> foo()
    INFO:with_time.timer:Decorator Example: 0.13396501541137695 seconds


with_time.SignalTimeout(seconds: float, exception=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
Raise an exception as an execution timeout. SignalTimeout uses `signal`_ implementation
which is only supported on Unix like os. By default *with_time.exceptions.TimeoutError*
but this can be changed by passing any initialized exception object as *exception*


SignalTimeout does attempt to restore signals it overwrites which make some but not all
nested scenarios of timeout work.

.. code-block:: python

    >>> import time
    >>> from with_time import SignalTimeout
    >>> with SignalTimeout(.1000):
    ...     time.sleep(.1337)
    ... 
    Traceback (most recent call last):
      File "<stdin>", line 2, in <module>
      File ".../with_time/timeout.py", line 21, in _handler
        raise self.exception
    with_time.exceptions.TimeoutError: Timed out
    >>>
    >>> # Custom Exception
    >>> with SignalTimeout(.1000, exception=RuntimeError("Oops")):
    ...     time.sleep(.1337)
    ... 
    Traceback (most recent call last):
      File "<stdin>", line 2, in <module>
      File ".../with_time/timeout.py", line 21, in _handler
        raise self.exception
    RuntimeError: Oops

.. _`signal`: https://docs.python.org/3/library/signal.html
.. _`time`: https://docs.python.org/3/library/time.html#time.get_clock_info
.. _`logging.debug, logging.warning...`: https://docs.python.org/3/library/logging.html#logging-levels
