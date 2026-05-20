from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QComboBox, QLabel, QApplication, QPushButton
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from config.settings import UI_TEXT, save_config

class LiveTranslatorWindow(QWidget):
    # 입력이 완료되었을 때 (1초 대기 후) 발생하는 시그널
    # 인자: 원문 텍스트, 출발 언어, 도착 언어
    translate_requested_signal = pyqtSignal(str, str, str)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
        self.update_ui_texts()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.resize(800, 500)
        
        # 디스코드 테마 스타일 적용 (다크 모드, 고대비, 깔끔한 모서리)
        self.setStyleSheet("""
            QWidget {
                background-color: #36393f;
                color: #dcddde;
                font-family: 'Malgun Gothic', 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #b9bbbe;
                font-size: 14px;
            }
            QComboBox {
                background-color: #202225;
                border: 1px solid #202225;
                border-radius: 4px;
                padding: 6px 10px;
                color: #dcddde;
                font-weight: bold;
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
            QTextEdit {
                background-color: #40444b;
                border: 1px solid #202225;
                border-radius: 8px;
                padding: 10px;
                color: #ffffff;
                font-size: 15px;
            }
            QTextEdit:focus {
                border: 1px solid #5865F2;
            }
            QTextEdit.pronunciation {
                background-color: #2f3136;
                color: #a3a6aa;
                font-size: 13px;
                border: 1px dashed #4f545c;
            }
            QPushButton {
                background-color: #5865F2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4752C4;
            }
            QPushButton:pressed {
                background-color: #3C45A5;
            }
            QPushButton:disabled {
                background-color: #3f4258;
                color: #72767d;
            }
            QScrollBar:vertical {
                border: none;
                background: #2f3136;
                width: 8px;
                margin: 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #202225;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #18191c;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # 메인 레이아웃 (좌/우 분할)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # ----------------- 왼쪽 영역 (입력) -----------------
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)
        
        left_top_layout = QHBoxLayout()
        self.src_lang_label = QLabel()
        self.src_lang_combo = QComboBox()
        self.src_lang_combo.addItems(["한국어", "日本語", "English", "中文"])
        src_lang = self.config.get("source_lang", "한국어")
        if src_lang in ["한국어", "日本語", "English", "中文"]:
            self.src_lang_combo.setCurrentText(src_lang)
            
        self.translate_btn = QPushButton()
        self.translate_btn.clicked.connect(self.request_translation)
        
        left_top_layout.addWidget(self.src_lang_label)
        left_top_layout.addWidget(self.src_lang_combo)
        left_top_layout.addStretch()
        left_top_layout.addWidget(self.translate_btn)
            
        self.src_input = QTextEdit()
        
        self.src_pronunciation = QTextEdit()
        self.src_pronunciation.setProperty("class", "pronunciation")
        self.src_pronunciation.setReadOnly(True)

        left_layout.addLayout(left_top_layout)
        left_layout.addWidget(self.src_input, 2) # 입력 영역 비율 2
        left_layout.addWidget(self.src_pronunciation, 1) # 발음 영역 비율 1

        # ----------------- 오른쪽 영역 (출력) -----------------
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        
        right_top_layout = QHBoxLayout()
        self.tgt_lang_label = QLabel()
        self.tgt_lang_combo = QComboBox()
        self.tgt_lang_combo.addItems(["한국어", "日本語", "English", "中文"])
        tgt_lang = self.config.get("target_lang", "日本語")
        if tgt_lang in ["한국어", "日本語", "English", "中文"]:
            self.tgt_lang_combo.setCurrentText(tgt_lang)
            
        self.copy_btn = QPushButton()
        self.copy_btn.clicked.connect(self.copy_result)
        
        right_top_layout.addWidget(self.tgt_lang_label)
        right_top_layout.addWidget(self.tgt_lang_combo)
        right_top_layout.addStretch()
        right_top_layout.addWidget(self.copy_btn)

        # 언어 선택 변경 시 실시간 반영 및 config 저장 연결
        self.src_lang_combo.currentTextChanged.connect(self.on_lang_changed)
        self.tgt_lang_combo.currentTextChanged.connect(self.on_lang_changed)
            
        self.tgt_output = QTextEdit()
        self.tgt_output.setReadOnly(True)
        
        self.tgt_pronunciation = QTextEdit()
        self.tgt_pronunciation.setProperty("class", "pronunciation")
        self.tgt_pronunciation.setReadOnly(True)

        right_layout.addLayout(right_top_layout)
        right_layout.addWidget(self.tgt_output, 2)
        right_layout.addWidget(self.tgt_pronunciation, 1)

        # 메인 레이아웃에 좌우 추가
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def request_translation(self):
        text = self.src_input.toPlainText().strip()
        if not text:
            # 입력이 지워졌으면 출력도 초기화
            self.tgt_output.clear()
            self.src_pronunciation.clear()
            self.tgt_pronunciation.clear()
            return
            
        src_lang = self.src_lang_combo.currentText()
        tgt_lang = self.tgt_lang_combo.currentText()
        
        # 번역 중 표시
        ui_lang = self.config.get("ui_lang", "한국어")
        if ui_lang not in UI_TEXT:
            ui_lang = "한국어"
        translating_text = UI_TEXT[ui_lang].get("translating", "번역 중...")
        self.tgt_output.setText(translating_text)
        
        # 컨트롤러로 시그널 전송
        self.translate_requested_signal.emit(text, src_lang, tgt_lang)

    def copy_result(self):
        text = self.tgt_output.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            
            # 복사 성공 시각적 피드백 표시
            ui_lang = self.config.get("ui_lang", "한국어")
            if ui_lang not in UI_TEXT:
                ui_lang = "한국어"
            
            copied_text = "복사 완료!" if ui_lang == "한국어" else ("コピー完了!" if ui_lang == "日本語" else "Copied!")
            original_btn_text = self.copy_btn.text()
            
            self.copy_btn.setText(copied_text)
            self.copy_btn.setEnabled(False)
            
            # 1초 뒤 원래 텍스트로 복원
            QTimer.singleShot(1000, lambda: self.reset_copy_btn(original_btn_text))
            
    def reset_copy_btn(self, original_text):
        self.copy_btn.setText(original_text)
        self.copy_btn.setEnabled(True)

    def update_result(self, translated_text: str, src_pronunciation: str, tgt_pronunciation: str):
        # 메인 컨트롤러에서 번역 결과를 받아 UI 업데이트
        self.tgt_output.setText(translated_text)
        self.src_pronunciation.setText(f"[발음]\n{src_pronunciation}" if src_pronunciation else "")
        self.tgt_pronunciation.setText(f"[발음]\n{tgt_pronunciation}" if tgt_pronunciation else "")

    def showEvent(self, event):
        super().showEvent(event)
        # 화면의 우측 하단에 위치하도록 이동
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        x = screen_geometry.width() - self.width() - 50
        y = screen_geometry.height() - self.height() - 50
        self.move(x, y)

    def reload_config(self, new_config):
        self.config = new_config
        # 설정 갱신 시 시그널 루프 방지를 위해 임시 차단
        self.src_lang_combo.blockSignals(True)
        self.tgt_lang_combo.blockSignals(True)
        
        src_lang = self.config.get("source_lang")
        if src_lang and self.src_lang_combo.findText(src_lang) >= 0:
            self.src_lang_combo.setCurrentText(src_lang)
            
        tgt_lang = self.config.get("target_lang")
        if tgt_lang and self.tgt_lang_combo.findText(tgt_lang) >= 0:
            self.tgt_lang_combo.setCurrentText(tgt_lang)
            
        self.src_lang_combo.blockSignals(False)
        self.tgt_lang_combo.blockSignals(False)
        
        self.update_ui_texts()

    def on_lang_changed(self):
        self.config["source_lang"] = self.src_lang_combo.currentText()
        self.config["target_lang"] = self.tgt_lang_combo.currentText()
        save_config(self.config)

    def update_ui_texts(self):
        ui_lang = self.config.get("ui_lang", "한국어")
        if ui_lang not in UI_TEXT:
            ui_lang = "한국어"
            
        texts = UI_TEXT[ui_lang]
        self.setWindowTitle(texts.get("live_title", "실시간 번역 (Live Translator)"))
        self.src_lang_label.setText(texts.get("src_lang", "탐지할 언어:"))
        self.tgt_lang_label.setText(texts.get("tgt_lang", "번역결과 언어:"))
        self.src_input.setPlaceholderText(texts.get("live_src_ph", "번역할 내용을 입력하세요..."))
        self.src_pronunciation.setPlaceholderText(texts.get("live_src_pron_ph", "원문의 발음이 여기에 표시됩니다."))
        self.tgt_output.setPlaceholderText(texts.get("live_tgt_ph", "번역 결과가 표시됩니다."))
        self.tgt_pronunciation.setPlaceholderText(texts.get("live_tgt_pron_ph", "번역된 결과의 발음이 여기에 표시됩니다."))
        self.translate_btn.setText(texts.get("live_translate_btn", "번역하기"))
        self.copy_btn.setText(texts.get("live_copy_btn", "복사"))
