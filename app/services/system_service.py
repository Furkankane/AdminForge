from __future__ import annotations

import getpass
import platform
import socket
from dataclasses import dataclass

import psutil

from app.core.command_runner import run_command


@dataclass
class SystemSnapshot:
    computer_name: str
    user_name: str
    os_name: str
    ip_address: str
    cpu_name: str
    ram_total_gb: str
    license_status: str
    license_key: str


def get_computer_name() -> str:
    return platform.node() or socket.gethostname()


def get_user_name() -> str:
    return getpass.getuser()


def get_os_name() -> str:
    system = platform.system()
    release = platform.release()
    version = platform.version()
    return f"{system} {release} ({version})"


def get_ip_address() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except Exception:
        return "Bilinmiyor"
    finally:
        sock.close()


def get_cpu_name() -> str:
    cpu_name = platform.processor().strip()
    if cpu_name:
        return cpu_name

    result = run_command("wmic cpu get name", shell="cmd", timeout=20)
    if result.success and result.stdout:
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if len(lines) >= 2:
            return lines[-1]
    return "Bilinmiyor"


def get_ram_total_gb() -> str:
    memory = psutil.virtual_memory()
    total_gb = memory.total / (1024 ** 3)
    return f"{total_gb:.2f} GB"


def get_windows_license_info() -> tuple[str, str]:
    license_status = "Bilinmiyor"
    license_key = "Bulunamadı"

    key_result = run_command(
        "wmic path softwarelicensingservice get OA3xOriginalProductKey",
        shell="cmd",
        timeout=15,
    )

    if key_result.success and key_result.stdout:
        lines = [line.strip() for line in key_result.stdout.splitlines() if line.strip()]
        if len(lines) >= 2:
            possible_key = lines[-1]
            if possible_key and "OA3xOriginalProductKey" not in possible_key:
                license_key = possible_key

    status_result = run_command(
        r'cscript //Nologo C:\Windows\System32\slmgr.vbs /xpr',
        shell="cmd",
        timeout=20,
    )

    if status_result.success and status_result.stdout:
        text_lower = status_result.stdout.lower()

        if "permanently activated" in text_lower or "kalıcı olarak etkinleştirildi" in text_lower:
            license_status = "Lisanslı"
        elif "not activated" in text_lower or "etkinleştirilmedi" in text_lower:
            license_status = "Lisanssız"
        else:
            cleaned = status_result.stdout.strip()
            if cleaned:
                license_status = cleaned

    return license_status, license_key


def get_system_snapshot() -> SystemSnapshot:
    license_status, license_key = get_windows_license_info()

    return SystemSnapshot(
        computer_name=get_computer_name(),
        user_name=get_user_name(),
        os_name=get_os_name(),
        ip_address=get_ip_address(),
        cpu_name=get_cpu_name(),
        ram_total_gb=get_ram_total_gb(),
        license_status=license_status,
        license_key=license_key,
    )