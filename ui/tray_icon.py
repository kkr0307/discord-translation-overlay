from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor

class TrayIcon(QSystemTrayIcon):
    def __init__(self, settings_window, app_quit_callback, parent=None):
        super().__init__(parent)
        self.settings_window = settings_window
        self.app_quit_callback = app_quit_callback
        
        # 기본 아이콘 생성 (간단한 색상 사각형)
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor("transparent"))
        painter = QPainter(pixmap)
        painter.setBrush(QColor("#7289DA")) # Discord 비슷한 색상
        painter.drawRoundedRect(2, 2, 28, 28, 5, 5)
        painter.end()
        self.setIcon(QIcon(pixmap))
        
        # 언어 설정 로드
        from config.settings import UI_TEXT
        ui_lang = self.settings_window.config.get("ui_lang", "한국어")
        texts = UI_TEXT.get(ui_lang, UI_TEXT["한국어"])
        
        # 메뉴 구성
        self.menu = QMenu()
        
        settings_action = self.menu.addAction(texts["settings"])
        settings_action.triggered.connect(self.show_settings)
        
        self.menu.addSeparator()
        
        quit_action = self.menu.addAction(texts["quit"])
        quit_action.triggered.connect(self.quit_app)
        
        self.setContextMenu(self.menu)
        
        # 더블클릭 이벤트 연결
        self.activated.connect(self.on_tray_icon_activated)
        
    def show_settings(self):
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def quit_app(self):
        self.app_quit_callback()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_settings()
