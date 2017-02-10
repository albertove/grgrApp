#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      BMGFOU
#
# Created:     10-11-2014
# Copyright:   (c) BMGFOU 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from xlrd import open_workbook
from xlutils.copy import copy
from xlwt import easyxf

#vinfile = open_workbook('vinnova.xls')

def thicknessSubbaseLayer(terras,traffic,subbase):
    calfile = open_workbook('grgrSite/grgrSIte/grgrApp/calculationgrgr.xlsx')
    sheet = calfile.sheet_by_index(0)
    if traffic == 1:
        cell = sheet.cell(18+terras,9)
    elif (traffic == 2) or (traffic == 3):
        cell = sheet.cell(18+terras,11)
    elif traffic == 4:
        cell = sheet.cell(18+terras,13)
    elif traffic == 5:
        cell = sheet.cell(18+terras,15)
    try:
        sublayer = cell.value.replace('*','')
    except:
        sublayer = cell.value
    if subbase == 2:
        porc = sheet.cell(18+terras,17)
        sublayer = float(sublayer)*(1.0 + float(porc.value)/100.0)
    return sublayer

def thicknessBaseLayer(val):
    calfile = open_workbook('grgrSite/grgrSIte/grgrApp/calculationgrgr.xlsx')
    sheet = calfile.sheet_by_index(0)
    cell = sheet.cell(10+val,3)
    return cell.value

def totalThickness(thicksubbase,thickbase,climatic,frost,thickcoarse,thickbedding):
    calfile = open_workbook('grgrSite/grgrSIte/grgrApp/calculationgrgr.xlsx')
    sheet = calfile.sheet_by_index(0)
    cell = sheet.cell(13+frost,17+climatic)

    if cell.value == '':
        thickcontrol = 0
    else:
        thickcontrol = float(cell.value)

    thicktotal = thicksubbase + thickbase + thickcoarse + thickbedding

    if thicktotal < thickcontrol:
        thicksubbase = thicksubbase + (thickcontrol - thicktotal)
    if thicksubbase < 200:
        fraction_subbase = '0/90'
    else:
        fraction_subbase = '0/32'
    return thicktotal,thicksubbase,fraction_subbase

