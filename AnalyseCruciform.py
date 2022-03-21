import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import pathlib
home=str(pathlib.Path.home())
for sidename in [1, 2, 3, 4, 5, 6, 7, 8]:
    # Initialize plotting parameters (to be manually changed)
    specimen = 'CC2' #CA1, CB1, CA2, CA2b, CA3-pre, CA4-pre, CB3-pre, CB3, CB4-pre, CB4 CC3-pre, CC4, CB5, CC4b
    sensors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] # Sensors to plot (10 near notch/weldtoe)
    path = home+r'/Villari/Experimental validation RFV2 - General/Experimental testing/IV. Cruciform-fatigue-test Jan 2022/'
    #______________________________________________________________________________
    
    import Specimens_infoCruciforms
    xmin, xmax, description, cycles, threshold, counterindex, stiffnessindex, device, strip, MTSlower, MTSupper, window, zeropoint, wrt = Specimens_infoCruciforms.get_settings(specimen, sidename)
    
      
    MTS_data = np.array(pd.read_table(path+specimen+'/MTS/'+specimen+'_MTS.csv', decimal=".", dtype=float, delimiter=";", skiprows=3, on_bad_lines='skip'))
    counter = MTS_data[:,counterindex]
    stiffness = MTS_data[:,stiffnessindex]
    threestrips = False
    
    #______________________________________________________________________________
    # open, read and filter RedFox data
    """ Relevant variables
    data (3D np.array):      Array containing the raw magnetic field data (x,y,z) per sensor for the defined strip per timestep [timestep, sensor, component]
    total (2D np.array):     Array containing the total magnetic field data per sensor for the defined strip per timestep
    """
    
    with open(path+specimen+'/RedFox/'+specimen+'_RedFox_'+device+'.txt') as f:
        file = f.readlines()[3:]
        number_of_meas = int(len(file))
        newdata = np.empty((number_of_meas,21), dtype=object)
        if len(file[1].split("\t")) > 22:
            threestrips=True
            newdata = np.empty((number_of_meas,31), dtype=object)
        
        strip1_pre = np.empty((number_of_meas,10), dtype=object)
        strip2_pre = np.empty((number_of_meas,10), dtype=object)
        strip3_pre = np.empty((number_of_meas,10), dtype=object)
        
        i = 0
        for line in file:
            newdata[i,:] = line.split("\t ")
            strip1_pre[i,:] = newdata[i,1:11]
            strip2_pre[i,:] = newdata[i,11:21]
            if threestrips==True:
                strip3_pre[i,:] = newdata[i,21:31]
            i = i+1
            
        strip1 = np.empty((number_of_meas,10,3), dtype=float)
        strip2 = np.empty((number_of_meas,10,3), dtype=float)
        if threestrips==True:
            strip3 = np.empty((number_of_meas,10,3), dtype=float)
        
        for i in range(number_of_meas):
            for j in range(10):
                reading1 = strip1_pre[i,j].split(';')
                reading2 = strip2_pre[i,j].split(';')
                if threestrips==True:
                    reading3 = strip3_pre[i,j].split(';') 
                for k in range(3):
                    strip1[i,j,k] = float(reading1[k])
                    strip2[i,j,k] = float(reading2[k])
                    if threestrips==True:
                        strip3[i,j,k] = float(reading3[k])
    
    total1 = np.sqrt(strip1[:,:,0]**2+strip1[:,:,1]**2+strip1[:,:,2]**2)
    total2 = np.sqrt(strip2[:,:,0]**2+strip2[:,:,1]**2+strip2[:,:,2]**2)
    if threestrips==True:
        total3 = np.sqrt(strip3[:,:,0]**2+strip3[:,:,1]**2+strip3[:,:,2]**2)
    
    def check_std(i, n):
        temp = 0
        for j in range(10):
            for k in range(3):
                slicey = strip1[i:i+n,j,k]
                temp = temp + np.std(slicey)/1000
        
        stdev = temp/30
        return stdev
    
    # filter data based on the standard deviation of consecutive measurements
    i = 0
    n = 3
    count = 0
    filtered_data1 = np.array([])
    filtered_data2 = np.array([])
    filtered_data3 = np.array([])
    
    while i < number_of_meas-3:
        if check_std(i,n) < threshold:
            move = 1
            nextval = check_std(i+move,n)
            while nextval < threshold:
                nextval = check_std(i+move,n)
                move += 1
            #print('i = {0}, count = {1} and std = {2}'.format(i, count+1, check_std(i,n)))
            #print(i)
            if count ==0:
                filtered_data1 = np.average(strip1[i+1:i+3,:,:],axis=0)
                filtered_data2 = np.average(strip2[i+1:i+3,:,:],axis=0)
                if threestrips==True:
                    filtered_data3 = np.average(strip3[i+1:i+3,:,:],axis=0)
            elif count ==1:
                filtered_data1 = np.stack((filtered_data1, np.average(strip1[i:i+2,:,:], axis=0)))
                filtered_data2 = np.stack((filtered_data2, np.average(strip2[i:i+2,:,:], axis=0)))
                if threestrips==True:
                    filtered_data3 = np.stack((filtered_data3, np.average(strip3[i+1:i+2,:,:], axis=0)))
            else:
                filtered_data1 = np.concatenate((filtered_data1, (np.average(strip1[i:i+2,:,:], axis=0)).reshape((1,10,3))),axis=0)
                filtered_data2 = np.concatenate((filtered_data2, (np.average(strip2[i:i+2,:,:], axis=0)).reshape((1,10,3))),axis=0)
                if threestrips==True:
                    filtered_data3 = np.concatenate((filtered_data3, (np.average(strip3[i:i+2,:,:], axis=0)).reshape((1,10,3))),axis=0)
                
            count += 1
            i = i+move+1
        else:
            i=i+1
        
    total1 = np.sqrt(filtered_data1[:,:,0]**2+filtered_data1[:,:,1]**2+filtered_data1[:,:,2]**2)
    total2 = np.sqrt(filtered_data2[:,:,0]**2+filtered_data2[:,:,1]**2+filtered_data2[:,:,2]**2)
    if threestrips==True:
        total3 = np.sqrt(filtered_data3[:,:,0]**2+filtered_data3[:,:,1]**2+filtered_data3[:,:,2]**2)
    
    if strip ==1:
        data = filtered_data1
        total = total1
           
    elif strip==2:
        data = filtered_data2
        total = total2
    
    else:
        data = filtered_data3
        total = total3
        
    
    #______________________________________________________________________________
    # Calculate LMV signals and norm
    """
    wrt (int):              Index of the lmv reference measurement in the data array
    lmv1 (2D np.array):     Array containing the 9 LMV1 (between sensor i and i+1) values per timestep
    lmv2 (2D np.array):     Array containing the 8 LMV2 (between sensor i and i+2) values per timestep
    ref (int):              Index of the norm reference measurement in the data array
    norm (np.array):        Array containing the 10 values for the norm of the vectorial change per timestep
    """
    
    lmv1 = np.empty((len(data),9)) # LMV1 is between sensor i and i+1
    for i in range(9):
        lmv1[:,i] = np.sqrt(((data[:,i+1,0]-data[:,i,0])-(data[wrt,i+1,0]-data[wrt,i,0]))**2+((data[:,i+1,1]-data[:,i,1])-(data[wrt,i+1,1]-data[wrt,i,1]))**2+((data[:,i+1,2]-data[:,i,2])-(data[wrt,i+1,2]-data[wrt,i,2]))**2)/((total[wrt,i+1]+total[wrt,i])/2)*100
    
    lmv2 = np.empty((len(data),8)) # LMV2 is between sensor i and i+2
    for i in range(8):
        lmv2[:,i] = np.sqrt(((data[:,i+2,0]-data[:,i,0])-(data[wrt,i+2,0]-data[wrt,i,0]))**2+((data[:,i+2,1]-data[:,i,1])-(data[wrt,i+2,1]-data[wrt,i,1]))**2+((data[:,i+2,2]-data[:,i,2])-(data[wrt,i+2,2]-data[wrt,i,2]))**2)/((total[wrt,i+2]+total[wrt,i])/2)*100
    
    norm = np.sqrt((data[:,:,0]-data[wrt,:,0])**2+(data[:,:,1]-data[wrt,:,1])**2,(data[:,:,2]-data[wrt,:,2])**2)
    
    np.save(path+'/Comparing tests/'+specimen+'-'+device+'-'+str(strip), data) # Save dat in .npy file for CompareSENB.py
    
    args1 = np.argwhere(stiffness <= MTSlower)
    args2 = np.argwhere(stiffness >= MTSupper)
    stiffness = np.delete(stiffness, np.concatenate((args1,args2), axis=None))
    #y = savgol_filter(stiffness, window, 3)
    #counter = np.delete(counter, np.concatenate((args1,args2), axis=None))
    
    #stiffness = y/y[0]*100 # Calculate percentual stiffness decline
    
    #Do plotting
    labels = ['x', 'y', 'z']
    colors = ['chartreuse', 'mediumspringgreen', 'darkturquoise', 'royalblue', 'midnightblue', 'mediumvioletred', 'crimson','red','darkorange', 'gold']
    colors2 = ['r', 'g', 'b']
    
    PHAUT_CB3 = np.array([0])
    cycles_PHAUT_CB3 = np.array([35300])
    
    PHAUT_CB3 = np.array([0])
    cycles_PHAUT_CB4 = np.array([10000, 40000, 65000])
    
    # for sensor in [5]:
    #     fig, ax0 = plt.subplots()
    #     ax1 = ax0.twinx()
    #     #ax1.scatter(counter[0::2],stiffness[0:], marker='o',s=25./fig.dpi, color='silver')
    #     ax1.set_ylabel('stiffness (N/mm)')
    #     ax1.set_ylim(0,1)
    #     for k in range(3):
    #         ax0.plot(cycles, data[:,sensor-1,k]/1000, marker='.', label=labels[k], color=colors2[k])
    #     ax0.plot(cycles, total[:,sensor-1]/1000, marker='.', label='tot', color='k')
    #     ax0.set_xlabel('no. cycles')
    #     ax0.set_ylabel('magnetic field (µT)')
    #     ax0.set_title(specimen+', Field per sensor\n'+description+' Device: '+device+', Strip '+str(strip)+', Sensor '+str(sensor))
    #     ax0.legend(loc=3)
    #     ax0.grid()
    #     plt.show()
        
    #     fig3, ax6 = plt.subplots()
    #     ax7 = ax6.twinx()
    #     #ax7.scatter(counter[0::2],stiffness[0:], marker='o',s=25./fig3.dpi, color='silver')
    #     ax7.set_ylabel('stiffness (N/mm)')
    #     ax7.set_ylim(0,250)
    #     ax6.plot(cycles, norm[:,sensor-1]/1000, marker='.')
    #     ax6.set_xlabel('no. cycles')
    #     ax6.set_ylabel('magnetic field (µT)')
    #     ax6.set_title(specimen+', Norm of vect. change\n'+description+' Device: '+device+', Strip '+str(strip)+', Sensor '+str(sensor))
    #     ax6.legend(loc=3)
    #     ax6.set_ylim(-5,50)
    #     ax6.grid()
    #     plt.show()
    
    #Initial field text box
    textstr = '\n'.join((
    r'Initial field (abs)',
    r'$|B|=%.0f µT$' % (0.001*np.average(total[2,:]), ),
    r'$B_x=%.0f µT$' % (abs(0.001*np.average(data[2,:,0])), ),
    r'$B_y=%.0f µT$' % (abs(0.001*np.average(data[2,:,1])), ),
    r'$B_z=%.0f µT$' % (abs(0.001*np.average(data[2,:,2])), )))
    props = dict(boxstyle='round', facecolor='honeydew', alpha=0.9)
    
