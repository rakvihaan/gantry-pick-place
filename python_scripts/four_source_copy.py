import serial
import time
import tray_data_4s as tray_data
# import main as mmmm
import random
import csv_functions as csv_func
import csv
import img_proc as imgp
# import threading

barcode_com_port = "COM19"
gantry_com_port = "COM3"

database_file = r'reg_tt_dataset.csv'

dist_x = 20.5
dist_y = 20.5

min_z = 20
max_z = 135

end_effector_stat = 1

close_gripper=0
open_gripper=1

tt_matrix=[]

last_rotation_pos = 3

def multi_cmd(inputCmd):
     movetoXY(inputCmd, len([char for char in inputCmd if char == ";"]))


def get_com_port(device_name):
	ports = serial.tools.list_ports.comports()
	for port, desc, hwid in sorted(ports):
		if device_name in desc:
			print("{}: {}".format(port, desc))	
			return port
          
    
def conv_to_ard_cmd(x,y,z,end,servo):
    return "%s %s %s %s %s ;" % (str(x), str(y), str(z), str(end), str(servo))
     

def goHome(cmd):
    cmd = "-1 -1 -1 2 %s ;" % last_rotation_pos 
    gantry_controller.write(cmd.encode('utf-8'))
    while((gantry_controller.read() != b'h')):
        pass


def rotate_gripper(rotation_pos):
    # print("rotating")
    cmd = "-1 -1 -1 9 %s ;" % rotation_pos 
    gantry_controller.write(cmd.encode('utf-8'))
    while((gantry_controller.read() != b'r')):
        pass



def movetoXY(cmd,countt):
    count = 0
    # countt = 3
    gantry_controller.write(cmd.encode('utf-8'))
    while(count!=countt):
        if(((pp:=device.readline().decode()) == "d\r\n")):
            count=count+1
            # print(count)
        # print(repr(pp))
    # temp=cmd.split(" ")
    # tray_data.current_position=[temp[0],temp[1],temp[2],temp[3]]
    # from main import update_current_pos
    # update_current_pos(tray_data.current_position)
    time.sleep(0.2)


def toggleEnd(cmd):
    if cmd == "close":
        cmd = "-1 -1 -1 0 %s ;" % last_rotation_pos 
    elif cmd == "open":
        cmd = "-1 -1 -1 1 %s ;" % last_rotation_pos
    gantry_controller.write(cmd.encode('utf-8'))
    while((tempp:=gantry_controller.read()) != b'e'):
        # print(tempp)
        pass
    # print(tempp)


def start_sorting(mode):
    global tt_matrixs
    # source_x, source_y = tray_id_to_xy(1, 0, 0)
    # movetoXY(conv_to_ard_cmd(source_x,source_y,min_z,1))
    count = 0
    inComp = 0
    inInComp = 0
    while True:
        print("sorting...")
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
            # dtt = tt_matrix
            # dtt = [[dtt[j][i] for j in range(len(dtt))] for i in range(len(dtt[0]))]
            # print("dtt")
            for a in range(0,4):
                if mode == "img":
                    # print("img",a)
                    # print(tt_matrix[a])
                    dtt = tt_matrix[a]
                    # dtt = [[dtt[j][i] for j in range(len(dtt))] for i in range(len(dtt[0]))]
                else:
                    # print("full")
                    dtt = tray_data.source_trays[a]
                print("matrix:",dtt)
                for col, val in enumerate(dtt):
                    for roww, value in enumerate(val):
                        # print(value)
                        if value == 1:
                            start_sort(a,col,roww)
                            # for row_idx, tray in enumerate(tray_data.dest_trays):
                            #     dest_tray_status = any(all(element != 0 for element in row) for row in tray)
                            #     if dest_tray_status == 1:
                            #         from main import update_status
                            #         update_status("Destination trays\n are full","red")
                            #         break
            for tray in tray_data.dest_trays:
                # print(tray)
                print("\n")

        #     tray_data.source_trays = [[] for _ in range(4)]
        #     tray_data.dest_trays = [[] for _ in range(5)]

        #     for tray in tray_data.source_trays:
        #         for i in range(0,12):
        #             tray.append([1]*4)

        #     for tray in tray_data.dest_trays:
        #         for i in range(0,12):
        #             tray.append([0]*4)
                
            count = 1
        else: 
            break


def get_dest_tray_id():
    return random.randint(1,4)
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


def search_csv_by_tt_id(csv_filename, keyword):
# def search_department(csv_file, target_tt_id):
    # print(csv_filename, keyword)
    csv_filename = r'E:\University\RAIS\scripts\gantry\multi_source\reg_tt_dataset.csv'
    try:
        with open(csv_filename, 'r', encoding='utf-8-sig') as file:
            # print(file)
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # print(row)
                if row['tt_id'] == keyword:
                #     from main import update_patient_dets
                #     update_patient_dets(row['first_name']+row['last_name'],row['age'],row['isCompleted'],row['department'],row['tt_id'])
                    # print(row['department'])
                    return row['department']
                else:
                #     from main import update_patient_dets
                #     update_patient_dets('NA','NA','NA','NA','Vacuum Tube Barcode Not Valid')
                    return '0'
    except:
        print("Error")

