import cv2
import numpy as np
import os

def bounding(addr,caliaddr):
    allimg=os.walk(addr)
    imags=[]
    for path,dir_list,file_list in allimg:
        for file_name in file_list:
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
        cv2.imshow("Bounding Rectangle", i)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return ans

def cali(addr):
    allfile=os.walk(addr)
    for path,dir_list,file_list in allfile:
        for file_name in file_name:
            
#bounding("/home/weihao/Downloads/grey_image/grey1/","oo")
