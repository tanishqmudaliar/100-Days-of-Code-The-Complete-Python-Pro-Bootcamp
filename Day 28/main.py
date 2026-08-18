import math
from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

timer = None
reps = 0

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global timer, reps

    if timer is not None:
        window.after_cancel(timer)
        timer = None

    reps = 0

    checkmark.config(text="")
    title.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")

    start.config(state="normal")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps

    # Prevent starting another timer while one is already running
    if timer is not None:
        return

    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # Start button disabled while timer is running
    start.config(state="disabled")

    if reps % 8 == 0:
        title.config(text="Break", fg=RED)
        countdown(long_break_sec)

    elif reps % 2 == 0:
        title.config(text="Break", fg=PINK)
        countdown(short_break_sec)

    else:
        title.config(text="Work", fg=GREEN)
        countdown(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):
    global timer

    count_min = math.floor(count / 60)
    count_sec = count % 60

    canvas.itemconfig(
        timer_text,
        text=f"{count_min:02d}:{count_sec:02d}"
    )

    if count > 0:
        timer = window.after(1000, countdown, count - 1)

    else:
        timer = None

        # Add one checkmark after every completed work session
        marks = "✔️" * (reps // 2)
        checkmark.config(text=marks)

        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(pady=50, padx=100, bg=YELLOW)

title = Label(
    text="Timer",
    bg=YELLOW,
    fg=GREEN,
    font=(FONT_NAME, 45, "bold")
)
title.grid(column=1, row=0)

canvas = Canvas(
    width=200,
    height=224,
    bg=YELLOW,
    highlightthickness=0
)

tomato = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato)

timer_text = canvas.create_text(
    100,
    130,
    text="00:00",
    fill="white",
    font=(FONT_NAME, 35, "bold")
)

canvas.grid(column=1, row=1)

start = Button(
    text="Start",
    highlightthickness=0,
    command=start_timer
)
start.grid(column=0, row=2)

reset = Button(
    text="Reset",
    highlightthickness=0,
    command=reset_timer
)
reset.grid(column=2, row=2)

checkmark = Label(
    text="",
    fg=GREEN,
    bg=YELLOW
)
checkmark.grid(column=1, row=3)

window.mainloop()