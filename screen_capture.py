import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget, QLabel, QSystemTrayIcon, QMenu, QStyle)
from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QPainter, QColor, QScreen, QIcon
from PIL import ImageGrab
import platform

# Determine the operating system
IS_MAC = platform.system() == 'Darwin'

# Import appropriate hotkey library based on OS
if IS_MAC:
    from pynput import keyboard
else:
    import keyboard as keyboard_win


class OverlayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.begin = QPoint()
        self.end = QPoint()
        self.is_drawing = False

        # Get primary screen geometry
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        # Set widget properties
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint |
                            Qt.WindowType.Tool)  # Tool flag helps with Mac compatibility
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Initialize coordinates
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0

    def paintEvent(self, event):
        if self.is_drawing:
            painter = QPainter(self)

            # Create semi-transparent overlay
            painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

            if not self.begin.isNull() and not self.end.isNull():
                rect = QRect(self.begin, self.end)
                # Clear selected area
                painter.eraseRect(rect)
                # Draw rectangle border
                painter.setPen(QColor(255, 255, 255))
                painter.drawRect(rect)

                # Show dimensions
                dimensions = f"{abs(rect.width())} x {abs(rect.height())}"
                painter.setPen(QColor(255, 255, 255))
                painter.drawText(rect.center(), dimensions)

    def mousePressEvent(self, event):
        self.is_drawing = True
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.is_drawing = False
        self.capture_screen()
        self.close()

    def capture_screen(self):
        if self.begin and self.end:
            # Get coordinates
            x1, y1 = min(self.begin.x(), self.end.x()), min(self.begin.y(), self.end.y())
            x2, y2 = max(self.begin.x(), self.end.x()), max(self.begin.y(), self.end.y())

            # Handle screen scaling for Mac
            if IS_MAC:
                scale = QApplication.primaryScreen().devicePixelRatio()
                x1, y1, x2, y2 = [int(coord * scale) for coord in [x1, y1, x2, y2]]

            # Capture and save
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot.save(f"screenshots/screenshot_{timestamp}.png")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setup_hotkeys()
        self.setup_tray()

    def initUI(self):
        self.setWindowTitle('Screen Capture Tool')
        self.setFixedSize(300, 150)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Capture button
        self.capture_button = QPushButton("Start Capture")
        self.capture_button.clicked.connect(self.start_capture)
        layout.addWidget(self.capture_button)

        # Instructions with hotkeys
        hotkey_text = "⌘ + Shift + X" if IS_MAC else "Ctrl + Shift + X"
        exit_hotkey = "⌘ + Shift + Q" if IS_MAC else "Ctrl + Shift + Q"
        instructions = QLabel(
            f"Click and drag to select area\n"
            f"Capture Hotkey: {hotkey_text}\n"
            f"Exit Hotkey: {exit_hotkey}"
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)

    def setup_hotkeys(self):
        if IS_MAC:
            # Setup Mac hotkeys using pynput
            self.listener = keyboard.GlobalHotKeys({
                '<cmd>+<shift>+x': self.start_capture,
                '<cmd>+<shift>+q': self.quit_app
            })
            self.listener.start()
        else:
            # Setup Windows hotkeys using keyboard
            keyboard_win.add_hotkey('ctrl+shift+x', self.start_capture)
            keyboard_win.add_hotkey('ctrl+shift+q', self.quit_app)

    def setup_tray(self):
        # Create system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_ComputerIcon')))

        # Create tray menu
        tray_menu = QMenu()
        capture_action = tray_menu.addAction("Capture")
        capture_action.triggered.connect(self.start_capture)
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def start_capture(self):
        self.hide()
        self.overlay = OverlayWidget()
        self.overlay.show()
        self.overlay.closed = lambda: self.show()

    def quit_app(self):
        if IS_MAC:
            self.listener.stop()
        QApplication.quit()

    def closeEvent(self, event):
        # Minimize to system tray instead of closing
        event.ignore()
        self.hide()


def main():
    app = QApplication(sys.argv)

    # Handle high DPI screens
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()