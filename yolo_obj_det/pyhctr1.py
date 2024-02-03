#Magician
import math

dType.SetPTPJointParams(api,200,200,200,200,200,200,200,200,0)
dType.SetPTPCoordinateParams(api,200,200,200,200,0)
dType.SetPTPJumpParams(api, 10, 200,0)
dType.SetPTPCommonParams(api, 100, 100,0)

dType.SetEndEffectorSuctionCup(api, 1,  1, isQueued=1)
dType.SetPTPCmd(api, 2, 243.1066, 36.02049, 26.0125, 14.5467, 1)
dType.SetPTPCmd(api, 2, 243.1066, 36.02049, 130.00, 14.5467, 1)
dType.SetPTPCmd(api, 2, 151.7801, 204.5036, 130.00, 59.4938, 1)
dType.SetPTPCmd(api, 2, 151.7801, 204.5036, 25.1837, 59.4938, 1)
dType.SetEndEffectorSuctionCup(api, 1,  0, isQueued=1)
dType.SetPTPCmd(api, 2, 183.4095, 146.6607, 78.6059, 44.7232, 1)
