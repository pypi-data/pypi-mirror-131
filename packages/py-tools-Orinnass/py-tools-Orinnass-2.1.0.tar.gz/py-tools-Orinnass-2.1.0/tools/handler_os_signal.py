from signal import Signals, signal as add_signal
from collections.abc import Callable
from types import FrameType


def add_handler(func: Callable[[int | Signals, int | FrameType | None], None], signal: int | Signals = Signals.SIGTERM):
    add_signal(signal, func)
