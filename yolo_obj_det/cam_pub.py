#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

cap = cv2.VideoCapture(2)

print(cap.isOpened())
bridge = CvBridge()

def talker():
    pub = rospy.Publisher('/webcam',Image, queue_size = 1)
    rospy.init_node('camera', anonymous = False)
    rate = rospy.Rate(30)
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if not ret:
            break

        msg = bridge.cv2_to_imgmsg(frame, "bgr8")
        pub.publish(msg)

        if rospy.is_shutdown():
            cap.release()

if __name__=='__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
