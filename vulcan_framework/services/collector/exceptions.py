# -*- coding: utf-8 -*-
# Time       : 2022/5/4 2:23
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
from typing import Optional, Sequence


class CollectorException(Exception):
    def __init__(self, msg: Optional[str] = None, stacktrace: Optional[Sequence[str]] = None):
        self.msg = msg
        self.stacktrace = stacktrace
        super().__init__()

    def __str__(self) -> str:
        exception_msg = "Message: {}\n".format(self.msg)
        if self.stacktrace:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += "Stacktrace:\n{}".format(stacktrace)
        return exception_msg


class PathMenuError(CollectorException):
    """
    - Unresolved null object received.
    - Network flutter when requesting meeting paper table of contents.
    """
