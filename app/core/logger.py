from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Literal

LogLevel = Literal["INFO", "SUCCESS", "WARNING", "ERROR"]

BASE_DIR = Path(__file__).resolve().parents[2]
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def get_log_file_path() -> Path:
    """
    Günlük log dosyasının yolunu döndürür.
    Örnek: logs/adminforge_2026-03-10.log
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    return LOGS_DIR / f"adminforge_{date_str}.log"


def write_log(level: LogLevel, message: str) -> Path:
    """
    Log mesajını dosyaya yazar ve yazılan dosya yolunu döndürür.
    """
    if not message or not message.strip():
        raise ValueError("Log mesajı boş olamaz.")

    log_file = get_log_file_path()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {message.strip()}\n"

    with log_file.open("a", encoding="utf-8") as f:
        f.write(line)

    return log_file


def log_info(message: str) -> Path:
    return write_log("INFO", message)


def log_success(message: str) -> Path:
    return write_log("SUCCESS", message)


def log_warning(message: str) -> Path:
    return write_log("WARNING", message)


def log_error(message: str) -> Path:
    return write_log("ERROR", message)