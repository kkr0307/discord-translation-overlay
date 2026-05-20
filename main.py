import sys
import asyncio
import threading
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal

from core.input_handler import MouseDragHandler
from core.text_extractor import extract_text_from_selection
from core.translator import Translator
from ui.overlay_window import OverlayWindow
from ui.settings_window import SettingsWindow
from ui.tray_icon import TrayIcon
from ui.api_key_window import ApiKeyWindow
from ui.live_window import LiveTranslatorWindow
from ui.update_dialog import UpdateController
from config.settings import save_config, APP_VERSION, GITHUB_REPO
from core.updater import check_for_updates

class AppController(QObject):
    # 스레드 간 안전한 데이터 전달을 위한 커스텀 시그널
    drag_completed_signal = pyqtSignal(int, int, int)
    mouse_clicked_signal = pyqtSignal()
    text_extracted_signal = pyqtSignal(str, int, int, int)
    translation_completed_signal = pyqtSignal(str, int, int, int, int) # text, x, y, font_size, req_id
    live_translation_completed_signal = pyqtSignal(dict, int) # result_dict, req_id

    def __init__(self):
        super().__init__()
        self.settings_window = SettingsWindow()
        self.overlay_window = OverlayWindow()
        self.translator = Translator()
        self.current_request_id = 0
        self.current_live_request_id = 0
        
        self.live_window = LiveTranslatorWindow(self.settings_window.config)
        
        # 시그널 연결
        self.drag_completed_signal.connect(self.on_drag_completed_slot)
        self.mouse_clicked_signal.connect(self.overlay_window.hide_translation)
        self.text_extracted_signal.connect(self.on_text_extracted_slot)
        self.translation_completed_signal.connect(self.on_translation_completed_slot)
        
        self.live_window.translate_requested_signal.connect(self.on_live_translate_requested)
        self.live_translation_completed_signal.connect(self.on_live_translation_completed)
        self.settings_window.open_live_window_signal.connect(self.show_live_window)
        self.settings_window.settings_saved_signal.connect(self.on_settings_saved)
        
        self.mouse_handler = None
        
    def on_settings_saved(self):
        self.live_window.reload_config(self.settings_window.config)
        
    def show_live_window(self):
        self.live_window.show()
        self.live_window.raise_()
        self.live_window.activateWindow()
        
    def start_hook(self):
        # 마우스 훅 시작
        drag_distance = self.settings_window.config.get("drag_min_distance", 10)
        self.mouse_handler = MouseDragHandler(
            on_drag_complete_callback=self.on_mouse_dragged,
            on_click_callback=self.on_mouse_clicked,
            min_distance=drag_distance
        )
        self.mouse_handler.start()

    def on_mouse_clicked(self):
        # pynput 백그라운드 스레드에서 클릭 감지 시 호출됨
        self.mouse_clicked_signal.emit()

    def on_mouse_dragged(self, x, y, bottom_y):
        # pynput 백그라운드 스레드에서 호출됨 -> 메인 스레드로 전달
        self.drag_completed_signal.emit(int(x), int(y), int(bottom_y))
        
    def on_drag_completed_slot(self, x, y, bottom_y):
        # UI 메인 스레드에서 실행
        # 텍스트 추출 작업 (I/O, asyncio sleep 포함)을 백그라운드 스레드로 분리
        def extract_job():
            text = asyncio.run(extract_text_from_selection())
            if text:
                self.text_extracted_signal.emit(text, x, y, bottom_y)
                
        threading.Thread(target=extract_job, daemon=True).start()

    def on_text_extracted_slot(self, text, x, y, bottom_y):
        config = self.settings_window.config
        
        # 번역기 API 키 최신화
        api_key = config.get("gemini_api_key", "")
        self.translator.update_api_key(api_key)
        
        # 새 요청이 들어올 때마다 고유 ID 발급
        self.current_request_id += 1
        req_id = self.current_request_id
        
        # 추출된 텍스트가 전달되면 번역 전 임시 메시지 표시
        # 드래그 영역과 텍스트 줄 수를 기반으로 폰트 크기 동적 계산
        drag_height = bottom_y - y
        num_lines = max(1, len(text.strip().splitlines()))
        estimated_line_height = drag_height / num_lines
        
        font_multiplier = config.get("font_size_multiplier", 0.65)
        font_min = config.get("font_size_min", 14)
        font_max = config.get("font_size_max", 36)
        
        font_size = int(estimated_line_height * font_multiplier)
        font_size = max(font_min, min(font_size, font_max)) # 너무 작거나 크지 않게 제한
        
        offset_x = config.get("overlay_offset_x", 10)
        offset_y = config.get("overlay_offset_y", 10)
        
        from config.settings import UI_TEXT
        ui_lang = config.get("ui_lang", "한국어")
        if ui_lang not in UI_TEXT:
            ui_lang = "한국어"
        translating_msg = UI_TEXT[ui_lang]["translating"]
        
        self.overlay_window.show_translation(translating_msg, x, y, font_size, offset_x, offset_y)
        
        source_lang = config.get("source_lang", "日本語")
        target_lang = config.get("target_lang", "한국어")
        
        # 텍스트 길이에 비례하여 동적으로 타임아웃 계산 + 재시도(Retry) 대기 시간을 고려하여 10초 여유 추가
        base_timeout = config.get("api_timeout_seconds", 5.0)
        dynamic_timeout = base_timeout + (len(text) * 0.05) + 10.0
        
        # 번역 API 호출 작업을 백그라운드 스레드로 분리
        def translate_job():
            try:
                # 무한 대기(hang) 방지를 위해 타임아웃 적용
                translated = asyncio.run(asyncio.wait_for(
                    self.translator.translate(text, source_lang, target_lang),
                    timeout=dynamic_timeout
                ))
            except asyncio.TimeoutError:
                translated = "응답 시간 초과 (Timeout)"
            except Exception as e:
                translated = "번역 실패 (Error)"
                
            self.translation_completed_signal.emit(translated, x, y, font_size, req_id)
            
        threading.Thread(target=translate_job, daemon=True).start()

    def on_translation_completed_slot(self, text, x, y, font_size, req_id):
        # 현재 진행 중인 최신 요청이 아니면(이전 요청이면) 무시
        if req_id != self.current_request_id:
            return
            
        config = self.settings_window.config
        offset_x = config.get("overlay_offset_x", 10)
        offset_y = config.get("overlay_offset_y", 10)
        
        # 번역된 결과를 화면에 표시
        self.overlay_window.show_translation(text, x, y, font_size, offset_x, offset_y)

    def on_live_translate_requested(self, text, source_lang, target_lang):
        config = self.settings_window.config
        api_key = config.get("gemini_api_key", "")
        self.translator.update_api_key(api_key)
        
        self.current_live_request_id += 1
        req_id = self.current_live_request_id
        
        ui_lang = config.get("ui_lang", "한국어")
        
        def live_translate_job():
            try:
                result = asyncio.run(self.translator.translate_live(text, source_lang, target_lang, ui_lang))
            except Exception as e:
                result = {"translated": "[Error] 번역 실패", "src_pronunciation": "", "tgt_pronunciation": ""}
            self.live_translation_completed_signal.emit(result, req_id)
            
        threading.Thread(target=live_translate_job, daemon=True).start()

    def on_live_translation_completed(self, result, req_id):
        if req_id != self.current_live_request_id:
            return
        self.live_window.update_result(
            result.get("translated", ""),
            result.get("src_pronunciation", ""),
            result.get("tgt_pronunciation", "")
        )

