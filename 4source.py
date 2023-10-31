import serial
import time
import tray_data_4s as tray_data
import random
import csv_functions as csv_func
# import img_proc as imgp
from pynput import keyboard
# import threading


database_file = "multi_source\d_database_dept.csv"

dist_x = 20.5
dist_y = 20.5

min_z = 10
max_z = 120

end_effector_stat = 1

close=0
open=1

def multi_cmd(inputCmd):
     movetoXY(inputCmd, len([char for char in inputCmd if char == ";"]))


def get_com_port(device_name):
	ports = serial.tools.list_ports.comports()
	for port, desc, hwid in sorted(ports):
		if device_name in desc:
			print("{}: {}".format(port, desc))	
			return port
          
try:
    # gantry_controller = serial.Serial(port = get_com_port("Mega"), baudrate=9600, timeout = 0.1)
    gantry_controller = serial.Serial(port="COM3", baudrate=115200, timeout = 0.1)
    device = tray_data.ReadLine(gantry_controller)
except:
    print("No Devices Connected")
    exit()
    

def conv_to_ard_cmd(x,y,z,end):
    return "%s %s %s %s ;" % (str(x), str(y), str(z), str(end))

def ardScanner(cmd):
     if cmd == "b":
        temp = "-1 -1 -1 6"
        gantry_controller.write(temp.encode('utf-8'))
     elif cmd == "n":
        temp = "-1 -1 -1 7"
        gantry_controller.write(temp.encode('utf-8'))
     

def goHome(cmd):
    cmd = "-1 -1 -1 2 ;"
    gantry_controller.write(cmd.encode('utf-8'))
    while((gantry_controller.read() != b'h')):
        pass



def movetoXY(cmd,countt):
    count = 0
    # countt = 3
    gantry_controller.write(cmd.encode('utf-8'))
    while(count!=countt):
        if((pp:=device.readline().decode()) == "e\r\n"):
            count=count+1
            # print(count)
        print(repr(pp))


def toggleEnd(cmd):
    if cmd == "close":
        cmd = "-1 -1 -1 0"
    elif cmd == "open":
        cmd = "-1 -1 -1 1"
    gantry_controller.write(cmd.encode('utf-8'))
    while((tempp:=gantry_controller.read()) != b'e'):
        print(tempp)
        pass
    print(tempp)

def move_gantry(cmd):
    global gantry_controller
    if cmd == "close":
        cmd = "-1 -1 -1 0"
    elif cmd == "open":
        cmd = "-1 -1 -1 1"
    elif cmd == "home":
        cmd = "-1 -1 -1 2"

    gantry_controller.write(cmd.encode('utf-8'))

    while True:
        if gantry_controller.read() == b'd':
            break
        if gantry_controller.read() == b'e':
            break
        if gantry_controller.read() == b'h':
            break
        else:
            pass


def start_sorting():
    # source_x, source_y = tray_id_to_xy(1, 0, 0)
    # movetoXY(conv_to_ard_cmd(source_x,source_y,min_z,1))
    count = 0
    inComp = 0
    inInComp = 0
    while True:
        # for row_idx, row in enumerate(td.tray_comp):
        #     for column_idx, column in enumerate(td.tray_comp):
        #         if 0 not in column:
        #             inComp = 1
        # for row_idx, row in enumerate(td.tray_inComp):
        #     for column_idx, column in enumerate(td.tray_inComp):
        #         if 0 not in column:
        #             inInComp = 1
        # if inInComp == 0 and inComp == 0:
        if count == 0:
            # dtt = imgp.get_filled_slots()
            for a in range(0,4):
                dtt = tray_data.source_trays[a]
                print(dtt)
                for col, val in enumerate(dtt):
                    for roww, value in enumerate(val):
                        if value == 1:
                            start_sort(a,col,roww)
            for tray in tray_data.dest_trays:
                print(tray)
                print("\n")

            tray_data.source_trays = [[] for _ in range(4)]
            tray_data.dest_trays = [[] for _ in range(5)]

            for tray in tray_data.source_trays:
                for i in range(0,12):
                    tray.append([1]*4)

            for tray in tray_data.dest_trays:
                for i in range(0,12):
                    tray.append([0]*4)
                
            count = 1
        else: 
            break


def get_dest_tray_id():
    return random.randint(0,4)
    # return 0


def tray_id_to_xy(tray_id,row,column,type):
    global dest_x, dest_y

    if type=="source":
        x_coord = tray_data.source_tray_coord[tray_id][0] + (row*dist_x)
        y_coord = tray_data.source_tray_coord[tray_id][1] - (column*dist_y)
    
    elif type=="dest":
        x_coord = tray_data.dest_tray_coord[tray_id][0] + (column*dist_x)
        y_coord = tray_data.dest_tray_coord[tray_id][1] + (row*dist_y)

    # print(x_coord, y_coord)
    return x_coord, y_coord


