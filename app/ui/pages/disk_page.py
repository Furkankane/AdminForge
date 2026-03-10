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


class DiskPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._build_ui()
        self._apply_local_styles()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Disk / Depolama")
        title.setObjectName("diskTitle")

        self.drive_input = QLineEdit()
        self.drive_input.setPlaceholderText("Sürücü gir... örn: C: veya D:")

        top_row = QHBoxLayout()

        self.chk_scan_button = QPushButton("CHKDSK /scan")
        self.chk_scan_button.clicked.connect(self._run_chkdsk_scan)

        self.chk_fix_button = QPushButton("CHKDSK /f")
        self.chk_fix_button.clicked.connect(self._run_chkdsk_fix)

        top_row.addWidget(self.drive_input)
        top_row.addWidget(self.chk_scan_button)
        top_row.addWidget(self.chk_fix_button)

        quick_title = QLabel("Hazır Disk Komutları")
        quick_title.setObjectName("diskSectionTitle")

        quick_grid = QGridLayout()
        quick_grid.setSpacing(10)

        self._add_quick_button(quick_grid, "Diskleri Listele", "wmic diskdrive get model,size,status", "cmd", 0, 0)
        self._add_quick_button(quick_grid, "Mantıksal Diskler", "wmic logicaldisk get caption,description,freespace,size", "cmd", 0, 1)
        self._add_quick_button(quick_grid, "Volume Bilgisi", "vol", "cmd", 0, 2)

        self._add_quick_button(quick_grid, "List Disk", "list disk", "diskpart", 1, 0)
        self._add_quick_button(quick_grid, "List Volume", "list volume", "diskpart", 1, 1)
        self._add_quick_button(quick_grid, "List Partition", "list partition", "diskpart", 1, 2)

        self._add_quick_button(quick_grid, "Disk Kullanımı", "Get-PSDrive -PSProvider FileSystem", "powershell", 2, 0)
        self._add_quick_button(quick_grid, "Temp Klasörü", "echo %TEMP%", "cmd", 2, 1)
        self._add_quick_button(quick_grid, "Sürücü Ağacı", "wmic volume get driveletter,label,capacity,freespace", "cmd", 2, 2)

        output_title = QLabel("Çıktı")
        output_title.setObjectName("diskSectionTitle")

        self.output_box = QPlainTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Disk ve depolama çıktıları burada görünecek...")

        layout.addWidget(title)
        layout.addLayout(top_row)
        layout.addWidget(quick_title)
        layout.addLayout(quick_grid)
        layout.addWidget(output_title)
        layout.addWidget(self.output_box)

    def _apply_local_styles(self) -> None:
        self.setStyleSheet(
            """
            QLabel#diskTitle {
                font-size: 26px;
                font-weight: 700;
                color: #2b2b2b;
            }

            QLabel#diskSectionTitle {
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
        button.clicked.connect(lambda _, c=command, s=shell: self._execute(c, s))
        layout.addWidget(button, row, col)

    def _run_chkdsk_scan(self) -> None:
        drive = self.drive_input.text().strip()
        if not drive:
            self.output_box.setPlainText("CHKDSK için sürücü gir.")
            return
        self._execute(f"chkdsk {drive} /scan", "cmd")

    def _run_chkdsk_fix(self) -> None:
        drive = self.drive_input.text().strip()
        if not drive:
            self.output_box.setPlainText("CHKDSK için sürücü gir.")
            return
        self._execute(f"chkdsk {drive} /f", "cmd")

    def _run_diskpart_script(self, script_text: str) -> None:
        import tempfile
        from pathlib import Path

        self.output_box.setPlainText("DiskPart komutu çalıştırılıyor...")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp_file:
            temp_file.write(script_text + "\n")
            temp_file.write("exit\n")
            temp_path = Path(temp_file.name)

        result = run_command(f'diskpart /s "{temp_path}"', shell="cmd", timeout=90)
        self.output_box.setPlainText(format_result(result))

        try:
            temp_path.unlink(missing_ok=True)
        except Exception:
            pass

    def _execute(self, command: str, shell: str) -> None:
        if shell == "diskpart":
            self._run_diskpart_script(command)
            return

        self.output_box.setPlainText("Komut çalıştırılıyor...")
        result = run_command(command=command, shell=shell, timeout=90)
        self.output_box.setPlainText(format_result(result))