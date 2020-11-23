import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import rasterio
from rasterio.windows import Window
from datetime import datetime
start_time = datetime.now()

def Koppen(P, T, z = 0):
    if np.isnan(P).all() == True:
        classification = 'Not classified'
    else:
        data = pd.DataFrame(data = (P, T), index = ['P', 'T']).transpose()

        MAP = np.sum(P)
        MAT = np.mean(T)
        Thot = np.max(T)
        Tcold = np.min(T)
        Tmonth10 = sum(map(lambda x : x > 10, T))
        Pdry = np.min(P)
        seqT = np.array((T[0], T[1], T[2], T[3], T[4], T[5], T[6], T[7], T[8], T[9], T[10], T[11], T[0], T[1], T[2], T[3], T[4]))
        seqP = np.array((P[0], P[1], P[2], P[3], P[4], P[5], P[6], P[7], P[8], P[9], P[10], P[11], P[0], P[1], P[2], P[3], P[4]))
        data['seqT'] = np.convolve(seqT, np.ones(6, dtype=np.int), mode='valid')
        data['seqP'] = np.convolve(seqP, np.ones(6, dtype=np.int), mode='valid')

        s_st = data['seqT'].idxmax(axis = 1)
        s_f = s_st + 6
        w_st = s_f
        w_f = w_st + 6

        if s_f > 12:
            s_f = s_f - 12
        if w_f > 12:
            w_f = w_f - 12
        if s_st > 12:
            s_st = s_st - 12
        if w_st > 12:
            w_st = w_st - 12

        drymonth = data['P'].idxmin(axis = 1)
        season = []

        if s_st < s_f and w_st < w_f:
            Psdry = data['P'][(data.index >= s_st) & (data.index < s_f)].min()
            Pwdry = (data['P'][(data.index >= w_st) & (data.index < w_f)].min())
            Pswet = data['P'][(data.index >= s_st) & (data.index < s_f)].max()
            Pwwet = (data['P'][(data.index >= w_st) & (data.index < w_f)].max())
            if s_st < drymonth and s_f > drymonth:
                season.append('summer')
            else:
                season.append('winter')

        if s_st < s_f and w_st > w_f:
            Psdry = data['P'][(data.index >= s_st) & (data.index < s_f)].min()
            Pwdry = (data['P'][(data.index >= w_st)].min(), data['P'][(data.index < w_f)].min())
            Pwdry = np.min(Pwdry)
            Pswet = data['P'][(data.index >= s_st) & (data.index < s_f)].max()
            Pwwet = (data['P'][(data.index >= w_st)].max(), data['P'][(data.index < w_f)].max())
            Pwwet = np.max(Pwwet)
            if s_st < drymonth and s_f > drymonth:
                season.append('summer')
            else:
                season.append('winter')

        if s_st > s_f and w_st < w_f:
            Psdry = (data['P'][(data.index >= s_st)].min(), data['P'][(data.index < s_f)].min())
            Psdry = np.min(Psdry)
            Pwdry = (data['P'][(data.index >= w_st) & (data.index < w_f)].min())
            Pswet = (data['P'][(data.index >= s_st)].max(), data['P'][(data.index < s_f)].max())
            Pswet = np.max(Pswet)
            Pwwet = (data['P'][(data.index >= w_st) & (data.index < w_f)].max())

            if w_st < drymonth and w_f > drymonth:
                season.append('winter')
            else:
                season.append('summer')

        if s_st < w_st:
            s_f = s_f - 1
            w_f = w_f - 1
        else:
            w_f = w_f - 1
            s_f = s_f - 1

        if w_st == 12:
            w_st = 0

        if 0.7 * MAP <= data['seqP'].loc[w_st]:
            Pthresh = 2 * MAT
        elif 0.7 * MAP <= data['seqP'].loc[s_st]:
            Pthresh = 2 * MAT + 28
        else:
            Pthresh = 2 * MAT + 14

        class_Kop = []

        if z >= 2300:
            if Thot >= 0:
                class_Kop.append('HT - Tundra')
            else:
                class_Kop.append('HF - Frost or Ice Cap')
        else:
            if Thot <= 10:
                if Thot > 0:
                    class_Kop.append('ET - Tundra')
                else:
                    class_Kop.append('EF - Frost or Ice Cap')
            else:
                if MAP < 10 * Pthresh:
                    if MAP < 5 * Pthresh:
                        if MAT >= 18:
                             class_Kop.append('BWh - Hot Waste')
                        else:
                             class_Kop.append('BWk - Cold Waste')
                    else:
                        if MAT >= 18:
                             class_Kop.append('BSh - Hot Steppe')
                        else:
                             class_Kop.append('BSk - Cold Steppe')
                else:
                    if Tcold >= 18:
                        if Pdry > 60:
                            class_Kop.append('Af - Tropical Wet')
                        else:
                            if MAP < (100 - (Pdry) * 25):
                                class_Kop.append('Am - Monsoon')
                            else:
                                if season == 'summer':
                                    class_Kop.append('As - Summer Savannah')
                                else:
                                    class_Kop.append('Aw - Winter Savannah')
                    else:
                        if Tcold > -3:
                            if Pwdry > Psdry and Pwdry > Psdry * 3 and Psdry < 40:
                                class_Kop.append('Cs')
                                if Thot >= 22:
                                    class_Kop.append('a')
                                elif Thot < 22 and Tmonth10 >= 4:
                                    class_Kop.append('b')
                                else:
                                    class_Kop.append('c') 
                            elif Psdry > Pwdry and Pswet > Pwdry * 10:
                                class_Kop.append('Cw')
                                if Thot >= 22:
                                    class_Kop.append('a')
                                elif Thot < 22 and Tmonth10 >= 4:
                                    class_Kop.append('b')
                                else:
                                    class_Kop.append('c')
                            else:
                                class_Kop.append('Cf')
                                if Thot >= 22:
                                    class_Kop.append('a')
                                elif Thot < 22 and Tmonth10 >= 4:
                                    class_Kop.append('b')
                                else:
                                    class_Kop.append('c')
                        else:
                            if Pwdry > Psdry and Pwdry > Psdry * 3 and Psdry < 40:
                                class_Kop.append('Ds')
                                if Thot >= 22:
                                    class_Kop.append('a')
                                elif Thot < 22 and Tmonth10 >= 4:
                                    class_Kop.append('b')
                                elif Tmonth10 < 4 and Tcold >= -38:
                                    class_Kop.append('c')
                                else:
                                    class_Kop.append('d')
                            elif Psdry > Pwdry and Pswet > Pwdry * 10:
                                class_Kop.append('Dw')
                                if Thot >= 22:
                                    class_Kop.append('a')
                                elif Thot < 22 and Tmonth10 >= 4:
                                    class_Kop.append('b')
                                elif Tmonth10 < 4 and Tcold >= -38:
                                    class_Kop.append('c')
                                else:
                                    class_Kop.append('d')
                            else:
                                class_Kop.append('Df')
                                if Thot >= 22:
                                    class_Kop.append('a')
                                elif Thot < 22 and Tmonth10 >= 4:
                                    class_Kop.append('b')
                                elif Tmonth10 < 4 and Tcold >= -38:
                                    class_Kop.append('c')
                                else:
                                    class_Kop.append('d')
        classification = ''.join(class_Kop)
    return classification

