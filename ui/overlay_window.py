from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect, QApplication
from PyQt6.QtCore import Qt, QTimer, QPoint
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
                font-weight: bold;
            }}
        """)
        
        translation_lines = []
        pronunciation_lines = []
        current_mode = None
        
        for line in text.strip().split('\n'):
            stripped = line.strip()
            if stripped.startswith("[번역]"):
                current_mode = "translation"
                content = stripped.replace("[번역]", "").strip()
                if content:
                    translation_lines.append(content)
                continue
            elif stripped.startswith("[발음]"):
                current_mode = "pronunciation"
                content = stripped.replace("[발음]", "").strip()
                if content:
                    pronunciation_lines.append(content)
                continue
                
            if current_mode == "translation":
                translation_lines.append(stripped)
            elif current_mode == "pronunciation":
                pronunciation_lines.append(stripped)
                
        translation_html = "<br>".join([line for line in translation_lines if line])
        pronunciation_html = "<br>".join([line for line in pronunciation_lines if line])
                
        if translation_html and pronunciation_html:
            # 위 아래를 명확하게 구분하기 위해 구분선(border-top)과 여백을 추가
            formatted_text = f"""
            <div style='margin-bottom: 8px;'>{translation_html}</div>
            <div style='
                font-size: {max(11, int(font_size * 0.75))}px; 
                color: #AAB8C2; 
                font-weight: normal;
                border-top: 1px solid rgba(255, 255, 255, 40);
                padding-top: 8px;
            '>{pronunciation_html}</div>
            """
            self.text_label.setText(formatted_text)
        else:
            self.text_label.setText(text.replace('\n', '<br>'))
            
        self.adjustSize()
        
        # 화면 경계 이탈 방지 보정 (오른쪽/아래로 잘리는 현상 차단)
        screen = QApplication.screenAt(QPoint(int(x), int(y)))
        if not screen:
            screen = QApplication.primaryScreen()
        screen_geo = screen.availableGeometry()
        
        pos_x = x + offset_x
        pos_y = y - offset_y
        
        # 우측 경계 초과 시 보정
        if pos_x + self.width() > screen_geo.right():
            pos_x = screen_geo.right() - self.width() - 15
            
        # 좌측 경계 초과 시 보정
        if pos_x < screen_geo.left():
            pos_x = screen_geo.left() + 15
            
        # 하단 경계 초과 시 보정
        if pos_y + self.height() > screen_geo.bottom():
            pos_y = screen_geo.bottom() - self.height() - 15
            
        # 상단 경계 초과 시 보정
        if pos_y < screen_geo.top():
            pos_y = screen_geo.top() + 15
            
        self.move(int(pos_x), int(pos_y))
        
        self.current_opacity = 1.0
        self.setWindowOpacity(self.current_opacity)
        self.show()

    def hide_translation(self):
        # 즉시 창을 숨김
        self.hide()
