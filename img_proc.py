import numpy as np
import torch
import cv2 as cv
import time

cap = cv.VideoCapture(1)
print("before")
model = torch.hub.load(r'E:\University\RAIS\scripts\yolo_img_p\yolov5','custom',path=r"E:\University\RAIS\scripts\yolo_img_p\yolov5\runs\train\exp\weights\last.pt",source='local', force_reload=True)
print("after")
model.conf = 0.85
dot_coordinates = []
stm=np.zeros((4,12),dtype=int)
ox=292
oy=368
dx=29
dy=25

filled=False

ofx=25 
ofy=15 

# while(True):

def getmatrix():
    global cap,model,dot_coordinates,stm,ox,oy,dx,dy
    ret, frame = cap.read()
    if not ret:
        # break
        pass
    
    original_height, original_width = frame.shape[:2]

	# Calculate the dimensions for the cropped frame
    new_width = int(original_width * 0.5)
    new_height = int(original_height * 0.5)

	# Calculate the coordinates for cropping (centered)
    # start_x = (original_width - new_width) // 2
    # start_y = (original_height - new_height) // 2
    # end_x = start_x + new_width
    # end_y = start_y + new_height

	

	# Crop the frame
    # cropped_frame = frame[start_y:end_y, start_x:end_x]
    # original_height, original_width = cropped_frame.shape[:2]
    # zoomed_frame = cv.resize(cropped_frame, (2 * original_width, 2 * original_height))
    # Display the cropped frame
    # cv.imshow('Frame', frame)
    # cv.imshow('Cropped Frame', cropped_frame)
    # cv.imshow('zoomed Frame', zoomed_frame)





    results = model(frame)
    df = results.pandas().xyxy[0]
    xmin = df.iloc[:,0]
    xmax = df.iloc[:,2]
    ymin = df.iloc[:,1]
    ymax = df.iloc[:,3]

    for i in range(len(xmax)):
        topright = [int(xmax[i]),int(ymax[i])]
        bottomright = [int(xmax[i]),int(ymin[i])]
        topleft = [int(xmin[i]),int(ymax[i])]
        bottomleft = [int(xmin[i]),int(ymin[i])]
        #print(bottomleft,bottomright,topleft,topright)
        

      
        
        cX = int((topleft[0] + bottomright[0]) / 2.0)
        cY = int((topleft[1] + bottomright[1]) / 2.0)
    
        center = (cX,cY)
        
        image = cv.circle(frame,(cX,cY), radius=0, color=(0, 0, 255), thickness=5)
        cv.imshow('YOLO',image)
        cv.waitKey(1)
        #image = cv.circle(image,c, radius=0, color=(255, 0, 255), thickness=5)
        
        dot_coordinates.append((cX, cY))
                  
        for i, coord in enumerate(dot_coordinates):
            print(f"Dot {i+1}: ({coord[0]}, {coord[1]})")
            
            for i in range(0,4):
                for j in range(0,12):
                    xv=ox+(j*dx)  
                    yv=oy+(i*dy) 

                        
                    if cX in range(xv-ofx,xv+ofx) and cY in range(yv-ofy,yv+ofy):
                        stm[i][j]=1
                    # else:
                    #     stm[i][j]=0
        if len(dot_coordinates)>96:
            dot_coordinates = []

        
        # cv.imshow('YOLO',image)
        # cv.waitKey(1)
        # file1.close()

    
def get_filled_slots():
    global stm
    getmatrix()
    temp = stm.copy()
    stm=np.zeros((4,12),dtype=int)
    print("tray")
    print(temp)
    return temp
# lastt = 0


# # while not filled:
while True:
    temp = get_filled_slots()
    print(temp)
#     print(lastt - (time.time_ns() // 1_000_000))
#     lastt = time.time_ns() // 1_000_000
