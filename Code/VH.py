import sys
sys.path.append("/home/weihao/VH-Mesh/tools")
import boundingbox3d as d3
import boundingbox2d as d2
import open3d as o3d
import numpy as np
import cv2
from JarvisMarch import GiftWrapping 

#get the 2D coordinates of cube in a imag
#Input: Pmat of the imag, 3D coordinates
def get2dcube(Pmat,cubeP):
    ans=[]
    for p in cubeP:
        ans.append(np.array(np.matmul(Pmat,p)))
    return ans

#return: 1--inside
#        0--on
#        -1--out
def isInside_oneImag(points,Imagaddr):
    imag=cv2.imread(Imagaddr)
    gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,0)
    contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #result=cv2.pointPolygonTest(contours,point,False)
    hull=GiftWrapping(points)
    leftedge=np.array([hull[0],hull[-1]])
    rightedge=[]
    for i in range(0,np.size(hull,0)-1):
        if hull[i][0]>=hull[i+1][0]:
            rightedge=np.array([hull[i],hull[i+1]])
            break
    x,y,w,h = cv2.boundingRect(contours[0])
    leftlimit=np.array([[x,y],[x,y+h]])
    rightlimit=np.array([[x+w,y],[x+w,y+h]])
    flag=1
    for p in leftedge:
        if cv2.pointPolygonTest(contours,p,False)==0:
            flag+=1
        else:
            flag+=cv2.pointPolygonTest(contours,p,False)
    for p in rightedge:
        if cv2.pointPolygonTest(contours,p,False)==0:
            flag+=1
        else:
            flag+=cv2.pointPolygonTest(contours,p,False)
    if flag==4:
        return 1 #inside
    elif flag==-4:
        #on or outside
        for i in range(leftedge[0][0],leftedge[1][0]):
            testp=np.array([leftedge[0][0],i])
            if cv2.pointPolygonTest(contours,p,False)!=-1:
                return 0
        
        for i in range(rightedge[0][0],rightedge[1][0]):
            testp=np.array([rightedge[0][0],i])
            if cv2.pointPolygonTest(contours,p,False)!=-1:
                return 0 
        return -1 #outside   

    else:
        return 0 #on    
    return result

def isInside_allImag(Pmats,Imagaddrs,NumberofImagsperPmat,cubeP):
    flag=1
    for i in range(0,np.size(Pmats)-1):
        xy=get2dcube(Pmats[i],cubeP)
        for j in range(0,NumberofImagsperPmat-1):
            ans=isInside_oneImag(xy,Imagaddrs[NumberofImagsperPmat\
                                          *i+j])
            if ans==-1:
                return -1 #outside
            flag*=ans 
    return flag



def ComputeVH(box,NumberofImag,Pmats,imagaddrset) :

    




caliaddr=input("Input the path of the calibration parameters")
NumberofImag=int(input("Input number of imags of each camara"))
Pmats=d2.cali(caliaddr)