def PyDData(variables):
    """
    variables[0] = pavement_area #D11
    variables[1] = type_paving #D12
    variables[2] = num_draining_pipe #D13
    variables[3] = thick_surf_course #D14
    variables[4] = thick_bedding_layer #D15
    variables[5] = thick_base_layer #D16
    variables[6] = thick_subbase_layer #D17
    variables[7] = ground_water #D18
    variables[8] = depth_draining #D19
    variables[9] = coeff_infiltration #D32
    variables[10] = height_open_volume #R13
    variables[11] = thickness_vegetation_layer #R14
    variables[12] = thickness_coarse_sand #R15
    variables[13] = thickness_coarse_aggregate_26 #R16
    variables[14] = thickness_coarse_aggregate_416 #R17
    variables[15] = position_draining_pipe_ditch #R20
    variables[16] = distance_overflow #R22
    variables[17] = R11
    variables[18] = R12
    variables[19] = R23
    variables[20] = R39
    variables[21] = R21
    """
    # D38 & D40
    if variables[1] == 1:
        D38 = 0.025
        D40 = 0.025
    elif variables[1] == 2:
        D38 = 0.15
        D40 = 0.18
    elif variables[1] == 3:
        D38 = 0.2
        D40 = 0.1
    else:
        D38 = 0.0
        D40 = 0.0
    D35 = 0.67
    D43 = variables[2]*5
    D44 = float(variables[0])/10000
    D45 = 1 - D38 - 0.175
    D46 = (variables[3]+variables[4]+variables[5]+variables[6])/1000
    D50 = 200.0/3600/1000 #D30
    D51 = 370.0/3600/1000 #D31
    D52 = 3600.0/3600/1000 #D32
    D53 = 3600.0/3600/1000 #D33
    D54 = 8.0/3600/1000 #D34
    D55 = D40*(D50*variables[0])*1000
    D56 = (D51*variables[0])*1000
    D57 = D52*variables[0]*1000
    D58 = D53*variables[0]*1000
    D59 = D54*variables[0]*1000
    D60 = variables[6]-variables[8]
    tableB = [3,5,10,15,20,25,30,35,40,45,50,55,60,70,80,90,100,110,120,140,160,180,210,240,270,300,360,540,720,1440]
    tableC = [353,314,228,181,151,131,116,104,95,88,81,76,71,64,58,53,49,46,42,39,35,32,29,26,24,22,19,14,12,7]
    tableD = [D38]*30
    tableE = [D44]*30
    # Q
    tableF = []
    tableG = []
    tableH = []
    tableI = []
    tableJ = []
    tableK = []
    tableL = []
    tableM = []
    tableN = []
    for k in range(30):
        if tableC[k]*tableD[k]*tableE[k]*1.1 < D55:
            tableF.append(tableC[k]*tableD[k]*tableE[k]*1.1)
        else:
            tableF.append(D55)

        if D59 < tableF[k]:
            tableG.append(D59)
        else:
            tableG.append(tableF[k])

        tableH.append(60.0*tableB[k]*(tableF[k]-tableG[k])/1000)

        if tableC[k]*tableD[k]*tableE[k]*1.1 < D55:
            tableI.append(0.0)
        else:
            tableI.append(tableC[k]*tableD[k]*tableE[k]*1.1-D55)

        if D43 < tableF[k]:
            tableJ.append(D43)
        else:
            tableJ.append(tableF[k])

        if D59+D43*D35 < tableF[k]:
            tableK.append(D59+D43*D35)
        else:
            tableK.append(tableF[k])

    D99 = max(tableH)
    D100 = 0.001*variables[0]*(variables[8]*0.32+variables[7]*0.05)
    for k in range(30):
        if D99<D100:
            tableL.append(0.0)
            tableM.append(0.0)
        else:
            tableL.append(60*tableB[k]*(tableF[k]-tableK[k])/1000)
            tableM.append(tableJ[k])
        tableN.append(tableH[k]+tableL[k])
    if D99 < D100:
        D101 = "nej"
    else:
        D101 = "kanske"
    D103 = max(tableL)
    D104 = variables[0]*0.001*D60*0.32
    D106 = 0
    D107 = D99 + D103
    D108 = D100 + D104
    for k in range(30):
        if tableN[k] == D107:
            D106 = D106 + tableB[k]

    if D107 < D108:
        D109 = "nej"
    else:
        D109 = "ja"

    # R-part
    if variables[20] == 2:
        R38 = 8
    else:
        R38 = 0

    R43 = variables[18]*5
    R44 = float(sum(variables[10:14]))/1000
    R45 = 200.0/3600/1000
    R46 = 3600.0/3600/1000
    R47 = 36000.0/3600/1000
    R48 = 36000.0/3600/1000
    R49 = 36000.0/3600/1000
    R50 = 100.0/3600/1000
    R51 = 8.0/3600/1000
    R98 = variables[0]*0.01*variables[17]*D45
    R52 = R45*R98*1000
    R53 = R46*R98*1000
    R54 = R47*R98*1000
    R55 = R48*R98*1000
    R56 = R49*R98*1000
    R57 = R50*R98*1000
    if variables[20] == 2:
        R58 = R51*R98*1000.0
    else:
        R58 = 0.0
    R59 = R43 + R58
    tableP = [3,5,10,15,20,25,30,35,40,45,50,55,60,70,80,90,100,110,120,140,160,180,210,240,270,300,360,540,720,1440]
    tableQ = [353,314,228,181,151,131,116,104,95,88,81,76,71,64,58,53,49,46,43,39,35,32,29,26,24,22,19,14,12,7]
    tableR = [D45]*30
    tableS = [D44]*30
    tableT = []
    tableU = []
    tableV = []
    tableW = []
    tableX = []
    tableY = []
    tableAA = []
    tableAB = []
    tableAC = []
    tableAD = []
    R101 = R98*variables[16]*1.0/1000
    for k in range(30):
        tableT.append((tableQ[k]*R98/10000) + (tableQ[k]*tableR[k]*tableS[k]*1.1) + tableI[k])
        if R52 < tableT[k]:
            tableU.append(R52)
        else:
            tableU.append(tableT[k])
        if R54 < tableT[k]:
            tableV.append(R54)
        else:
            tableV.append(tableT[k])
        if tableV[k] > R43*0.67 + R58:
            tableW.append(R43*0.67 + R58)
        else:
            tableW.append(tableV[k])
        if variables[11] + variables[12] == 0:
            tableX.append(60*tableP[k]*(tableT[k]-tableW[k])/1000)
        else:
            tableX.append(60*tableP[k]*(tableT[k]-tableU[k])/1000)
        if tableX[k] < R101:
            tableY.append(tableX[k])
        else:
            tableY.append(R101)
        if tableY[k]<R101:
            tableAA.append(0)
        else:
            tableAA.append(60*tableP[k]*(tableT[k]-tableW[k])/1000)
    R103 = R98*0.001*variables[21]*0.31
    R104 = R98*(variables[11]*0.25 + variables[12]*0.25 + variables[13]*0.31 + variables[14]*0.32)/1000
    R105 = 0
    R109 = R98*(1.0*(variables[10]-variables[16]))/1000
    R110 = R101 + R103 + R104 + R109

    for k in range(30):
        tableAB.append(tableY[k]+tableAA[k])
        tableAC.append(R101)
        if tableAB[k] < tableAC[k]:
            tableAD.append(0)
        else:
            tableAD.append(tableAB[k] - tableAC[k])

    print R59
    print tableAB
    R99 = max(tableAB)
    for k in range(30):
        if tableAB[k] == R99:
            R105 = R105 + tableP[k]
    if R110 > R99:
        R102 = "ja"
    else:
        R102 = "nej"
    design_intensity_rain = 0
    design_intensity_rain_ditch = 0
    for k in range(30):
        if tableB[k] == D106:
            design_intensity_rain = tableC[k]

        if  int(tableP[k]) == int(R105):
            design_intensity_rain_ditch = tableQ[k]

    DRespons = [D106,D108,D107,D101,D109,R105,R110,R99,R102,design_intensity_rain,design_intensity_rain_ditch]
    return DRespons

