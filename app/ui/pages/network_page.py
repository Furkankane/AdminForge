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


class NetworkPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._build_ui()
        self._apply_local_styles()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Ağ Araçları")
        title.setObjectName("networkTitle")

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Hedef gir... örn: google.com veya 8.8.8.8")

        top_row = QHBoxLayout()

        self.ping_button = QPushButton("Ping")
        self.ping_button.clicked.connect(self._run_ping)

        self.nslookup_button = QPushButton("Nslookup")
        self.nslookup_button.clicked.connect(self._run_nslookup)

        self.tracert_button = QPushButton("Tracert")
        self.tracert_button.clicked.connect(self._run_tracert)

        top_row.addWidget(self.target_input)
        top_row.addWidget(self.ping_button)
        top_row.addWidget(self.nslookup_button)
        top_row.addWidget(self.tracert_button)

        quick_title = QLabel("Hazır Ağ Komutları")
        quick_title.setObjectName("networkSectionTitle")

        quick_grid = QGridLayout()
        quick_grid.setSpacing(10)

        self._add_quick_button(quick_grid, "IP Config", "ipconfig /all", 0, 0)
        self._add_quick_button(quick_grid, "Netstat", "netstat -ano", 0, 1)
        self._add_quick_button(quick_grid, "ARP", "arp -a", 0, 2)
        self._add_quick_button(quick_grid, "Route Print", "route print", 1, 0)
        self._add_quick_button(quick_grid, "Flush DNS", "ipconfig /flushdns", 1, 1)
        self._add_quick_button(quick_grid, "Whoami", "whoami", 1, 2)

        output_title = QLabel("Çıktı")
        output_title.setObjectName("networkSectionTitle")

        self.output_box = QPlainTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Ağ komut çıktıları burada görünecek...")

        layout.addWidget(title)
        layout.addLayout(top_row)
        layout.addWidget(quick_title)
        layout.addLayout(quick_grid)
        layout.addWidget(output_title)
        layout.addWidget(self.output_box)

    def _apply_local_styles(self) -> None:
        self.setStyleSheet(
            """
            QLabel#networkTitle {
                font-size: 26px;
                font-weight: 700;
                color: #2b2b2b;
            }

            QLabel#networkSectionTitle {
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

    def _add_quick_button(self, layout: QGridLayout, text: str, command: str, row: int, col: int) -> None:
        button = QPushButton(text)
        button.clicked.connect(lambda _, c=command: self._execute(c))
        layout.addWidget(button, row, col)

    def _run_ping(self) -> None:
        target = self.target_input.text().strip()
        if not target:
            self.output_box.setPlainText("Ping için hedef gir.")
            return
        self._execute(f"ping {target}")

    def _run_nslookup(self) -> None:
        target = self.target_input.text().strip()
        if not target:
            self.output_box.setPlainText("Nslookup için hedef gir.")
            return
        self._execute(f"nslookup {target}")

    def _run_tracert(self) -> None:
        target = self.target_input.text().strip()
        if not target:
            self.output_box.setPlainText("Tracert için hedef gir.")
            return
        self._execute(f"tracert {target}")

    def _execute(self, command: str) -> None:
        self.output_box.setPlainText("Komut çalıştırılıyor...")
        result = run_command(command=command, shell="cmd", timeout=90)
        self.output_box.setPlainText(format_result(result))