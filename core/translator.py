import asyncio
from google import genai
from config.settings import get_system_prompt

class Translator:
    def __init__(self):
        self.client = None
        self.api_key = ""
        
    def update_api_key(self, api_key: str):
        if api_key and api_key != self.api_key:
            self.api_key = api_key
            self.client = genai.Client(api_key=api_key)
            
    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if not text:
            return ""
            
        if not self.client:
            return "[Error] API 키가 설정되지 않았습니다. 설정창에서 입력해주세요."
            
        system_prompt = get_system_prompt(source_lang, target_lang)
        
        try:
            # 완전 무료이자 가장 가볍고 빠른 모델 (과금 없음, 무료 티어 제공)
            response = await self.client.aio.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=text,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.3
                )
            )
            return response.text.strip()
        except Exception as e:
            try:
                # 실패 시 또 다른 무료 티어 모델로 폴백
                response = await self.client.aio.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=text,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.3
                    )
                )
                return response.text.strip()
            except Exception as fallback_e:
                return f"[Error] 번역 중 오류 발생: {str(e)} / Fallback Error: {str(fallback_e)}"