path_pr1 = r"C:\Dimos\database\Koppen\wc2.1_30s_prec\wc2.1_30s_prec_01.tif"
path_pr2 = r"C:\Dimos\database\Koppen\wc2.1_30s_prec\wc2.1_30s_prec_02.tif"
path_pr3 = r"C:\Dimos\database\Koppen\wc2.1_30s_prec\wc2.1_30s_prec_03.tif"
path_pr4 = r"C:\Dimos\database\Koppen\wc2.1_30s_prec\wc2.1_30s_prec_04.tif"
path_pr5 = r"C:\Dimos\database\Koppen\wc2.1_30s_prec\wc2.1_30s_prec_05.tif"
path_pr6 = r"C:\Dimos\database\Koppen\wc2.1_30s_prec\wc2.1_30s_prec_06.tif"
path_pr7 = r"C:\Dimos\database\Koppen\wc2.1_30s_prec\wc2.1_30s_prec_07.tif"
path_pr8 = r"C:\Dimos\database\Koppen\wc2.1_30s_prec\wc2.1_30s_prec_08.tif"
path_pr9 = r"C:\Dimos\database\Koppen\wc2.1_30s_prec\wc2.1_30s_prec_09.tif"
path_pr10 = r"C:\Dimos\database\Koppen\wc2.1_30s_prec\wc2.1_30s_prec_10.tif"
path_pr11 = r"C:\Dimos\database\Koppen\wc2.1_30s_prec\wc2.1_30s_prec_11.tif"
path_pr12 = r"C:\Dimos\database\Koppen\wc2.1_30s_prec\wc2.1_30s_prec_12.tif"

path_tm1 = r"C:\Dimos\database\Koppen\wc2.1_30s_tavg\wc2.1_30s_tavg_01.tif"
path_tm2 = r"C:\Dimos\database\Koppen\wc2.1_30s_tavg\wc2.1_30s_tavg_02.tif"
path_tm3 = r"C:\Dimos\database\Koppen\wc2.1_30s_tavg\wc2.1_30s_tavg_03.tif"
path_tm4 = r"C:\Dimos\database\Koppen\wc2.1_30s_tavg\wc2.1_30s_tavg_04.tif"
path_tm5 = r"C:\Dimos\database\Koppen\wc2.1_30s_tavg\wc2.1_30s_tavg_05.tif"
path_tm6 = r"C:\Dimos\database\Koppen\wc2.1_30s_tavg\wc2.1_30s_tavg_06.tif"
path_tm7 = r"C:\Dimos\database\Koppen\wc2.1_30s_tavg\wc2.1_30s_tavg_07.tif"
path_tm8 = r"C:\Dimos\database\Koppen\wc2.1_30s_tavg\wc2.1_30s_tavg_08.tif"
path_tm9 = r"C:\Dimos\database\Koppen\wc2.1_30s_tavg\wc2.1_30s_tavg_09.tif"
path_tm10 = r"C:\Dimos\database\Koppen\wc2.1_30s_tavg\wc2.1_30s_tavg_10.tif"
path_tm11 = r"C:\Dimos\database\Koppen\wc2.1_30s_tavg\wc2.1_30s_tavg_11.tif"
path_tm12 = r"C:\Dimos\database\Koppen\wc2.1_30s_tavg\wc2.1_30s_tavg_12.tif"

