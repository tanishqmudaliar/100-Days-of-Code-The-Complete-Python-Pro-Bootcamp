import tkinter as tk

window = tk.Tk()
window.title("Mile to Kilometer Converter")
window.config(padx=20, pady=20)

def calculate():
    miles = float(input.get())
    kilometers = miles * 1.609344
    output["text"] = f"{kilometers:.2f}"

label1 = tk.Label(text="is equal to", font=("Times New Roman", 12, "bold"))
label1.grid(column=0, row=1)

input = tk.Entry(width=20)
input.grid(column=1, row=0)

output = tk.Label(text="0", font=("Times New Roman", 12, "bold"))
output.grid(column=1, row=1)

button = tk.Button(text="Calculate", command=calculate)
button.grid(column=1, row=2)

label2 = tk.Label(text="Miles", font=("Times New Roman", 12, "bold"))
label2.grid(column=2, row=0)

label3 = tk.Label(text="Kilometers", font=("Times New Roman", 12, "bold"))
label3.grid(column=2, row=1)

window.mainloop()