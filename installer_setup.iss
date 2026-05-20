[Setup]
; [필수] AppId는 윈도우가 이 프로그램을 고유하게 인식하고, 나중에 업데이트 시 덮어쓰기 및 제어판 인식을 보장하는 고유 식별자(주민등록번호)입니다.
AppId={{5E4C2F1A-987B-4D3E-A1C2-8B7C6D5E4F3A}
; 프로그램 기본 정보
AppName=Discord Translation Overlay
AppVersion=1.0
AppPublisher=Local Developer
UninstallDisplayName=Discord Translation Overlay
UninstallDisplayIcon={app}\DiscordTranslator.exe
DefaultDirName={autopf}\DiscordTranslator
DefaultGroupName=Discord Translation Overlay
OutputBaseFilename=DiscordTranslator_Installer
Compression=lzma2
SolidCompression=yes
OutputDir=dist
PrivilegesRequired=admin

; [QoL] 모던 스타일 마법사 UI 적용
WizardStyle=modern

; 설치 경로를 항상 사용자가 직접 선택할 수 있도록 강제 옵션 추가
DisableDirPage=no
UsePreviousAppDir=no
CloseApplications=yes

[Languages]
; [QoL] 다국어 지원 (OS 언어에 맞춰 설치 창 언어가 자동으로 한국어/영어/일본어로 뜹니다)
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Tasks]
; [QoL] 사용자가 바탕화면 아이콘 생성 및 윈도우 부팅 시 자동 실행 여부를 선택할 수 있게 합니다.
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"


[Files]
Source: "dist\DiscordTranslator.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; 시작 프로그램 메뉴 바로가기 및 언인스톨러
Name: "{group}\Discord Translation Overlay"; Filename: "{app}\DiscordTranslator.exe"
Name: "{group}\Uninstall Discord Translation Overlay"; Filename: "{uninstallexe}"
; 바탕화면 바로가기 (사용자가 체크했을 때만 생성)
Name: "{autodesktop}\Discord Translation Overlay"; Filename: "{app}\DiscordTranslator.exe"; Tasks: desktopicon



[Run]
; 설치 완료 직후 프로그램 자동 실행 (사용자가 체크 해제 가능)
Filename: "{app}\DiscordTranslator.exe"; Description: "{cm:LaunchProgram,Discord Translation Overlay}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; [깔끔한 삭제] 프로그램 삭제 시 사용자 폴더에 남아있는 찌꺼기(API 키 및 설정이 담긴 config.json 폴더)까지 완전히 지워버립니다.
Type: filesandordirs; Name: "{%USERPROFILE}\.discord_translator"
