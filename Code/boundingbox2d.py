import cv2
import numpy as np
import os

def bounding(addr):
    allimg=os.walk(addr)
    imags=[]
    imagaddr=[]
    for path,dir_list,file_list in allimg:
        file_list.sort(reverse=False)
        for file_name in file_list:
            imagaddr.append(np.array(os.path.join(path,file_name)))
            imag=cv2.imread(os.path.join(path,file_name))
            imags.append(np.array(imag))
    #imag=cv2.imread(addr)
    #imag=cv2.imread("/home/weihao/Downloads/VH-Datasets/action1/direc1/Silhouette1_0000.png")
    #cv2.imshow("imag",imag)
    #cv2.waitKey(0)
    ans=[]
    for i in imags:
        gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,127,255,0)
        contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        x,y,w,h = cv2.boundingRect(cnt)
        #ans=list[x,x+w,y,y+h]
        #imag = cv2.drawContours(imag,[cnt],0,(0,255,255),2)
        i = cv2.rectangle(i,(x,y),(x+w,y+h),(0,255,0),2)
        print(x,x+w,y,y+h)
        ans.append(np.array([x,x+w,y,y+h]))
        #cv2.imshow("Bounding Rectangle", i)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    return ans,imagaddr

def as_num(x):
    y='{:.10f}'.format(x)
    return y

def cali(addr):
    allfile=os.walk(addr)
    Calidata=[]
    for path,dir_list,file_list in allfile:
        file_list.sort(reverse=False)
        for file_name in file_list:
            print(os.path.join(path,file_name)+"\n")
            with open(os.path.join(path,file_name),errors='ignore') as f:
                k_set=[]
                #lines=f.readlines(3)
                for i in range(0,3):
                    l=f.readline()
                    l=l.replace("\n","")
                    k_list=l.split(" ")
                    k1=float(as_num(float(k_list[0])))
                    k2=float(as_num(float(k_list[1])))
                    k3=float(as_num(float(k_list[2])))
                    k4=float(as_num(float(k_list[3])))
                    #k_set.append(np.array([k1,k2,k3,k4]))
                    k_set.append(np.array([k1,k2,k3,k4]))
            

            Calidata.append(np.array(k_set))
    return Calidata

#bounding("/home/weihao/Downloads/grey_image/grey1/","oo")
#bounding("/home/weihao/VH-Mesh/asset/TestImag")
#print(cali("/home/weihao/Downloads/calibration/calibration-pmat/"))