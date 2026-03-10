APP_STYLESHEET = """
QMainWindow {
    background: #1f2329;
}

QWidget {
    color: #e6edf3;
    font-size: 13px;
}

QFrame {
    background: #262b33;
    border: 1px solid #3a414b;
    border-radius: 16px;
}

QLabel {
    color: #e6edf3;
    background: transparent;
    border: none;
}

QLabel#titleLabel {
    font-size: 30px;
    font-weight: 700;
    color: #f0f6fc;
}

QLabel#subtitleLabel {
    font-size: 14px;
    color: #9da7b3;
}

QLabel#contentTitle {
    font-size: 22px;
    font-weight: 600;
    color: #f0f6fc;
}

QLabel#contentInfo {
    font-size: 14px;
    color: #b8c0cc;
}

QListWidget {
    background: #262b33;
    border: 1px solid #3a414b;
    border-radius: 16px;
    padding: 10px;
    font-size: 14px;
    color: #e6edf3;
    outline: none;
}

QListWidget::item {
    padding: 12px 10px;
    border-radius: 10px;
    margin-bottom: 4px;
}

QListWidget::item:hover {
    background: #30363d;
}

QListWidget::item:selected {
    background: #2f81f7;
    color: #ffffff;
    font-weight: 600;
}

QFrame#infoCard {
    background: #2d333b;
    border: 1px solid #3a414b;
    border-radius: 14px;
    padding: 16px;
}

QLabel#cardTitle {
    font-size: 12px;
    color: #9da7b3;
}

QLabel#cardValue {
    font-size: 18px;
    font-weight: 600;
    color: #f0f6fc;
}

QPushButton {
    min-height: 38px;
    padding: 8px 14px;
    border: 1px solid #3a414b;
    border-radius: 10px;
    background: #2d333b;
    color: #e6edf3;
    font-weight: 600;
}

QPushButton:hover {
    background: #36404a;
}

QPushButton:pressed {
    background: #414b57;
}

QLineEdit, QPlainTextEdit, QComboBox {
    background: #22272e;
    color: #e6edf3;
    border: 1px solid #3a414b;
    border-radius: 10px;
    padding: 8px 10px;
    selection-background-color: #2f81f7;
    selection-color: #ffffff;
}

QPlainTextEdit {
    border-radius: 12px;
}

QComboBox {
    min-height: 38px;
    padding: 6px 10px;
}

QComboBox QAbstractItemView {
    background: #22272e;
    color: #e6edf3;
    border: 1px solid #3a414b;
    selection-background-color: #2f81f7;
    selection-color: #ffffff;
}

QLabel#commandTitle,
QLabel#networkTitle,
QLabel#diskTitle,
QLabel#repairTitle,
QLabel#servicesTitle,
QLabel#reportsTitle,
QLabel#settingsTitle {
    font-size: 26px;
    font-weight: 700;
    color: #f0f6fc;
}

QLabel#commandSectionTitle,
QLabel#networkSectionTitle,
QLabel#diskSectionTitle,
QLabel#repairSectionTitle,
QLabel#servicesSectionTitle,
QLabel#reportsSectionTitle,
QLabel#settingsSectionTitle,
QLabel#sectionTitle {
    font-size: 15px;
    font-weight: 600;
    color: #c9d1d9;
    margin-top: 8px;
}
"""