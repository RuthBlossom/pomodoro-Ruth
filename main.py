from tkinter import *
import math
import winsound
import pygame
# Initialize pygame mixer
pygame.mixer.init()
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
# global variable
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
	window.after_cancel(timer)
	# timer_text 00:00
	canvas.itemconfig(timer_text, text="00:00")
	# title_label "Timer"
	title_Label.config(text="Timer")
	# reset check_marks
	check_marks.config(text="")
	global reps
	reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
	global reps
	reps += 1

	work_sec = WORK_MIN * 60
	short_break_sec = SHORT_BREAK_MIN * 60
	long_break_sec = LONG_BREAK_MIN * 60

	# If it's the 8th rep
	if reps % 8 == 0:
		count_down(long_break_sec)
		title_Label.config(text="Break", fg=RED)
	# If it's 2nd/4th/6th rep:
	elif reps % 2 == 0:
		count_down(short_break_sec)
		title_Label.config(text="Break", fg=PINK)
	# If it's the 1st/3rd/5th/7th rep:
	else:
		count_down(work_sec)
		title_Label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):
	count_min = math.floor(count / 60)
	count_sec = count % 60
	if count_sec < 10:
		count_sec = f"0{count_sec}"

	canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

	if count == 0:
		try:
			# Play a sound using pygame mixer
			pygame.mixer.music.load("your_sound_file.wav")  # Replace with the actual path to your sound file
			pygame.mixer.music.play()
		except Exception as e:
			print(f"Error playing sound: {e}")

	if count > 0:
		global timer
		timer = window.after(1000, count_down, count - 1)
	else:
		start_timer()
		# create a temporary variable
		marks = ""
		work_sessions = math.floor(reps / 2)
		for _ in range(work_sessions):
			marks += "✔"
		check_marks.config(text=marks)


# So now when I run the code, it's going to call this method passing in 5 over here, and then it's going to wait for
# one second, and then it's going to call this function count_down passing in five minus one


# import time
# Cant do this as it interferes with mainloop()
# count = 5
# while True:
#     time.sleep(1)
#     count -= 1


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, background=YELLOW)
# count_down(5)

# def say_something(thing):
#     print(thing)
#
# window.after(1000, say_something, "Hello" )

title_Label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_Label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# count_down(5)

# Tomato-themed button styles
button_style = {
	"bg": ["#ff4d4d", "#ff1a1a"],  # Gradient background (lighter to darker red)
	"fg": "white",
	"font": (FONT_NAME, 12, "bold"),
	"padx": 12,
	"pady": 6,
	"borderwidth": 0,
	"highlightthickness": 0,
	"activebackground": "#ff1a1a",  # Background color when the button is clicked
}

# Simple pulsating effect for the buttons
# def pulsate(button):
# 	current_bg = button.cget("background")
# 	new_bg = button_style["bg"][1] if current_bg == button_style["bg"][0] else button_style["bg"][0]
# 	button.config(background=new_bg)
# 	window.after(500, pulsate, button)


start_button = Button(text="Start", **button_style, command=start_timer)
start_button.grid(column=0, row=2)
# pulsate(start_button)

restart_button = Button(text="Reset", **button_style, command=reset_timer)
restart_button.grid(column=2, row=2)
# pulsate(restart_button)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

window.mainloop()
