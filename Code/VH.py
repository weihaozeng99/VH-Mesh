import sys
sys.path.append("/home/weihao/VH-Mesh/tools")
import boundingbox3d as d3
import boundingbox2d as d2
import open3d as o3d
import numpy as np
import cv2
from JarvisMarch import GiftWrapping 

 

def TwoPtoEightP(P):
    x0=P[0][0]
    y0=P[0][1]
    z0=P[0][2]
    x1=P[1][0]
    y1=P[1][1]
    z1=P[1][2]
    Points=[]
    Points.append(np.array(P[0]))#1
    Points.append(np.array([x0,y1,z0]))#2
    Points.append(np.array([x1,y1,z0]))#3
    Points.append(np.array([x1,y0,z0]))#4
    Points.append(np.array([x0,y0,z1]))#5
    Points.append(np.array([x0,y1,z1]))#6
    Points.append(np.array(P[1]))#7
    Points.append(np.array([x1,y0,z1]))#8
    return Points

#get the 2D coordinates of cube in a imag
#Input: Pmat of the imag, 
#       3D coordinates: [x0,y0,z0]
#                       [x1,y1,z1] 
#                       (point 1 and point 7)
def get2dcube(Pmat,cubeP):
    ans=[]
    Points=TwoPtoEightP(cubeP)
    for p in Points:
        newp=np.array([p[0],p[1],p[2],1])
        #print(newp)
        temp=np.matmul(Pmat,newp)

        ans.append(np.array([(temp[0]/temp[2]),(temp[1]/temp[2])]))
    return ans

#return: 1--inside
#        0--on
#        -1--out.
#input: points--8 points
def isInside_oneImag(points,Imagaddr):
    imag=cv2.imread(str(Imagaddr))
    gray = cv2.cvtColor(imag, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,0)
    contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #result=cv2.pointPolygonTest(contours,point,False)
    hull=GiftWrapping(np.array(points))
    leftedge=np.array([hull[0],hull[-1]])
    rightedge=[]
    if np.size(hull,0)>1:
        for i in range(0,np.size(hull,0)):
            next=i
            if i+1==np.size(hull,0):
                next=0
            if hull[i][0]>=hull[next][0]:
                rightedge=np.array([hull[i],hull[next+1]])
                break
    else:
        rightedge=leftedge
    #x,y,w,h = cv2.boundingRect(contours[0])
    #leftlimit=np.array([[x,y],[x,y+h]])
    #rightlimit=np.array([[x+w,y],[x+w,y+h]])
    flag=1
    for p in leftedge:
        temp=cv2.pointPolygonTest(contours[0],p,False)
        if temp:
            flag+=1
        else:
            flag+=temp
    for p in rightedge:
        temp=cv2.pointPolygonTest(contours[0],p,False)
        if temp==0:
            flag+=1
        else:
            flag+=temp
    if flag==4:
        return 1 #inside
    elif flag==-4:
        #on or outside
        for i in range(leftedge[0][0],leftedge[1][0]+1):
            testp=np.array([leftedge[0][0],i])
            if cv2.pointPolygonTest(contours[0],p,False)!=-1:
                return 0
        
        for i in range(rightedge[0][0],rightedge[1][0]+1):
            testp=np.array([rightedge[0][0],i])
            if cv2.pointPolygonTest(contours[0],p,False)!=-1:
                return 0 
        return -1 #outside   

    else:
        return 0 #on    
    return result

#CubeP --2 Points
def isInside_allImag(Pmats,Imagaddrs,NumberofImagsperPmat,cubeP):
    flag=1
    for i in range(0,np.size(Pmats,0)):
        xy=get2dcube(Pmats[i],cubeP)
        for j in range(0,NumberofImagsperPmat):
            ans=isInside_oneImag(xy,Imagaddrs[NumberofImagsperPmat\
                                          *i+j])
            if ans==-1:
                return -1 #outside
            flag*=ans 
    return flag

def SpiltSpace(CubeP):
    ans=[]
    x0=CubeP[0][0]
    y0=CubeP[0][1]
    z0=CubeP[0][2]
    x1=CubeP[1][0]
    y1=CubeP[1][1]
    z1=CubeP[1][2]
    xnew=(x0+x1)*0.5
    ynew=(y0+y1)*0.5
    znew=(z0+z1)*0.5
    
    ans.append(np.array([[x0,y0,z0],[xnew,ynew,znew]]))
    ans.append(np.array([[x0,ynew,z0],[xnew,y1,znew]]))
    ans.append(np.array([[xnew,ynew,z0],[x1,y1,znew]]))
    ans.append(np.array([[xnew,y0,z0],[x1,ynew,znew]]))
    
    ans.append(np.array([[x0,y0,znew],[xnew,ynew,z1]]))
    ans.append(np.array([[x0,ynew,znew],[xnew,y1,z1]]))
    ans.append(np.array([[xnew,ynew,znew],[x1,y1,z1]]))
    ans.append(np.array([[xnew,y1,znew],[x1,ynew,z1]]))

    return ans


    
def ComputeVH(CubeP,NumberofImag,Pmats,imagaddrset,Max,ans) :
    #ans=[]
    if Max<0:
        final=TwoPtoEightP(CubeP)
        ans.append(np.array(final))
        return ans
    flag=isInside_allImag(Pmats,imagaddrset,NumberofImag,CubeP)
    if flag==0:#on
        space=SpiltSpace(CubeP)
        for cube in space:
            ComputeVH(cube,NumberofImag,Pmats,imagaddrset,Max-1,ans)
            #ans.append(np.array(temp))
    elif flag==-1:#outside disgard
        return
    else:
        final=TwoPtoEightP(CubeP)
        ans.append(np.array(final))
        return ans
        

    




#caliaddr=input("Input the path of the calibration parameters")
#NumberofImag=int(input("Input number of imags of each camara"))
#Pmats=d2.cali(caliaddr)