rows = 21600
cols = 43200

koppen = []
# k = np.random.randint(0, rows, 1)
# l = np.random.randint(0, cols, 1)

# rows = 10800
# cols = 25600
# pls = 25

for k in range(0, rows):
    for l in range(0, cols):
        prec1 = rasterio.open(path_pr1).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        prec2 = rasterio.open(path_pr2).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        prec3 = rasterio.open(path_pr3).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        prec4 = rasterio.open(path_pr4).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        prec5 = rasterio.open(path_pr5).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        prec6 = rasterio.open(path_pr6).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        prec7 = rasterio.open(path_pr7).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        prec8 = rasterio.open(path_pr8).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        prec9 = rasterio.open(path_pr9).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        prec10 = rasterio.open(path_pr10).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        prec11 = rasterio.open(path_pr11).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        prec12 = rasterio.open(path_pr12).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        
        temp1 = rasterio.open(path_tm1).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        temp2 = rasterio.open(path_tm2).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        temp3 = rasterio.open(path_tm3).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        temp4 = rasterio.open(path_tm4).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        temp5 = rasterio.open(path_tm5).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        temp6 = rasterio.open(path_tm6).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        temp7 = rasterio.open(path_tm7).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        temp8 = rasterio.open(path_tm8).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        temp9 = rasterio.open(path_tm9).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        temp10 = rasterio.open(path_tm10).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        temp11 = rasterio.open(path_tm11).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        temp12 = rasterio.open(path_tm12).read(window=Window.from_slices((k, k + 1), (l, l + 1))).ravel()
        
        prec = (prec1, prec2, prec3, prec4, prec5, prec6, prec7, prec8, prec9, prec10, prec11, prec12)
        prec = np.vstack(prec).ravel()
        prec = np.where(prec < 0, np.nan, prec)
        
        temp = (temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9, temp10, temp11, temp12)
        temp = np.vstack(temp).ravel()
        temp = np.where(temp < -500, np.nan, temp)
    
        koppen.append(Koppen(prec, temp, 0))

koppen_map = np.reshape(koppen, (cols, rows))
koppen_code = koppen_map.copy()

koppen_code[koppen_code == 'Af - Tropical Wet'] = 0
koppen_code[koppen_code == 'Am - Monsoon'] = 1
koppen_code[koppen_code == 'As - Summer Savannah'] = 2
koppen_code[koppen_code == 'Aw - Winter Savannah'] = 3
koppen_code[koppen_code == 'BWh - Hot Waste'] = 4
koppen_code[koppen_code == 'BWk - Cold Waste'] = 5
koppen_code[koppen_code == 'BSh - Hot Steppe'] = 6
koppen_code[koppen_code == 'BSk - Cold Steppe'] = 7
koppen_code[koppen_code == 'Cfa'] = 8
koppen_code[koppen_code == 'Cfb'] = 9
koppen_code[koppen_code == 'Cfc'] = 10
koppen_code[koppen_code == 'Csa'] = 11
koppen_code[koppen_code == 'Csb'] = 12
koppen_code[koppen_code == 'Csc'] = 13
koppen_code[koppen_code == 'Cwa'] = 14
koppen_code[koppen_code == 'Cwb'] = 15
koppen_code[koppen_code == 'Cwc'] = 16
koppen_code[koppen_code == 'Dfa'] = 17
koppen_code[koppen_code == 'Dfb'] = 18
koppen_code[koppen_code == 'Dfc'] = 19
koppen_code[koppen_code == 'Dfd'] = 20
koppen_code[koppen_code == 'Dsa'] = 21
koppen_code[koppen_code == 'Dsb'] = 22
koppen_code[koppen_code == 'Dsc'] = 23
koppen_code[koppen_code == 'Dsd'] = 24
koppen_code[koppen_code == 'Dwa'] = 25
koppen_code[koppen_code == 'Dwb'] = 26
koppen_code[koppen_code == 'Dwc'] = 27
koppen_code[koppen_code == 'Dwd'] = 28
koppen_code[koppen_code == 'ET - Tundra'] = 29
koppen_code[koppen_code == 'EF - Frost or Ice Cap'] = 30
koppen_code[koppen_code == 'HT - Tundra'] = 31
koppen_code[koppen_code == 'HF - Frost or Ice Cap'] = 32
koppen_code[koppen_code == 'Not classified'] = np.nan

koppen_code = koppen_code.astype("float")

end_time = datetime.now()
net_time = end_time - start_time
net_time