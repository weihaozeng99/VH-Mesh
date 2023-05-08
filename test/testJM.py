import sys
import numpy as np
sys.path.append("/home/weihao/VH-Mesh/tools")
from JarvisMarch import GiftWrapping 

P=[[0,0],[2,2],[3,2],[4,0],[2,3],[0,4],[4,4],[3,3],[-1,3]]
hull=GiftWrapping(np.array(P))
leftedge=np.array([hull[0],hull[-1]])
rightedge=[]
for i in range(0,np.size(hull,0)-1):
    if hull[i][0]>=hull[i+1][0]:
        rightedge=np.array([hull[i],hull[i+1]])
        break
print(leftedge)
print(rightedge)
