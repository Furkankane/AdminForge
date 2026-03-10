from __future__ import annotations

from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.core.command_runner import format_result, run_command


class ServicesPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._build_ui()
        self._apply_local_styles()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Servisler")
        title.setObjectName("servicesTitle")

        top_row = QHBoxLayout()

        self.service_input = QLineEdit()
        self.service_input.setPlaceholderText("Servis adı gir... örn: Spooler")

        self.status_button = QPushButton("Durum")
        self.status_button.clicked.connect(self._service_status)

        self.start_button = QPushButton("Başlat")
        self.start_button.clicked.connect(self._service_start)

        self.stop_button = QPushButton("Durdur")
        self.stop_button.clicked.connect(self._service_stop)

        top_row.addWidget(self.service_input)
        top_row.addWidget(self.status_button)
        top_row.addWidget(self.start_button)
        top_row.addWidget(self.stop_button)

        quick_title = QLabel("Hazır Servis Komutları")
        quick_title.setObjectName("servicesSectionTitle")

        grid = QGridLayout()
        grid.setSpacing(10)

        self._add_button(grid, "Çalışan Servisler", lambda: self._execute_powershell("Get-Service | Where-Object {$_.Status -eq 'Running'} | Sort-Object Name"), 0, 0)
        self._add_button(grid, "Duran Servisler", lambda: self._execute_powershell("Get-Service | Where-Object {$_.Status -eq 'Stopped'} | Sort-Object Name"), 0, 1)
        self._add_button(grid, "Tüm Servisler", lambda: self._execute("sc query state= all"), 0, 2)

        self._add_button(grid, "Get-Service", lambda: self._execute_powershell("Get-Service"), 1, 0)
        self._add_button(grid, "Services.msc", lambda: self._execute("services.msc"), 1, 1)
        self._add_button(grid, "Tasklist", lambda: self._execute("tasklist"), 1, 2)

        output_title = QLabel("Çıktı")
        output_title.setObjectName("servicesSectionTitle")

        self.output_box = QPlainTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Servis çıktıları burada görünecek...")

        layout.addWidget(title)
        layout.addLayout(top_row)
        layout.addWidget(quick_title)
        layout.addLayout(grid)
        layout.addWidget(output_title)
        layout.addWidget(self.output_box)

    def _apply_local_styles(self) -> None:
        self.setStyleSheet(
            """
            QLabel#servicesTitle {
                font-size: 26px;
                font-weight: 700;
                color: #2b2b2b;
            }

            QLabel#servicesSectionTitle {
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

    def _service_status(self) -> None:
        name = self.service_input.text().strip()
        if not name:
            self.output_box.setPlainText("Servis adı gir.")
            return
        self._execute_powershell(f"Get-Service -Name '{name}' | Format-List *")

    def _service_start(self) -> None:
        name = self.service_input.text().strip()
        if not name:
            self.output_box.setPlainText("Servis adı gir.")
            return
        self._execute_powershell(f"Start-Service -Name '{name}'; Get-Service -Name '{name}'")

    def _service_stop(self) -> None:
        name = self.service_input.text().strip()
        if not name:
            self.output_box.setPlainText("Servis adı gir.")
            return
        self._execute_powershell(f"Stop-Service -Name '{name}' -Force; Get-Service -Name '{name}'")

    def _execute(self, command: str) -> None:
        self.output_box.setPlainText("Komut çalıştırılıyor...")
        result = run_command(command=command, shell="cmd", timeout=120)
        self.output_box.setPlainText(format_result(result))

    def _execute_powershell(self, command: str) -> None:
        self.output_box.setPlainText("PowerShell komutu çalıştırılıyor...")
        result = run_command(command=command, shell="powershell", timeout=120)
        self.output_box.setPlainText(format_result(result))