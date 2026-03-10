from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.core.logger import get_log_file_path
from app.services.system_service import get_system_snapshot


class ReportsPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._build_ui()
        self._apply_local_styles()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Raporlar")
        title.setObjectName("reportsTitle")

        button_grid = QGridLayout()
        button_grid.setSpacing(10)

        self.export_txt_button = QPushButton("TXT Sistem Raporu Oluştur")
        self.export_txt_button.clicked.connect(self._export_txt_report)

        self.open_logs_button = QPushButton("Güncel Log Dosyasını Aç")
        self.open_logs_button.clicked.connect(self._open_current_log)

        self.refresh_button = QPushButton("Önizlemeyi Yenile")
        self.refresh_button.clicked.connect(self._load_preview)

        self.export_log_info_button = QPushButton("Log Yolunu Göster")
        self.export_log_info_button.clicked.connect(self._show_log_path)

        button_grid.addWidget(self.export_txt_button, 0, 0)
        button_grid.addWidget(self.open_logs_button, 0, 1)
        button_grid.addWidget(self.refresh_button, 1, 0)
        button_grid.addWidget(self.export_log_info_button, 1, 1)

        preview_title = QLabel("Rapor Önizleme")
        preview_title.setObjectName("reportsSectionTitle")

        self.preview_box = QPlainTextEdit()
        self.preview_box.setReadOnly(True)

        layout.addWidget(title)
        layout.addLayout(button_grid)
        layout.addWidget(preview_title)
        layout.addWidget(self.preview_box)

        self._load_preview()

    def _apply_local_styles(self) -> None:
        self.setStyleSheet(
            """
            QLabel#reportsTitle {
                font-size: 26px;
                font-weight: 700;
                color: #2b2b2b;
            }

            QLabel#reportsSectionTitle {
                font-size: 15px;
                font-weight: 600;
                color: #2b2b2b;
                margin-top: 8px;
            }

            QPushButton {
                min-height: 38px;
                padding: 8px 14px;
                border: 1px solid #cfc7bb;
                border-radius: 10px;
                background: #f4efe7;
                color: #222222;
                font-weight: 600;
            }

            QPushButton:hover {
                background: #ebe4d8;
            }

            QPlainTextEdit {
                background: #ffffff;
                color: #111111;
                border: 1px solid #cfc7bb;
                border-radius: 12px;
                padding: 8px;
            }
            """
        )

    def _build_report_text(self) -> str:
        snapshot = get_system_snapshot()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return (
            "=== AdminForge Sistem Raporu ===\n"
            f"Oluşturulma Zamanı : {now}\n"
            f"Bilgisayar         : {snapshot.computer_name}\n"
            f"Kullanıcı          : {snapshot.user_name}\n"
            f"İşletim Sistemi    : {snapshot.os_name}\n"
            f"IP Adresi          : {snapshot.ip_address}\n"
            f"CPU                : {snapshot.cpu_name}\n"
            f"RAM                : {snapshot.ram_total_gb}\n"
        )

    def _load_preview(self) -> None:
        self.preview_box.setPlainText(self._build_report_text())

    def _export_txt_report(self) -> None:
        base_dir = Path(__file__).resolve().parents[3]
        output_dir = base_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        file_name = f"adminforge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = output_dir / file_name
        file_path.write_text(self._build_report_text(), encoding="utf-8")

        self.preview_box.setPlainText(
            self._build_report_text() + f"\n\nRapor kaydedildi:\n{file_path}"
        )

    def _open_current_log(self) -> None:
        log_path = get_log_file_path()
        if not log_path.exists():
            self.preview_box.setPlainText(f"Log dosyası henüz oluşmadı:\n{log_path}")
            return

        try:
            import os
            os.startfile(log_path)
            self.preview_box.setPlainText(f"Güncel log dosyası açıldı:\n{log_path}")
        except Exception as exc:
            self.preview_box.setPlainText(f"Log dosyası açılamadı:\n{exc}")

    def _show_log_path(self) -> None:
        log_path = get_log_file_path()
        self.preview_box.setPlainText(f"Güncel log yolu:\n{log_path}")