import boundingbox2d as bb
import numpy as np
import open3d as o3d
import os

def get3dbox(xlim,ylim,zlim,vsize):
    x=np.linspace(xlim[0],xlim[1],vsize[0])
    y=np.linspace(ylim[0],ylim[1],vsize[1])
    z=np.linspace(zlim[0],zlim[1],vsize[2])
    f=open("pointcloud.xyz",'wt',encoding='ascii')
    for i in x:
        for j in y:
            for k in z:
                rawdata=str(i)+" "+str(j)+" "+str(k)
                data=rawdata.encode('ascii')
                data=str(data).replace("b'","").replace("'","")
                f.write(str(data))
                f.write("\n")
                #print(data,file=f)
    f.close()
    pcd=o3d.io.read_point_cloud("/home/weihao/VH-Mesh/pointcloud.xyz",format='xyz') 
    print(pcd)
    print(np.asarray(pcd.points)) 
    os.remove("/home/weihao/VH-Mesh/pointcloud.xyz")
    octree=o3d.geometry.Octree()
    octree.convert_from_point_cloud(pcd)
    #o3d.visualization.draw_geometries([octree])
    return octree

def getlimits(x, y ,z):
    ans=[]

    return ans



xlim=[1,50]
ylim=[1,50]
zlim=[1,50]
vsize=[50,50,50]
get3dbox(xlim,ylim,zlim,vsize)