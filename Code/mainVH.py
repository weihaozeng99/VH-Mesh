import VH
import mcubes
import numpy as np
import boundingbox2d as bb
import boundingbox3d as bbb
import ReadPmat as R

#caliaddr=input("Input the path of the calibration parameters")
caliaddr="/home/weihao/Downloads/Test/cali_P/temple_par.txt"
Pmats=R.ReadPmat(caliaddr)
#imagaddr=input("Input the path of the imags")
imagaddr="/home/weihao/Downloads/Test/Imags/"

Noues,imags=bb.bounding(imagaddr)
NumberofImag=1
#NumberofImag=int(input("Input number of imags of each camara"))
TestCube=[[-0.06,0.002,-0.05],[0.05,0.17,0.04]]
#TestCube.append(np.array([[-3,2,1],[2,3,3]]))
points=[]
VH.ComputeVH(TestCube,NumberofImag,Pmats,imags,5,points)
maxV=np.max(points)
isoV=maxV-np.round((maxV/100)*5)-0.5
v,t=mcubes.marching_cubes(np.array(points),1.5)
mcubes.export_obj(v, t, '/home/weihao/VH-Mesh/test/VH.obj')