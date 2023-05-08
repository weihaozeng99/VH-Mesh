import numpy as np

def ReadPmat(Pmataddr):
    Pmats=[]
    with open(Pmataddr,errors='ignore') as f:
        NumberofPmat=int(f.readline())
        for i in range(0,NumberofPmat):
            rawdata=f.readline()
            rawdata=rawdata.replace("\n","")
            datalist=rawdata.split(" ")
            datalist=datalist[1:]
            #print(datalist)
            Kmat=[]
            for j in range(0,3):
                row=[]
                for k in range(0,3):
                    row.append(float(datalist[3*j+k]))
                Kmat.append(np.array(row))
            #print(Kmat)
            Rmat=[]
            for j in range(0,3):
                row=[]
                for k in range(0,3):
                    row.append(float(datalist[3*j+k+9]))
                Rmat.append(np.array(row))
            #print(Rmat)
            t1=float(datalist[-3])
            t2=float(datalist[-2])
            t3=float(datalist[-1])
            Tmat=[]
            Tmat.append(np.array([t1,t2,t3]))
            #print(Tmat)
            Kmat=np.matrix(Kmat)
            Rmat=np.matrix(Rmat)
            Tmat=np.matrix(Tmat)
            temp=np.c_[Rmat,Tmat.T]
            #print(temp)
            Pmat=np.matmul(Kmat,temp)
            #print(Pmat)
            Pmats.append(np.array(Pmat))
    return Pmats



ReadPmat("/home/weihao/Downloads/temple/temple_par.txt")