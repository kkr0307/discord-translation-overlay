import asyncio
from google import genai
from config.settings import get_system_prompt, get_live_translation_prompt

class Translator:
    def __init__(self):
        self.client = None
        self.api_key = ""
        
    def update_api_key(self, api_key: str):
        if api_key and api_key != self.api_key:
            self.api_key = api_key
            self.client = genai.Client(api_key=api_key)
            
    async def _call_api_with_retry(self, model_name: str, text: str, system_prompt: str, max_retries: int = 2) -> str:
        for attempt in range(max_retries + 1):
            try:
                response = await self.client.aio.models.generate_content(
                    model=model_name,
                    contents=text,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.3
                    )
                )
                return response.text.strip()
            except Exception as e:
                err_msg = str(e)
                # 503 (Service Unavailable) 또는 429 (Too Many Requests) 에러 시 재시도
                if attempt < max_retries and ("503" in err_msg or "429" in err_msg or "quota" in err_msg.lower()):
                    await asyncio.sleep(1.0 * (attempt + 1)) # 1초, 2초 대기 후 재시도
                    continue
                raise e # 최대 재시도 횟수 초과 또는 다른 종류의 에러면 밖으로 던짐

    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if not text:
            return ""
            
        if not self.client:
            return "[Error] API 키가 설정되지 않았습니다. 설정창에서 입력해주세요."
            
        system_prompt = get_system_prompt(source_lang, target_lang)
        
        try:
            # 기본 모델 시도 (오류 시 내부적으로 최대 2번 더 재시도함)
            return await self._call_api_with_retry('gemini-3.1-flash-lite', text, system_prompt, max_retries=2)
        except Exception as e:
            try:
                # 기본 모델이 끝내 실패한 경우 폴백 모델 시도 (오류 시 1번 재시도)
                return await self._call_api_with_retry('gemini-2.0-flash', text, system_prompt, max_retries=1)
            except Exception as fallback_e:
                return f"[Error] 번역 서버(Gemini)에 일시적인 장애가 있습니다. (503)\n잠시 후 다시 드래그해주세요."

    async def translate_live(self, text: str, source_lang: str, target_lang: str, ui_lang: str) -> dict:
        if not text:
            return {"translated": "", "src_pronunciation": "", "tgt_pronunciation": ""}
            
        if not self.client:
            return {"translated": "[Error] API 키가 설정되지 않았습니다.", "src_pronunciation": "", "tgt_pronunciation": ""}
            
        system_prompt = get_live_translation_prompt(source_lang, target_lang, ui_lang)
        
        try:
            raw_result = await self._call_api_with_retry('gemini-3.1-flash-lite', text, system_prompt, max_retries=2)
        except Exception as e:
            try:
                raw_result = await self._call_api_with_retry('gemini-2.0-flash', text, system_prompt, max_retries=1)
            except Exception as fallback_e:
                return {"translated": "[Error] 서버 장애", "src_pronunciation": "", "tgt_pronunciation": ""}
                
        result = {"translated": "", "src_pronunciation": "", "tgt_pronunciation": ""}
        current_mode = None
        translated_lines = []
        src_pron_lines = []
        tgt_pron_lines = []
        
        for line in raw_result.strip().split('\n'):
            stripped = line.strip()
            if stripped.startswith("[번역]"):
                current_mode = "translated"
                content = stripped.replace("[번역]", "").strip()
                if content: translated_lines.append(content)
                continue
            elif stripped.startswith("[원본발음]"):
                current_mode = "src_pronunciation"
                content = stripped.replace("[원본발음]", "").strip()
                if content: src_pron_lines.append(content)
                continue
            elif stripped.startswith("[번역발음]"):
                current_mode = "tgt_pronunciation"
                content = stripped.replace("[번역발음]", "").strip()
                if content: tgt_pron_lines.append(content)
                continue
                
            if current_mode == "translated":
                translated_lines.append(stripped)
            elif current_mode == "src_pronunciation":
                src_pron_lines.append(stripped)
            elif current_mode == "tgt_pronunciation":
                tgt_pron_lines.append(stripped)
                
        result["translated"] = "\n".join([l for l in translated_lines if l])
        result["src_pronunciation"] = "\n".join([l for l in src_pron_lines if l])
        result["tgt_pronunciation"] = "\n".join([l for l in tgt_pron_lines if l])
        
        if not result["translated"] and raw_result:
            result["translated"] = raw_result
            
        return result
