# 🌍 Discord Translation Overlay (디스코드 번역 오버레이 / ディスコード翻訳オーバーレイ)

> 🤖 **Vibe Coding Project:** This project's code was built from concept to deployment entirely through pair-programming with AI agents (Vibe Coding).
> 이 프로젝트는 기획부터 개발, 성능 최적화, 배포 세팅까지 AI 에이전트와의 페어 프로그래밍(바이브 코딩)을 통해 100% 작성되었습니다.
> このプロジェクトは、企画から開発、最適化、ビルド設定までAIエージェントとのペアプログラミング（バイブコーディング）を通じて100%作成されました。

---

## 📌 Language Select
* [English](#-english)
* [한국어 (Korean)](#-한국어)
* [日本語 (Japanese)](#-日本語)

---

## 🇺🇸 English

A lightweight, high-performance desktop application designed to translate text on your screen (Discord, games, web browsers) instantly when you drag-select text. 

---

### 🚀 Key Features
1. **Drag-to-Translate Overlay:**
   * Simply drag and select text anywhere on your screen. A sleek, semi-transparent overlay showing translation and pronunciation pops up next to your cursor and fades away automatically.
2. **Live Translation Window:**
   * A bidirectional translator window inspired by Discord's dark theme. Perfect for typing outbound messages. It preserves line breaks, nuances, and slangs.
3. **High-Performance Optimizations:**
   * **TCP Keep-Alive connection pooling:** Relies on a persistent background thread and event loop, slashing SSL handshake latencies by **100ms - 300ms** per API request.
   * **Fast Copy Mapping:** Automatically speeds up PyAutoGUI's keyboard latency to `5ms` during translation, making the whole copy action take less than **20ms**.
   * **Smart Filters:** Instantly skips API calls for non-translatable text (e.g. spaces, symbols, numbers) to conserve your Gemini API quota.
   * **Auto-saved UI settings:** Changing language dropdowns inside the Live Translation window automatically saves to the configuration file in real-time.
4. **Auto-Updater:**
   * Checks GitHub Releases upon startup. Safely downloads and installs new versions in one click.

---

### 📦 Installation & Usage

1. **Download:**
   * Visit the [GitHub Releases](https://github.com/kkr0307/discord-translation-overlay/releases) page and download `DiscordTranslator_Installer.exe`.
2. **Get a Free Gemini API Key:**
   * Go to [Google AI Studio](https://aistudio.google.com/), log in, and click **"Get API key"** to create a free API key.
3. **Run & Configure:**
   * Run the installer. On the first launch, paste your API Key in the settings window.
   * Select your source language, target language, and UI language, then click **Save**.
4. **Start Translating!**
   * Drag-select any text on your screen, and the translation overlay will instantly pop up.

---

### ❓ FAQ

* **Q. The program window disappeared!**
  * A. The app runs in the system tray. Look for the translation icon in the taskbar corner (bottom right on Windows) and right-click it.
* **Q. Translations are not showing up.**
  * A. Please verify your API Key in the settings window. Under the free tier, API usage might be temporarily rate-limited if you send too many requests in a short time.
* **Q. Does it work inside full-screen games?**
  * A. Yes, as long as the game is running in **Borderless Windowed** mode and allows text selection/dragging.

---

### 🛠 Tech Stack & Credits
* **Framework:** Python, PyQt6, pynput, pyautogui, pyperclip
* **AI Model:** Google Gemini 3.1 Flash-Lite (via `google-genai` SDK)
* **Version:** v1.1.0

---

## 🇰🇷 한국어

디스코드, PC 게임, 웹 브라우저 등 화면에 표시된 외국어를 **마우스 드래그 한 번으로 즉시 번역 결과를 오버레이 창으로 띄워주는** 초경량 고성능 번역 헬퍼입니다.

---

### 🚀 주요 기능
1. **드래그 즉시 번역 오버레이:**
   * 화면의 텍스트를 마우스로 드래그하면 마우스 커서 옆에 투명한 번역창이 즉시 생성됩니다. 번역 내용과 원어 발음이 정갈하게 표기되며, 확인 후 알아서 자연스럽게 페이드아웃되어 사라집니다.
2. **실시간 양방향 번역 창 (Live Translator):**
   * 디스코드 스타일의 어두운 테마가 가미된 독립 번역 창입니다. 원문의 어조(반말/존댓말)와 느낌표, 인터넷 신조어(`ㅎㅇ`, `ㅋㅋ` 등)까지 원래 어조 그대로 자연스럽게 번역해 줍니다.
3. **최상급 성능 최적화:**
   * **TCP Keep-Alive 유지:** 프로그램 기동 시 백그라운드 스레드에서 단일 비동기 루프를 유지하여, API를 호출할 때마다 발생하던 SSL 핸드셰이크 지연을 없애 응답 속도를 **100ms~300ms 단축**했습니다.
   * **초고속 복사 트래킹:** 복사 키매핑(PyAutoGUI) 딜레이를 복사 시에만 임시로 `5ms`로 단축시켜, 전체 텍스트 수집 시간을 **20ms 미만**으로 단축했습니다.
   * **기호/숫자 필터링:** 한글, 영어, 일본어 등 문자적 의미가 없는 특수 문자나 숫자 드래그 시 API를 호출하지 않고 생략하여 무료 API 사용 쿼터를 적극 보존합니다.
   * **언어 선택 실시간 저장:** 실시간 번역 창에서 언어 콤보박스를 조절하면 설정 파일(`config.json`)에 즉시 반영 및 저장됩니다.
4. **원클릭 자동 업데이트:**
   * 앱 실행 시 GitHub Releases에 업로드된 최신 배포본 파일(`DiscordTranslator_Installer.exe`)을 조회하여 클릭 한 번으로 무설치 자동 다운로드 및 업데이트를 완료합니다.

---

### 📦 설치 및 실행 방법

1. **설치 파일 다운로드:**
   * GitHub [Releases](https://github.com/kkr0307/discord-translation-overlay/releases) 탭에서 최신 버전의 `DiscordTranslator_Installer.exe`를 다운로드하여 실행합니다.
2. **무료 API 키 발급:**
   * [Google AI Studio](https://aistudio.google.com/)에 접속하여 구글 로그인 후 **'Get API key'**를 클릭하여 고유 API 키를 무료로 발급받습니다.
3. **설정 등록:**
   * 최초 앱 구동 시 표시되는 다크 테마 설정 창에 발급받은 API 키를 붙여넣고 번역 대상 언어를 지정한 뒤 **저장(Save)**을 누릅니다.
4. **번역 시작!**
   * 윈도우 상의 텍스트를 마우스로 드래그하여 선택하면 팝업 창에 번역 결과가 나타납니다.

---

### ❓ 자주 묻는 질문 (FAQ)

* **Q. 프로그램 창이 사라졌습니다.**
  * A. 본 프로그램은 시스템 백그라운드 트레이에서 동작합니다. 작업 표시줄 우측 하단 시스템 트레이에서 `번역 아이콘`을 찾은 뒤 우클릭하여 설정이나 실시간 번역창을 열 수 있습니다.
* **Q. 드래그를 해도 번역 결과가 뜨지 않아요.**
  * A. 입력하신 API 키가 올바른지 확인해 주세요. 또한 Gemini API 무료 티어(Rate Limit)의 분당 요청 가능 회수를 초과한 경우 잠시 응답이 멈출 수 있습니다.
* **Q. 게임 내부에서도 사용이 가능한가요?**
  * A. 게임 화면이 **테두리 없는 창 모드(Borderless)**로 실행 중이며 마우스로 드래그 선택이 가능한 형태라면 어디서든 정상 작동합니다.

---

### 🛠 기술 스택 및 버전 정보
* **프레임워크:** Python, PyQt6, pynput, pyautogui, pyperclip
* **사용 AI 모델:** Google Gemini 3.1 Flash-Lite (공식 `google-genai` SDK 적용)
* **버전:** v1.1.0

---

## 🇯🇵 日本語

ディスコードやPCゲーム、ウェブブラウザ上で外国語のテキストを**マウスドラッグするだけで、瞬時に翻訳結果と発音をオーバーレイ表示**する軽量・高速な翻訳アシ스턴트アプリです。

---

### 🚀 主な機能
1. **ドラッグ翻訳オーバーレイ:**
   * 画面上の文字列をドラッグするだけで、マウスカーソルの横に翻訳結果と発音のガイドがフェードイン表示されます。確認後、数秒で自動的にフェードアウトして消えるため作業を邪魔しません。
2. **リアルタイム双方向翻訳ウィンドウ:**
   * ディスコード風のダークテーマが施された翻訳ウィンドウです。タメ口・敬語などのニュアンスや、ネットスラング（`ㅎㅇ`、`ㅋㅋ`など）も元の口調そのままの表現に自然に翻訳します。
3. **極限まで追求された最適化:**
   * **TCP Keep-Aliveによる接続維持:** アプリ起動時にバックグラウンドで非同期イベントループを常駐化させることで、API呼び出しごとのSSLハンドシェイク遅延を解消し、応答速度を **100ms〜300ms 短縮**しました。
   * **超高速コピー入力:** コピー実行時のみ一時的にキー入力ディレイ（PyAutoGUI PAUSE）を`5ms`に短縮し、テキスト抽出処理を **20ms 未満**で完了します。
   * **不要なAPI呼び出しの排除:** 記号や数字のみのドラッグなど、翻訳の必要がないテキストは事前にフィルタリングし、APIリクエストをスキップして無料枠のクォータを節約します。
   * **設定の自動同期・保存:** リアルタイム翻訳ウィンドウで変更した言語設定は、設定ファイル(`config.json`)へ自動的に同期され永続化されます。
4. **自動アップデート機能:**
   * 起動時にGitHub Releasesの最新版(`DiscordTranslator_Installer.exe`)を確認し、ワンクリックでダウンロードから上書きインストールまでを自動的に実行します。

---

### 📦 インストールと使用方法

1. **ダウンロード:**
   * GitHub [Releases](https://github.com/kkr0307/discord-translation-overlay/releases) ページから最新版の `DiscordTranslator_Installer.exe` をダウンロードし、インストールします。
2. **無料のGemini APIキー取得:**
   * [Google AI Studio](https://aistudio.google.com/) にアクセスし、Googleアカウントでログインして **"Get API key"** をクリックし、APIキーを無料で作成します。
3. **キーと初期言語の設定:**
   * アプリ起動時に表示される設定画面に取得したAPIキーを入力し、翻訳先と翻訳元の言語を設定後、**保存(Save)** をクリックします。
4. **翻訳の開始!**
   * 画面上のテキストをマウスでドラッグするだけで、翻訳結果が表示されるようになります。

---

### ❓ よくある質問 (FAQ)

* **Q. アプリのウィンドウが見当たりません。**
  * A. 本アプリはシステムトレイ常駐型です。画面右下のタスクバートレイから `翻訳アイコン` を探して右クリックし、設定やリアルタイム翻訳ウィンドウを開いてください。
* **Q. ドラッグしても翻訳が表示されません。**
  * A. 設定した API キーが正しいか確認してください。無料プランの制限（Rate Limit）を超えた場合、一時的に応答が停止することがあります。
* **Q. ゲーム画面の中でも動きますか？**
  * A. ゲームが **「ボーダーレスウィンドウ(仮想フルスクリーン)」** モードで起動し、テキストがドラッグ選択可能な状態であれば問題なく動作します。

---

### 🛠 技術スタックとバージョン情報
* **フレームワーク:** Python, PyQt6, pynput, pyautogui, pyperclip
* **使用AIモデル:** Google Gemini 3.1 Flash-Lite (`google-genai` SDK)
* **バージョン:** v1.1.0