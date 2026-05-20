import urllib.request
import json
import tempfile
import os
import threading
from packaging import version # We can use standard packaging if available, but let's stick to simple string comparison if packaging isn't in requirements.

def parse_version(v_str):
    # 'v1.0.1' -> [1, 0, 1]
    v_str = v_str.lower().replace('v', '')
    try:
        return [int(x) for x in v_str.split('.')]
    except ValueError:
        return [0, 0, 0]

def check_for_updates(current_version, repo, callback):
    def run_check():
        try:
            url = f"https://api.github.com/repos/{repo}/releases/latest"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                latest_version = data.get("tag_name")
                
                if not latest_version:
                    return
                
                cur_v = parse_version(current_version)
                lat_v = parse_version(latest_version)
                
                # Check if latest version is strictly greater
                if lat_v > cur_v:
                    assets = data.get("assets", [])
                    download_url = None
                    for asset in assets:
                        if asset.get("name") == "DiscordTranslator_Installer.exe":
                            download_url = asset.get("browser_download_url")
                            break
                    if download_url:
                        # 보안 검증: 공식 GitHub 도메인만 승인
                        if download_url.startswith("https://github.com/") or download_url.startswith("https://objects.githubusercontent.com/"):
                            callback(latest_version, download_url)
                        else:
                            print(f"Rejected insecure download URL: {download_url}")
        except Exception as e:
            print(f"Update check failed: {e}")
            
    threading.Thread(target=run_check, daemon=True).start()

def download_and_run_installer(download_url, progress_callback, completion_callback):
    def run_download():
        try:
            temp_dir = tempfile.gettempdir()
            installer_path = os.path.join(temp_dir, "DiscordTranslator_Installer.exe")
            
            # Remove previous file if exists
            if os.path.exists(installer_path):
                os.remove(installer_path)
            
            req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                total_size = int(response.getheader('Content-Length', 0))
                downloaded = 0
                chunk_size = 8192
                
                with open(installer_path, 'wb') as f:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            progress_callback(progress)
                            
            # 다운로드 완료
            completion_callback(installer_path)
            
        except Exception as e:
            print(f"Download failed: {e}")
            completion_callback(None)

    threading.Thread(target=run_download, daemon=True).start()