def main():
    app = QApplication(sys.argv)
    
    # 마지막 창(설정창 등)이 닫혀도 프로그램이 종료되지 않도록 설정 (트레이에서 실행 유지)
    app.setQuitOnLastWindowClosed(False)
    
    controller = AppController()
    
    # 자동 업데이트 확인 (비동기)
    update_controller = UpdateController(parent_widget=controller.settings_window, quit_callback=app.quit)
    check_for_updates(APP_VERSION, GITHUB_REPO, update_controller.update_available_signal.emit)
    
    # API 키 확인 및 입력창 표시
    if not controller.settings_window.config.get("gemini_api_key"):
        api_window = ApiKeyWindow(controller.settings_window.config, save_callback=save_config)
        api_window.exec()
        
        # 입력 후에도 키가 없으면 프로그램 종료
        if not controller.settings_window.config.get("gemini_api_key"):
            print("API Key is required to run this application.")
            sys.exit(0)
            
    # API 키가 확인되면 마우스 훅 시작
    controller.start_hook()
    
    tray_icon = TrayIcon(
        settings_window=controller.settings_window, 
        live_window=controller.live_window,
        app_quit_callback=app.quit
    )
    
    # 설정이 저장될 때 트레이 아이콘의 언어도 갱신되도록 연결
    controller.settings_window.settings_saved_signal.connect(tray_icon.update_ui_texts)
    
    tray_icon.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