# =============================================================================
# #%%    
#     fig4, ax7 = plt.subplots()
#     ax8 = ax7.twinx()
# # =============================================================================
# #     for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
# #         ax7.plot(cycles, norm[:,i]/1000, label='sensor {0}'.format(i+1), color=colors[i], linewidth=1.0)
# # =============================================================================
#     ax8.text(int(20000+xmin), 87, textstr, fontsize=8, verticalalignment='top', bbox=props)
#     ax7.set_xlim(xmin,xmax)
#     ax8.set_xlim(xmin,xmax)
#     ax7.set_ylim(0,50)
#     ax7.set_ylabel('norm. vect. change (muT)')
#     ax7.set_title(specimen+', '+' Norm \n'+description+', Strip '+str(sidename))
#     ax8.scatter(counter+xmin,stiffness, marker='o',s=25./fig4.dpi, color='silver', label='stiffness')
#     ax7.legend(loc=2, fontsize=8)
#     ax8.set_ylabel('stifness (% of original)')
#     ax8.set_ylim(75,105)
#     ax7.grid()
#     plt.show()
# #%%    
#     fig3, ax5 = plt.subplots()
#     ax6 = ax5.twinx()
#     for i in [0, 2, 4, 6, 8]:
#         ax5.plot(cycles, lmv1[:,i], label='sensor {0} and {1}'.format(i+1,i+2), color=colors[i], linewidth=1.0)
#     ax6.text(int(20000+xmin), 88.5, textstr, fontsize=8, verticalalignment='top', bbox=props)
#     ax5.set_xlim(xmin,xmax)
#     ax6.set_xlim(xmin,xmax)
#     ax5.set_ylim(0,50)
#     ax5.hlines(5, 0, 3e6, color='silver', linestyles='dashed')
#     ax5.set_ylabel('LMV (%)')
#     ax5.set_title(specimen+', '+' LMV signals \n'+description+', Strip '+str(sidename))
#     ax6.scatter(counter+xmin,stiffness, marker='o',s=25./fig3.dpi, color='silver', label='stiffness')
#     ax5.legend(loc=2, fontsize=8)
#     ax6.set_ylabel('stifness (% of original)')
#     ax6.set_ylim(75,105)
#     ax5.grid()
#     plt.show()
#     
#     fig5, ax9 = plt.subplots()
#     ax10 = ax9.twinx()
#     for i in range(8):
#         ax9.plot(cycles, lmv2[:,i], label='sensor {0} and {1}'.format(i+1,i+3), color=colors[i], linewidth=1.0)
#     ax10.text(int(20000+xmin), 90.5, textstr, fontsize=8, verticalalignment='top', bbox=props)
#     ax9.set_xlim(xmin+5,xmax)
#     ax10.set_xlim(xmin,xmax)
#     ax9.set_ylim(0,50)
#     ax9.hlines(5, 0, 3e6, color='silver', linestyles='dashed')
#     ax9.set_ylabel('LMV (%)')
#     ax9.set_title(specimen+', '+' LMV2 signals\n'+description+', Strip '+str(sidename))
#     ax10.scatter(counter+xmin,stiffness, marker='o',s=25./fig5.dpi, color='silver', label='stiffness')
#     ax9.legend(loc=2, fontsize=8)
#     ax10.set_ylabel('stifness (% of original)')
#     ax10.set_ylim(75,105)
#     ax9.grid()
#     plt.show()
#     
#     
# 
# =============================================================================
