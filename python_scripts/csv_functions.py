
# import keyboard
import datetime
import tkinter as tk
from tkinter import ttk
# import func2 as f
import random
import time
import csv
from pynput import keyboard
# import config as tt_cfg

def get_curr_time():
    global current_datetime
    current_datetime = datetime.datetime.now()
    year = current_datetime.year
    month =current_datetime.month
    day = current_datetime.day
    hour = current_datetime.hour
    minute = current_datetime.minute
    second = current_datetime.second
    temp = str(year)+str(month)+str(day)+"_"+ str(hour)+str(minute)+".csv"
    return temp



count = 000
ranid = 1

# barcode=""
# # cfgg.temp_bar = ""

# def on_press(key,listener):
#     global barcode
#     print("sdf")
#     try:
#         if key == keyboard.Key.enter:
#             cfgg.temp_bar = barcode
#             barcode=""
#             print(cfgg.temp_bar)
#             f.writee('n')
#             listener.stop()
#         else:
#             barcode+=key.char	
#     except:
#         pass

# import threading

# def read_barcode():
#     # global cfgg.temp_bar
#     # print("sdf")
#     f.writee('b')
#     with keyboard.Listener(on_press=lambda event:on_press(event,listener)) as listener:
#         listener.join()
#         return cfgg.temp_bar

# keep_barcode = threading.Thread(traget=read_barcode())
# keep_barcode.setDaemon(True)
# keep_barcode.start()





def create_empty_csv(num_rows, num_columns):
    # global filename
    filename = get_curr_time()

    # Create an empty CSV file with the specified columns
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['', 'A', 'B', 'C', 'D']
        writer.writerow(header)

        # Fill the CSV file with "Not Used" in all rows and columns
        for row_num in range(1, num_rows + 1):
            row_data = ['Not Used'] * num_columns
            writer.writerow([row_num] + row_data)

def update_csv_value(filename, row_index, col_index, new_value):
    # Read the CSV file and store its contents in memory
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Check if the row and column indices are within the range of the data
    if row_index < 1 or row_index >= len(data):
        raise IndexError("Row index is out of range.")
    if col_index < 1 or col_index >= len(data[0]):
        raise IndexError("Column index is out of range.")

    # Modify the specific cell value
    data[row_index][col_index] = new_value

    # Write the updated data back to the CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def close_window_and_file(window, csvfile):
    csvfile.close()
    window.destroy()


def display_csv_data(filename):
    # Read data from the CSV file
    data = []
    with open(filename, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)

    # Create a new Tkinter window
    window = tk.Tk()
    window.title("CSV Data Display")
    window.geometry("600x300")

    # Create a Treeview widget to display the data in a table format
    tree = ttk.Treeview(window, columns=data[0], show="headings")
    for col in data[0]:
        tree.heading(col, text=col, anchor='center')
        tree.column(col, anchor='center', width=80)  # Adjust the column width as needed
    tree.pack(fill="both", expand=True)

    # Insert the data into the Treeview widget
    for row in data[1:]:
        tree.insert("", "end", values=row)

    # Create a close button
    close_button = tk.Button(window, text="Close", command=lambda: close_window_and_file(window, csvfile))
    close_button.pack()

    # Run the Tkinter main loop
    window.mainloop()

def get_tray_id(tt_data):
    if tt_data[5] == '1':
        tray_id = 2
        return tray_id
    elif tt_data[5] == '0':
        tray_id = 3
        return tray_id
    else:
        tray_id = 3
        return tray_id

def search_csv_by_tt_id(csv_filename, keyword):
    with open(csv_filename, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            if row['tt_id'] == keyword:
                return row.get('isCompleted', 'Not Found')
        else:
            return 0

filename1 = "temp_tray"

def create_empty_csv_trays(filename1, rows, columns):
    with open(filename1, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        data = [[0 for _ in range(columns)] for _ in range(rows)]
        writer.writerows(data)

def update_cell_trays(filename1, row, column):
    with open(filename1, mode='r') as csvfile:
        reader = csv.reader(csvfile)
        data = [row for row in reader]

    if 0 <= row < len(data) and 0 <= column < len(data[0]):
        data[row][column] = 1

    with open(filename1, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

        