#Magician
import math


dType.SetPTPJointParams(api,200,200,200,200,200,200,200,200,0)
dType.SetPTPCoordinateParams(api,200,200,200,200,0)
dType.SetPTPJumpParams(api, 10, 200,0)
dType.SetPTPCommonParams(api, 100, 100,0)

pos = dType.GetPose(api)
print(pos[0],pos[1],pos[2],pos[3])