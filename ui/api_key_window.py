from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
import webbrowser

class ApiKeyWindow(QDialog):
    def __init__(self, config, save_callback=None):
        super().__init__()
        self.config = config
        self.save_callback = save_callback
        
        self.setWindowTitle("Gemini API Key Required")
        self.setFixedSize(400, 220)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        title_label = QLabel("Welcome to Discord Translation Overlay!")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(title_label)
        
        desc_label = QLabel(
            "To use this application, you need a free Google Gemini API Key.<br>"
            "Please get one from <a href='https://aistudio.google.com/app/apikey'>Google AI Studio</a>."
        )
        desc_label.setOpenExternalLinks(True)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter your GEMINI_API_KEY here...")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setText(self.config.get("gemini_api_key", ""))
        self.api_key_input.setStyleSheet("padding: 5px; font-size: 12px;")
        layout.addWidget(self.api_key_input)
        
        save_btn = QPushButton("Save && Continue")
        save_btn.setStyleSheet("padding: 8px; font-weight: bold;")
        save_btn.clicked.connect(self.save_key)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)
        
    def save_key(self):
        api_key = self.api_key_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Warning", "Please enter a valid API Key.")
            return
            
        self.config["gemini_api_key"] = api_key
        if self.save_callback:
            self.save_callback(self.config)
            
        QMessageBox.information(self, "Success", "API Key saved successfully!")
        self.accept()
