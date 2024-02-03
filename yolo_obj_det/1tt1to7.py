#Magician
import math
import numpy as np

dType.SetPTPJointParams(api,200,200,200,200,200,200,200,200,0)
dType.SetPTPCoordinateParams(api,200,200,200,200,0)
dType.SetPTPJumpParams(api, 10, 200,0)
dType.SetPTPCommonParams(api, 100, 100,0)

ox=-112.39449310302734   
oy= -237.9935302734375
theta=((180*(np.arctan([oy/ox ]))/math.pi)-180)

dType.SetPTPCmd(api, 2, ox,oy, 130.0, theta, 1)
dType.SetEndEffectorSuctionCup(api, 1,  1, isQueued=1)
dType.SetPTPCmd(api, 2, ox,oy, 24.5125, theta, 1)
dType.SetPTPCmd(api, 2, ox,oy, 130.0, theta, 1)
dx=21.1645
dy=19.4893
theta=((180*(np.arctan([oy/ox+(6*dx) ]))/math.pi)-180)
dType.SetPTPCmd(api, 2, (ox+(6*dx)),oy, 130.0, theta, 1)
dType.SetPTPCmd(api, 2, (ox+(6*dx)),oy, 26.0125, theta, 1)
dType.SetEndEffectorSuctionCup(api, 1,  0, isQueued=1)
dType.SetPTPCmd(api, 2, (ox+(6*dx)),oy, 60.0125, theta, 1)