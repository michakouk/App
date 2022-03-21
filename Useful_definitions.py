# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 14:56:14 2022

@author: MichaelaKoukoutsi
"""
import Specimens_infoCruciforms
import numpy as np
def SpecimenInfo(specimen,sidename):
    return Specimens_infoCruciforms.get_settings(specimen, sidename)
def color_string(array):
    return 'rgb('+str(array[0])+','+str(array[1])+','+str(array[2])+',1)'
def Opacity(color,opacity):
    return 'rgba('+str(color[0])+','+str(color[1])+','+str(color[2])+','+str(opacity)+')'
def TOTLMV(data,lmv_pair,ref):
    X=[data[:,s,0] for s in lmv_pair]; Y=[data[:,s,1] for s in lmv_pair]; Z=[data[:,s,2] for s in lmv_pair]
    X_LMV=X[1]-X[0]; Y_LMV=Y[1]-Y[0]; Z_LMV=Z[1]-Z[0]
    TOT0=(np.sqrt(X[0][ref]**2+Y[0][ref]**2+Z[0][ref]**2)+np.sqrt(X[1][ref]**2+Y[1][ref]**2+Z[1][ref]**2))/2
    TOTLMV=np.sqrt((X_LMV[:]-X_LMV[ref])**2+(Y_LMV[:]-Y_LMV[ref])**2+(Z_LMV[:]-Z_LMV[ref])**2)/TOT0
    return TOTLMV
def NormOfTotField(data,s,ref):
    X=data[:,s,0]; Y=data[:,s,1]; Z=data[:,s,2]
    Tot0=np.sqrt(X[ref]**2+Y[ref]**2+Z[ref]**2)
    NormTot=np.sqrt((X-X[ref])**2+(Y-Y[ref])**2+(Z-Z[ref])**2)/Tot0
    return NormTot
def color_text(colors, texts):
    #s = '$\color{' + str(color) +'}{ ' + text + '}$'
    s=''
    for i in range(len(colors)):
        s =s+ '\color{' + color_string(colors[i]) +'}{ ' + texts[i] + '}     '
    s='$'+s+'$'
    return s