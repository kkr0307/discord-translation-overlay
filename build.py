import os
import subprocess
import shutil
import sys

def build():
    print("Starting PyInstaller build process...")
    
    # 이전 빌드 잔재 정리
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
        
    # PyInstaller 명령어 구성
    # --noconfirm: 기존 빌드 덮어쓰기
    # --onefile: 단일 실행 파일(.exe)로 압축
    # --windowed: 콘솔 창 숨김 (백그라운드 실행)
    # --name: 생성될 파일 이름 지정
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "DiscordTranslator",
        "--hidden-import", "pkg_resources._vendor.jaraco.text",
        "--hidden-import", "pkg_resources._vendor.jaraco.context",
        "--hidden-import", "pkg_resources._vendor.jaraco.functools",
        "--hidden-import", "jaraco.text",
        "--hidden-import", "jaraco.context",
        "--hidden-import", "jaraco.functools",
        "--hidden-import", "platformdirs",
        "--hidden-import", "pkg_resources.extern.platformdirs",
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n[SUCCESS] Build completed successfully!")
        print("Executable can be found in the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Build failed with error: {e}")
        
if __name__ == "__main__":
    build()
