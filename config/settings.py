import os
import json
from pathlib import Path
import sys
from dotenv import load_dotenv

# .env 로드 (개발용, 배포용 exe 실행 시에는 무시)
if not getattr(sys, 'frozen', False):
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

def to_english_name(lang: str) -> str:
    lang = lang.strip()
    mapping = {
        "한국어": "Korean",
        "日本語": "Japanese",
        "English": "English",
        "English(US)": "English",
        "중국어": "Chinese",
        "中文": "Chinese",
        "스페인어": "Spanish",
        "프랑스어": "French"
    }
    return mapping.get(lang, lang)

def get_script_name(lang: str) -> str:
    lang_en = to_english_name(lang)
    if lang_en == "Korean":
        return "Hangul (Korean characters)"
    elif lang_en == "Japanese":
        return "Katakana"
    elif lang_en == "English":
        return "Latin alphabet"
    elif lang_en == "Chinese":
        return "Pinyin"
    else:
        return "Latin alphabet"

def get_system_prompt(source_lang: str, target_lang: str) -> str:
    src_en = to_english_name(source_lang)
    tgt_en = to_english_name(target_lang)
    tgt_script = get_script_name(target_lang)
    
    return (
        f"You are a translation assistant. Translate the discord/game chat from {src_en} to {tgt_en}.\n"
        f"Instructions:\n"
        f"1. Translate literally (word-for-word translation as much as possible) rather than freely/paraphrasing. Keep the tone and politeness level exactly as the original (e.g., if the original is informal/casual, do not translate into formal/polite language. If it is polite, translate it into polite language).\n"
        f"2. Keep internet slangs, abbreviations, or initial-consonant slangs (like 'ㅎㅇ', 'ㅋㅋ') and translate them into similar slangs of {tgt_en}.\n"
        f"3. Write the phonetic pronunciation of the original {src_en} text using {tgt_script} (sound out the pronunciation).\n"
        f"4. If the original text contains multiple lines, preserve the line breaks in both the translation and the pronunciation.\n\n"
        f"Format the output strictly as follows (do not add any explanations or introductory text):\n"
        f"[번역]\n"
        f"(Translation with preserved line breaks)\n"
        f"[발음]\n"
        f"(Pronunciation with preserved line breaks)"
    )

def get_live_translation_prompt(source_lang: str, target_lang: str, ui_lang: str) -> str:
    src_en = to_english_name(source_lang)
    tgt_en = to_english_name(target_lang)
    ui_script = get_script_name(ui_lang)
    
    return (
        f"Translate the given text from {src_en} to {tgt_en}.\n"
        f"Instructions:\n"
        f"1. Never change the original nuance and tone. Match casual tone to casual tone, and formal to formal. (For example, if the input is casual like '번역 기능 테스트 중', do not add polite endings like Japanese '입니다' or 'です/ます').\n"
        f"2. Do not normalize internet slang, abbreviations, or initial-consonant slangs (like 'ㅎㅇ', 'ㅋㅋ') to standard speech; translate them to similar slang/nuance in {tgt_en}.\n"
        f"3. Write the phonetic pronunciation of the original text ({src_en}) and the translated text ({tgt_en}) using {ui_script} (e.g. if the UI language is Korean, write the pronunciations in Hangul characters).\n"
        f"4. Keep the exact line breaks of the original text.\n\n"
        f"Format the output strictly as follows (do not add any explanations or introductory text):\n"
        f"[번역]\n"
        f"(Translated text)\n"
        f"[원본발음]\n"
        f"(Pronunciation of original text)\n"
        f"[번역발음]\n"
        f"(Pronunciation of translated text)"
    )
