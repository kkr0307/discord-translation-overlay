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
        self.setStyleSheet("""
            QDialog {
                background-color: #36393f;
                color: #dcddde;
                font-family: 'Malgun Gothic', 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #dcddde;
            }
            QLineEdit {
                background-color: #202225;
                border: 1px solid #202225;
                border-radius: 6px;
                padding: 8px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #5865F2;
            }
            QPushButton {
                background-color: #5865F2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4752C4;
            }
            QPushButton:pressed {
                background-color: #3C45A5;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel("Welcome to Discord Translation Overlay!")
        title_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title_label)
        
        desc_label = QLabel(
            "To use this application, you need a free Google Gemini API Key.<br>"
            "Please get one from <a href='https://aistudio.google.com/app/apikey' style='color: #00b0f4; text-decoration: none; font-weight: bold;'>Google AI Studio</a>."
        )
        desc_label.setOpenExternalLinks(True)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-size: 13px; line-height: 1.4;")
        layout.addWidget(desc_label)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter your GEMINI_API_KEY here...")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setText(self.config.get("gemini_api_key", ""))
        layout.addWidget(self.api_key_input)
        
        save_btn = QPushButton("Save & Continue")
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
