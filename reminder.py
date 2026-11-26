import ctypes
import json
import random
import sys
import tkinter as tk
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
CONFIG_PATH = APP_DIR / "config.json"
DEFAULT_CONFIG = {
    "title": "A Quick Reminder",
    "messages": [
        "Water break, water break! Stay hydrated.",
        "Take a short break away from the screen.",
        "Stop coding, go have lunch. 😤"
    ],
    "interval_minutes": 60,
    "show_seconds": 15,
    "width": 700,
    "background": "#20242b",
    "foreground": "#f4f5f7",
    "accent": "#ff00c3",
    "bottom_offset": 100,
    "right_offset": 28,
    "show_on_start": True
}


def load_config():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        config = DEFAULT_CONFIG.copy()
        config.update(data)
        messages = config.get("messages")
        if not isinstance(messages, list):
            messages = []
        config["messages"] = [str(m).strip() for m in messages if str(m).strip()]
        if not config["messages"]:
            config["messages"] = DEFAULT_CONFIG["messages"]
        return config
    except Exception as exc:
        print(f"Could not read config.json: {exc}", file=sys.stderr)
        return DEFAULT_CONFIG.copy()


def enable_dpi_awareness():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


class Reminder:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.window = None
        self.hide_job = None
        self.next_job = None
        self.last_message = None
        self.root.withdraw()
        self.root.after(500, self.show_reminder if config["show_on_start"] else self.schedule_next)

    def choose_message(self):
        messages = self.config["messages"]
        choices = [m for m in messages if m != self.last_message] or messages
        self.last_message = random.choice(choices)
        return self.last_message

    def show_reminder(self):
        self.schedule_next()
        self.dismiss()
        win = tk.Toplevel(self.root)
        self.window = win
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.configure(bg=self.config["background"])
        try:
            win.attributes("-alpha", 0.97)
        except tk.TclError:
            pass

        width = int(self.config["width"])
        height = 124
        win.update_idletasks()
        screen_w, screen_h = win.winfo_screenwidth(), win.winfo_screenheight()
        x = screen_w - width - int(self.config["right_offset"])
        y = screen_h - height - int(self.config["bottom_offset"])
        win.geometry(f"{width}x{height}+{x}+{y}")

        bg = self.config["background"]
        fg = self.config["foreground"]
        outer = tk.Frame(win, bg=bg, highlightthickness=1, highlightbackground="#3b424d")
        outer.pack(fill="both", expand=True)

        header = tk.Frame(outer, bg=bg)
        header.pack(fill="x", padx=18, pady=(12, 0))
        tk.Label(header, text="●", fg=self.config["accent"], bg=bg,
                 font=("Segoe UI", 14)).pack(side="left", anchor="center")
        tk.Label(header, text=self.config["title"], fg=fg, bg=bg,
                 font=("Segoe UI Semibold", 14)).pack(side="left", anchor="center", padx=(8, 0))
        close = tk.Label(header, text="×", fg="#aeb6c2", bg=bg,
                         font=("Segoe UI", 17), cursor="hand2")
        close.pack(side="right", anchor="center")
        close.bind("<Button-1>", lambda _event: self.dismiss())

        body = tk.Label(outer, text=self.choose_message(), fg=fg, bg=bg,
                        font=("Segoe UI", 11), justify="left", anchor="nw",
                        wraplength=width - 38)
        body.pack(fill="x", padx=18, pady=(4, 12))
        body.bind("<Button-1>", lambda _event: self.dismiss())
        outer.bind("<Button-1>", lambda _event: self.dismiss())

        seconds = max(3, int(self.config["show_seconds"]))
        self.hide_job = self.root.after(seconds * 1000, self.dismiss)

    def dismiss(self):
        if self.hide_job is not None:
            try:
                self.root.after_cancel(self.hide_job)
            except Exception:
                pass
            self.hide_job = None
        if self.window is not None:
            try:
                if self.window.winfo_exists():
                    self.window.destroy()
            except tk.TclError:
                pass
            self.window = None

    def schedule_next(self):
        if self.next_job is not None:
            try:
                self.root.after_cancel(self.next_job)
            except Exception:
                pass
        minutes = max(1, int(self.config["interval_minutes"]))
        self.next_job = self.root.after(minutes * 60 * 1000, self.show_reminder)


def main():
    if sys.platform != "win32":
        raise SystemExit("This app is designed for Windows 11.")
    enable_dpi_awareness()
    root = tk.Tk()
    root.withdraw()
    Reminder(root, load_config())
    root.mainloop()


if __name__ == "__main__":
    main()