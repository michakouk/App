# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 14:22:16 2022

Plot the Magnetic field data of the cruciform specimens in subplots.
z-direction: each LMV for multiple strips, each Tot Norm for multiple strips
y-direction: each distance for many LMVs, each distance for all the the Tot Norm

@author: MichaelaKoukoutsi
"""
import plotly.io as pio
pio.renderers.default='browser'
import plotly.graph_objects as go
from CompareCruciform import Strip
from PIL import Image
import numpy as np
import pathlib
import pandas as pd
from Useful_definitions import SpecimenInfo,TOTLMV,Opacity,color_text,NormOfTotField
from plotly import subplots
from scipy.signal import savgol_filter
specimen='CA3'
home=str(pathlib.Path.home())
path = home+r'/Villari/Experimental validation RFV2 - General/Experimental testing/IV. Cruciform-fatigue-test Jan 2022/'
front_sidename=[1,2,5,6]; back_sidename=[3,4,7,8]
sidename_location={1:'5mm from the intact weld toe',2:'5mm from the weld toe of the initiation',5:'25mm from the intact weld toe',6:'25mm from the weld toe of the initiation',
                   3:'5mm from the intact weld toe',4:'5mm from the weld toe of the initiation',7:'25mm from the intact weld toe',8:'25 mm from the weld toe of the initiation'}
colors=[(250,239,14),(255, 1, 1),(15,249,43),(22,153,242)]
coloredtext=['yellow','red','lime','blue']
def Reject_outliers(data,factor):
    u=np.nanmean(data)
    std=np.nanstd(data)
    data=[d for d in data if u-factor*std<=d<=u+factor*std]
    return data
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
   
    #if row==1 and col==1:
    for cy in counter:
        if 0.999*cycles[i]<=cy<=1.01*cycles[i]:
            ind=list(counter).index(cy)
            stiff=round(stiffness[ind],2)
            stiff_pace=round(stiffness_pace[ind],2)
            break
        
    fig.add_trace(go.Scatter(x=counter,y=stiffness,mode='lines',line=dict(width=4,color='orange'),name='stiffness',showlegend=show),row=row_stiff,col=col_stiff,secondary_y=False)
    #fig.add_trace(go.Scatter(x=counter,y=stiffness_pace*100,mode='lines',line=dict(width=4,color='purple'),name='stiffness',showlegend=False),row=row_stiff,col=col_stiff,secondary_y=True)
    fig.update_yaxes(title='Stiffness [%]',showline=True,linewidth=2,linecolor='black',row=row_stiff,col=col_stiff,showgrid=True,gridwidth=1,gridcolor='black',secondary_y=False)
    #fig.update_yaxes(title='Stiffness Reduction Trend [%]',tickvals=[stiff_pace*100],showline=True,linewidth=2,linecolor='black',row=row_stiff,col=col_stiff,showgrid=True,gridwidth=1,gridcolor='black',secondary_y=True)
    fig.update_xaxes(title='Cycles',showline=True,linewidth=2,linecolor='black',row=row_stiff,col=col_stiff,tickvals=[round(cycles[i])],showgrid=True,gridwidth=1,gridcolor='black')
    return fig
def Plot_NormTotField(title,i,fig,specimen,S,ref,row,col,show,side,row_stiff,col_stiff):
    xmin, xlim, description, cycles, threshold, counterindex, stiffnessindex, device, strip, MTSlower, MTSupper, window, zeropoint, wrt=SpecimenInfo(specimen,1)
    MTS_data = np.array(pd.read_table(path+specimen+'/MTS/'+specimen+'_MTS.csv', decimal=".", dtype=float, delimiter=";", skiprows=3, on_bad_lines='skip'))
    counter = MTS_data[:,counterindex]
    stiffness = MTS_data[:,stiffnessindex]
    args1 = np.argwhere(stiffness <= MTSlower)
    args2 = np.argwhere(stiffness >= MTSupper)
    stiffness = np.delete(stiffness, np.concatenate((args1,args2), axis=None))
    y = savgol_filter(stiffness, window, 3)
    counter = np.delete(counter, np.concatenate((args1,args2), axis=None))
    stiffness = y/y[0]*100 # Calculate percentual stiffness decline
    stiffness_pace=abs(y-y[0])/y[0]
    text=[]
    for no,sidename in enumerate(side):
        data= Strip(specimen, sidename).LoadData()
        TotNorm=NormOfTotField(data,S,ref)
        text.append("Strip "+str(sidename)+":"+str(round(TotNorm[i]*100,1))+"\% ,")
        fig.add_trace(go.Scatter(x=cycles[ref:i+1],y=TotNorm[ref:i+1]*100,name=sidename_location[sidename],mode='lines',line=dict(color=Opacity(colors[no],1),width=4),showlegend=show),row=row,col=col)
        fig.add_trace(go.Scatter(x=cycles[i:],y=TotNorm[i:]*100,name=sidename_location[sidename],mode='lines',line=dict(color=Opacity(colors[no],0.4),width=4),showlegend=False),row=row,col=col)
        fig.add_trace(go.Scatter(x=[cycles[i]],y=[TotNorm[i]*100],mode='markers',marker=dict(color=Opacity(colors[no],1),size=15),showlegend=False),row=row,col=col)

    text_annotation=color_text(colors, text)
    fig.add_trace(go.Scatter(x=[cycles[ref],cycles[-1]],y=[5,5],mode='lines',line=dict(color='black',dash='dash'),showlegend=False),row=row,col=col)
    fig.update_xaxes(title='Cycles',showline=True,linewidth=2,linecolor='black',range=[cycles[ref],counter[-1]+2e4],row=row,col=col,tickvals=[cycles[i]])
    fig.update_yaxes(title='Norm Tot change[%] for the sensor <b>'+str(S+1)+"</b>",titlefont=dict(size=25),showline=True,linewidth=2,linecolor='black',row=row,col=col,range=[0,25])
    fig.add_annotation(text=text_annotation,row=row,col=col,x=cycles[ref]+11e4,y=24,font=dict(size=40),bgcolor="black",ax=-10,opacity=0.9,
                ay=0)
    fig.update_layout(title='Norm of the total field for the specimen '+specimen+":"+description+". Cycles="+str(round(cycles[i]))+"| Failure:"+str(round(counter[-1]))+title,
                      width=3200,height=3000,legend=dict(x=0,y=1,orientation="h",bordercolor='black',borderwidth=1),plot_bgcolor='rgba(0,0,0,0)',font=dict(size=30,family='Helvetica'))
    #if row==1 and col==1:
    for cy in counter:
        if 0.9999*cycles[i]<=cy<=1.01*cycles[i]:
            ind=list(counter).index(cy)
            stiff=round(stiffness[ind],2)
            stiff_pace=round(stiffness_pace[ind],2)
            break
        
    fig.add_trace(go.Scatter(x=counter,y=stiffness,mode='lines',line=dict(width=4,color='orange'),name='stiffness',showlegend=show),row=row_stiff,col=col_stiff,secondary_y=False)
    fig.add_trace(go.Scatter(x=counter,y=stiffness_pace*100,mode='lines',line=dict(width=4,color='purple'),name='stiffness',showlegend=False),row=row_stiff,col=col_stiff,secondary_y=True)
    fig.update_yaxes(title='Stiffness [%]',tickvals=[stiff],showline=True,linewidth=2,linecolor='black',row=row_stiff,col=col_stiff,showgrid=True,gridwidth=1,gridcolor='black',secondary_y=False)
    fig.update_yaxes(title='Stiffness Reduction Trend [%]',tickvals=[stiff_pace*100],showline=True,linewidth=2,linecolor='black',row=row_stiff,col=col_stiff,showgrid=True,gridwidth=1,gridcolor='black',secondary_y=True)
    fig.update_xaxes(title='Cycles',showline=True,linewidth=2,linecolor='black',row=row_stiff,col=col_stiff,tickvals=[round(cycles[i])],showgrid=True,gridwidth=1,gridcolor='black')
    return fig
colors_sensors=[(255, 1, 1), (254, 119, 18), (254, 254, 18), (130, 254, 18), (1,117,5), (159,255,218),(2,227,244),(2,88,244), (165,115,255),(133,0,254)]
def Plot_NormTotField_Strip(title,i,fig,specimen,sensors,ref,row,col,show,sidename,row_stiff,col_stiff):
    xmin, xlim, description, cycles, threshold, counterindex, stiffnessindex, device, strip, MTSlower, MTSupper, window, zeropoint, wrt=SpecimenInfo(specimen,1)
    MTS_data = np.array(pd.read_table(path+specimen+'/MTS/'+specimen+'_MTS.csv', decimal=".", dtype=float, delimiter=";", skiprows=3, on_bad_lines='skip'))
    counter = MTS_data[:,counterindex]
# =============================================================================
#     stiffness = MTS_data[:,stiffnessindex]
#     args1 = np.argwhere(stiffness <= MTSlower)
#     args2 = np.argwhere(stiffness >= MTSupper)
#     stiffness = np.delete(stiffness, np.concatenate((args1,args2), axis=None))
#     y = savgol_filter(stiffness, window, 3)
#     counter = np.delete(counter, np.concatenate((args1,args2), axis=None))
#     stiffness = y/y[0]*100 # Calculate percentual stiffness decline
#     stiffness_pace=abs(y-y[0])/y[0]
# =============================================================================
    #text=[]
    for no,S in enumerate(sensors):
        data= Strip(specimen, sidename).LoadData()
        TotNorm=NormOfTotField(data,S,ref)
        #text.append("Strip "+str(sidename)+":"+str(round(TotNorm[i]*100,1))+"\% ,")
        fig.add_trace(go.Scatter(x=cycles[ref:i+1],y=TotNorm[ref:i+1]*100,name='<b>Sensor '+str(S+1)+'</b>',mode='lines',line=dict(color=Opacity(colors_sensors[no],1),width=4),showlegend=show),row=row,col=col)
        fig.add_trace(go.Scatter(x=cycles[i:],y=TotNorm[i:]*100,name='<b>Sensor '+str(S+1)+'</b>',mode='lines',line=dict(color=Opacity(colors_sensors[no],0.4),width=4),showlegend=False),row=row,col=col)
        fig.add_trace(go.Scatter(x=[cycles[i]],y=[TotNorm[i]*100],mode='markers',marker=dict(color=Opacity(colors_sensors[no],1),size=15),showlegend=False),row=row,col=col)

    #text_annotation=color_text(colors, text)
    fig.add_trace(go.Scatter(x=[cycles[ref],cycles[-1]],y=[5,5],mode='lines',line=dict(color='black',dash='dash'),showlegend=False),row=row,col=col)
    fig.update_xaxes(title='Cycles',showline=True,linewidth=2,linecolor='black',range=[cycles[ref],cycles[-1]+2e4],row=row,col=col,tickvals=[cycles[i]])
    fig.update_yaxes(title='Strip '+str(sidename)+" - "+sidename_location[sidename],titlefont=dict(size=25),showline=True,linewidth=2,linecolor='black',row=row,col=col,range=[0,25])
# =============================================================================
#     fig.add_annotation(text=text_annotation,row=row,col=col,x=cycles[ref]+11e4,y=24,font=dict(size=40),bgcolor="black",ax=-10,opacity=0.9,
#                 ay=0)
# =============================================================================
    fig.update_layout(title='Norm of the total field for the specimen '+specimen+":"+description+". Cycles="+str(round(cycles[i]))+"| Failure:"+str(round(counter[-1]))+title,
                      width=3200,height=3500,legend=dict(x=0,y=1,orientation="h",bordercolor='black',borderwidth=1),plot_bgcolor='rgba(0,0,0,0)',font=dict(size=30,family='Helvetica'))
    #if row==1 and col==1:
# =============================================================================
#     for cy in counter:
#         if 0.9999*cycles[i]<=cy<=1.01*cycles[i]:
#             ind=list(counter).index(cy)
#             stiff=round(stiffness[ind],2)
#             stiff_pace=round(stiffness_pace[ind],2)
#             break
#         
#     fig.add_trace(go.Scatter(x=counter,y=stiffness,mode='lines',line=dict(width=4,color='orange'),name='stiffness',showlegend=show),row=row_stiff,col=col_stiff,secondary_y=False)
#     fig.add_trace(go.Scatter(x=counter,y=stiffness_pace*100,mode='lines',line=dict(width=4,color='purple'),name='stiffness',showlegend=False),row=row_stiff,col=col_stiff,secondary_y=True)
#     fig.update_yaxes(title='Stiffness [%]',tickvals=[stiff],showline=True,linewidth=2,linecolor='black',row=row_stiff,col=col_stiff,showgrid=True,gridwidth=1,gridcolor='black',secondary_y=False)
#     fig.update_yaxes(title='Stiffness Reduction Trend [%]',tickvals=[stiff_pace*100],showline=True,linewidth=2,linecolor='black',row=row_stiff,col=col_stiff,showgrid=True,gridwidth=1,gridcolor='black',secondary_y=True)
#     fig.update_xaxes(title='Cycles',showline=True,linewidth=2,linecolor='black',row=row_stiff,col=col_stiff,tickvals=[round(cycles[i])],showgrid=True,gridwidth=1,gridcolor='black')
# =============================================================================
    return fig
def Plot_LMV__Strip(title,i,fig,specimen,lmv_pairs,ref,row,col,show,sidename):
    xmin, xlim, description, cycles, threshold, counterindex, stiffnessindex, device, strip, MTSlower, MTSupper, window, zeropoint, wrt=SpecimenInfo(specimen,sidename)
    MTS_data = np.array(pd.read_table(path+specimen+'/MTS/'+specimen+'_MTS.csv', decimal=".", dtype=float, delimiter=";", skiprows=3, on_bad_lines='skip'))
    counter = MTS_data[:,counterindex]
# =============================================================================
#     stiffness = MTS_data[:,stiffnessindex]
#     args1 = np.argwhere(stiffness <= MTSlower)
#     args2 = np.argwhere(stiffness >= MTSupper)
#     stiffness = np.delete(stiffness, np.concatenate((args1,args2), axis=None))
#     y = savgol_filter(stiffness, window, 3)
#     counter = np.delete(counter, np.concatenate((args1,args2), axis=None))
#     stiffness = y/y[0]*100 # Calculate percentual stiffness decline
#     stiffness_pace=abs(y-y[0])/y[0]
# =============================================================================
    #text=[]
    for no,lmv in enumerate(lmv_pairs):
        data= Strip(specimen, sidename).LoadData()
        TOT_LMV=TOTLMV(data,lmv,ref)
        #text.append("Strip "+str(sidename)+":"+str(round(TotNorm[i]*100,1))+"\% ,")
        S0=lmv[0];S1=lmv[1]
        fig.add_trace(go.Scatter(x=cycles[ref:i+1],y=TOT_LMV[ref:i+1]*100,name='<b>LMV S'+str(S0+1)+'- S'+str(S1+1)+'</b>',mode='lines',line=dict(color=Opacity(colors_sensors[no],1),width=4),showlegend=show),row=row,col=col)
        fig.add_trace(go.Scatter(x=cycles[i:],y=TOT_LMV[i:]*100,name='<b>LMV S'+str(S0+1)+'- S'+str(S1+1)+'</b>',mode='lines',line=dict(color=Opacity(colors_sensors[no],0.4),width=4),showlegend=False),row=row,col=col)
        fig.add_trace(go.Scatter(x=[cycles[i]],y=[TOT_LMV[i]*100],mode='markers',marker=dict(color=Opacity(colors_sensors[no],1),size=15),showlegend=False),row=row,col=col)

    #text_annotation=color_text(colors, text)
    fig.add_trace(go.Scatter(x=[cycles[ref],cycles[-1]],y=[5,5],mode='lines',line=dict(color='black',dash='dash'),showlegend=False),row=row,col=col)
    fig.update_xaxes(title='Cycles',showline=True,linewidth=2,linecolor='black',range=[cycles[ref],cycles[-1]+2e4],row=row,col=col,tickvals=[cycles[i]])
    #'<b>Strip '+str(sidename)+" - "+sidename_location[sidename]+"</b>"
    fig.update_yaxes(title="<b>0"+device+"- strip"+str(strip)+"</b>",titlefont=dict(size=30),showline=True,linewidth=2,linecolor='black',row=row,col=col,range=[0,25])
# =============================================================================
#     fig.add_annotation(text=text_annotation,row=row,col=col,x=cycles[ref]+11e4,y=24,font=dict(size=40),bgcolor="black",ax=-10,opacity=0.9,
#                 ay=0)
# =============================================================================
    fig.update_layout(title='LMV percentual change for the specimen '+specimen+":"+description+". Cycles="+str(round(cycles[i]))+"| Failure:"+str(round(counter[-1]))+title,
                      width=3200,height=3500,legend=dict(x=0,y=1,orientation="h",bordercolor='black',borderwidth=1),plot_bgcolor='rgba(0,0,0,0)',font=dict(size=40,family='Helvetica'))
#%% Plots
t_margin=0.05;l_margin=0.01

lmv_pairs=[[0,4],[1,4],[2,4],[3,4],[4,5],[4,6],[4,7],[4,8],[4,9]]; 
lmv_pairs1=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9]];rows1=[1,1,2,2,2,3,3,3,4];cols1=[1,2,1,2,3,1,2,3,1]
lmv_pairs2=[[0,3],[1,4],[2,5],[3,6],[4,7],[5,8],[6,9]];rows2=[1,2,2,3,3,4,4];cols2=[2,1,2,1,2,1,2]
if specimen=='CA1':
    ref=3
else:
    ref=1
i=ref
#%% front side Norm (1-10)
sensors=[0,1,2,3,4,5,6,7,8,9]; rows_cols_S=[[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3],[4,1],[4,2]]
image_front = Image.open("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\CA1\Front side.png")
img_width_f=419;img_height_f=845;scale_f=0.5
title="<i> - Front-side strips</i>"
i=ref
img_row=1;img_col=4
while i<100: 
    row_stiff=1;col_stiff=1
    fig=subplots.make_subplots(rows=4,cols=4,specs=[[{"t":t_margin,"secondary_y":True},{"t":t_margin,"l":l_margin},{"t":t_margin,"l":l_margin},{"rowspan":2}],[{},{"l":l_margin},{"l":l_margin},{}],[{},{"l":l_margin},{"l":l_margin},{}],[{},{"l":l_margin},{"l":l_margin},{}]])
    fig.add_layout_image(
                    x=0,
                    sizex=img_width_f*scale_f,
                    y=img_height_f*scale_f,#+500
                    sizey=img_height_f*scale_f,
                    xref="x",
                    yref="y",
                    opacity=1,
                    layer="below",
                    sizing="stretch",
                    source=image_front,row=img_row,col=img_col
            )
    fig.update_yaxes(range=[0,img_height_f*scale_f],row=img_row,col=img_col,visible=False);fig.update_xaxes(range=[0,img_width_f*scale_f],row=img_row,col=img_col,visible=False)
    for s in range(len(sensors)):
        if s==0:
            show=True
        else:
            show=False
        Plot_NormTotField(title,i,fig,'CA1',sensors[s],1,rows_cols_S[s][0],rows_cols_S[s][1],show,front_sidename,row_stiff,col_stiff)
    fig.write_image("C:\\Users\\MichaelaKoukoutsi\\Villari\\Experimental validation RFV2 - General\\Experimental testing\\IV. Cruciform-fatigue-test Jan 2022\\CA1\\Analysis\\Front Side\\Norm of the Tot Field\\NormTot Sensors 1-10_distance front"+str(round(i))+".png",format="png")
    i+=1
#%% back side Norm (1-10)
sensors=[0,1,2,3,4,5,6,7,8,9]; rows_cols_S=[[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3],[4,1],[4,2]]
image_back = Image.open("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\CA1\Back Side.png")
img_width_b=320;img_height_b=844;scale_b=0.5
title="<i> - Back-side strips</i>"
i=ref
img_row=1;img_col=4
while i<100: 
    row_stiff=1;col_stiff=1
    fig=subplots.make_subplots(rows=4,cols=4,specs=[[{"t":t_margin,"secondary_y":True},{"t":t_margin,"l":l_margin},{"t":t_margin,"l":l_margin},{"rowspan":2}],[{},{"l":l_margin},{"l":l_margin},{}],[{},{"l":l_margin},{"l":l_margin},{}],[{},{"l":l_margin},{"l":l_margin},{}]])
    fig.add_layout_image(
                    x=0,
                    sizex=img_width_b*scale_b,
                    y=img_height_b*scale_b,#+500
                    sizey=img_height_b*scale_b,
                    xref="x",
                    yref="y",
                    opacity=1,
                    layer="below",
                    sizing="stretch",
                    source=image_back,row=img_row,col=img_col
            )
    fig.update_yaxes(range=[0,img_height_b*scale_b],row=img_row,col=img_col,visible=False);fig.update_xaxes(range=[0,img_width_b*scale_b],row=img_row,col=img_col,visible=False)
    for s in range(len(sensors)):
        if s==0:
            show=True
        else:
            show=False
        Plot_NormTotField(title,i,fig,'CA1',sensors[s],1,rows_cols_S[s][0],rows_cols_S[s][1],show,back_sidename,row_stiff,col_stiff)
    fig.write_image("C:\\Users\\MichaelaKoukoutsi\\Villari\\Experimental validation RFV2 - General\\Experimental testing\\IV. Cruciform-fatigue-test Jan 2022\\CA1\\Analysis\\Back Side\\Norm of the Tot Field\\NormTot Sensors 1-10_distance back"+str(round(i))+".png",format="png")
    i+=1
#%% Tot Norm/ Strip Front & Back
sensors=[0,1,2,3,4,5,6,7,8,9]; rows_cols_side=[[1,1],[1,2],[2,1],[2,2],[3,1],[3,2],[4,1],[4,2]]   
front_back_sidename=front_sidename+back_sidename
image_back = Image.open("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\CA1\Back Side.png")
img_width_b=320;img_height_b=844;scale_b=0.5;row_col_imgB=[3,3]
image_front = Image.open("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\CA1\Front side.png")
img_width_f=419;img_height_f=845;scale_f=0.2;row_col_imgF=[1,3]
i=ref
title='<i>Front & Back Strips</i>'
while i<100:
    fig=subplots.make_subplots(rows=4,cols=3,specs=[[{"t":t_margin},{"t":t_margin},{"rowspan":2}],[{},{"l":l_margin},{}],
                                                    [{},{"l":l_margin},{"rowspan":2}],[{},{"l":l_margin},{}]])
    
    fig.add_layout_image(
                    x=0,
                    sizex=img_width_b*scale_b,
                    y=img_height_b*scale_b,#+500
                    sizey=img_height_b*scale_b,
                    xref="x",
                    yref="y",
                    opacity=1,
                    layer="below",
                    sizing="stretch",
                    source=image_back,row=row_col_imgB[0],col=row_col_imgB[1]
            )
    fig.update_yaxes(range=[0,img_height_b*scale_b],row=row_col_imgB[0],col=row_col_imgB[1],visible=False);fig.update_xaxes(range=[0,img_width_b*scale_b],row=row_col_imgB[0],col=row_col_imgB[1],visible=False)
    fig.add_layout_image(
                    x=0,
                    sizex=img_width_f*scale_f,
                    y=img_height_f*scale_f,#+500
                    sizey=img_height_f*scale_f,
                    xref="x",
                    yref="y",
                    opacity=1,
                    layer="below",
                    sizing="stretch",
                    source=image_front,row=row_col_imgF[0],col=row_col_imgF[1]
            )
    fig.update_yaxes(range=[0,img_height_f*scale_f],row=row_col_imgF[0],col=row_col_imgF[1],visible=False);fig.update_xaxes(range=[0,img_width_f*scale_f],row=row_col_imgF[0],col=row_col_imgF[1],visible=False)
    for no in range(len(front_back_sidename)):
        if no==0:
            show=True
        else:
            show=False
        sidename=front_back_sidename[no]
        Plot_NormTotField_Strip(title, i, fig, specimen, sensors, ref, rows_cols_side[no][0], rows_cols_side[no][1], show, sidename, row_stiff, col_stiff)
    fig.write_image("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\CA1\Analysis\Tot Norm Both Sides\Tot Norm 1-10 both sides "+str(round(i))+".png",format="png")
    i=i+1


#%% front side LMV1 (1-10 step 1)
image_front = Image.open("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\\"+specimen+"\Front side.png")
img_width_f=image_front.size[0];img_height_f=image_front.size[1];scale_f=0.5
image_crack=Image.open("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\CA3\CA3_fracture.jpeg")
img_crack_width=image_crack.size[0];img_crack_height=image_crack.size[1]
title="<i> - Front-side strips</i>"
i=ref
rows_cols1=[[1,2],[2,1],[2,2],[3,1],[3,2],[4,1],[4,2],[5,1],[5,2]]
while i<100: 
    row_stiff=1;col_stiff=1
    fig=subplots.make_subplots(rows=5,cols=3,specs=[[{"t":t_margin,"secondary_y":True},{"t":t_margin,"l":l_margin},{"t":t_margin,"l":l_margin,"rowspan":2}],[{},{"l":l_margin},{"l":l_margin}],[{},{"l":l_margin},{"l":l_margin,"rowspan":2,"t":t_margin}],[{},{"l":l_margin},{"l":l_margin}],[{},{"l":l_margin},{"l":l_margin}]])
    fig.add_layout_image(
                    x=0,
                    sizex=img_width_f,
                    y=img_height_f,
                    sizey=img_height_f,
                    xref="x",
                    yref="y",
                    opacity=1,
                    layer="below",
                    sizing="stretch",
                    source=image_front,row=1,col=3
            )
    fig.add_layout_image(
                    x=0,
                    sizex=img_crack_width,
                    y=img_crack_height,
                    sizey=img_crack_height,
                    xref="x",
                    yref="y",
                    opacity=1,
                    layer="below",
                    sizing="stretch",
                    source=image_crack,row=3,col=3
            )
    fig.update_yaxes(range=[0,img_height_f],row=1,col=3,visible=False);fig.update_xaxes(range=[0,img_width_f],row=1,col=3,visible=False)
    fig.update_yaxes(range=[0,img_crack_height],row=3,col=3,visible=False);fig.update_xaxes(range=[0,img_crack_width],row=3,col=3,visible=False)
    for lmv in range(len(lmv_pairs1)):
        if lmv==0:
            show=True
        else:
            show=False
        ZLMV1(title,i,fig,'CA3',lmv_pairs1[lmv],1,rows_cols1[lmv][0],rows_cols1[lmv][1],show,[1,2,5,8],row_stiff,col_stiff)
    fig.write_image("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\CA3\Analysis\Front Side\LMV_1-10__step1_distance_"+str(round(i))+"front.png",format="png")
    i+=1
    

#%% LMV/ Strip Front & Back
rows_cols_side=[[1,1],[1,2],[2,1],[2,2],[3,1],[3,2],[4,1],[4,2]] 
lmv_pairs=[[0,2],[1,3],[3,5],[2,4],[5,7],[4,6],[6,8],[7,9]]  
front_back_sidename=front_sidename+back_sidename
image_back = Image.open("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\\"+specimen+"\Back Side.png")
img_width_b=image_back.size[0];img_height_b=image_back.size[1];scale_b=0.5;row_col_imgB=[3,3]
image_front = Image.open("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\\"+specimen+"\Front side.png")
img_width_f=image_front.size[0];img_height_f=image_front.size[1];scale_f=0.2;row_col_imgF=[1,3]
i=ref
title='<i>Front & Back Strips</i>'
while i<100:
    fig=subplots.make_subplots(rows=4,cols=3,specs=[[{"t":t_margin},{"t":t_margin},{"rowspan":2}],[{},{"l":l_margin},{}],
                                                    [{},{"l":l_margin},{"rowspan":2}],[{},{"l":l_margin},{}]])
    
    fig.add_layout_image(
                    x=0,
                    sizex=img_width_b*scale_b,
                    y=img_height_b*scale_b,#+500
                    sizey=img_height_b*scale_b,
                    xref="x",
                    yref="y",
                    opacity=1,
                    layer="below",
                    sizing="stretch",
                    source=image_back,row=row_col_imgB[0],col=row_col_imgB[1]
            )
    fig.update_yaxes(range=[0,img_height_b*scale_b],row=row_col_imgB[0],col=row_col_imgB[1],visible=False);fig.update_xaxes(range=[0,img_width_b*scale_b],row=row_col_imgB[0],col=row_col_imgB[1],visible=False)
    fig.add_layout_image(
                    x=0,
                    sizex=img_width_f*scale_f,
                    y=img_height_f*scale_f,#+500
                    sizey=img_height_f*scale_f,
                    xref="x",
                    yref="y",
                    opacity=1,
                    layer="below",
                    sizing="stretch",
                    source=image_front,row=row_col_imgF[0],col=row_col_imgF[1]
            )
    fig.update_yaxes(range=[0,img_height_f*scale_f],row=row_col_imgF[0],col=row_col_imgF[1],visible=False);fig.update_xaxes(range=[0,img_width_f*scale_f],row=row_col_imgF[0],col=row_col_imgF[1],visible=False)
    for no in range(len(front_back_sidename)):
        if no==0:
            show=True
        else:
            show=False
        sidename=front_back_sidename[no]
        Plot_LMV__Strip(title, i, fig, specimen, lmv_pairs, ref, rows_cols_side[no][0], rows_cols_side[no][1], show, sidename)
    fig.write_image("C:\/Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\CA3\Analysis\LMV_step2_both_sides_"+str(round(i))+".png",format="png")
    i=i+1



#%% front side LMV1 (1-10 step 1)
image_front = Image.open("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\CA1\Front side.png")
img_width_f=419;img_height_f=845;scale_f=0.5
title="<i> - Front-side strips</i>"
i=ref
while i<100: 
    row_stiff=1;col_stiff=1
    fig=subplots.make_subplots(rows=4,cols=3,specs=[[{"t":t_margin,"secondary_y":True},{"t":t_margin,"l":l_margin},{"t":t_margin,"l":l_margin,"rowspan":3}],[{},{"l":l_margin},{"l":l_margin}],[{},{"l":l_margin},{"l":l_margin}],[{},{"l":l_margin},{"l":l_margin}]])
    fig.add_layout_image(
                    x=0,
                    sizex=img_width_f*scale_f,
                    y=img_height_f*scale_f,#+500
                    sizey=img_height_f*scale_f,
                    xref="x",
                    yref="y",
                    opacity=1,
                    layer="below",
                    sizing="stretch",
                    source=image_front,row=1,col=3
            )
    fig.update_yaxes(range=[0,img_height_f*scale_f],row=1,col=3,visible=False);fig.update_xaxes(range=[0,img_width_f*scale_f],row=1,col=3,visible=False)
    for lmv in range(len(lmv_pairs2)):
        if lmv==0:
            show=True
        else:
            show=False
        ZLMV1(title,i,fig,'CA1',lmv_pairs2[lmv],1,rows2[lmv],cols2[lmv],show,front_sidename,row_stiff,col_stiff)
    fig.write_image("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\CA1\Analysis\Front Side\LMV #1-#10.step3\LMV_1-10__step3_distance_"+str(round(i))+"front.png",format="png")
    i+=1
    break

#%% back side LMV1 (1-10, step 1)
image_back = Image.open("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\\"+specimen+"\Back Side.png")
img_width_b=image_back.size[0];img_height_b=image_back.size[1];scale_b=0.5
image_crack=Image.open("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\CA3\CA3_fracture.jpeg")
img_crack_width=image_crack.size[0];img_crack_height=image_crack.size[1]
rows_cols1=[[1,2],[2,1],[2,2],[3,1],[3,2],[4,1],[4,2],[5,1],[5,2]]
if specimen=='CA1':
    ref=3
i=ref
title="<i> - Back-side strips</i>"
while i<100: 
    row_stiff=1;col_stiff=1;col_img=3;row_img=1
    fig=subplots.make_subplots(rows=5,cols=3,specs=[[{"t":t_margin,"secondary_y":True},{"t":t_margin,"l":l_margin},{"t":t_margin,"l":l_margin,"rowspan":2}],[{},{"l":l_margin},{"l":l_margin}],[{},{"l":l_margin},{"l":l_margin,"rowspan":2}],[{},{"l":l_margin},{"l":l_margin}],[{},{"l":l_margin},{"l":l_margin}]])
    fig.add_layout_image(
                    x=0,
                    sizex=img_width_b*scale_b,
                    y=img_height_b*scale_b,#+500
                    sizey=img_height_b*scale_b,
                    xref="x",
                    yref="y",
                    opacity=1,
                    layer="below",
                    sizing="stretch",
                    source=image_back,row=1,col=col_img
            )
    fig.add_layout_image(
                    x=0,
                    sizex=img_crack_width,
                    y=img_crack_height,#+500
                    sizey=img_crack_height,
                    xref="x",
                    yref="y",
                    opacity=1,
                    layer="below",
                    sizing="stretch",
                    source=image_crack,row=3,col=3
            )
    fig.update_yaxes(range=[0,img_height_b*scale_b],row=row_img,col=col_img,visible=False);fig.update_xaxes(range=[0,img_width_b*scale_b],row=row_img,col=col_img,visible=False)
    fig.update_yaxes(range=[0,img_crack_height],row=3,col=3,visible=False);fig.update_xaxes(range=[0,img_crack_width],row=3,col=3,visible=False)
    for lmv in range(len(lmv_pairs1)):
        if lmv==0:
            show=True
        else:
            show=False
        ZLMV1(title,i,fig,'CA3',lmv_pairs1[lmv],1,rows_cols1[lmv][0],rows_cols1[lmv][1],show,[3,4,6,7],row_stiff,col_stiff)
    fig.write_image("C:\\Users\MichaelaKoukoutsi\Villari\Experimental validation RFV2 - General\Experimental testing\IV. Cruciform-fatigue-test Jan 2022\CA3\Analysis\Back Side\LMV_1-10_step1_distance_"+str(round(i))+"_back.png",format="png")
    i+=1
