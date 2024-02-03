import numpy as np
import torch
import cv2 as cv


cap = cv.VideoCapture(1)
model = torch.hub.load(r'yolo_img_p\yolov5','custom',path=r"yolo_img_p\yolov5\runs\train\exp\weights\last.pt",source='local', force_reload=True)
model.conf = 0.85
dot_coordinates = []
stm=np.zeros((4,12),dtype=int)
ox=41
oy= 101
dx=50
dy=50
# =============================================================================
# ofx=25
# ofy=15
# =============================================================================
ofx=25 #30#25
ofy=15 #30#15
# add the path to your best.pt in path
while(True):
    
    ret, frame = cap.read()
    if not ret:
        break

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
        
        dot_coordinates.append((cX, cY))
        # ##########################################################################
        # if len(dot_coordinates) > 0:
        #     # Find the minimum area bounding rectangle (rotated rectangle) for all detected centers
        #     rect = cv.minAreaRect(np.array(dot_coordinates))
        #     box = cv.boxPoints(rect)
        #     box = np.int0(box)

        #     # Draw the rotated rectangle on the frame
        #     cv.drawContours(frame, [box], 0, (255, 0, 0), 2)
            
        #     ox, oy= box[1]
            

        #     # Detect points on the top line (above the top-left point)
        #     tl = [dot_coordinates for dot_coordinates in dot_coordinates if dot_coordinates[1] < oy]
        #     spx = min(tl, key=lambda p: np.linalg.norm(np.array(p) - np.array([ox, oy]))) if tl else (0, 0)
        #     dx=int(spx[0]-ox)
        #     # Detect points on the left line (to the left of the top-left point)
        #     ll = [dot_coordinates for dot_coordinates in dot_coordinates if dot_coordinates[0] < ox]
        #     spy = min(ll, key=lambda p: np.linalg.norm(np.array(p) - np.array([ox, oy]))) if ll else (0, 0)
        #     dy=int(spy[1]-oy)
            #######################################################################
        # file1 = open("C:/DobotStudio/myfile.txt","w")
                  
        for i, coord in enumerate(dot_coordinates):
            print(f"Dot {i+1}: ({coord[0]}, {coord[1]})")
            
            for i in range(0,4):
                for j in range(0,12):
                    xv=ox+(j*dx)   #(j*38)
                    yv=oy+(i*dy)   #(i*34)

                        
                    if cX in range(xv-ofx,xv+ofx) and cY in range(yv-ofy,yv+ofy):
                        stm[i][j]=1
                    # file1.writelines(str(stm[i][j]))
                #file1.writelines("\n")
                # if (i==3):
                  #file1.writelines("\n")
                #   file1.seek(0)
                  
               
        # print(stm)
        #file1.close()
        
        
        cv.imshow('YOLO',image)
        cv.waitKey(1)
        # file1.close()
    key = cv.waitKey(10)
    if key == 27:
        break     
    
   

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

