import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab
from datetime import datetime
import os
import time


class TransparentScreenCapture:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen Capture")

        # Make window frameless
        # self.root.overrideredirect(True)

        # Set window transparency (0.3 = 70% transparent)
        self.root.attributes('-alpha', 0.3)

        # Always on top
        self.root.attributes('-topmost', True)

        # Default size
        self.width = 400
        self.height = 200

        # Create main frame with black background
        self.main_frame = tk.Frame(
            self.root,
            bg='black',
            highlightthickness=2,
            highlightbackground='black'
        )
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Bind mouse events for dragging
        self.main_frame.bind('<Button-1>', self.start_move)
        self.main_frame.bind('<B1-Motion>', self.on_move)
        self.main_frame.bind('<Enter>', self.on_enter)
        self.main_frame.bind('<Leave>', self.on_leave)

        # Create button frame
        button_frame = tk.Frame(self.main_frame, bg='black')
        button_frame.pack(side=tk.BOTTOM, pady=5)

        # Create capture button
        self.capture_btn = tk.Button(
            button_frame,
            text="Search",
            command=self.capture_screen,
            bg='black',
            fg='white',
            relief=tk.FLAT,
            padx=10
        )
        self.capture_btn.pack(side=tk.LEFT, padx=5)

        # Create close button
        self.close_btn = tk.Button(
            button_frame,
            text="Close",
            command=self.root.quit,
            bg='black',
            fg='white',
            relief=tk.FLAT,
            padx=10
        )
        self.close_btn.pack(side=tk.LEFT, padx=5)

        # Variables for window movement
        self.x = 0
        self.y = 0

        # Create screenshots directory if it doesn't exist
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')

        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.root.geometry(f'{self.width}x{self.height}+{x}+{y}')

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def on_enter(self, event):
        # Make window more opaque when mouse enters
        self.root.attributes('-alpha', 0.5)

    def on_leave(self, event):
        # Make window more transparent when mouse leaves
        self.root.attributes('-alpha', 0.3)

    def capture_screen(self):
        # Get window position
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        w = self.root.winfo_width()
        h = self.root.winfo_height()

        # Hide window temporarily for clean capture
        self.root.withdraw()
        self.root.update()

        time.sleep(1)

        # Capture the screen area
        screenshot = ImageGrab.grab(bbox=(
            x + 2,  # Add offset for border
            y + 2,  # Add offset for border
            x + w - 2,
            y + h - 2
        ))

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/capture_{timestamp}.png"

        # Save the screenshot
        screenshot.save(filename)

        # Show window again
        self.root.deiconify()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TransparentScreenCapture()
    app.run()