from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QLineEdit
from config.settings import load_config, save_config, UI_TEXT

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 180)
        
        self.config = load_config()
        self.languages = ["한국어", "English(US)", "日本語", "중국어", "스페인어", "프랑스어"]
        self.ui_languages = ["한국어", "English(US)", "日本語"]
        
        self.init_ui()
        self.update_ui_texts()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # UI Language (Fixed label text to English)
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
        save_config(self.config)
        QMessageBox.information(self, texts["save_title"], texts["save_success"])
        self.hide()
