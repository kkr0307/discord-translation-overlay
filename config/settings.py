import os
import json
from pathlib import Path
from dotenv import load_dotenv

# .env 로드 (개발용)
load_dotenv()

APP_VERSION = "v1.0.0"
GITHUB_REPO = "kkr0307/discord-translation-overlay"

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
        "window_title": "번역 설정",
        "open_live": "실시간 번역창 열기",
        "live_title": "실시간 번역 (Live Translator)",
        "live_src_ph": "번역할 내용을 입력하세요...",
        "live_src_pron_ph": "원문의 발음이 여기에 표시됩니다.",
        "live_tgt_ph": "번역 결과가 표시됩니다.",
        "live_tgt_pron_ph": "번역된 결과의 발음이 여기에 표시됩니다.",
        "live_translate_btn": "번역하기",
        "live_copy_btn": "복사"
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
        "window_title": "Translation Settings",
        "open_live": "Open Live Translator",
        "live_title": "Live Translator",
        "live_src_ph": "Enter text to translate...",
        "live_src_pron_ph": "Pronunciation of the source text will appear here.",
        "live_tgt_ph": "Translation result will appear here.",
        "live_tgt_pron_ph": "Pronunciation of the translated text will appear here.",
        "live_translate_btn": "Translate",
        "live_copy_btn": "Copy"
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
        "window_title": "翻訳設定",
        "open_live": "リアルタイム翻訳を開く",
        "live_title": "リアルタイム翻訳 (Live Translator)",
        "live_src_ph": "翻訳する内容を入力してください...",
        "live_src_pron_ph": "原文の発音がここに表示されます。",
        "live_tgt_ph": "翻訳結果がここに表示されます。",
        "live_tgt_pron_ph": "翻訳された結果の発音がここに表示されます。",
        "live_translate_btn": "翻訳する",
        "live_copy_btn": "コピー"
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
        f"디스코드/게임 중의 {source_lang} 대화를 {target_lang}로 번역해줘.\n"
        f"조건 1: 의역을 배제하고 원문에 쓰인 단어들을 최대한 1:1 대응하여 직역할 것. 특히 원문의 어조(존댓말이면 존댓말, 반말이면 반말)를 원래 뉘앙스 그대로 유지할 것. (예: 반말/평서문인데 경어를 붙이지 말 것.)\n"
        f"조건 2: 'ㅎㅇ', 'ㅋㅋ' 같은 인터넷 신조어나 초성 등은 임의로 정제하지 말고, {target_lang}의 비슷한 뉘앙스를 가진 슬랭으로 번역할 것.\n"
        f"조건 3: 원문의 {source_lang} 발음을 {target_lang} 문자로 소리나는 대로 적어줄 것.\n"
        f"조건 4: 원문에 여러 줄의 문장이 있다면, 번역과 발음 모두 원본의 줄바꿈 위치를 똑같이 유지할 것.\n"
        f"출력 형식은 반드시 아래와 같이 [번역]과 [발음] 블록으로 나누어 출력해 (다른 부가 설명 금지):\n"
        f"[번역]\n"
        f"(원문의 줄바꿈을 유지한 번역 내용)\n"
        f"[발음]\n"
        f"(원문의 줄바꿈을 유지한 발음 표기)"
    )

def get_live_translation_prompt(source_lang: str, target_lang: str, ui_lang: str) -> str:
    return (
        f"입력된 {source_lang} 문장을 {target_lang}로 번역해줘.\n"
        f"조건 1: 원문의 뉘앙스와 어조를 절대 임의로 바꾸지 말 것. (예: 반말이면 반말로, 경어면 경어로. '번역 기능 테스트 중'처럼 평서문/반말인 경우 '데스/마스' 등의 경어를 붙이지 말고 그대로 번역할 것.)\n"
        f"조건 2: 'ㅎㅇ', 'ㅋㅋ', 초성 등의 인터넷 신조어나 줄임말은 평범한 말(예: 안녕)로 정제하지 말고, {target_lang}의 비슷한 뉘앙스를 가진 슬랭으로 번역할 것.\n"
        f"조건 3: 원문({source_lang})의 발음과 번역된 문장({target_lang})의 발음을 각각 {ui_lang} 문자로 소리나는 대로 적어줄 것.\n"
        f"조건 4: 원문에 줄바꿈이 있다면 줄바꿈 위치도 반드시 유지할 것.\n"
        f"반드시 아래와 같은 블록 형식으로만 응답해 (다른 부가 설명 절대 금지):\n"
        f"[번역]\n"
        f"(번역 결과)\n"
        f"[원본발음]\n"
        f"(원본 문장의 발음)\n"
        f"[번역발음]\n"
        f"(번역된 문장의 발음)"
    )
