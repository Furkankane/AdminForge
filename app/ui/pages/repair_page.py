from __future__ import annotations

from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.core.command_runner import format_result, run_command


class RepairPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._build_ui()
        self._apply_local_styles()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Sistem Onarım")
        title.setObjectName("repairTitle")

        self.drive_input = QLineEdit()
        self.drive_input.setPlaceholderText("CHKDSK için sürücü gir... örn: C:")

        quick_title = QLabel("Onarım ve Bakım Araçları")
        quick_title.setObjectName("repairSectionTitle")

        grid = QGridLayout()
        grid.setSpacing(10)

        self._add_button(grid, "SFC /SCANNOW", lambda: self._execute("sfc /scannow"), 0, 0)
        self._add_button(grid, "DISM ScanHealth", lambda: self._execute("DISM /Online /Cleanup-Image /ScanHealth"), 0, 1)
        self._add_button(grid, "DISM RestoreHealth", lambda: self._execute("DISM /Online /Cleanup-Image /RestoreHealth"), 0, 2)

        self._add_button(grid, "GPUpdate /force", lambda: self._execute("gpupdate /force"), 1, 0)
        self._add_button(grid, "System Info", lambda: self._execute("systeminfo"), 1, 1)
        self._add_button(grid, "Whoami", lambda: self._execute("whoami"), 1, 2)

        self._add_button(grid, "CHKDSK /scan", self._run_chkdsk_scan, 2, 0)
        self._add_button(grid, "CHKDSK /f", self._run_chkdsk_fix, 2, 1)
        self._add_button(grid, "Temp Klasörü", lambda: self._execute("echo %TEMP%"), 2, 2)

        self._add_button(grid, "Services Console", lambda: self._execute("services.msc"), 3, 0)
        self._add_button(grid, "Event Viewer", lambda: self._execute("eventvwr"), 3, 1)
        self._add_button(grid, "Task Manager", lambda: self._execute("taskmgr"), 3, 2)

        output_title = QLabel("Çıktı")
        output_title.setObjectName("repairSectionTitle")

        self.output_box = QPlainTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Onarım komut çıktıları burada görünecek...")

        layout.addWidget(title)
        layout.addWidget(self.drive_input)
        layout.addWidget(quick_title)
        layout.addLayout(grid)
        layout.addWidget(output_title)
        layout.addWidget(self.output_box)

    def _apply_local_styles(self) -> None:
        self.setStyleSheet(
            """
            QLabel#repairTitle {
                font-size: 26px;
                font-weight: 700;
                color: #2b2b2b;
            }

            QLabel#repairSectionTitle {
                font-size: 15px;
                font-weight: 600;
                color: #2b2b2b;
                margin-top: 8px;
            }

            QLineEdit {
                min-height: 38px;
                padding: 8px 10px;
                border: 1px solid #cfc7bb;
                border-radius: 10px;
                background: #ffffff;
                color: #222222;
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

    def _add_button(self, layout: QGridLayout, text: str, callback, row: int, col: int) -> None:
        button = QPushButton(text)
        button.clicked.connect(callback)
        layout.addWidget(button, row, col)

    def _run_chkdsk_scan(self) -> None:
        drive = self.drive_input.text().strip()
        if not drive:
            self.output_box.setPlainText("CHKDSK için sürücü gir.")
            return
        self._execute(f"chkdsk {drive} /scan")

    def _run_chkdsk_fix(self) -> None:
        drive = self.drive_input.text().strip()
        if not drive:
            self.output_box.setPlainText("CHKDSK için sürücü gir.")
            return
        self._execute(f"chkdsk {drive} /f")

    def _execute(self, command: str) -> None:
        self.output_box.setPlainText("Komut çalıştırılıyor...")
        result = run_command(command=command, shell="cmd", timeout=120)
        self.output_box.setPlainText(format_result(result))