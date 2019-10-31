# -*- coding: utf-8 -*-
import time
import matplotlib.pyplot as plt
import numpy as np
from random import randint
from scipy import optimize
import pandas as pd

import Function
import de_soma_Insight
import de_bounds_matriz

def AvaliaX(X):
  nrow,ncol=X.shape
  fitness = np.asarray([Fun(ind) for ind in X])
  best_idx = np.argmin(fitness)
  best = X[best_idx]
  fobj_best = fitness[best_idx]
  y=fitness
  BEST=best
  FOBEST=fobj_best
  XY= np.c_[X,y] #concatena x e y em 2 colunas            
  XYsorted = XY[XY[:,-1].argsort()] #Ordena a partir da last col(Y) for all row
  x=XYsorted[:,0:ncol]
  XY=XYsorted
  BEST_XY =np.append(BEST,FOBEST)
  return XY,BEST_XY,BEST,FOBEST

# Functions
def sigmoid(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

def tasig(x,deriv=False):
    if(deriv==True):
        return 1-x*x
    return 2/(1+np.exp(-2*x))-1

# purelin function
def purelin(x,deriv=False):
    if(deriv==True):
        return 1
    return x

# funcao normatiza dados
def Normatiza(x_train,X_max,X_min):
    strings=list(x_train)
    k=-1
    for i in strings:
        k=k+1
        max_x=X_max[k]
        min_x=X_min[k]
        a=(max_x+min_x)/2
        b=(max_x-min_x)/2
        x_train[i]=(x_train[i]-a)/b
    return x_train

def GetMatriz(ANN):
  nrow0=int(ANN.iloc[0,1]);#print(nrow0);
  ncol0=int(ANN.iloc[1,1]);#print(ncol0);
  nrow1=int(ANN.iloc[2,1]);#print(nrow1);
  ncol1=int(ANN.iloc[3,1]);#print(ncol1);
  Col=np.array(range(2,ncol0+2)); # print(Col)
  Row=np.array(range(0,nrow0)); # print(Row)
  syn0=np.array(ANN.iloc[Row,Col])
  syn0=pd.DataFrame(syn0).dropna() 
  syn0=np.array(syn0)
  ncol=int(ANN.iloc[0,1])
  syn1=ANN.iloc[:,(ncol0+ncol1+1)] ;#print(syn1_F)
  nrow=len(np.array(syn1.dropna()))
  A=np.zeros((nrow,1));
  A[:,0]=np.copy(syn1.dropna());
  syn1=np.copy(A);#print(pd.DataFrame(syn1_F))
  X_max=np.array(ANN.iloc[:,ncol-1].dropna());#print(X_max_F)
  X_min=np.array(ANN.iloc[:,ncol-2].dropna());#print(X_min_F)

  return syn0,syn1,X_max,X_min

# funcao retorna os dados a forma original
def Original(x_train,X_max,X_min):
    strings=list(x)
    k=-1
    for i in strings:
        k=k+1
        max_x=X_max[k]
        min_x=X_min[k]
        a=(max_x+min_x)/2
        b=(max_x-min_x)/2
        x_train[i]=x_train[i]*b+a
    return x_train

def ANN_ycal(syn0,syn1,X_train):
  l0 = X_train
  l1 = tasig(np.dot(l0,syn0))
  l2 = purelin(np.dot(l1,syn1))
  y_calc=np.reshape(l2,len(l2))
  return y_calc

def Classifica(ycalc):
  n=len(ycalc)
  for i in range(n):
    if(ycalc[i]<0):
      ycalc[i]=-1
    else:
      ycalc[i]=1
  return ycalc
