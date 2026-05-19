# 📄 Project Specification: Discord Local Overlay Translator

## **1. Project Overview**

본 프로젝트는 Discord 환경에서 발생하는 외국어(주로 일본어) 텍스트를 사용자가 마우스로 드래그하면, 백그라운드에서 이를 감지하여 문맥에 맞게 번역한 후 화면 최상단 오버레이 창으로 결과를 띄워주는 순수 로컬 기반 Windows(또는 멀티플랫폼) 애플리케이션이다.

- **주요 목적:** 온라인 게임 중 발생하는 캐주얼한 대화, 은어, 줄임말 등의 맥락을 파악하여 자연스러운 한국어 구어체로 실시간 번역.
- **특징:** 별도의 외부 백엔드 서버 없이 사용자 PC에서 백그라운드 프로세스로 동작. 클립보드 제어 및 비동기 LLM API 호출을 통해 UI 프리징 없는 가벼운 동작 보장.

## **2. Tech Stack**

- **Core Language:** Python 3.10+
- **LLM API:** Google Gemini 1.5 Flash (사용자 API 키 입력 방식, 비동기 호출)
- **Input Handling:** `pynput` (글로벌 마우스 이벤트 훅), `pyautogui` / `keyboard` (단축키 제어)
- **Clipboard Management:** `pyperclip`
- **Overlay UI:** `PyQt6` 또는 `PySide6` (Frameless 투명 윈도우 및 시스템 트레이)
- **Async/Network:** `asyncio`, `google-genai` (또는 `httpx`)

## **3. System Architecture & Directory Structure**

프로젝트는 관심사 분리(Separation of Concerns)를 원칙으로 4개의 주요 계층으로 모듈화된다. API 키와 사용자 설정(출발/도착 언어 등)은 권한 충돌 방지를 위해 사용자 홈 디렉토리(예: `~/.discord_translator/config.json`)에 안전하게 보관하여 관리한다.

**Plaintext**

`discord-overlay-translator/
├── main.py                 # 진입점 및 모듈 간 Event-Driven 파이프라인 구성
├── requirements.txt
├── config/
│   └── settings.py         # 사용자 홈 디렉토리의 config.json 관리, 설정값 로드 및 프롬프트 동적 생성
├── core/
│   ├── input_handler.py    # 글로벌 마우스 훅, Drag & Drop 좌표 및 이벤트 감지
│   ├── text_extractor.py   # 자동 Ctrl+C 트리거 및 클립보드 텍스트 획득/복구
│   └── translator.py       # Gemini 1.5 Flash 비동기 API 통신 및 에러 핸들링
└── ui/
    ├── overlay_window.py   # X, Y 좌표 기반 텍스트 렌더링 (투명 배경, Fade-out 애니메이션)
    ├── settings_window.py  # 출발/도착 언어 선택 및 API 키 입력 UI
    └── tray_icon.py        # 시스템 트레이 제어 (설정창 진입, 앱 활성/비활성, 종료)
    
├── build.py                # PyInstaller를 이용한 단일 실행파일 빌드 스크립트
└── installer_setup.iss     # Inno Setup을 이용한 윈도우 설치 마법사 생성 스크립트`

## **4. Core Pipeline (Data Flow)**

1. **Event Listen:** `input_handler`가 마우스 좌클릭 Pressed -> Drag -> Released 시퀀스를 감지.
2. **Extract:** 마우스 드롭 완료 시, `text_extractor`가 `Ctrl+C` 이벤트를 발생시키고 0.1초 대기 후 클립보드에서 텍스트 데이터 추출.
3. **Translate (Async):** 추출된 텍스트가 `translator`로 전달됨. Gemini API에 비동기로 번역 요청 전송.
    - *System Prompt:* 설정창에서 선택된 탐지할 언어와 번역 결과 언어를 반영하여 동적으로 프롬프트 생성. "디스코드/게임 중의 친근한 {source_lang} 대화를 {target_lang} 구어체로 자연스럽게 번역."
4. **Render:** 번역된 결과 스트링이 리턴되면, `overlay_window`가 마우스 Release 좌표(`X2, Y2`) 바로 위쪽에 팝업을 렌더링. 지정된 시간(예: 4초) 후 서서히 페이드아웃하며 소멸.

## **5. Development Phases (개발 마일스톤)**

### **Phase 1: Core Logic & CLI Prototype (핵심 기능 구현)**

- `pynput`을 이용한 드래그 이벤트 감지 로직 완성.
- 클립보드 데이터 I/O 로직 작성 및 기존 클립보드 데이터 복구 로직 구현.
- Gemini 1.5 Flash API 연동 및 비동기 번역 함수 작성. 콘솔(CLI) 상에서 파이프라인 정상 동작 확인.

### **Phase 2: Overlay UI & UX (시각화)**

- `PyQt6`를 이용한 Frameless / Always-on-top 윈도우 구현.
- 마우스 커서 좌표 계산 알고리즘 및 오버레이 윈도우 이동 로직 적용.
- 자연스러운 UI 경험을 위한 Fade-in / Fade-out 타이머 및 투명도 조절 기능 추가.

### **Phase 3: System Integration & Packaging (시스템 통합 및 배포)**

- 사용자 편의를 위한 System Tray Icon 적용 및 설정 UI 창(`settings_window.py`)을 통해 언어 동적 변경.
- 앱 최초 실행 시 API 키가 없으면 팝업창을 띄워 입력받고 사용자 홈 디렉토리(AppData 등)에 안전하게 저장.
- `PyInstaller`를 이용한 단일 `.exe` 실행 파일 패키징 및 배포 자동화.
- `Inno Setup` 등을 활용하여 일반 사용자도 쉽게 설치/제거할 수 있는 Windows 설치 마법사(Installer) 제작.

---

**[To AI Assistant]**
이상의 내용을 프로젝트 전체의 "Context" 및 "System Instruction"으로 인식하십시오. 본 문서의 아키텍처와 기술 스택을 기반으로, 모듈별 구체적인 Python 코드 작성이나 설계 개선안에 대한 후속 요청을 처리해 주시면 됩니다.
