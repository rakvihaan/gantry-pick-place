import tkinter as tk
# from PIL import Image, ImageTk
import tray_data_4s as tray_data
import four_source_copy as functions
import cv2 as cv
import random
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Gantry")
root.geometry("1010x500")
# root.configure(background='#3d3d3d')

def submit_button_click():#currently does nothing
    x_value = x_entry.get()
    y_value = y_entry.get()
    z_value = z_entry.get()

    x_entry.delete(0, tk.END)
    y_entry.delete(0, tk.END)
    z_entry.delete(0, tk.END)

    update_current_pos([x_value,y_value,z_value])

start_col = 1

def home_button_click():#calls home func in 4source and updates gui elements
    # pass
    global canvas
    functions.goHome("home")
    functions.last_rotation_pos = 3
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#33dd2d", outline="#33dd2d")

def go_button_click():#moves the gantry to given x,y,z coords
    x_value = x_entry.get()
    y_value = y_entry.get()
    z_value = z_entry.get()

    print("X:", x_value)
    print("Y:", y_value)
    print("Z:", z_value)

    x_entry.delete(0, tk.END)
    y_entry.delete(0, tk.END)
    z_entry.delete(0, tk.END)

    update_current_pos([x_value,y_value,z_value,0])
    functions.moveXYZ(x_value,y_value,z_value)
    # pass


def toggle_button_click():#toggles end effector
    functions.toggle_end_effector()
    # pass
    
def buffer_tray_image():#for vacuum tubes image
    global gantry_tray_img
    updateTrayImage(gantry_tray_img)

def updateTrayImage(gantry_tray_img):#for vacuum tubes image
    # global gantry_tray_img
    print(gantry_tray_img)
    image = cv.imread(r"tt_tray.png")

    source_trays = [[] for _ in range(4)]

    for tray in source_trays:
        for i in range(0,12):
            tray.append([random.randint(0,1)]*4)
    # # print(source_trays)

    d=31.8

    for k,tray in enumerate(source_trays):
        print(tray)
        for i,row in enumerate(tray):
            # print(row)
            for j,slot in enumerate(row):
                # print(slot)
                if slot == 1:
                    image = cv.circle(image,(int(tray_data.tray_vis_coord[k][0]+(i*d)),int(tray_data.tray_vis_coord[k][1]-(j*d))), radius=0, color=(0, 0, 255), thickness=15)

    # # return image
    scale_percent=35
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)

    resized_image = cv.resize(image, (width, height), interpolation=cv.INTER_AREA)

    opencv_image_rgb = cv.cvtColor(resized_image, cv.COLOR_BGR2RGB)
    imagetk = ImageTk.PhotoImage(Image.fromarray(opencv_image_rgb))
    print("sdfsdfsdfrgrhgeiogjruighusiernvsjerigNGHNSUIDUJRIOGBJERJBIRNBRJ")
    gantry_tray_img.config(image=imagetk)
    gantry_tray_img.image(imagetk)



def start_sorting_main():#starts the main sorting function
    functions.sorting_imgp()

def cali_camera():#need to call the bounds function in img_proc, add the required prompts to before
    pass

def update_current_pos(pos):#updates the current position
    global x_curr_entry,y_curr_entry,z_curr_entry
    print(pos)

    x_curr_entry.delete(0, tk.END)
    y_curr_entry.delete(0, tk.END)
    z_curr_entry.delete(0, tk.END)
    end_curr_entry.delete(0, tk.END)

    x_curr_entry.insert(0,pos[0])
    y_curr_entry.insert(0,pos[1])
    z_curr_entry.insert(0,pos[2])
    end_curr_entry.insert(0,pos[3])

def update_status(message,bgc):#updates the message on top
    global gantry_status_text
    gantry_status_text.config(text = message, bg = bgc)

def update_patient_dets(name,age,comp,dept,ttid):#displays the vacuum tube details
    global curr_tt_text
    temp = "{} \nName: {} \nAge: {} \nAll Tests Done: {} \nDepartment: {}".format(ttid,name,age,comp,dept)
    curr_tt_text.set(temp)

