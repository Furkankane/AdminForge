from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.config import WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from app.constants import SIDEBAR_ITEMS, WELCOME_SUBTITLE, WELCOME_TITLE
from app.services.system_service import get_system_snapshot
from app.ui.pages.disk_page import DiskPage
from app.ui.pages.network_page import NetworkPage
from app.ui.pages.repair_page import RepairPage
from app.ui.pages.reports_page import ReportsPage
from app.ui.pages.services_page import ServicesPage
from app.ui.pages.settings_page import SettingsPage
from app.ui.styles import APP_STYLESHEET
from app.ui.widgets.command_box import CommandBox
from app.ui.widgets.info_card import InfoCard


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self._build_ui()
        self._apply_styles()
        self._load_system_snapshot()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(12)

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(240)
        self.sidebar.addItems(SIDEBAR_ITEMS)
        self.sidebar.setCurrentRow(0)
        self.sidebar.currentRowChanged.connect(self._change_page)

        self.stack = QStackedWidget()

        dashboard_page = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_page)
        dashboard_layout.setContentsMargins(24, 24, 24, 24)
        dashboard_layout.setSpacing(12)

        self.title_label = QLabel(WELCOME_TITLE)
        self.title_label.setObjectName("titleLabel")

        self.subtitle_label = QLabel(WELCOME_SUBTITLE)
        self.subtitle_label.setObjectName("subtitleLabel")

        self.content_title = QLabel("Dashboard")
        self.content_title.setObjectName("contentTitle")

        self.content_info = QLabel("AdminForge dashboard yüklendi.")
        self.content_info.setObjectName("contentInfo")
        self.content_info.setWordWrap(True)
        self.content_info.setAlignment(Qt.AlignmentFlag.AlignTop)

        cards_layout = QGridLayout()

        self.card_computer = InfoCard("Bilgisayar", "Loading...")
        self.card_user = InfoCard("Kullanıcı", "Loading...")
        self.card_os = InfoCard("İşletim Sistemi", "Loading...")
        self.card_ip = InfoCard("IP Adresi", "Loading...")
        self.card_cpu = InfoCard("CPU", "Loading...")
        self.card_ram = InfoCard("RAM", "Loading...")
        self.card_license_status = InfoCard("Lisans Durumu", "Loading...")
        self.card_license_key = InfoCard("Lisans Key", "Loading...")

        cards_layout.addWidget(self.card_computer, 0, 0)
        cards_layout.addWidget(self.card_user, 0, 1)
        cards_layout.addWidget(self.card_os, 0, 2)
        cards_layout.addWidget(self.card_ip, 1, 0)
        cards_layout.addWidget(self.card_cpu, 1, 1)
        cards_layout.addWidget(self.card_ram, 1, 2)
        cards_layout.addWidget(self.card_license_status, 2, 0)
        cards_layout.addWidget(self.card_license_key, 2, 1, 1, 2)

        dashboard_layout.addWidget(self.title_label)
        dashboard_layout.addWidget(self.subtitle_label)
        dashboard_layout.addSpacing(24)
        dashboard_layout.addWidget(self.content_title)
        dashboard_layout.addWidget(self.content_info)
        dashboard_layout.addLayout(cards_layout)
        dashboard_layout.addStretch()

        command_page = QWidget()
        command_layout = QVBoxLayout(command_page)
        command_layout.setContentsMargins(0, 0, 0, 0)
        command_layout.addWidget(CommandBox())

        network_page = NetworkPage()
        disk_page = DiskPage()
        repair_page = RepairPage()
        services_page = ServicesPage()
        reports_page = ReportsPage()
        settings_page = SettingsPage()

        self.stack.addWidget(dashboard_page)   # 0
        self.stack.addWidget(command_page)     # 1
        self.stack.addWidget(network_page)     # 2
        self.stack.addWidget(disk_page)        # 3
        self.stack.addWidget(repair_page)      # 4
        self.stack.addWidget(services_page)    # 5
        self.stack.addWidget(reports_page)     # 6
        self.stack.addWidget(settings_page)    # 7

        root_layout.addWidget(self.sidebar)
        root_layout.addWidget(self.stack)

    def _change_page(self, index: int) -> None:
        if 0 <= index <= 7:
            self.stack.setCurrentIndex(index)

    def _load_system_snapshot(self) -> None:
        snapshot = get_system_snapshot()

        self.card_computer.value.setText(snapshot.computer_name)
        self.card_user.value.setText(snapshot.user_name)
        self.card_os.value.setText(snapshot.os_name)
        self.card_ip.value.setText(snapshot.ip_address)
        self.card_cpu.value.setText(snapshot.cpu_name)
        self.card_ram.value.setText(snapshot.ram_total_gb)
        self.card_license_status.value.setText(snapshot.license_status)
        self.card_license_key.value.setText(snapshot.license_key)

    def _apply_styles(self) -> None:
        self.setStyleSheet(APP_STYLESHEET)