#!/usr/bin/env python3

import argparse
import rospy
import cv2 as cv
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import imutils
import torch
from matplotlib import pyplot as plt
import pandas as pd
from geometry_msgs.msg import PoseStamped
import math

calibration_data = np.load('/home/vineet/yolov5/camera_calibration_data.npz')
cameraMatrix = calibration_data['camera_matrix']
dist = calibration_data['dist_coeffs']
cv_image = None

msg = PoseStamped()

def tt_center(frame): 
    h,  w = frame.shape[:2]
    newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))
    frame = cv.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)
    
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

        d = math.dist(topright,bottomright)
        #print(d)
        p_to_m = d/0.015
        #print(p_to_m)

        center_x = frame.shape[1]//2
        center_y = frame.shape[0]//2

        c = [center_x,center_y]
        
        cX = int((topleft[0] + bottomright[0]) / 2.0)
        cY = int((topleft[1] + bottomright[1]) / 2.0)
    
        center = [cX,cY]
        #print(center)
        
        image = cv.circle(frame,center, radius=0, color=(0, 0, 255), thickness=5)
        image = cv.circle(image,c, radius=0, color=(255, 0, 255), thickness=5)

        cv.imshow('YOLO',image)
        cv.waitKey(1)
        
        X = cX - center_x
        Y = cY - center_y

        Fx = 575.430566
        Fy = 533.039258
        dZ = 0.32

        #x = X/p_to_m
        #y = Y/p_to_m
        #z = 0.27
        x= dZ*X/Fx
        y= dZ*Y/Fy
        print(x,y)
        
        centre = (x,y,dZ)
        msg.header.frame_id = 'camera'
        msg.pose.position.x = y
        msg.pose.position.y = x
        msg.pose.position.z = dZ
        msg.pose.orientation.x = 0
        msg.pose.orientation.y = 0
        msg.pose.orientation.z = 0
        msg.pose.orientation.w = 1

        pub.publish(msg)



def identify_testtube(frame):
    results = model(frame)
    
    #cv.imshow('YOLO',np.squeeze(results.render()))
    #cv.waitKey(1)
    print(results)
    tt_center(frame)
           
def callback(data):
    try:
        bridge = CvBridge()
        frame = bridge.imgmsg_to_cv2(data,"bgr8")
        identify_testtube(frame)
         
    except CvBridgeError as e:
        print(e)

if __name__ == '__main__':
    model = torch.hub.load('ultralytics/yolov5','custom',path='/home/vineet/yolov5/yolov5/runs/train/exp/weights/last.pt', force_reload=True)
    model.conf = 0.7
    rospy.init_node('yolo', anonymous=True)
    pub = rospy.Publisher('/cam_pose',PoseStamped, queue_size = 1)
    image_sub = rospy.Subscriber("/webcam", Image, callback, queue_size = 1, buff_size=2**24)
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv.destroyAllWindows()

