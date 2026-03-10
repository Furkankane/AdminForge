from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.core.command_runner import format_result, run_command


class CommandBox(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._build_ui()
        self._apply_local_styles()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Komut Merkezi")
        title.setObjectName("commandTitle")

        top_row = QHBoxLayout()

        self.shell_select = QComboBox()
        self.shell_select.addItems(["cmd", "powershell"])
        self.shell_select.setFixedWidth(160)

        self.run_button = QPushButton("Çalıştır")
        self.run_button.clicked.connect(self._run_command)

        self.clear_button = QPushButton("Temizle")
        self.clear_button.clicked.connect(self._clear_output)

        top_row.addWidget(self.shell_select)
        top_row.addWidget(self.run_button)
        top_row.addWidget(self.clear_button)
        top_row.addStretch()

        self.command_input = QPlainTextEdit()
        self.command_input.setPlaceholderText("Komut gir... örn: ipconfig /all")
        self.command_input.setFixedHeight(100)

        quick_title = QLabel("Hazır Komutlar")
        quick_title.setObjectName("commandSectionTitle")

        quick_grid = QGridLayout()
        quick_grid.setSpacing(10)

        self._add_quick_button(quick_grid, "IP Config", "ipconfig /all", "cmd", 0, 0)
        self._add_quick_button(quick_grid, "Ping Google", "ping google.com", "cmd", 0, 1)
        self._add_quick_button(quick_grid, "System Info", "systeminfo", "cmd", 0, 2)
        self._add_quick_button(quick_grid, "Whoami", "whoami", "cmd", 1, 0)
        self._add_quick_button(quick_grid, "GPUpdate", "gpupdate /force", "cmd", 1, 1)
        self._add_quick_button(quick_grid, "Get-Date", "Get-Date", "powershell", 1, 2)
        self._add_quick_button(quick_grid, "Get-Service", "Get-Service", "powershell", 2, 0)
        self._add_quick_button(quick_grid, "Netstat", "netstat -ano", "cmd", 2, 1)
        self._add_quick_button(quick_grid, "Hostname", "hostname", "cmd", 2, 2)

        output_title = QLabel("Çıktı")
        output_title.setObjectName("commandSectionTitle")

        self.output_box = QPlainTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Çıktı burada görünecek...")

        layout.addWidget(title)
        layout.addLayout(top_row)
        layout.addWidget(self.command_input)
        layout.addWidget(quick_title)
        layout.addLayout(quick_grid)
        layout.addWidget(output_title)
        layout.addWidget(self.output_box)

    def _apply_local_styles(self) -> None:
        self.setStyleSheet(
            """
            QLabel#commandTitle {
                font-size: 26px;
                font-weight: 700;
                color: #2b2b2b;
            }

            QLabel#commandSectionTitle {
                font-size: 15px;
                font-weight: 600;
                color: #2b2b2b;
                margin-top: 8px;
            }

            QComboBox {
                min-height: 38px;
                padding: 6px 10px;
                border: 1px solid #cfc7bb;
                border-radius: 10px;
                background: #ffffff;
                color: #222222;
            }

            QPlainTextEdit {
                background: #ffffff;
                color: #111111;
                border: 1px solid #cfc7bb;
                border-radius: 12px;
                padding: 8px;
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
            """
        )

    def _add_quick_button(
        self,
        layout: QGridLayout,
        text: str,
        command: str,
        shell: str,
        row: int,
        col: int,
    ) -> None:
        button = QPushButton(text)
        button.clicked.connect(lambda _, c=command, s=shell: self._run_preset_command(c, s))
        layout.addWidget(button, row, col)

    def _run_preset_command(self, command: str, shell: str) -> None:
        self.shell_select.setCurrentText(shell)
        self.command_input.setPlainText(command)
        self._execute(command, shell)

    def _run_command(self) -> None:
        command = self.command_input.toPlainText().strip()
        shell = self.shell_select.currentText()
        self._execute(command, shell)

    def _execute(self, command: str, shell: str) -> None:
        if not command:
            self.output_box.setPlainText("Komut boş olamaz.")
            return

        self.output_box.setPlainText("Komut çalıştırılıyor...")
        result = run_command(command=command, shell=shell, timeout=60)
        self.output_box.setPlainText(format_result(result))

    def _clear_output(self) -> None:
        self.output_box.clear()