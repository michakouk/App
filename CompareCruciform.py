import numpy as np
import matplotlib.pyplot as plt
import pathlib
home=str(pathlib.Path.home())

class Strip:
    def __init__(self, specimen, sidename):
        self.specimen = specimen
        self.sidename = sidename
        #self.name = name
        
        import Specimens_infoCruciforms
        xmin, xlim, description, cycles, threshold, counterindex, stiffnessindex, device, strip, MTSlower, MTSupper, window, zeropoint, wrt = Specimens_infoCruciforms.get_settings(specimen, sidename)
        
        self.device = device
        self.strip = strip
        self.cycles = cycles

    def LoadData(self):
        path = home+'//Villari/Experimental validation RFV2 - General/Experimental testing/IV. Cruciform-fatigue-test Jan 2022/Comparing tests/'
        data = np.load(path+self.specimen+'-'+self.device+'-'+str(self.strip)+'.npy')
        return data
    def load_data(self, wrt):
        
        
        path = home+'//Villari/Experimental validation RFV2 - General/Experimental testing/IV. Cruciform-fatigue-test Jan 2022/Comparing tests/'
        data = np.load(path+self.specimen+'-'+self.device+'-'+str(self.strip)+'.npy')


        lmv = np.empty((len(data),9))
        lmv2 = np.empty((len(data),8))
        norm = np.empty((len(data),10))

        total = np.sqrt(data[:,:,0]**2+data[:,:,1]**2+data[:,:,2]**2)
        for i in range(9):
            lmv[:,i] = np.sqrt(((data[:,i+1,0]-data[:,i,0])-(data[wrt,i+1,0]-data[wrt,i,0]))**2+((data[:,i+1,1]-data[:,i,1])-(data[wrt,i+1,1]-data[wrt,i,1]))**2+((data[:,i+1,2]-data[:,i,2])-(data[wrt,i+1,2]-data[wrt,i,2]))**2)/((total[wrt,i+1]+total[wrt,i])/2)*100
        
        for i in range(8):
            lmv2[:,i] = np.sqrt(((data[:,i+2,0]-data[:,i,0])-(data[wrt,i+2,0]-data[wrt,i,0]))**2+((data[:,i+2,1]-data[:,i,1])-(data[wrt,i+2,1]-data[wrt,i,1]))**2+((data[:,i+2,2]-data[:,i,2])-(data[wrt,i+2,2]-data[wrt,i,2]))**2)/((total[wrt,i+2]+total[wrt,i])/2)*100
    
        norm = np.sqrt((data[:,:,0]-data[wrt,:,0])**2+(data[:,:,1]-data[wrt,:,1])**2,(data[:,:,2]-data[wrt,:,2])**2)
        
        return data#lmv, lmv2, norm
    
# =============================================================================
# # Strip A
# specimen = 'CB1'
# sidename = 4
# name = 'CB1, 14-140kN'
# StripA = Strip(specimen, sidename, name)
# lmvA, lmv2A, normA = StripA.load_data(2)
# 
# # Strip B
# specimen = 'CB2'
# sidename = 2
# name = 'CB2, 8-80kN'
# StripB = Strip(specimen, sidename, name)
# lmvB, lmv2B, normB = StripB.load_data(2)
# 
# # Strip C
# specimen = 'CC1'
# sidename = 3
# name = 'CC1, 26.4-264kN'
# StripC = Strip(specimen, sidename, name)
# lmvC, lmv2C, normC = StripC.load_data(2)
# 
# # Strip D
# specimen = 'CC2'
# sidename = 4
# name = 'CC2, 20-200kN'
# StripD = Strip(specimen, sidename, name)
# lmvD, lmv2D, normD = StripD.load_data(2) 
# 
# Strips = [StripA, StripB]
# 
# colors = ['mediumspringgreen', 'darkturquoise', 'royalblue', 'midnightblue', 'mediumvioletred', 'crimson','red','darkorange', 'gold']
# wrt = 2
# senscomp = [7]
# 
# plt.figure()
# axes = plt.gca()
# axes.xaxis.grid()
# plt.plot(StripC.cycles/StripC.cycles[-1], lmvC[:,2], label='{0}\n max LMV'.format(StripC.name), linestyle='--')
# plt.plot(StripD.cycles/StripD.cycles[-1], lmvD[:,2], label='{0}\n max LMV'.format(StripD.name), linestyle='-')
# plt.title('Comparison load levels partial weld')
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.xlim(0.3,1)
# plt.ylim(0,30)
# plt.hlines(5, 0, 1, color='silver', linestyles='dashed')
# plt.xlabel('test length')
# plt.ylabel('LMV (%)')
# plt.show()
# =============================================================================
