import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.preprocessing import StandardScaler


def normal_eqn(df,deg):
    df2=df.copy()
    for i in range(len(deg)):
        dpow=np.power(df2.iloc[:,i],deg[i])
        df2.iloc[:,i]=dpow
    n=len(df2.columns)-1
    D=df2.iloc[:,0:n].to_numpy()
    D=np.insert(D,0,1,axis=1)
    R=df2.iloc[:,n].to_numpy()
    DT=np.transpose(D)
    DTD=np.matmul(DT,D)
    if np.linalg.det(DTD)==0:
        return 0,0
    DTDinv=np.linalg.inv(DTD)
    DTR=np.matmul(DT,R)
    W=np.matmul(DTDinv,DTR)
    gx=W[0]
    for i in range(n):
        gx+=W[i+1]*df2.iloc[:,i]
        i+=1
    gx=gx.tolist()
    W=W.tolist()
    return W,gx



def best_hypothesis(df):
    df2=df.copy()
    n=len(df2.columns)-1
    deg=[]
    for i in range(n):
        deg.append(1)
    final_deg=[]
    for i in range(n):
        deg2=deg.copy()
        W,gx=normal_eqn(df2,deg2)
        if gx==0:
            continue
        rmse=metrics.mean_squared_error(df2.iloc[:,n],gx)
        d=1
        deg2[i]=0.9
        W,gx=normal_eqn(df2,deg2)
        if gx==0:
            continue
        rtemp=metrics.mean_squared_error(df2.iloc[:,n],gx)
        if rtemp<rmse:
            rmse=rtemp
            d=deg2[i]
            while(deg2[i]>0):
                deg2[i]=round((deg2[i]-0.1),2)
                W,gx=normal_eqn(df2,deg2)
                if gx==0:
                    continue
                rtemp=metrics.mean_squared_error(df2.iloc[:,n],gx)
                if rtemp<rmse:
                    rmse=rtemp
                    d=deg2[i]
                else:
                    break
        else:
            deg2[i]=1
            W,gx=normal_eqn(df2,deg2)
            rmse=metrics.mean_squared_error(df2.iloc[:,n],gx)
            while(deg2[i]<20):
                deg2[i]+=1
                W,gx=normal_eqn(df2,deg2)
                if gx==0:
                    continue
                rtemp=metrics.mean_squared_error(df2.iloc[:,n],gx)
                if rtemp<rmse:
                    rmse=rtemp
                    d=deg2[i]
                else:
                    dtemp=deg2[i]+1
                    deg2[i]=d
                    while(deg2[i]<dtemp):
                        deg2[i]=round(deg2[i]+0.1,2)
                        W,gx=normal_eqn(df2,deg2)
                        if gx==0:
                            continue
                        rtemp=metrics.mean_squared_error(df2.iloc[:,n],gx)
                        if rtemp<rmse:
                            rmse=rtemp
                            d=deg2[i]
                            continue
                        else:
                            break
                    break
        final_deg.append(d)
    return final_deg
                    



#the gradient descent function
def grad_eqn(df,deg):
    for i in range(len(deg)):
        dpow=np.power(df.iloc[:,i],deg[i])
        df.iloc[:,i]=dpow
    nc=len(df.columns)-1
    l=len(df.iloc[:,1])
    D=df.iloc[:,0:nc].to_numpy()
    sc=StandardScaler()
    D=sc.fit_transform(D)
    D=np.insert(D,0,1,axis=1)
    y= df.iloc[:,nc].to_numpy()
    w=np.zeros(nc+1)
    alpha=0.01
    epochs=45
    for e in range(epochs):
        j=0
        i=0
        hy=np.zeros(l)
        for i in range(l):
            while(j<=nc):
                hy[i]+=w[j]*D[i,j]
                j+=1   
            j=0

        w_temp=np.zeros(nc+1)
        k=0
        for k in range(nc+1):
            m=0
            for m in range(l):
                w_temp[k]=w_temp[k]+(hy[m]-y[m])*D[m,k]
            w[k]=w[k]-alpha*(1/l)*(w_temp[k])
        
    gx=w[0]
    for z in range(nc):
        gx+=w[z+1]*df.iloc[:,z]
        z=z+1
    
    return w,gx