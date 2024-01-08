import threading
import tkinter as tk
from tkinter import ttk
import time


class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

        self.is_countdown_active = False
        self.is_countdown_paused = False
        self.remaining_seconds = 0
        self.countdown_thread = None

    def setup_ui(self):
        self.root.title("Countdown Timer")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#2E2E2E")
        self.style.configure(
            "TLabel",
            background="#2E2E2E",
            foreground="#FF4081",
            font=("Helvetica", 16, "bold"),
        )
        self.style.configure(
            "TButton",
            background="#008CBA",  # Hintergrundfarbe des Buttons
            foreground="#FF4081",  # Textfarbe des Buttons
            font=("Helvetica", 12, "bold"),
        )

        self.create_main_frame()

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root, padding=(20, 20), style="TFrame")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.create_label(
            "Countdown Timer", row=0, column=0, columnspan=4, pady=10
        )

        self.hour_var, self.minute_var, self.second_var = (
            tk.StringVar(value="0"),
            tk.StringVar(value="0"),
            tk.StringVar(value="0"),
        )

        self.create_time_entry("Hours", self.hour_var, row=1, column=0)
        self.create_time_entry("Minutes", self.minute_var, row=1, column=1)
        self.create_time_entry("Seconds", self.second_var, row=1, column=2)

        self.start_button = self.create_button(
            "Start Countdown", self.start_countdown, row=3, column=0, pady=20
        )
        self.pause_button = self.create_button(
            "Pause", self.pause_countdown, row=3, column=1, pady=20
        )
        self.resume_button = self.create_button(
            "Resume",
            self.resume_countdown,
            row=3,
            column=2,
            state="disabled",
            pady=20,
        )
        self.reset_button = self.create_button(
            "Reset", self.reset_countdown, row=3, column=3, pady=20
        )

        self.timer_label = self.create_label(
            "", row=4, column=0, columnspan=4, pady=20
        )

    def create_label(self, text, row, column, columnspan=1, pady=0):
        label = ttk.Label(self.main_frame, text=text, style="TLabel")
        label.grid(row=row, column=column, columnspan=columnspan, pady=pady)
        return label

    def create_time_entry(self, label_text, variable, row, column):
        ttk.Label(self.main_frame, text=label_text, style="TLabel").grid(
            row=row, column=column, padx=5, pady=5
        )
        entry = ttk.Entry(
            self.main_frame,
            textvariable=variable,
            width=5,
            font=("Helvetica", 14),
            foreground="#FF4081",
        )
        entry.grid(row=row + 1, column=column, padx=5, pady=5)
        ttk.Label(
            self.main_frame, text=label_text[0].lower(), style="TLabel"
        ).grid(row=row + 1, column=column + 1, padx=5, pady=5)

    def create_button(self, text, command, row, column, state="normal", pady=0):
        button = ttk.Button(
            self.main_frame,
            text=text,
            command=command,
            style="TButton",
            state=state,
        )
        button.grid(row=row, column=column, pady=pady)
        return button

    def start_countdown(self):
        try:
            if not self.is_countdown_active:
                hours, minutes, seconds = map(
                    int,
                    (
                        self.hour_var.get(),
                        self.minute_var.get(),
                        self.second_var.get(),
                    ),
                )
                total_seconds = hours * 3600 + minutes * 60 + seconds

                if total_seconds > 0:
                    self.is_countdown_active = True
                    self.start_button["state"] = "disabled"
                    self.pause_button["state"] = "normal"
                    self.resume_button["state"] = "disabled"
                    self.reset_button["state"] = "normal"
                    self.remaining_seconds = total_seconds
                    self.countdown_thread = threading.Thread(
                        target=self.countdown, daemon=True
                    )
                    self.countdown_thread.start()
                else:
                    self.timer_label.config(
                        text="Please enter a positive duration!"
                    )
            else:
                self.timer_label.config(text="Countdown is already active!")
        except ValueError:
            self.timer_label.config(text="Please enter valid numbers!")

    def pause_countdown(self):
        if self.is_countdown_active and not self.is_countdown_paused:
            self.is_countdown_paused = True
            self.resume_button["state"] = "normal"
            self.pause_button["state"] = "disabled"
        else:
            self.timer_label.config(
                text="Countdown is not active or already paused!"
            )

    def resume_countdown(self):
        if self.is_countdown_active and self.is_countdown_paused:
            self.is_countdown_paused = False
            self.resume_button["state"] = "disabled"
            self.pause_button["state"] = "normal"
            threading.Thread(target=self.countdown, daemon=True).start()
        else:
            self.timer_label.config(text="Countdown is not paused!")

    def reset_countdown(self):
        self.is_countdown_active = False
        self.is_countdown_paused = False
        self.start_button["state"] = "normal"
        self.pause_button["state"] = "disabled"
        self.resume_button["state"] = "disabled"
        self.reset_button["state"] = "disabled"
        self.remaining_seconds = 0
        self.timer_label.config(text="Countdown reset!")

    def countdown(self):
        while (
            self.remaining_seconds > 0
            and self.is_countdown_active
            and not self.is_countdown_paused
        ):
            hours, remainder = divmod(self.remaining_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.timer_label.config(
                text="Time left: {:02d}:{:02d}:{:02d}".format(
                    hours, minutes, seconds
                )
            )
            self.root.update()
            time.sleep(1)
            self.remaining_seconds -= 1

        if self.is_countdown_active and not self.is_countdown_paused:
            self.timer_label.config(text="Countdown complete!")
            self.start_button["state"] = "normal"
            self.pause_button["state"] = "disabled"
            self.resume_button["state"] = "disabled"
            self.reset_button["state"] = "disabled"
            self.is_countdown_active = False


if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()
