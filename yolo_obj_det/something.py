import numpy as np
import cv2
import torch
import cv2 as cv

cap = cv2.VideoCapture(2)
model = torch.hub.load('ultralytics/yolov5','custom',path='/home/vineet/yolov5/yolov5/runs/train/exp/weights/last.pt',  force_reload=True)
model.conf = 0.85
# add the path to your best.pt in path
while(True):
    
    ret, frame = cap.read()

    results = model(frame)
    df = results.pandas().xyxy[0]  # im predictions (pandas)
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
        #print(center)
        
        image = cv.circle(frame,(cX,cY), radius=0, color=(0, 0, 255), thickness=5)
        #image = cv.circle(image,c, radius=0, color=(255, 0, 255), thickness=5)

        cv.imshow('YOLO',image)
        cv.waitKey(1)
        
    
   

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
