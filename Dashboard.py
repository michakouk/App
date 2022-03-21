# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 11:28:22 2022

@author: MichaelaKoukoutsi
"""
import plotly.graph_objects as go # or plotly.express as px
fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )
from plotly import subplots
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc
from ZLMV import LMV_Dash,Dash_NormTotField
from PIL import Image
from Useful_definitions import SpecimenInfo
from cruciform_info import cruciforms_information as info
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
#%% Plots
t_margin=0.05;l_margin=0.01
lmv_pairs=[[0,4],[1,4],[2,4],[3,4],[4,5],[4,6],[4,7],[4,8],[4,9]]; 
lmv_pairs1=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9]];rows1=[1,1,2,2,2,3,3,3,4];cols1=[1,2,1,2,3,1,2,3,1]
lmv_pairs2=[[0,3],[1,4],[2,5],[3,6],[4,7],[5,8],[6,9]];rows2=[1,2,2,3,3,4,4];cols2=[2,1,2,1,2,1,2]

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])
fig1=go.Figure()
fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)');fig1.update_yaxes(visible=False);fig1.update_xaxes(visible=False)
#app = dash.Dash()
Norm_tab=html.Div([html.P("Use the slider to see the dots moving.",style={"margin-left":'20px'}),dcc.Slider(id="cycles-Norm",value=5,tooltip={"placement": "bottom", "always_visible": True}),dcc.Graph(figure=fig1,id='Norm Tot',style={'height':'1500px','width':'2000px',"margin-left":'20px'}),])
tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="LMVs", tab_id="tab-LMV",children=[html.Div([html.H5("Plot the LMV between the sensors with step:"),dcc.Input(id="input1",type="number",min=1,max=4, placeholder="Type the step", value=1,style={'marginRight':'10px'}),
        ],style={'margin-left':'20px'}),
    #dcc.Input(id="input2",min=1,max=10, type="number", placeholder="Type the sensor 2", value=2,debounce=True)
    #dcc.Loading([
        dbc.Row([dbc.Col([html.P("Use the slider to see the dots moving.",style={"margin-left":'20px'}),dcc.Slider(id="cycles",value=5,tooltip={"placement": "bottom", "always_visible": True}),dcc.Graph(id='LMV figure',figure=fig1,style={"height":"1800px","width":"1900px","margin-left":'20px'}),
                      html.P(id='text')]),])]),
                dbc.Tab(label="Tot Norm", tab_id="tab-Norm",children=[Norm_tab]),
                dbc.Tab(label="Specimen Pictures", tab_id="tab-pictures",children=[dbc.Row([dbc.Col([dcc.Graph(id='Side Picture',figure=fig1)],style={'margin-left':'20px'}),
                          dbc.Col([dcc.Graph(id='Failure Picture',figure=fig1)])])])
            ],
            id="tabs",
            active_tab="tab-LMV",
        ),
        html.Div(id="content"),
    ]
)

app.layout = html.Div([html.H1("Cruciform Tests Analysis",style={'margin-left':'20px'}),html.Hr(),html.H4(["Cruciform tests samples"],style={'margin-left':'20px'}),dcc.Dropdown(id='specimen',
   options=[
       {'label': 'CA1', 'value': 'CA1'},
       {'label': 'CA2b', 'value': 'CA2b'},
       {'label': 'CA3', 'value': 'CA3'},
       {'label': 'CA4', 'value': 'CA4'},
       {'label': 'CB1', 'value': 'CB1'},
       {'label': 'CB2', 'value': 'CB2'},
       {'label': 'CB3', 'value': 'CB3'},
       {'label': 'CB4', 'value': 'CB4'},
       {'label': 'CB5', 'value': 'CB5'},
       {'label': 'CC2', 'value': 'CC2'},
       {'label': 'CC4b', 'value': 'CC4b'},
       
   ],
   value='CA1',style={'margin-left':'20px','width':'100px'}
),html.H4(children=["Sample Side"],style={'margin-top':'20px','margin-left':'20px',"font-weight":'italic'}),
    dcc.Checklist(id='Sample Side',
   options=[
       {'label': 'Front Side', 'value': 'front side'},
       {'label': 'Back Side', 'value': 'back side'},
   ],
   value=['front side'],labelStyle={'margin-left':'20px'}
),tabs,
        #])
    
])
@app.callback(Output('cycles','min'),Output('cycles','max'),Output('cycles-Norm','min'),Output('cycles-Norm','max'),Input('specimen','value'))
def slider(specimen):
    if specimen=='CA1':
        ref=3
    else:
        ref=1
    xmin, xlim, description, cycles, threshold, counterindex, stiffnessindex, device, strip, MTSlower, MTSupper, window, zeropoint, wrt=SpecimenInfo(specimen,1)
    minimum=ref
    maximum=len(cycles)
    return minimum,maximum,minimum,maximum
import base64
@app.callback(Output('Side Picture','figure'),Output('Failure Picture','figure'),
Output('Side Picture','style'),Output('Failure Picture','style'),Input('Sample Side','value'),Input('specimen','value'),)
def pictures(side,specimen):
    if side==['front side']:
        label='Front-side Picture'
        photo="Front Side"
    else:
        label="Back-side Picture"
        photo="Back Side"
    fig_side=go.Figure();fig_failure=go.Figure()
    try:
        image_front = Image.open(specimen+"\\"+photo+".png")
    except:
        try:
            image_front = Image.open(specimen+"\\"+photo+".jpeg")
        except:
            image_front = Image.open(specimen+"\\"+photo+".jpg")
    img_width_f=image_front.size[0];img_height_f=image_front.size[1];
    try:
        image_crack=Image.open(specimen+"\\"+specimen+"_fracture.jpeg")
    except:
        image_crack=Image.open(specimen+"\\"+specimen+"_fracture.jpg")

    img_crack_width=image_crack.size[0];img_crack_height=image_crack.size[1] 
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir('assets//') if isfile(join('assets//', f))]
    if specimen+'_fracture.jpeg' in onlyfiles:
        img_c=specimen+'_fracture.jpeg'
    elif specimen+'_fracture.jpg' in onlyfiles:
        img_c=specimen+'_fracture.jpg'
    if specimen+' '+photo+".png" in onlyfiles:
        img_f=specimen+' '+photo+".png"
    elif specimen+' '+photo+".jpg" in onlyfiles:
        img_f=specimen+' '+photo+".jpg"
    fig_side.add_layout_image(
                        x=0,
                        sizex=img_width_f,
                        y=img_height_f,
                        sizey=img_height_f,
                        xref="x",
                        yref="y",
                        opacity=1,
                        layer="below",
                        sizing="stretch",
                        source=app.get_asset_url(img_f)
                )
    fig_failure.add_layout_image(
                    x=0,
                    sizex=img_crack_width,
                    y=img_crack_height,
                    sizey=img_crack_height,
                    xref="x",
                    yref="y",
                    opacity=1,
                    layer="below",
                    sizing="stretch",
                    source=app.get_asset_url(img_c))
    fig_side.update_layout(title=label,font=dict(size=20))
    fig_side.update_yaxes(range=[0,img_height_f],visible=False);fig_side.update_xaxes(range=[0,img_width_f],visible=False)
    width=0.3
    style_side={'width':str(width*100)+"vw","height":str(img_height_f*width/img_width_f*100)+"vw"}
    fig_failure.update_yaxes(range=[0,img_crack_height],visible=False);fig_failure.update_xaxes(range=[0,img_crack_width],visible=False)
    fig_failure.update_layout(title="Sample Failure",font=dict(size=20))
    width2=0.25
    style_failure={'width':str(width2*100)+"vw","height":str(img_crack_height/img_crack_width*width2*100)+"vw"}
    return fig_side,fig_failure,style_side,style_failure
@app.callback(
    Output('LMV figure','figure'),Output('Norm Tot','figure'),
    
    Input('specimen','value'),Input('Sample Side','value'),Input("input1",'value'),Input('cycles','value'),Input("tabs","active_tab"),Input('cycles-Norm','value')
)
    
def plot_LMV(specimen,side,step,cycle,active_tab,cycles_Norm):
    if side==['front side']:
            strips=info[specimen]['front sidename']
            title="<i> - Front-side strips</i>"
    else:
        strips=info[specimen]['back sidename']
        title="<i> - Back-side strips</i>"
    if active_tab=='tab-LMV':
        if specimen=='CA1':
            ref=3
        else:
            ref=2
        xmin, xlim, description, cycles, threshold, counterindex, stiffnessindex, device, strip, MTSlower, MTSupper, window, zeropoint, wrt=SpecimenInfo(specimen,1)
        
        i=round(cycle)
        
        #fig=subplots.make_subplots(rows=5,cols=3,specs=[[{"t":t_margin,"secondary_y":True},{"t":t_margin,"l":l_margin},{"t":t_margin,"l":l_margin,"rowspan":2}],[{},{"l":l_margin},{"l":l_margin}],[{},{"l":l_margin},{"l":l_margin,"rowspan":2,"t":t_margin}],[{},{"l":l_margin},{"l":l_margin}],[{},{"l":l_margin},{"l":l_margin}]])
        MTS_data = np.array(pd.read_table(specimen+'/MTS/'+specimen+'_MTS.csv', decimal=".", dtype=float, delimiter=";", skiprows=3, on_bad_lines='skip'))
        counter = MTS_data[:,counterindex]
        stiffness = MTS_data[:,stiffnessindex]
        try:
    # =============================================================================
            args1 = np.argwhere(stiffness <= MTSlower)
            args2 = np.argwhere(stiffness >= MTSupper)
            stiffness = np.delete(stiffness, np.concatenate((args1,args2), axis=None))
            y = stiffness
            #counter = np.delete(counter, np.concatenate((args1,args2), axis=None))
            stiffness = y/y[0]*100
        except:
            stifness=stiffness
        # =============================================================================
             # Calculate percentual stiffness decline
        rows_cols=[[1,1],[1,2],[1,3],[1,4],[2,1],[2,2],[2,3],[2,4],[3,1],[3,2]]
        lmv_pairs=[[i,i+step] for i in range(0,9) if i+step<=9]
        fig=subplots.make_subplots(rows=3,cols=4,specs=[[{"t":t_margin},{"l":l_margin,"t":t_margin},{"l":l_margin,"t":t_margin},{"t":t_margin,"l":l_margin}],[{},{"l":l_margin},{"l":l_margin},{"l":l_margin}],[{},{"l":l_margin},{"l":l_margin},{"l":l_margin}]])
        fig.add_trace(go.Scatter(x=[c for c in counter[:-1]],y=stiffness,mode='lines',line=dict(color='black'),name='stiffness'),row=3,col=2)
        fig.update_xaxes(title="Cycles",tickvals=[cycles[i]],row=3,col=2,showgrid=True,gridcolor='grey',showline=True,linewidth=2,linecolor='black');
        fig.update_yaxes(title='Stiffness [%]',row=3,col=2,showline=True,linewidth=2,linecolor='black')
       
        for ind,lmv in enumerate(lmv_pairs):
            if ind==0:
                show=True
            else:
                show=False
            LMV_Dash(title,i,fig,specimen,lmv,ref,strips,show,rows_cols[ind][0],rows_cols[ind][1])
        return fig,fig1
    else:
        if specimen=='CA1':
            ref=3
        else:
            ref=2
        xmin, xlim, description, cycles, threshold, counterindex, stiffnessindex, device, strip, MTSlower, MTSupper, window, zeropoint, wrt=SpecimenInfo(specimen,1)
        sensors=[1,2,3,4,5,6,7,8,9,10]
        i=round(cycles_Norm)
        rows_cols=[[1,1],[1,2],[1,3],[1,4],[2,1],[2,2],[2,3],[2,4],[3,1],[3,2]]
        fig=subplots.make_subplots(rows=3,cols=4)
        for s in range(len(sensors)):
            if s==0:
                show=True
            else:
                show=False
            Dash_NormTotField(title, i, fig, specimen, s, ref, rows_cols[s][0], rows_cols[s][1], show, strips)
        return fig1,fig
app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter