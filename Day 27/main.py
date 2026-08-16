import tkinter

window = tkinter.Tk()
window.title("My first GUI Program")
window.minsize(500, 300)

def button_clicked():
    answer = input.get() if input.get() != "" else "No Input"
    my_label["text"] = answer

my_label = tkinter.Label(text="I am a label", font=("Times New Roman", 24, "bold"))
my_label.grid(column=0, row=0)

button = tkinter.Button(text="Click Me", command=button_clicked)
button.grid(column=1, row=1)

button = tkinter.Button(text="Click Me", command=button_clicked)
button.grid(column=2, row=0)

input = tkinter.Entry(width=20)
input.grid(column=3, row=2)

window.mainloop()