# def search_csv_by_tt_id(csv_filename, keyword):
# # def search_department(csv_file, target_tt_id):
#     print(csv_filename, keyword)
#     keyword = str(keyword)
#     with open(csv_filename, 'r', encoding='utf-8-sig') as file:
#         # Use 'utf-8-sig' encoding to handle the BOM
#         csv_reader = csv.DictReader(file)
#         for row in csv_reader:
#             print(row)
#             if row['tt_id'] == keyword:
#                 # print(row['department'])
#                 return row['department']
#     # If tt_id is not found
#             else:
#                 return '0'



def start_sort(source_tray_id, column, row):
    global dist_x,dist_y,end_effector_stat,last_rotation_pos
    print("sorttttt")
    source_x, source_y = tray_id_to_xy(source_tray_id, column, row, "source")
    # print("Source: ",source_x, source_y)
    # print(conv_to_ard_cmd(source_x, source_y, min_z, open_gripper,3))

    movetoXY(conv_to_ard_cmd(source_x, source_y, min_z, open_gripper, last_rotation_pos), 1)
    movetoXY(conv_to_ard_cmd(source_x, source_y, max_z, close_gripper, last_rotation_pos), 1)
    movetoXY(conv_to_ard_cmd(source_x, source_y, min_z, close_gripper, last_rotation_pos), 1)
    
    t_data=read_barcode()
    print("inside sort", t_data)
    if not t_data == None:
        print("not none")
        dest_tray = int(search_csv_by_tt_id(database_file, t_data))
        dest_tray=get_dest_tray_id()
    else:
        print("none")
        dest_tray = 0

    last_rotation_pos = 3
    rotate_gripper(last_rotation_pos)


    print("Dest: ",dest_tray)
    # print(tray_data.dest_tray_coord[dest_tray])
    temp_slot = get_emp_slot(tray_data.dest_trays[dest_tray])
    
    # print(temp_slot)
    dest_x,dest_y = tray_id_to_xy(dest_tray, temp_slot[0], temp_slot[1],  "dest")
    # print("Dest: ",dest_x,dest_y)
    # tray_data.dest_trays[dest_tray][temp_slot[0]][temp_slot[1]]=t_data
    # movetoXY(conv_to_ard_cmd(-1, -1, -1, close, 3), 1)
    # last_rotation_pos = 3
    tray_data.dest_trays[dest_tray][temp_slot[0]][temp_slot[1]]=1

    movetoXY(conv_to_ard_cmd(dest_x, dest_y, min_z, close_gripper, last_rotation_pos), 1)
    movetoXY(conv_to_ard_cmd(dest_x, dest_y, max_z, open_gripper, last_rotation_pos), 1)
    movetoXY(conv_to_ard_cmd(dest_x, dest_y, min_z, open_gripper, last_rotation_pos), 1)
    print("------------------------------------------------------------")


# barcode_data = ""
def moveXYZ(x,y,z):
    global last_rotation_pos
    movetoXY(conv_to_ard_cmd(x,y,z,end_effector_stat,last_rotation_pos), 1)
    # last_rotation_pos = servo

def read_barcode():
    global last_rotation_pos
    print("barcode")
    barcode_data = ""
    count=0
    barcode_scanner.flushInput()
    # ms=time.time*1000
    start_time = time.time()
    while not barcode_data and not (time_taken:=time.time()-start_time) >= 4:
    # while not barcode_data:
        barcode_data = barcode_scanner.readline().decode('utf-8').strip()
        # print("1")
        # print(time_taken)
        if time_taken > 1:
            if last_rotation_pos <= 180 and not barcode_data:
                # barcode_data = barcode_scanner.readline().decode('utf-8').strip()
                # print("more than 1")
                # if last_rotation_pos >= 183:
                #     last_rotation_pos = last_rotation_pos - 45
                # if barcode_data:
                #     break
                if last_rotation_pos < 183:
                    last_rotation_pos = last_rotation_pos + 45
                # print(last_rotation_pos)
                rotate_gripper(last_rotation_pos-3)
                time.sleep(1)
    if not barcode_data:
        print("no barcode data")
        return None
    print(barcode_data)
    return barcode_data


def drift_check():
    dtt = tray_data.source_trays[0]
    # print(dtt)
    for _ in range(0,10):
        for i, row in enumerate(dtt):
            for j, value in enumerate(row):
                source_x, source_y = tray_id_to_xy(0, i, j, "source")
                # print("Source: ",source_x, source_y)
                movetoXY(conv_to_ard_cmd(source_x, source_y, 20, open_gripper,last_rotation_pos), 1)

