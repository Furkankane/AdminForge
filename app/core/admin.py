from __future__ import annotations

import ctypes
import subprocess
import sys
from pathlib import Path


def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin() -> bool:
    try:
        if getattr(sys, "frozen", False):
            exe_path = Path(sys.executable).resolve()
            params = " ".join(f'"{arg}"' for arg in sys.argv[1:])

            result = ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                str(exe_path),
                params,
                str(exe_path.parent),
                1,
            )
            return result > 32

        script_path = Path(sys.argv[0]).resolve()
        pythonw_path = Path(sys.executable).with_name("pythonw.exe")

        params = f'"{script_path}"'
        if len(sys.argv) > 1:
            extra = " ".join(f'"{arg}"' for arg in sys.argv[1:])
            params = f"{params} {extra}"

        result = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            str(pythonw_path),
            params,
            str(script_path.parent),
            1,
        )
        return result > 32

    except Exception:
        return False