def DData(variables):
    vinnovafile = open_workbook('grgrSite/grgrSIte/grgrApp/vinnova.xls')
    r_sheet = vinnovafile.sheet_by_index(0)
    #celltype = sheet.cell(11,3)
    #wb = copy(vinnovafile)
    #w_sheet = vinnovafile.sheet_by_index(0)

    for k in range(len(variables)):
        if k == 9:
            #w_sheet.write(37,3,variables[k])
            r_sheet.cell(31,3).value = variables[k]
        elif k>9:
            #w_sheet.write(2+k,17,variables[k])
            r_sheet.cell(2+k,17).value = variables[k]
        elif k>14:
            #w_sheet.write(4+k,17,variables[k])
            r_sheet.cell(4+k,17).value = variables[k]
        else:
            #w_sheet.write(10+k,3,variables[k])
            r_sheet.cell(10+k,3).value = variables[k]

    #wb.save('grgrSite/grgrSIte/grgrApp/vinnovatemp.xls')
    #wb.save('grgrApp/grgrSIte/grgrApp/vinnovatemp.xls')
    #vinnovafile = open_workbook('grgrSite/grgrSIte/grgrApp/vinnovatemp.xls')
    #vinnovafile = open_workbook('grgrApp/grgrSIte/grgrApp/vinnovatemp.xls')
    #r_sheet = vinnovafile.sheet_by_index(0)
    design_duration_rain = r_sheet.cell(105,3).value #D106
    available_volume = r_sheet.cell(107,3).value #D108
    required_volume = r_sheet.cell(106,3).value #D107
    for k in range(65,95):
        if r_sheet.cell(k,1).value == design_duration_rain:
            design_intensity_rain = r_sheet.cell(k,2).value
    D101 = r_sheet.cell(100,3).value
    D109 = r_sheet.cell(108,3).value
    design_duration_rain_ditch = r_sheet.cell(104,17).value #R105
    available_volume_ditch = r_sheet.cell(109,17).value #R110
    required_volume_ditch = r_sheet.cell(98,17).value #R99
    for k in range(65,95):
        if r_sheet.cell(k,15).value == design_duration_rain:
            design_intensity_rain_ditch = r_sheet.cell(k,16).value
    R102 = r_sheet.cell(101,17).value
    wb = copy(vinnovafile)
    wb.save('grgrSite/grgrSIte/grgrApp/vinnovatemp.xlsx')
    #vinnovafile = open_workbook('grgrApp/grgrSIte/grgrApp/vinnovatemp.xls')
    DRespons = [design_duration_rain,available_volume,required_volume,D101,D109,design_duration_rain_ditch,available_volume_ditch,required_volume_ditch,R102,design_intensity_rain,design_intensity_rain_ditch]
    #print DRespons
    return DRespons

def valueCell(calfile,row,col):
    """
    Read value from Sheet=sheet at Row = row and Column = col.
    Return this value.
    """
    sheet = calfile.sheet_by_index(0)
    cell = sheet.cell(row,col)
    return cell.value

if __name__ == '__main__':
    main()