def	get_emp_slot(tray_list):
    for row_idx, row in enumerate(tray_list):
        if 0 in row:
            col_idx = row.index(0)
			# return [col_idx, row_idx]
            return [row_idx, col_idx]


def start_sort(source_tray_id, column, row):
    global dist_x,dist_y,end_effector_stat
    inputstring = ""

    source_x, source_y = tray_id_to_xy(source_tray_id, column, row, "source")
    print("Source: ",source_x, source_y)

    movetoXY(conv_to_ard_cmd(source_x, source_y, min_z, open), 1)
    # inputstring = inputstring + conv_to_ard_cmd(source_x, source_y, min_z, open)
    movetoXY(conv_to_ard_cmd(source_x, source_y, max_z, close), 1)
    # inputstring = inputstring + conv_to_ard_cmd(source_x, source_y, min_z, close)
    movetoXY(conv_to_ard_cmd(source_x, source_y, min_z, close), 1)
    # inputstring = inputstring + conv_to_ard_cmd(source_x, source_y, min_z, close)

    dest_tray=get_dest_tray_id()
    print("Dest: ",dest_tray)
    print(tray_data.dest_tray_coord[dest_tray])
    temp_slot = get_emp_slot(tray_data.dest_trays[dest_tray])
    # print(temp_slot)
    dest_x,dest_y = tray_id_to_xy(dest_tray, temp_slot[0], temp_slot[1],  "dest")
    print("Dest: ",dest_x,dest_y)
    tray_data.dest_trays[dest_tray][temp_slot[0]][temp_slot[1]]=1

    movetoXY(conv_to_ard_cmd(dest_x, dest_y, min_z, close), 1)
    # inputstring = inputstring + conv_to_ard_cmd(dest_x, dest_y, min_z, close)
    movetoXY(conv_to_ard_cmd(dest_x, dest_y, max_z, open), 1)
    # inputstring = inputstring + conv_to_ard_cmd(dest_x, dest_y, min_z, open)
    movetoXY(conv_to_ard_cmd(dest_x, dest_y, min_z, open), 1)
    # inputstring = inputstring + conv_to_ard_cmd(dest_x, dest_y, min_z, open)
    # print(inputstring)
    # multi_cmd(inputstring)
    print("------------------------------------------------------------")

key_pressed = False
terminate_flag = False

def key_check_timer():
    global terminate_flag
    while not terminate_flag:
        if not key_pressed:
        # no_key_pressed_action()
        # pass
            time.sleep(1)
        # pass

def terminate_thread():
    global terminate_flag
    terminate_flag = True

barcode=""
temp_bar = ""


def on_press(key,listener):
	global barcode,temp_bar,r
	# global barcode
	# print("sdf")
	try:
		if key == keyboard.Key.enter:
			temp_bar = barcode
			barcode=""
			# print(temp_bar)
			ardScanner('n')
			# to_r(2)
			listener.stop()
			# r=0
		else:
			barcode+=key.char
			terminate_thread()
			key_check_thread.join()
			# writee('n')
	except:
		pass

def read_barcode():
	global barcode,temp_bar,key_pressed,terminate_flag
	key_pressed = False
	terminate_flag = False
	# print("sdf")
	ardScanner('b')
	# key_check_thread = threading.Thread(target=key_check_timer)
	# key_check_thread.daemon = True
	# key_check_thread.start()
	with keyboard.Listener(on_press=lambda event:on_press(event,listener)) as listener:
		try:
			listener.join()
			
			# writee('n')
			return temp_bar
		except:
			# r=r+1
			# print(r)
			pass


if __name__=="__main__":
    # global end_effector_stat
    while True:
        print(" 1. To cont. sorting\n 2. To enter coord \n 3. To Home \n 4. Toggle end effectorn \n 5. Barcode Scanner")
        try:
            optt = int(input("Option:"))
        
            if optt == 1:
                start_sorting()
            elif optt == 2:
                coordd = input("Enter coord:")
                # movetoXY(coordd,1)
                print(repr(coordd))
                multi_cmd(coordd)
            elif optt == 3:
                goHome("home")
            elif optt == 4:
                if end_effector_stat == 0:
                    toggleEnd("open")
                    end_effector_stat = 1
                elif end_effector_stat == 1:
                    toggleEnd("close")
                    end_effector_stat = 0
            elif optt == 5:
                # print(read_barcode())
                tt_data=read_barcode()
                dest_tray = int(csv_func.search_csv_by_tt_id(database_file, tt_data))
                print(dest_tray)
            else:
                pass
        except:
            pass