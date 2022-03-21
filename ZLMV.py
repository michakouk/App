# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:13:21 2022

@author: MichaelaKoukoutsi
"""
import plotly.io as pio
pio.renderers.default='browser'
import plotly.graph_objects as go
from CompareCruciform import Strip
import numpy as np
import pathlib
import pandas as pd
from Useful_definitions import SpecimenInfo,TOTLMV,Opacity,color_text,NormOfTotField

home=str(pathlib.Path.home())
path = home+r'/Villari/Experimental validation RFV2 - General/Experimental testing/IV. Cruciform-fatigue-test Jan 2022/'
colors=[(250,239,14),(255, 1, 1),(15,249,43),(22,153,242)]
def LMV_Dash(title,i,fig,specimen,lmv_pair,ref,side,show,row,col):
    xmin, xlim, description, cycles, threshold, counterindex, stiffnessindex, device, strip, MTSlower, MTSupper, window, zeropoint, wrt=SpecimenInfo(specimen,1)
    MTS_data = np.array(pd.read_table(path+specimen+'/MTS/'+specimen+'_MTS.csv', decimal=".", dtype=float, delimiter=";", skiprows=3, on_bad_lines='skip'))
    counter = MTS_data[:,counterindex]
    stiffness = MTS_data[:,stiffnessindex]
    #stiffness=savgol_filter(stiffness,window,1)
    #stiffness=Reject_outliers(stiffness,1)
# =============================================================================
#     args1 = np.argwhere(stiffness <= MTSlower)
#     args2 = np.argwhere(stiffness >= MTSupper)
#     stiffness = np.delete(stiffness, np.concatenate((args1,args2), axis=None))
#     print(stiffness)
# =============================================================================
    y = stiffness
    #counter = np.delete(counter, np.concatenate((args1,args2), axis=None))
    stiffness = y/y[0]*100 # Calculate percentual stiffness decline
    stiffness_pace=abs(y-y[0])/y[0]
    text=[]
    for no,sidename in enumerate(side):
        xmin, xlim, description, cycles, threshold, counterindex, stiffnessindex, device, strip, MTSlower, MTSupper, window, zeropoint, wrt=SpecimenInfo(specimen,sidename)
        data= Strip(specimen, sidename).LoadData()
  
        TOT_LMV=TOTLMV(data,lmv_pair,ref)

        text.append("Strip 0"+device+'-'+str(strip)+":"+str(round(TOT_LMV[i]*100,1))+"\% ,")
        fig.add_trace(go.Scatter(x=cycles[ref:i+1],y=TOT_LMV[ref:i+1]*100,name=str(sidename),mode='lines',line=dict(color=Opacity(colors[no],1),width=4),showlegend=show),row=row,col=col)
        fig.add_trace(go.Scatter(x=cycles[i:],y=TOT_LMV[i:]*100,name=str(sidename),mode='lines',line=dict(color=Opacity(colors[no],0.4),width=4),showlegend=False),row=row,col=col)
        fig.add_trace(go.Scatter(x=[cycles[i]],y=[TOT_LMV[i]*100],mode='markers',marker=dict(color=Opacity(colors[no],1),size=15),showlegend=False),row=row,col=col)

    fig.add_trace(go.Scatter(x=[cycles[ref],cycles[-1]],y=[5,5],mode='lines',line=dict(color='black',dash='dash'),showlegend=False),row=row,col=col)
    fig.update_xaxes(title='Cycles',showline=True,linewidth=2,linecolor='black',tickvals=[cycles[i]],range=[cycles[ref],cycles[-1]],row=row,col=col)
    fig.update_yaxes(title='LMV change[%] between the sensors <b>'+str(lmv_pair[0]+1)+'-'+str(lmv_pair[1]+1)+"</b>",titlefont=dict(size=25),showline=True,linewidth=2,linecolor='black',range=[0,25],row=row,col=col)
    
    fig.update_layout(title='LMV change for the specimen '+specimen+":"+description+".<br> Cycles="+str(round(cycles[i]))+"| Failure:"+str(round(cycles[-1]))+title,
                      legend=dict(x=0,y=1,orientation="h",bordercolor='black',borderwidth=1,title='Strip:'),plot_bgcolor='rgba(0,0,0,0)',font=dict(size=20,family='Helvetica'))

    return fig
def Dash_NormTotField(title,i,fig,specimen,S,ref,row,col,show,side):
    xmin, xlim, description, cycles, threshold, counterindex, stiffnessindex, device, strip, MTSlower, MTSupper, window, zeropoint, wrt=SpecimenInfo(specimen,1)
    MTS_data = np.array(pd.read_table(path+specimen+'/MTS/'+specimen+'_MTS.csv', decimal=".", dtype=float, delimiter=";", skiprows=3, on_bad_lines='skip'))
    counter = MTS_data[:,counterindex]
    text=[]
    for no,sidename in enumerate(side):
        data= Strip(specimen, sidename).LoadData()
        TotNorm=NormOfTotField(data,S,ref)
        text.append("Strip "+str(sidename)+":"+str(round(TotNorm[i]*100,1))+"\% ,")
        fig.add_trace(go.Scatter(x=cycles[ref:i+1],y=TotNorm[ref:i+1]*100,name=str(sidename),mode='lines',line=dict(color=Opacity(colors[no],1),width=4),showlegend=show),row=row,col=col)
        fig.add_trace(go.Scatter(x=cycles[i:],y=TotNorm[i:]*100,name=str(sidename),mode='lines',line=dict(color=Opacity(colors[no],0.4),width=4),showlegend=False),row=row,col=col)
        fig.add_trace(go.Scatter(x=[cycles[i]],y=[TotNorm[i]*100],mode='markers',marker=dict(color=Opacity(colors[no],1),size=15),showlegend=False),row=row,col=col)

    text_annotation=color_text(colors, text)
    fig.add_trace(go.Scatter(x=[cycles[ref],cycles[-1]],y=[5,5],mode='lines',line=dict(color='black',dash='dash'),showlegend=False),row=row,col=col)
    fig.update_xaxes(title='Cycles',showline=True,linewidth=2,linecolor='black',range=[cycles[ref],cycles[-1]],row=row,col=col,tickvals=[cycles[i]])
    fig.update_yaxes(title='Norm Tot change[%] for the sensor <b>'+str(S+1)+"</b>",titlefont=dict(size=25),showline=True,linewidth=2,linecolor='black',row=row,col=col,range=[0,25])
    fig.update_layout(title='Norm of the total field for the specimen '+specimen+":"+description+". Cycles="+str(round(cycles[i]))+"| Failure:"+str(round(counter[-1]))+title,
                      legend=dict(x=0,y=1,orientation="h",bordercolor='black',borderwidth=1),plot_bgcolor='rgba(0,0,0,0)',font=dict(size=20,family='Helvetica'))
    return fig
def ZLMV1(title,i,fig,specimen,lmv_pair,ref,row,col,show,side,row_stiff,col_stiff):
    xmin, xlim, description, cycles, threshold, counterindex, stiffnessindex, device, strip, MTSlower, MTSupper, window, zeropoint, wrt=SpecimenInfo(specimen,1)
    MTS_data = np.array(pd.read_table(path+specimen+'/MTS/'+specimen+'_MTS.csv', decimal=".", dtype=float, delimiter=";", skiprows=3, on_bad_lines='skip'))
    counter = MTS_data[:,counterindex]
    stiffness = MTS_data[:,stiffnessindex]
    #stiffness=savgol_filter(stiffness,window,1)
    #stiffness=Reject_outliers(stiffness,1)
# =============================================================================
#     args1 = np.argwhere(stiffness <= MTSlower)
#     args2 = np.argwhere(stiffness >= MTSupper)
#     stiffness = np.delete(stiffness, np.concatenate((args1,args2), axis=None))
#     print(stiffness)
# =============================================================================
    y = stiffness
    #counter = np.delete(counter, np.concatenate((args1,args2), axis=None))
    stiffness = y/y[0]*100 # Calculate percentual stiffness decline
    stiffness_pace=abs(y-y[0])/y[0]
    text=[]
    for no,sidename in enumerate(side):
        xmin, xlim, description, cycles, threshold, counterindex, stiffnessindex, device, strip, MTSlower, MTSupper, window, zeropoint, wrt=SpecimenInfo(specimen,sidename)
        data= Strip(specimen, sidename).LoadData()
  
        TOT_LMV=TOTLMV(data,lmv_pair,ref)

        text.append("Strip 0"+device+'-'+str(strip)+":"+str(round(TOT_LMV[i]*100,1))+"\% ,")
        fig.add_trace(go.Scatter(x=cycles[ref:i+1],y=TOT_LMV[ref:i+1]*100,name="0"+device+'-'+str(strip),mode='lines',line=dict(color=Opacity(colors[no],1),width=4),showlegend=show),row=row,col=col)
        fig.add_trace(go.Scatter(x=cycles[i:],y=TOT_LMV[i:]*100,name="0"+device+'-'+str(strip),mode='lines',line=dict(color=Opacity(colors[no],0.4),width=4),showlegend=False),row=row,col=col)
        fig.add_trace(go.Scatter(x=[cycles[i]],y=[TOT_LMV[i]*100],mode='markers',marker=dict(color=Opacity(colors[no],1),size=15),showlegend=False),row=row,col=col)

    text_annotation=color_text(colors, text)
    fig.add_trace(go.Scatter(x=[cycles[ref],cycles[-1]],y=[5,5],mode='lines',line=dict(color='black',dash='dash'),showlegend=False),row=row,col=col)
    fig.update_xaxes(title='Cycles',showline=True,linewidth=2,linecolor='black',row=row,col=col,tickvals=[cycles[i]],range=[cycles[ref],cycles[-1]])
    fig.update_yaxes(title='LMV change[%] between the sensors <b>'+str(lmv_pair[0]+1)+'-'+str(lmv_pair[1]+1)+"</b>",titlefont=dict(size=25),showline=True,linewidth=2,linecolor='black',row=row,col=col,range=[0,25])
    fig.add_annotation(text=text_annotation,row=row,col=col,x=cycles[ref]+10e4,y=24,font=dict(size=30),bgcolor="black",ax=-10,opacity=0.9,
                ay=0)
    fig.update_layout(title='LMV change for the specimen '+specimen+":"+description+". Cycles="+str(round(cycles[i]))+"| Failure:"+str(round(cycles[-1]))+title,
                      width=3000,height=3000,legend=dict(x=0,y=1,orientation="h",bordercolor='black',borderwidth=1,title='RFV-Strip:'),plot_bgcolor='rgba(0,0,0,0)',font=dict(size=30,family='Helvetica'))

    fig.add_trace(go.Scatter(x=counter,y=stiffness,mode='lines',line=dict(width=4,color='orange'),name='stiffness',showlegend=show),row=row_stiff,col=col_stiff,secondary_y=False)
    #fig.add_trace(go.Scatter(x=counter,y=stiffness_pace*100,mode='lines',line=dict(width=4,color='purple'),name='stiffness',showlegend=False),row=row_stiff,col=col_stiff,secondary_y=True)
    fig.update_yaxes(title='Stiffness [%]',showline=True,linewidth=2,linecolor='black',row=row_stiff,col=col_stiff,showgrid=True,gridwidth=1,gridcolor='black',secondary_y=False)
    #fig.update_yaxes(title='Stiffness Reduction Trend [%]',tickvals=[stiff_pace*100],showline=True,linewidth=2,linecolor='black',row=row_stiff,col=col_stiff,showgrid=True,gridwidth=1,gridcolor='black',secondary_y=True)
    fig.update_xaxes(title='Cycles',showline=True,linewidth=2,linecolor='black',row=row_stiff,col=col_stiff,tickvals=[round(cycles[i])],showgrid=True,gridwidth=1,gridcolor='black')
    return fig