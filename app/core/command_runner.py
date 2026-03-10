from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from typing import Literal

from app.core.logger import log_error, log_info, log_success, log_warning

ShellType = Literal["cmd", "powershell"]


@dataclass
class CommandResult:
    shell: ShellType
    command: str
    success: bool
    returncode: int
    stdout: str
    stderr: str
    duration_seconds: float


def _decode_output(data: bytes | None) -> str:
    if not data:
        return ""

    for encoding in ("utf-8", "cp1254", "cp850", "latin1"):
        try:
            return data.decode(encoding)
        except Exception:
            continue

    return data.decode(errors="ignore")


def run_command(command: str, shell: ShellType = "cmd", timeout: int = 60) -> CommandResult:
    if not command or not command.strip():
        raise ValueError("Komut boş olamaz.")

    log_info(f"Komut çalıştırılacak | shell={shell} | command={command}")
    start = time.perf_counter()

    try:
        if shell == "powershell":
            proc = subprocess.Popen(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    command,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        elif shell == "cmd":
            proc = subprocess.Popen(
                ["cmd", "/c", command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        else:
            raise ValueError(f"Desteklenmeyen shell tipi: {shell}")

        try:
            stdout_bytes, stderr_bytes = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout_bytes, stderr_bytes = proc.communicate()

            end = time.perf_counter()
            result = CommandResult(
                shell=shell,
                command=command,
                success=False,
                returncode=-1,
                stdout=_decode_output(stdout_bytes).strip(),
                stderr=f"Komut zaman aşımına uğradı. Timeout: {timeout} saniye",
                duration_seconds=round(end - start, 3),
            )
            log_error(
                f"Komut timeout | shell={result.shell} | duration={result.duration_seconds}s | "
                f"command={result.command} | stderr={result.stderr}"
            )
            return result

        end = time.perf_counter()

        result = CommandResult(
            shell=shell,
            command=command,
            success=(proc.returncode == 0),
            returncode=proc.returncode if proc.returncode is not None else -1,
            stdout=_decode_output(stdout_bytes).strip(),
            stderr=_decode_output(stderr_bytes).strip(),
            duration_seconds=round(end - start, 3),
        )

        if result.success:
            log_success(
                f"Komut başarılı | shell={result.shell} | returncode={result.returncode} | "
                f"duration={result.duration_seconds}s | command={result.command}"
            )
        else:
            log_warning(
                f"Komut hata ile tamamlandı | shell={result.shell} | returncode={result.returncode} | "
                f"duration={result.duration_seconds}s | command={result.command} | stderr={result.stderr or '[yok]'}"
            )

        return result

    except Exception as exc:
        end = time.perf_counter()
        result = CommandResult(
            shell=shell,
            command=command,
            success=False,
            returncode=-1,
            stdout="",
            stderr=f"Beklenmeyen hata: {exc}",
            duration_seconds=round(end - start, 3),
        )
        log_error(
            f"Komut exception | shell={result.shell} | duration={result.duration_seconds}s | "
            f"command={result.command} | stderr={result.stderr}"
        )
        return result


def format_result(result: CommandResult) -> str:
    lines = [
        "=" * 70,
        f"Shell      : {result.shell}",
        f"Command    : {result.command}",
        f"Success    : {result.success}",
        f"ReturnCode : {result.returncode}",
        f"Duration   : {result.duration_seconds} sn",
        "-" * 70,
        "STDOUT:",
        result.stdout or "[çıktı yok]",
        "-" * 70,
        "STDERR:",
        result.stderr or "[hata yok]",
        "=" * 70,
    ]
    return "\n".join(lines)