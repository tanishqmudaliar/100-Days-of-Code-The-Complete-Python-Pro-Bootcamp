import tkinter

window = tkinter.Tk()
window.title("My first GUI Program")
window.minsize(500, 300)

my_label = tkinter.Label(text="I am a label", font=("Times New Roman", 24, "bold"))
my_label.pack()

def button_clicked():
    answer = input.get() if input.get() != "" else "No Input"
    my_label["text"] = answer

button = tkinter.Button(text="Click Me", command=button_clicked)
button.pack()

input = tkinter.Entry(width=20)
input.pack()

window.mainloop()