import boundingbox2d as bb
import numpy as np
import open3d as o3d

def get3dbox(xlim,ylim,zlim,vsize):
    x=np.linspace(xlim[0],xlim[1],vsize[0])
    y=np.linspace(ylim[0],ylim[1],vsize[1])
    z=np.linspace(zlim[0],zlim[1],vsize[2])
    f=open("pointcloud.xyz",'a')
    for i in x:
        for j in y:
            for k in z:
                data="["+str(i)+", "+str(j)+", "+str(k)+"]\n"
                f.write(data)
    f.close()
            



xlim=[1,50]
ylim=[1,50]
zlim=[1,50]
vsize=[50,50,50]
get3dbox(xlim,ylim,zlim,vsize)