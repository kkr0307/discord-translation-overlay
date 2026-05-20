from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QLineEdit
from PyQt6.QtCore import pyqtSignal
from config.settings import load_config, save_config, UI_TEXT

class SettingsWindow(QWidget):
    open_live_window_signal = pyqtSignal()
    settings_saved_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 310)
        
        self.config = load_config()
        self.languages = ["한국어", "English(US)", "日本語", "중국어", "스페인어", "프랑스어"]
        self.ui_languages = ["한국어", "English(US)", "日本語"]
        
        self.init_ui()
        self.update_ui_texts()
        
    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #36393f;
                color: #dcddde;
                font-family: 'Malgun Gothic', 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #dcddde;
            }
            QLineEdit {
                background-color: #202225;
                border: 1px solid #202225;
                border-radius: 4px;
                padding: 6px 10px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 1px solid #5865F2;
            }
            QComboBox {
                background-color: #202225;
                border: 1px solid #202225;
                border-radius: 4px;
                padding: 6px 10px;
                color: #dcddde;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #2f3136;
                color: #dcddde;
                selection-background-color: #5865F2;
                border: 1px solid #202225;
            }
            QPushButton {
                background-color: #5865F2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4752C4;
            }
            QPushButton:pressed {
                background-color: #3C45A5;
            }
            QPushButton#open_live_btn {
                background-color: #4f545c;
            }
            QPushButton#open_live_btn:hover {
                background-color: #686d73;
            }
            QPushButton#open_live_btn:pressed {
                background-color: #43474e;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # UI Language
        ui_lang_layout = QHBoxLayout()
        self.ui_lang_label = QLabel("UI Language:")
        self.ui_lang_combo = QComboBox()
        self.ui_lang_combo.addItems(self.ui_languages)
        self.ui_lang_combo.setCurrentText(self.config.get("ui_lang", "한국어"))
        self.ui_lang_combo.currentTextChanged.connect(self.update_ui_texts)
        ui_lang_layout.addWidget(self.ui_lang_label)
        ui_lang_layout.addWidget(self.ui_lang_combo)
        layout.addLayout(ui_lang_layout)
        
        # API Key
        api_layout = QHBoxLayout()
        self.api_label = QLabel()
        self.api_input = QLineEdit()
        self.api_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_input.setText(self.config.get("gemini_api_key", ""))
        api_layout.addWidget(self.api_label)
        api_layout.addWidget(self.api_input)
        layout.addLayout(api_layout)
        
        # Source Language
        src_layout = QHBoxLayout()
        self.src_label = QLabel()
        self.src_combo = QComboBox()
        self.src_combo.addItems(self.languages)
        self.src_combo.setCurrentText(self.config.get("source_lang", "日本語"))
        src_layout.addWidget(self.src_label)
        src_layout.addWidget(self.src_combo)
        layout.addLayout(src_layout)
        
        # Target Language
        tgt_layout = QHBoxLayout()
        self.tgt_label = QLabel()
        self.tgt_combo = QComboBox()
        self.tgt_combo.addItems(self.languages)
        self.tgt_combo.setCurrentText(self.config.get("target_lang", "한국어"))
        tgt_layout.addWidget(self.tgt_label)
        tgt_layout.addWidget(self.tgt_combo)
        layout.addLayout(tgt_layout)
        
        # Font Size
        font_layout = QHBoxLayout()
        self.font_size_label = QLabel()
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems([str(i) for i in [12, 14, 16, 18, 20, 24, 28, 32]])
        self.font_size_combo.setCurrentText(str(self.config.get("font_size", 16)))
        font_layout.addWidget(self.font_size_label)
        font_layout.addWidget(self.font_size_combo)
        layout.addLayout(font_layout)
        
        # Open Live Window Button
        self.open_live_btn = QPushButton()
        self.open_live_btn.setObjectName("open_live_btn")
        self.open_live_btn.clicked.connect(self.open_live_window_signal.emit)
        layout.addWidget(self.open_live_btn)
        
        # Save Button
        self.save_btn = QPushButton()
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)
        
        self.setLayout(layout)
        
    def update_ui_texts(self):
        ui_lang = self.ui_lang_combo.currentText()
        if ui_lang not in UI_TEXT:
            ui_lang = "한국어"
            
        texts = UI_TEXT[ui_lang]
        self.setWindowTitle(texts["window_title"])
        self.api_label.setText(texts["api_key"])
        self.src_label.setText(texts["src_lang"])
        self.tgt_label.setText(texts["tgt_lang"])
        self.font_size_label.setText(texts["font_size"])
        self.open_live_btn.setText(texts.get("open_live", "실시간 번역창 열기"))
        self.save_btn.setText(texts["save"])

    def save_settings(self):
        ui_lang = self.ui_lang_combo.currentText()
        if ui_lang not in UI_TEXT:
            ui_lang = "한국어"
        texts = UI_TEXT[ui_lang]
        
        self.config["ui_lang"] = ui_lang
        self.config["gemini_api_key"] = self.api_input.text().strip()
        self.config["source_lang"] = self.src_combo.currentText()
        self.config["target_lang"] = self.tgt_combo.currentText()
        self.config["font_size"] = int(self.font_size_combo.currentText())
        save_config(self.config)
        self.settings_saved_signal.emit()
        QMessageBox.information(self, texts["save_title"], texts["save_success"])
        self.hide()
