import threading
from pynput import mouse

class MouseDragHandler:
    def __init__(self, on_drag_complete_callback, on_click_callback=None, min_distance=10):
        """
        on_drag_complete_callback: 드래그가 완료되었을 때 호출될 콜백 함수.
        on_click_callback: 마우스 클릭이 감지되었을 때 호출될 콜백 함수.
        min_distance: 드래그로 인식할 최소 이동 픽셀 거리.
        """
        self.on_drag_complete_callback = on_drag_complete_callback
        self.on_click_callback = on_click_callback
        self.min_distance = min_distance
        self.is_pressed = False
        self.start_pos = (0, 0)
        self.listener = mouse.Listener(
            on_click=self.on_click
        )

    def on_click(self, x, y, button, pressed):
        # 마우스를 누르는 순간 무조건 다른 곳을 클릭한 것으로 간주하여 콜백 호출
        if pressed and self.on_click_callback:
            self.on_click_callback()
            
        if button == mouse.Button.left:
            if pressed:
                self.is_pressed = True
                self.start_pos = (x, y)
            else:
                if self.is_pressed:
                    self.is_pressed = False
                    end_pos = (x, y)
                    # 드래그로 간주할 최소 거리 (예: 10픽셀 이상 이동 시)
                    distance = ((end_pos[0] - self.start_pos[0])**2 + (end_pos[1] - self.start_pos[1])**2)**0.5
                    if distance > self.min_distance:
                        # 드래그 영역의 가장 우측(가장 큰 x), 가장 상단(가장 작은 y), 가장 하단(가장 큰 y) 좌표를 계산
                        right_x = max(self.start_pos[0], end_pos[0])
                        top_y = min(self.start_pos[1], end_pos[1])
                        bottom_y = max(self.start_pos[1], end_pos[1])
                        
                        # 드래그가 감지되면 콜백 호출
                        if self.on_drag_complete_callback:
                            self.on_drag_complete_callback(right_x, top_y, bottom_y)

    def start(self):
        # 데몬 스레드로 실행하여 메인 프로그램 종료 시 함께 종료되도록 함
        self.listener_thread = threading.Thread(target=self.listener.start, daemon=True)
        self.listener_thread.start()

    def stop(self):
        self.listener.stop()
