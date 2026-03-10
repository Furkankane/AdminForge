import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from app.core.admin import is_admin, relaunch_as_admin
from app.ui.main_window import MainWindow


def main() -> int:
    if not is_admin():
        ok = relaunch_as_admin()
        if ok:
            return 0

        app = QApplication(sys.argv)
        QMessageBox.critical(None, "AdminForge", "Yönetici olarak başlatılamadı.")
        return 1

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())