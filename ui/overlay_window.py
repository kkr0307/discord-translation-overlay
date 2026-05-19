from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPalette

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 윈도우 속성 설정: 타이틀바 없음, 최상단, 투명 배경, 작업표시줄 숨김
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.init_ui()
        self.current_opacity = 1.0

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.text_label = QLabel("번역 결과")
        self.text_label.setStyleSheet("""
            QLabel {
                background-color: rgba(25, 25, 30, 240);
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 12px;
                padding: 16px 24px;
                font-family: 'Malgun Gothic', 'Segoe UI', sans-serif;
                font-size: 18px;
                font-weight: 500;
            }
        """)
        # 박스 크기를 텍스트 길이에 맞춰 동적으로 확장되도록 WordWrap 해제 (같은 줄이면 같은 줄에 뜨게 됨)
        self.text_label.setWordWrap(False)
        
        # 고급스러운 그림자 효과 추가
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 8)
        self.text_label.setGraphicsEffect(shadow)
        
        layout.addWidget(self.text_label)
        self.setLayout(layout)

    def show_translation(self, text: str, x: int, y: int, font_size: int = 18, offset_x: int = 10, offset_y: int = 10):
        # 폰트 크기에 비례하여 패딩과 모서리 둥글기를 동적 계산
        padding_v = max(8, font_size // 2)
        padding_h = max(12, int(font_size * 0.8))
        border_radius = max(6, font_size // 2)
        
        self.text_label.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(25, 25, 30, 240);
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: {border_radius}px;
                padding: {padding_v}px {padding_h}px;
                font-family: 'Malgun Gothic', 'Segoe UI', sans-serif;
                font-size: {font_size}px;
                font-weight: 500;
            }}
        """)
        
        self.text_label.setText(text)
        self.adjustSize()
        
        # 팝업 박스의 "배경 테두리 상단"이 드래그 상단(y)과 일치하도록 오프셋 보정
        pos_x = x + offset_x
        pos_y = y - offset_y
        self.move(pos_x, pos_y)
        
        self.current_opacity = 1.0
        self.setWindowOpacity(self.current_opacity)
        self.show()

    def hide_translation(self):
        # 즉시 창을 숨김
        self.hide()
