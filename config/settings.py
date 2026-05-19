import os
import json
from pathlib import Path
from dotenv import load_dotenv

# .env 로드 (개발용)
load_dotenv()

# 실행 파일 권한 문제를 피하기 위해 사용자 홈 디렉토리 하위에 설정 폴더 생성
CONFIG_DIR = Path.home() / ".discord_translator"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "gemini_api_key": "",
    "source_lang": "日本語",
    "target_lang": "한국어",
    "ui_lang": "한국어",

    
    # 세부 설정값들 (Advanced Settings)
    "api_timeout_seconds": 5.0,
    "drag_min_distance": 10,
    "font_size_multiplier": 0.65,
    "font_size_min": 14,
    "font_size_max": 36,
    "overlay_offset_x": 10,
    "overlay_offset_y": 10
}

UI_TEXT = {
    "한국어": {
        "api_key": "API 키:",
        "src_lang": "탐지할 언어:",
        "tgt_lang": "번역결과 언어:",
        "save": "설정 저장",
        "save_success": "설정이 성공적으로 저장되었습니다.",
        "save_title": "저장 완료",
        "translating": "번역 중...",
        "settings": "설정 (Settings)",
        "quit": "종료 (Quit)",
        "window_title": "번역 설정"
    },
    "English(US)": {
        "api_key": "API Key:",
        "src_lang": "Source Language:",
        "tgt_lang": "Target Language:",
        "save": "Save Settings",
        "save_success": "Settings saved successfully.",
        "save_title": "Save Complete",
        "translating": "Translating...",
        "settings": "Settings",
        "quit": "Quit",
        "window_title": "Translation Settings"
    },
    "日本語": {
        "api_key": "API キー:",
        "src_lang": "検出言語:",
        "tgt_lang": "翻訳先言語:",
        "save": "設定を保存",
        "save_success": "設定が正常に保存されました。",
        "save_title": "保存完了",
        "translating": "翻訳中...",
        "settings": "設定 (Settings)",
        "quit": "終了 (Quit)",
        "window_title": "翻訳設定"
    }
}

def load_config():
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 필요한 키가 없으면 기본값으로 채움
                for k, v in DEFAULT_CONFIG.items():
                    if k not in data:
                        data[k] = v
                        
                # 기존 .env 환경 변수가 우선하면 가져오기 (마이그레이션 용도)
                env_api_key = os.getenv("GEMINI_API_KEY")
                if env_api_key and not data.get("gemini_api_key"):
                    data["gemini_api_key"] = env_api_key
                    
                return data
        except Exception as e:
            print(f"설정 파일 읽기 오류: {e}")
            return DEFAULT_CONFIG.copy()
    else:
        # 최초 실행 시 환경 변수 확인
        initial_config = DEFAULT_CONFIG.copy()
        env_api_key = os.getenv("GEMINI_API_KEY")
        if env_api_key:
            initial_config["gemini_api_key"] = env_api_key
        return initial_config

def save_config(config_data):
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"설정 파일 저장 오류: {e}")

def get_system_prompt(source_lang: str, target_lang: str) -> str:
    return (
        f"디스코드/게임 중의 친근한 {source_lang} 대화(은어, 줄임말 포함)를 "
        f"{target_lang} 구어체로 자연스럽게 번역해줘. 부가 설명 없이 번역 결과만 출력해."
    )
