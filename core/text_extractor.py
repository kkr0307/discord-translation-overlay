import asyncio
import pyautogui
import pyperclip
import time

async def extract_text_from_selection() -> str:
    """
    현재 선택된 텍스트를 Ctrl+C를 통해 클립보드로 복사하고 가져옵니다.
    기존 클립보드 내용을 보존합니다.
    """
    # 1. 기존 클립보드 데이터 백업
    original_clipboard = pyperclip.paste()
    
    # 임시로 클립보드 비우기 (복사 성공 여부 확인용)
    pyperclip.copy('')
    
    # 2. Ctrl+C 키보드 이벤트 발생
    pyautogui.hotkey('ctrl', 'c')
    
    # 3. 클립보드에 텍스트가 들어올 때까지 대기 (최대 0.5초)
    extracted_text = ""
    for _ in range(10):
        await asyncio.sleep(0.05)
        extracted_text = pyperclip.paste()
        if extracted_text:
            break
            
    # 4. 클립보드 원래 데이터로 복구
    if original_clipboard:
        pyperclip.copy(original_clipboard)
    else:
        pyperclip.copy('')
        
    return extracted_text.strip()