def sorting_imgp():
    global last_rotation_pos,tt_matrix
    while True:
        #tray 1 and 2
        movetoXY("290 400 1 0 3 ",1)
        # print("afgeayugbl")
        tt_matrix.append(imgp.imgg(tray_data.tray1_frame_bounds))
        tt_matrix.append(imgp.imgg(tray_data.tray2_frame_bounds))

        #tray 3 and 4
        movetoXY("600 400 1 0 3 ",1)
        tt_matrix.append(imgp.imgg(tray_data.tray3_frame_bounds))
        tt_matrix.append(imgp.imgg(tray_data.tray4_frame_bounds))
        # print(tt_matrix)
        # from main import buffer_tray_image
        # buffer_tray_image(tt_matrix)
        # for row_idx, tray in enumerate(tt_matrix):
        #     print("inside emmu")
        #     source_tray_status = any(all(element != 1 for element in row) for row in tray)
        # if not source_tray_status:
        #     print("break")
        #     break
        # print("out")
        movetoXY("300 400 10 1 3 ",1)
        start_sorting("img")

        # tt_matrix = [[] for _ in range(4)]
        # for tray in tt_matrix:
        #     for i in range(0,12):
        #         tray.append([0]*4)
        # buffer_tray_image(tt_matrix)
        
        tt_matrix=[]

def toggle_end_effector():
    global end_effector_stat
    if end_effector_stat == 0:
        toggleEnd("open")
        end_effector_stat = 1
    elif end_effector_stat == 1:
        toggleEnd("close")
        end_effector_stat = 0

def gantry_menu():
    global last_rotation_pos,tt_matrix,end_effector_stat
    while True:
        print(" 1. Sorting with Img Proc \n 2. Sort whole Tray \n 3. To enter coord \n 4. To Home \n 5. Toggle end effector \n 6. Barcode Scanner \n 7. Drift Check \n 8. Test Barcode \n \033[9m9. Test Img Proc\033[0m ")
        try:
            optt = int(input("Option:"))
            if optt == 1:
                while True:
                    #tray 1 and 2
                    movetoXY("290 400 1 0 3 ",1)
                    print("afgeayugbl")
                    # tt_matrix=imgp.imgg(tray_data.tray2_frame_bounds)
                    # tt_matrix.append(imgp.imgg(tray_data.tray1_frame_bounds))

                    #tray 3 and 4
                    movetoXY("600 400 10 1 3 ",1)
                    tt_matrix.append(imgp.imgg(tray_data.tray3_frame_bounds))
                    # tt_matrix.append(imgp.imgg(tray_data.tray4_frame_bounds))
                    print(tt_matrix)
                    # from main import updateTrayImage
                    # updateTrayImage(tt_matrix)
                    # for row_idx, tray in enumerate(tt_matrix):
                    #     print("inside emmu")
                    #     source_tray_status = any(all(element != 1 for element in row) for row in tray)
                    # if not source_tray_status:
                    #     print("break")
                    #     break
                    # print("out")
                    start_sorting("img")

                    # tt_matrix = [[] for _ in range(4)]
                    # for tray in tt_matrix:
                    #     for i in range(0,12):
                    #         tray.append([0]*4)
                    # # updateTrayImage(tt_matrix)

                    tt_matrix=[]
            elif optt == 2:
                start_sorting("full")
            elif optt == 3:
                coordd = input("Enter coord:")
                print(repr(coordd))
                movetoXY(coordd,1)
            elif optt == 4:
                goHome("home")
                last_rotation_pos = 3
            elif optt == 5:
                if end_effector_stat == 0:
                    toggleEnd("open")
                    end_effector_stat = 1
                elif end_effector_stat == 1:
                    toggleEnd("close")
                    end_effector_stat = 0
            elif optt == 6:
                tt_data=read_barcode()
                dest_tray = int(csv_func.search_csv_by_tt_id(database_file, 'R10503130-71'))
                print(dest_tray)
            elif optt==7:
                 print("6")
                 drift_check()
            elif optt==8:
                 print("7")
                 coordd = input("Enter coord:")
                 print(repr(coordd))
                 multi_cmd(coordd)
                 t_data=read_barcode()
                 print(t_data)
            elif optt==9:
                movetoXY("290 400 10 1",1)
                print("afnaefuehl")
                # import img_proc as imgp
                tt_matrix = imgp.imgg(tray_data.tray1_2_coord)
                print(tt_matrix)
            elif optt==10:
                gantry_controller.close()
                barcode_scanner.close()
                exit()
            else:
                pass
        except:
            pass

try:
    gantry_controller = serial.Serial(port=gantry_com_port, baudrate=115200, timeout = 0.1)
    barcode_scanner = serial.Serial(port=barcode_com_port, baudrate=9600, timeout=0.1)
    device = tray_data.ReadLine(gantry_controller)
except:
    print("No Devices Connected")
    exit()

if __name__=="__main__":
    try:
        gantry_controller = serial.Serial(port=gantry_com_port, baudrate=115200, timeout = 0.1)
        barcode_scanner = serial.Serial(port=barcode_com_port, baudrate=9600, timeout=0.1)
        device = tray_data.ReadLine(gantry_controller)
    except:
        print("No Devices Connected")
        exit()
    gantry_menu()