def main_gui(gantry_tray_img):
    global root,canvas,radius,x,y,x_entry,y_entry,z_entry,gantry_status_text,x_curr_entry,y_curr_entry,z_curr_entry,end_curr_entry,curr_tt_text
    for i in range(15):  
        root.columnconfigure(i, minsize=20)  

    gantry_label = tk.Label(root,text="Vacuum Tube Sorter",font=("Arial 18 bold" ), anchor="center").grid(row=0,column=8, columnspan=8, padx=2, pady=5)


    # button_width = 20
    home_button = tk.Button(root, text="Home", command=home_button_click, width = 20).grid(row=2, column=start_col, padx=2, pady=5, columnspan=5)

    toggle_button = tk.Button(root, text="Get Destination Tray ID", command=buffer_tray_image, width = 20).grid(row=4, column=start_col, columnspan=5, padx=2, pady=5)

    sort_button = tk.Button(root, text="Start Sorting", command=start_sorting_main, width = 20).grid(row=3, column=start_col, columnspan=5, padx=2, pady=5)

    cam_calibration_button = tk.Button(root, text="Setup Camera", command=cali_camera, width = 20).grid(row=5, column=start_col, columnspan=5, padx=2, pady=5)

    canvas = tk.Canvas(root, width=7, height=7, bg="white")
    x, y, radius = 5, 5, 3
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="red", outline="red")
    canvas.grid(row=2, column=start_col)

    goto_col=start_col+6
    goto_row=2

    app = tk.Label(root, text="Move End Effector:",  height=1, anchor="center", font="Ariel 10 bold").grid(row=1, column=goto_col-1,columnspan=3)

    x_label = tk.Label(root, text="X:", anchor="w")
    x_entry = tk.Entry(root, width=10)

    y_label = tk.Label(root, text="Y:", anchor="w")
    y_entry = tk.Entry(root, width=10)

    z_label = tk.Label(root, text="Z:", anchor="w")
    z_entry = tk.Entry(root, width=10)

    # end_label = tk.Label(root, text="End:", anchor="w")
    # end_entry = tk.Entry(root, width=5)


    go_to_coord = tk.Button(root, text="Go", command=go_button_click, width=10)
    go_to_end = tk.Button(root, text="Toggle", command=toggle_button_click, width=10,bg="#4ac97f")


    # Arrange the labels, entry boxes, and button in a grid
    x_label.grid(row=goto_row, column=goto_col-1, padx=2, pady=5, sticky=tk.E)
    x_entry.grid(row=goto_row, column=goto_col, padx=2, pady=5)

    y_label.grid(row=goto_row+1, column=goto_col-1, padx=2, pady=5, sticky=tk.E)
    y_entry.grid(row=goto_row+1, column=goto_col, padx=2, pady=5)

    z_label.grid(row=goto_row+2, column=goto_col-1, padx=2, pady=5, sticky=tk.E)
    z_entry.grid(row=goto_row+2, column=goto_col, padx=2, pady=5)

    # end_label.grid(row=goto_row+3, column=goto_col-1, padx=2, pady=5, sticky=tk.E)
    # end_entry.grid(row=goto_row+3, column=goto_col, padx=2, pady=5)

    go_to_coord.grid(row=goto_row+3, column=goto_col-3, columnspan=6, pady=5)
    go_to_end.grid(row=goto_row+4, column=goto_col-3, columnspan=6, pady=5)

    # app = tk.Label(root, text="     ", width=5, height=1).grid(row=5, column=7)

    # gapp2 = tk.Label(root, text="     ", width=5).grid(row=3, column=9)
    x_curr_label = tk.Label(root, text="X:     ", anchor="w")
    x_curr_entry = tk.Entry(root, width=10)

    y_curr_label = tk.Label(root, text="Y:     ", anchor="w")
    y_curr_entry = tk.Entry(root, width=10)

    z_curr_label = tk.Label(root, text="Z:    ", anchor="w")
    z_curr_entry = tk.Entry(root, width=10)

    end_curr_label = tk.Label(root, text="End:    ", anchor="w")
    end_curr_entry = tk.Entry(root, width=10)

    curr_col=goto_col+4

    app = tk.Label(root, text="Current Position:",  height=1, anchor="center", font="Ariel 10 bold").grid(row=1, column=curr_col-1,columnspan=5)

    x_curr_label.grid(row=2, column=curr_col-1, padx=2, pady=5, sticky=tk.E)
    x_curr_entry.grid(row=2, column=curr_col, padx=2, pady=5)

    y_curr_label.grid(row=3, column=curr_col-1, padx=2, pady=5, sticky=tk.E)
    y_curr_entry.grid(row=3, column=curr_col, padx=2, pady=5)

    z_curr_label.grid(row=4, column=curr_col-1, padx=2, pady=5, sticky=tk.E)
    z_curr_entry.grid(row=4, column=curr_col, padx=2, pady=5)

    end_curr_label.grid(row=5, column=curr_col-1, padx=2, pady=5, sticky=tk.E)
    end_curr_entry.grid(row=5, column=curr_col, padx=2, pady=5)

    curr_tt_text = tk.StringVar()
    curr_tt_id = tk.Label(root, text="Test Tube Details:",  height=1, font="Ariel 10 bold", justify="left").grid(row=8, column=curr_col-5, columnspan=3, padx=50)
    curr_tt = tk.Label(root, width=30, height=10, bg="#404040",fg="white",textvariable=curr_tt_text, anchor='nw',justify='left').grid(row=9, column=curr_col-5, padx=50, pady=5, rowspan=10,columnspan=6)

    empty_text = tk.Label(root,text="",height=1).grid(row=7, column=0)

    dest_tray_id = tk.Label(root, text="Destination Tray ID:",  height=1, font="Ariel 10 bold", justify="left").grid(row=8, column=2, columnspan=3)
    dest_col = 2
    dest_tray_1 = tk.Label(root, text=" 1: ", anchor="w").grid(row=9, column=dest_col, padx=2, pady=5, sticky=tk.E)
    dest_tray_1 = tk.Entry(root, width=15).grid(row=9, column=dest_col+1, padx=2, pady=5)

    dest_tray_2 = tk.Label(root, text=" 2: ", anchor="w").grid(row=9+1, column=dest_col+0, padx=2, pady=5, sticky=tk.E)
    dest_tray_2 = tk.Entry(root, width=15).grid(row=9+1, column=dest_col+1, padx=2, pady=5)

    dest_tray_3 = tk.Label(root, text=" 3: ", anchor="w").grid(row=9+2, column=dest_col+0, padx=2, pady=5, sticky=tk.E)
    dest_tray_3 = tk.Entry(root, width=15).grid(row=9+2, column=dest_col+1, padx=2, pady=5)

    dest_tray_4 = tk.Label(root, text=" 4: ", anchor="w").grid(row=9+3, column=dest_col+0, padx=2, pady=5, sticky=tk.E)
    dest_tray_4 = tk.Entry(root, width=15).grid(row=9+3, column=dest_col+1, padx=2, pady=5)

    dest_tray_5 = tk.Label(root, text=" 5: ", anchor="w").grid(row=9+4, column=dest_col+0, padx=2, pady=5, sticky=tk.E)
    dest_tray_5 = tk.Entry(root, width=15).grid(row=9+4, column=dest_col+1, padx=2, pady=5)


    # image = cv.imread(r"tt_tray.png")

    # scale_percent=35
    # width = int(image.shape[1] * scale_percent / 100)
    # height = int(image.shape[0] * scale_percent / 100)

    # resized_image = cv.resize(image, (width, height), interpolation=cv.INTER_AREA)

    # opencv_image_rgb = cv.cvtColor(resized_image, cv.COLOR_BGR2RGB)
    # imagetk = ImageTk.PhotoImage(Image.fromarray(opencv_image_rgb))

    # gantry_tray_img = tk.Label(root, image=imagetk)
    gantry_tray_img.grid(row=3, column=15, padx=2, pady=5,rowspan=13,columnspan=5)

    # gantry_status = tk.Text(root,width=18,height=3,bg="red").grid(row=1, column=18, padx=2, pady=5,rowspan=4,columnspan=6)
    gantry_status_text = tk.Label(root, text="Not\nInitialized", anchor="center",bg="green",font="Ariel 12 bold",fg = "white")
    gantry_status_text.grid(row=1, column=18, padx=12, pady=15, sticky=tk.E,rowspan=2)


    root.mainloop()

if __name__=="__main__":
    image = cv.imread(r"tt_tray.png")

    scale_percent=35
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)

    resized_image = cv.resize(image, (width, height), interpolation=cv.INTER_AREA)

    opencv_image_rgb = cv.cvtColor(resized_image, cv.COLOR_BGR2RGB)
    imagetk = ImageTk.PhotoImage(Image.fromarray(opencv_image_rgb))

    gantry_tray_img = tk.Label(root, image=imagetk)
    main_gui(gantry_tray_img)