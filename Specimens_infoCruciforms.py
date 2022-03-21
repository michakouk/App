import numpy as np

"""
xmin (int):                 lower bound of x-axis
xmax (int):                 Upper bound of x-axis
description (string):       Text displayed in title of graphs
cycles (np.array):          Cycle numbers at which the MTS paused for a RF measurement
threshold (float):          Determines the sensitivity of the std algorithm for filtering the RF data,
                            should be picked such that the number of filtered data points matches cycles
counterindex (int):         Picks the right column from the MTS data file
stiffnessindex (int):       Picks the right column from the MTS data file
sensplacement (np.array)    Encodes how the strips were attached to the specimen, see setup.png in each of the specimen folders
device (str)
strip (int)
"""

def get_settings(specimen, sidename):

    if specimen == 'CA1':
        xmin = 0
        xlim = 214000
        description = 'Fully welded'
        cycles1 = np.linspace(0,100,11)
        cycles2 = np.linspace(105,200,20)
        cycles3 = np.linspace(202.5,212.5,5)
        cycles4 = np.array([213])
        cycles = 1000*np.concatenate((cycles1, cycles2, cycles3, cycles4))
        threshold = 0.2
        counterindex = 3
        stiffnessindex = 16
        MTSlower = 400
        MTSupper = 500
        window = 101
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 61, 29, 70, 29, 61],[1, 2, 2, 1, 1, 3, 2, 3]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2
    
    elif specimen == 'CB1':
        xmin = 0
        xlim = 129000
        description = 'Fillet weld, 14-140kN'
        cycles1 = np.linspace(0,100,11)
        cycles2 = np.linspace(110,125,4)
        cycles3 = np.array([128])
        cycles = 1000*np.concatenate((cycles1, cycles2))
        threshold = 0.25
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 400
        MTSupper = 500
        window = 1001
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 61, 70, 61, 29],[3, 1, 2, 1, 1, 2, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2
        
    elif specimen == 'CA2':
        xmin = 0
        xlim = 2500000
        description = 'Fully welded'
        cycles1 = np.linspace(0,800,41)
        cycles2 = np.linspace(810,1400,60)
        cycles3 = np.linspace(1405,2290,178)
        cycles = 1000*np.concatenate((cycles1, cycles2, cycles3))
        threshold = 0.1
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 400
        MTSupper = 500
        window = 1001
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 61, 70, 61, 29, 29],[1, 2, 2, 3, 3, 1, 1, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2

    elif specimen == 'CA2b':
        xmin = 2050000
        xlim = 2350000
        description = 'Fully welded'
        cycles1 = np.linspace(0,800,41)
        cycles2 = np.linspace(810,1400,60)
        cycles3 = np.linspace(1405,2290,178)
        cycles = np.array([10000, 20000,30000,40000,50000,60000,70000,80000,90000,100000,110000,120000,130000,140000,150000,160000,170000,180000,190000,200000,210000,220000,230000,240000,250000,260000,270000,280000,290000,300000,310000,320000,330000,340000,350000,360000,370000,380000,390000,400000,410000,420000,430000,440000,450000,460000,470000,480000,490000,500000,510000,520000,530000,540000,550000,560000,570000,580000,590000,600000,610000,620000,630000,640000,650000,660000,670000,680000,690000,700000,710000,720000,730000,740000,750000,760000,770000,780000,790000,800000,810000,820000,830000,840000,850000,860000,870000,880000,890000,900000,910000,920000,930000,940000,950000,960000,970000,980000,990000,1000000,1010000,1020000,1030000,1040000,1050000,1060000,1070000,1080000,1090000,1100000,1110000,1120000,1130000,1140000,1150000,1160000,1170000,1180000,1190000,1200000,1210000,1220000,1230000,1240000,1250000,1260000,1270000,1280000,1290000,1300000,1310000,1320000,1330000,1340000,1350000,1360000,1370000,1380000,1390000,1400000,1410000,1420000,1430000,1440000,1450000,1460000,1470000,1480000,1490000,1500000,1510000,1520000,1530000,1540000,1550000,1560000,1570000,1580000,1590000,1600000,1610000,1620000,1630000,1640000,1650000,1660000,1670000,1680000,1690000,1700000,1710000,1720000,1730000,1740000,1750000,1760000,1770000,1780000,1790000,1800000,1810000,1820000,1830000,1840000,1850000,1860000,1870000,1880000,1890000,1900000,1910000,1920000,1930000,1940000,1950000,1960000,1970000,1980000,1990000,2000000,2010000,2020000,2030000,2040000,2050000,2060000,2070000,2080000,2090000,2100000,2110000,2120000,2130000,2140000,2150000,2160000,2170000,2180000,2190000,2200000,2205000,2210000,2215000,2220000,2225000,2230000,2235000,2240000,2245000,2250000,2255000,2260000,2265000,2270000,2275000,2280000,2285000,2290000,2295000,2300000,2305000,2310000,2325000,2330000,2334000])
        threshold = 0.1
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 400
        MTSupper = 500
        window = 1001
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 29, 61],[1, 2, 2, 2, 3, 1, 1, 3]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 205
        
    elif specimen == 'CB2':
        xmin = 0
        xlim = 600000
        description = 'Fillet weld, 8-80kN'
        cycles1 = np.linspace(0,100,6)
        cycles2 = np.linspace(110,590,49)
        cycles3 = np.array([128])
        cycles = 1000*np.array([0,20,40,60,80,100,110,120,130,140,150,160,170,180,190,200,210,220,230,260,270,280,290,300,310,320,330,340,350,360,370,380,390,400,410,420,430,440,450,460,470,480,490,500,510,520,530,540,550,560,570,580,590])
        threshold = 0.1
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 200
        MTSupper = 500
        window = 1001
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 61, 70, 61, 29],[3, 1, 2, 1, 1, 2, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2
       
    elif specimen == 'CC2':
        xmin = 0
        xlim = 230000
        description = 'Partial weld, @26.4-264kN'
        cycles1 = np.linspace(0,150,16)
        cycles2 = np.linspace(150,225,15)
        cycles3 = np.array([228])
        cycles = 1000*np.concatenate((cycles1, cycles2, cycles3))
        threshold = 0.1
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 30
        MTSupper = 90
        window = 1001
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2

    elif specimen == 'CC1':
        xmin = 0
        xlim = 72000
        description = 'Partial weld, @20-200kN'
        cycles = np.array([0, 20000, 40000, 58000, 60000, 63170, 65500, 67000, 69872, 70862])
        threshold = 0.1
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 30
        MTSupper = 90
        window = 1001
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2

    elif specimen == 'CA3-pre':
        xmin = 0
        xlim = 250000
        description = 'Prefatigueing CA3 @27-270kN'
        cycles1 = np.linspace(0,80,5)
        cycles2 = np.linspace(100,240,15)
        cycles = 1000*np.concatenate((cycles1, cycles2))
        threshold = 0.2
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 400
        MTSupper = 490
        window = 1001
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2
        
    elif specimen == 'CA4-pre':
        xmin = 0
        xlim = 250000
        description = 'Prefatigueing CA4 @27-270kN'
        cycles1 = np.linspace(0,100,6)
        cycles2 = np.linspace(110,240,14)
        cycles = 1000*np.concatenate((cycles1, cycles2))
        threshold = 0.1
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 440
        MTSupper = 450
        window = 101
        zeropoint = 1000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2
    
    elif specimen == 'CB3-pre':
        xmin = 0
        xlim = 250000
        description = 'Prefatigueing CB3 @9-90kN'
        cycles1 = np.linspace(0,100,6)
        cycles2 = np.linspace(110,240,14)
        cycles = 1000*np.concatenate((cycles1, cycles2))
        threshold = 0.1
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 440
        MTSupper = 455
        window = 101
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2
        
    elif specimen == 'CB4-pre':
        xmin = 0
        xlim = 250000
        description = 'Prefatigueing CB4 @9-90kN'
        cycles = 1000*np.array([0, 20, 40, 60, 80, 100, 110, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 240])
        threshold = 0.1
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 420
        MTSupper = 460
        window = 101
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2

    elif specimen == 'CC3-pre':
        xmin = 0
        xlim = 250000
        description = 'Prefatigueing CC3 @16-160kN'
        cycles1 = np.linspace(0,100,6)
        cycles2 = np.linspace(110,250,15)
        cycles = 1000*np.concatenate((cycles1, cycles2))
        threshold = 0.1
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 400
        MTSupper = 459
        window = 505
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2

    elif specimen == 'CC4':
        xmin = 0
        xlim = 1600000
        description = 'CC4 @15-150kN'
        cycles1 = np.linspace(0,100,6)
        cycles2 = np.linspace(110,1560,146)
        cycles = 1000*np.concatenate((cycles1, cycles2))
        threshold = 0.2
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 400
        MTSupper = 500
        window = 101
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2

    elif specimen == 'CC5-pre':
        xmin = 0
        xlim = 250000
        description = 'Prefatigueing CC5 @16-160kN'
        cycles1 = np.linspace(0,100,6)
        cycles2 = np.linspace(110,240,14)
        cycles = 1000*np.concatenate((cycles1, cycles2))
        threshold = 0.1
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 30
        MTSupper = 90
        window = 101
        zeropoint = 100
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2
        
    elif specimen == 'CB3':
        xmin = 250000
        xlim = 215000+250000
        description = 'PAUT CB3 @9-90kN'
        if sidename in [1, 2, 5]:
            cycles = 1000*np.array([0, 10, 20, 30, 35.3, 50, 60, 70, 80, 90, 100, 120, 130, 140, 160, 170, 180, 190, 200, 205, 208, 210.6, 211.674, 212.786])
        elif sidename in [3, 6, 7]:
            cycles = 1000*np.array([0, 10, 20, 30, 35.3, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 170, 180, 190, 200, 205, 208, 210, 210.6, 211.674, 212.786])
        elif sidename in [4, 8]:
            cycles = 1000*np.array([0, 10, 20, 30, 35.3, 50, 60, 70, 80, 90, 100, 120, 130, 140, 160, 170, 180, 190, 200, 205, 208, 210, 210.6, 211.674, 212.786])
        cycles = cycles + 250000
        threshold = 0.13
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 150
        MTSupper = 440
        window = 101
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2
        
    elif specimen == 'CB4':
        xmin = 250000
        xlim = 150000+250000
        description = 'PAUT CB4 @10-100kN'
        if sidename in [1, 2, 5]:
            cycles = 1000*np.array([0, 10, 20, 30, 40, 50, 60, 63.910, 70, 80, 90, 100, 105, 110, 120, 130, 140, 147.300, 147.800])
        elif sidename in [3, 6, 7]:
            cycles = 1000*np.array([0, 10, 20, 30, 40, 50, 55, 60, 63.910, 70, 80, 90, 100, 105, 110, 120, 130, 140, 147.300, 147.800])
        elif sidename in [4, 8]:
            cycles = 1000*np.array([0, 10, 20, 30, 40, 50, 60, 63.910, 70, 80, 90, 100, 105, 110, 120, 130, 140, 147.300, 147.800])
        cycles = cycles + 250000
        threshold = 0.13
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 150
        MTSupper = 440
        window = 101
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2
        
    elif specimen == 'CA3':
        xmin = 250000
        xlim = 142000+250000
        description = 'PAUT CA4 @27-270kN'
        cycles = 1000*np.array([0, 10, 11, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 125, 130, 134, 139, 141])
        cycles = cycles + 250000
        threshold = 0.1
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 150
        MTSupper = 440
        window = 101
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 3
        
    elif specimen == 'CA4':
        xmin = 250000
        xlim = 240000+250000
        description = 'PAUT CA4 @30-300kN'
        if sidename in [1, 2, 5, 4, 8]:
            cycles = 1000*np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 132.350, 140, 150, 160, 170, 180, 190, 200, 210, 215.302, 230, 235.100, 237.500])
        else:
            cycles = 1000*np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 132.350, 140, 150, 160, 170, 180, 190, 200, 210, 215.302, 230, 235.100, 237.500])
        cycles = cycles + 250000
        threshold = 0.175
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 150
        MTSupper = 440
        window = 101
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2
        
    elif specimen == 'CB5':
        xmin = 0
        xlim = 167500
        description = 'AE by Lu benchmarking, @12-120kN'
        cycles = 1000*np.array([0, 20, 40, 52.5, 60, 80, 100, 110, 120, 130, 140, 150, 155, 160, 165, 166.782, 167.340, 167.419])
        threshold = 0.175
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 150
        MTSupper = 440
        window = 101
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2

    elif specimen == 'CC4b':
        xmin = 1800000
        xlim = 600000+1800000
        description = 'High cycle fatigue, @15-150kN'
        if sidename in [1, 2, 5]:
            cycles = 1000*np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 490, 510, 530, 540, 560, 565, 590, 600, 600.5, 601, 601.5, 602, 602.5])
        elif sidename in [3, 6, 7]:
            cycles = 1000*np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 490, 510, 530, 540, 560, 590, 600, 600.5, 601, 601.5, 602, 602.5])
        else:
            cycles = 1000*np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 490, 495, 510, 530, 540, 560, 565, 590, 600, 600.5, 601, 601.5, 602, 602.5])
        cycles=cycles+1800000
        threshold = 0.15
        counterindex = 3
        stiffnessindex = 11
        MTSlower = 150
        MTSupper = 440
        window = 101
        zeropoint = 2000
        sensplacement = np.array([[70, 70, 61, 29, 70, 61, 61, 29],[1, 2, 2, 1, 3, 1, 3, 2]])
        device = str(sensplacement[0, sidename-1])
        strip = sensplacement[1, sidename-1]
        wrt = 2
    
    return xmin, xlim, description, cycles, threshold, counterindex, stiffnessindex, device, strip, MTSlower, MTSupper, window, zeropoint, wrt