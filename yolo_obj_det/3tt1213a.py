#Magician
import math
import numpy as np

dType.SetPTPJointParams(api,200,200,200,200,200,200,200,200,0)
dType.SetPTPCoordinateParams(api,200,200,200,200,0)
dType.SetPTPJumpParams(api, 10, 200,0)
dType.SetPTPCommonParams(api, 100, 100,0)

ox=-113.21271514892578 
oy=-240.3009490966797
ans=np.arctan([oy/ox ])
theta=((180*ans/math.pi)-180)
dType.SetPTPCmd(api, 2, ox,oy, 26.0125, theta, 1)
dx=21.1645
dy=19.4893
ans=np.arctan([oy/ox ])
theta=((180*ans/math.pi)-180)
dType.SetPTPCmd(api, 2, ox+dx,oy, 26.0125, theta, 1)
ans=np.arctan([oy/ox ])
theta=((180*ans/math.pi)-180)
dType.SetPTPCmd(api, 2, ox,oy-dy, 26.0125, theta, 1)