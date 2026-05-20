from PyQt6.QtWidgets import QMessageBox, QProgressDialog, QApplication
from PyQt6.QtCore import QObject, pyqtSignal
from core.updater import download_and_run_installer
import os

class UpdateController(QObject):
    update_available_signal = pyqtSignal(str, str) # version, download_url
    progress_signal = pyqtSignal(int)
    download_complete_signal = pyqtSignal(str) # installer_path
    
    def __init__(self, parent_widget=None, quit_callback=None):
        super().__init__()
        self.parent_widget = parent_widget
        self.quit_callback = quit_callback
        self.progress_dialog = None
        
        self.update_available_signal.connect(self.on_update_available)
        self.progress_signal.connect(self.on_progress)
        self.download_complete_signal.connect(self.on_download_complete)
        
    def on_update_available(self, version, download_url):
        reply = QMessageBox.question(
            self.parent_widget,
            "업데이트 알림 (Update Available)",
            f"새로운 버전({version})이 출시되었습니다.\n지금 다운로드하고 업데이트하시겠습니까?\n\nNew version ({version}) is available.\nDo you want to download and update now?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.progress_dialog = QProgressDialog("업데이트 다운로드 중... (Downloading update...)", "취소", 0, 100, self.parent_widget)
            self.progress_dialog.setWindowTitle("업데이트")
            self.progress_dialog.setWindowModality(2) # ApplicationModal
            self.progress_dialog.setAutoClose(True)
            self.progress_dialog.setAutoReset(True)
            self.progress_dialog.setMinimumDuration(0)
            self.progress_dialog.setValue(0)
            
            # Start download
            download_and_run_installer(download_url, self.progress_signal.emit, self.download_complete_signal.emit)

    def on_progress(self, percent):
        if self.progress_dialog and not self.progress_dialog.wasCanceled():
            self.progress_dialog.setValue(percent)
            
    def on_download_complete(self, installer_path):
        if self.progress_dialog:
            self.progress_dialog.setValue(100)
            self.progress_dialog.close()
            
        if installer_path and os.path.exists(installer_path):
            try:
                os.startfile(installer_path)
                if self.quit_callback:
                    self.quit_callback()
            except Exception as e:
                QMessageBox.critical(self.parent_widget, "오류", f"설치 프로그램을 실행하는 중 오류가 발생했습니다:\n{e}")
        else:
            QMessageBox.critical(self.parent_widget, "오류", "업데이트 다운로드에 실패했습니다.")
