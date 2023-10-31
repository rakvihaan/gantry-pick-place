import tkinter as tk

root = tk.Tk()
root.title("Gantry")
root.geometry("455x250")

def submit_button_click():
    x_value = x_entry.get()
    y_value = y_entry.get()
    z_value = z_entry.get()

    # You can use the values of x_value, y_value, and z_value as needed
    print("X:", x_value)
    print("Y:", y_value)
    print("Z:", z_value)

start_col = 4

def home_button_click():
    pass

def go_button_click():
    pass

def toggle_button_click():
    pass

def start_sorting_main():
    pass


for i in range(15):  
    root.columnconfigure(i, minsize=20)  

# button_width = 20
home_button = tk.Button(root, text="Home", command=home_button_click, width = 40)
home_button.grid(row=2, column=start_col, padx=2, pady=5, columnspan=9)
toggle_button = tk.Button(root, text="Toggle End Effector", command=toggle_button_click, width = 40)
toggle_button.grid(row=1, column=start_col, columnspan=9, padx=2, pady=5)
sort_button = tk.Button(root, text="Start Sorting", command=start_sorting_main, width = 40)
sort_button.grid(row=3, column=start_col, columnspan=9, padx=2, pady=5)



x_label = tk.Label(root, text="X:")
x_entry = tk.Entry(root, width=5)

y_label = tk.Label(root, text="Y:")
y_entry = tk.Entry(root, width=5)

z_label = tk.Label(root, text="Z:")
z_entry = tk.Entry(root, width=5)

end_label = tk.Label(root, text="End:")
end_entry = tk.Entry(root, width=5)


go_to_coord = tk.Button(root, text="Go", command=submit_button_click, width=5)

# Arrange the labels, entry boxes, and button in a grid
x_label.grid(row=0, column=start_col, padx=2, pady=5, sticky=tk.E)
x_entry.grid(row=0, column=start_col+1, padx=2, pady=5)

y_label.grid(row=0, column=start_col+2, padx=2, pady=5, sticky=tk.E)
y_entry.grid(row=0, column=start_col+3, padx=2, pady=5)

z_label.grid(row=0, column=start_col+4, padx=2, pady=5, sticky=tk.E)
z_entry.grid(row=0, column=start_col+5, padx=2, pady=5)

end_label.grid(row=0, column=start_col+6, padx=2, pady=5, sticky=tk.E)
end_entry.grid(row=0, column=start_col+7, padx=2, pady=5)

go_to_coord.grid(row=0, column=start_col+8, columnspan=1, pady=5)

app = tk.Label(root, text="     ", width=5, height=1).grid(row=5, column=7)
app = tk.Label(root, text="Current Position:",  height=1).grid(row=6, column=start_col+1,columnspan=3)
# gapp2 = tk.Label(root, text="     ", width=5).grid(row=3, column=9)
x_curr_label = tk.Label(root, text="X:")
x_curr_entry = tk.Entry(root, width=5)

y_curr_label = tk.Label(root, text="Y:")
y_curr_entry = tk.Entry(root, width=5)

z_curr_label = tk.Label(root, text="Z:")
z_curr_entry = tk.Entry(root, width=5)

end_curr_label = tk.Label(root, text="End:")
end_curr_entry = tk.Entry(root, width=5)

x_curr_label.grid(row=7, column=start_col, padx=2, pady=5, sticky=tk.E)
x_curr_entry.grid(row=7, column=start_col+1, padx=2, pady=5)

y_curr_label.grid(row=7, column=start_col+2, padx=2, pady=5, sticky=tk.E)
y_curr_entry.grid(row=7, column=start_col+3, padx=2, pady=5)

z_curr_label.grid(row=7, column=start_col+4, padx=2, pady=5, sticky=tk.E)
z_curr_entry.grid(row=7, column=start_col+5, padx=2, pady=5)

end_curr_label.grid(row=7, column=start_col+6, padx=2, pady=5, sticky=tk.E)
end_curr_entry.grid(row=7, column=start_col+7, padx=2, pady=5)


root.mainloop()
