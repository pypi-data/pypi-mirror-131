# SPDX-License-Identifier: Apache-2.0

import os
import sys

try:
    import pydevd_pycharm
    import _pydev_bundle
except ImportError:
    pass


def connect(port=12345):
    pydevd_pycharm.settrace('localhost', port=port,
                            stdoutToServer=True, stderrToServer=True,
                            suspend=False)


def connect_if_env(port=12345, env='WU_CONNECT_PYCHARM') -> bool:
    if os.getenv(env) != '1':
        return False

    connect(port)
    return True


def restore_sys_stdin():
    """
    Restore the original behavior of sys.stdin.

    After calling connect() or connect_if_env() (which call
    pydevd_pycharm.settrace()), sys.{stdin,stdout,stderr} will be overridden:

    - sys.stdin: io.TextIOWrapper -> _pydev_bundle.pydev_stdin.DebugConsoleStdIn
    - sys.stdout: io.TextIOWrapper -> _pydevd_bundle.pydevd_io.IORedirector
    - sys.stderr: io.TextIOWrapper -> _pydevd_bundle.pydevd_io.IORedirector

    The original sys.stdin.read() (sys.__stdin__.read()) reads **all input**
    from the standard input (at least on Linux; TODO: correct for any
    platform?), but new sys.stdin.read() reads **only one line**.
    """
    if sys.stdin is sys.__stdin__:
        return
    assert isinstance(sys.stdin, _pydev_bundle.pydev_stdin.DebugConsoleStdIn)
    sys.stdin = sys.__stdin__
