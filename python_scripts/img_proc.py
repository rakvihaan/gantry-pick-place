import numpy as np
import torch
import cv2 as cv
# import time
from math import atan2
# import tray_data_4s as tray_data
# import matplotlib.pyplot as plt

cap = cv.VideoCapture(1)
print("Img Processing")
model = torch.hub.load(r'..\yolo_obj_det\yolov5','custom',path=r"..\yolo_obj_det\yolov5\runs\train\exp\weights\last.pt",source='local', force_reload=True)

model.conf = 0.85
dot_coordinates = []
stm=np.zeros((4,12),dtype=int)
ox=90
oy=108

dx=73
dy=79
# ox=292
# oy=368
# dx=29
# dy=25

filled=False

ofx=40
ofy=40

#
def getmatrix(frame):
    global cap,model,dot_coordinates,stm,ox,oy,dx,dy
    # ret, frame = cap.read()
    # if not ret:
    #     # break
    #     pass
    
    results = model(frame)
    df = results.pandas().xyxy[0]
    xmin = df.iloc[:,0]
    xmax = df.iloc[:,2]
    ymin = df.iloc[:,1]
    ymax = df.iloc[:,3]

    for i in range(len(xmax)):
        bottomright = [int(xmax[i]),int(ymin[i])]
        topleft = [int(xmin[i]),int(ymax[i])]
        
        cX = int((topleft[0] + bottomright[0]) / 2.0)
        cY = int((topleft[1] + bottomright[1]) / 2.0)
    
        center = (cX,cY)
        
        image = cv.circle(frame,(cX,cY), radius=0, color=(0, 0, 255), thickness=5)
        
        dot_coordinates.append((cX, cY))
                  
        for i, coord in enumerate(dot_coordinates):
            # print(f"Dot {i+1}: ({coord[0]}, {coord[1]})")
            for i in range(0,4):
                for j in range(0,12):
                    xv=ox+(j*dx)  
                    yv=oy+(i*dy) 
                        
                    if cX in range(xv-ofx,xv+ofx) and cY in range(yv-ofy,yv+ofy):
                        stm[i][j]=1

        if len(dot_coordinates)>96:
            dot_coordinates = []
        
        # cv.imshow('YOLO',image)
        # cv.waitKey(1)

#to get tray boundary coords for calibration    
def get_tray_bounds(frame):
    tt_count = 0
    while not tt_count == 4:
        global cap,model,stm,ox,oy,dx,dy
        dot_coordinates=[]
        ret, frame = cap.read()

        results = model(frame)
        df = results.pandas().xyxy[0]
        xmin = df.iloc[:,0]
        xmax = df.iloc[:,2]
        ymin = df.iloc[:,1]
        ymax = df.iloc[:,3]

        for i in range(len(xmax)):
            bottomright = [int(xmax[i]),int(ymin[i])]
            topleft = [int(xmin[i]),int(ymax[i])]
            
            cX = int((topleft[0] + bottomright[0]) / 2.0)
            cY = int((topleft[1] + bottomright[1]) / 2.0)
        
            center = (cX,cY)
            
            image = cv.circle(frame,(cX,cY), radius=0, color=(0, 0, 255), thickness=5)
            image = frame
            cv.imshow('YOLO',image)
            cv.waitKey(1)
            
            dot_coordinates.append([cX, cY])
            tt_count = len(dot_coordinates)
            
    if len(dot_coordinates)==4:
        center = (sum(x for x, y in dot_coordinates) / len(dot_coordinates), sum(y for x, y in dot_coordinates) / len(dot_coordinates))

        sorted_coordinates = sorted(dot_coordinates, key=lambda point: atan2(point[1] - center[1], point[0] - center[0]))

        print(sorted_coordinates)

        tray_bounds=[]
        offset_bounds=50
        for i, coord in enumerate(sorted_coordinates):
            if i == 0:
                tray_bounds.append([coord[0]-offset_bounds,coord[1]-offset_bounds])
            if i == 1:
                tray_bounds.append([coord[0]+offset_bounds,coord[1]-offset_bounds])
            if i == 2:
                tray_bounds.append([coord[0]+offset_bounds,coord[1]+offset_bounds])
            if i == 3:
                tray_bounds.append([coord[0]-offset_bounds,coord[1]+offset_bounds])
        print(tray_bounds)
        return tray_bounds,frame

#useless for now
def get_filled_slots(frame):
    global stm
    getmatrix(frame)
    temp = stm.copy()
    stm=np.zeros((4,12),dtype=int)
    # print("tray")
    # print(temp)
    return temp

#to get the pallet presence matrix
def imgg(bounds):
    global editttt
    ret, image = cap.read()
    print("imgbounds")
    width, height = image.shape[0], image.shape[1]
    pts1 = np.float32(bounds)
    pts2 = np.float32([[0,0],[height,0],[height,width],[0,width]])
    M = cv.getPerspectiveTransform(pts1,pts2)
    dst = cv.warpPerspective(image,M,(height,width))

    width_scale_factor = 1.6

    height, width = dst.shape[:2]

    new_width = int(width * width_scale_factor)

    stretched_image = cv.resize(dst, (new_width, height))

    cv.imshow("Rotated and Cropped Image", stretched_image)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    temp = get_filled_slots(stretched_image)
    temp = [[temp[j][i] for j in range(len(temp))] for i in range(len(temp[0]))]
    # print(temp)
    return temp

# ret, frame = cap.read()
# get_tray_bounds(frame)

# print("tray1:")
# imgg([[95, -38], [639, -41], [639, 177], [101, 183]])
# print("tray2:")
# print(imgg([[99, 177], [640, 169], [645, 388], [98, 396]]))

# [[72, -32], [617, -37], [619, 178], [79, 194]]
# [[76, 189], [622, 171], [626, 390], [81, 412]]
#after wiring
#[[95, -38], [639, -41], [639, 177], [101, 183]]
#[[99, 177], [640, 169], [645, 388], [98, 396]]