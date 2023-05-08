import VH
import mcubes
import numpy as np
import boundingbox2d as bb
import boundingbox3d as bbb

#caliaddr=input("Input the path of the calibration parameters")
caliaddr="/home/weihao/Downloads/calibration/calibration-pmat/"
Pmats=bb.cali(caliaddr)
#imagaddr=input("Input the path of the imags")
imagaddr="/home/weihao/VH-Mesh/asset/TestImag"

Noues,imags=bb.bounding(imagaddr)
NumberofImag=1
#NumberofImag=int(input("Input number of imags of each camara"))
TestCube=[[-1.5,1.5,1],[1.5,3,3]]
#TestCube.append(np.array([[-3,2,1],[2,3,3]]))
points=[]
VH.ComputeVH(TestCube,NumberofImag,Pmats,imags,2,points)
maxV=np.max(points)
isoV=maxV-np.round((maxV/100)*5)-0.5
v,t=mcubes.marching_cubes(np.array(points),isoV)
mcubes.export_obj(v, t, '/home/weihao/VH-Mesh/test/VH.obj')