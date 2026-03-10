from __future__ import annotations

from PySide6.QtWidgets import QLabel, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget

from app.config import APP_AUTHOR, APP_NAME, APP_SIGNATURE, APP_VERSION


class SettingsPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._build_ui()
        self._apply_local_styles()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Ayarlar")
        title.setObjectName("settingsTitle")

        info_title = QLabel("Uygulama Bilgileri")
        info_title.setObjectName("settingsSectionTitle")

        self.info_box = QPlainTextEdit()
        self.info_box.setReadOnly(True)
        self._reload_info_text()

        self.reload_button = QPushButton("Bilgileri Yenile")
        self.reload_button.clicked.connect(self._reload_info)

        layout.addWidget(title)
        layout.addWidget(info_title)
        layout.addWidget(self.info_box)
        layout.addWidget(self.reload_button)
        layout.addStretch()

    def _apply_local_styles(self) -> None:
        self.setStyleSheet(
            """
            QLabel#settingsTitle {
                font-size: 26px;
                font-weight: 700;
                color: #2b2b2b;
            }

            QLabel#settingsSectionTitle {
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

    def _reload_info_text(self) -> None:
        self.info_box.setPlainText(
            f"Uygulama Adı : {APP_NAME}\n"
            f"Sürüm        : {APP_VERSION}\n"
            f"Yazar        : {APP_AUTHOR}\n"
            f"İmza         : {APP_SIGNATURE}\n"
            f"\n"
            f"Bu sayfa ileride tema, log seviyesi, varsayılan shell,\n"
            f"otomatik yenileme ve EXE build bilgileri için genişletilecek."
        )

    def _reload_info(self) -> None:
        self._reload_info_text()