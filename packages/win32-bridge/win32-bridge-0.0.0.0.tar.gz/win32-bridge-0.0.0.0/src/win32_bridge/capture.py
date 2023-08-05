import json
import src.win32_bridge


class CaptureWindow:
    def __init__(self):
        self.mouse_delay = src.win32_bridge.mouse_delay
        self.wait_delay = src.win32_bridge.wait_delay
        print(self.mouse_delay, self.wait_delay)

