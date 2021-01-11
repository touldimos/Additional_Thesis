import pandas as pd
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from rasterio.windows import Window
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap
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

#Set the new matrices
prec, T, kop = ([] for i in range(3))

prec1 = r'C:\Dimos\database\Koppen\wc2.1_30s_prec\wc2.1_30s_prec_0{}.tif'
prec2 = r'C:\Dimos\database\Koppen\wc2.1_30s_prec\wc2.1_30s_prec_{}.tif'
temp1 = r'C:\Dimos\database\Koppen\wc2.1_30s_tavg\wc2.1_30s_tavg_0{}.tif'
temp2 = r'C:\Dimos\database\Koppen\wc2.1_30s_tavg\wc2.1_30s_tavg_{}.tif'
elev_raster = r'C:\Dimos\database\Koppen\wc2.1_30s_elev\wc2.1_30s_elev.tif'

start_row = 10000
end_row = 10050
start_col = 25000
end_col = 25050

#Raster read
for im in range(1, 10):
    w1 = (rasterio.open(prec1.format(im)))
    prec.append(np.array(w1.read(window=Window.from_slices((start_row, end_row), (start_col, end_col)))))
for im in range(10, 13):
    w1 = (rasterio.open(prec2.format(im)))
    prec.append(w1.read(window=Window.from_slices((start_row, end_row), (start_col, end_col))))
for im in range(1, 10):
    w0 = (rasterio.open(temp1.format(im)))
    T.append(w0.read(window=Window.from_slices((start_row, end_row), (start_col, end_col))))
for im in range(10, 13):
    w0 = (rasterio.open(temp2.format(im)))
    T.append(w0.read(window=Window.from_slices((start_row, end_row), (start_col, end_col))))

elev = (rasterio.open(elev_raster)).read(window=Window.from_slices((start_row, end_row), (start_col, end_col)))

# #Get rid of Nan values
prec = np.reshape(prec, (12, end_row - start_row, end_col - start_col))
prec = prec.astype("float")
prec[prec < 0] = np.nan


T = np.reshape(T, (12, end_row - start_row, end_col - start_col))
T = T.astype("float")
T[T < -3e+38] = np.nan

elev = np.reshape(elev, (1, end_row - start_row, end_col - start_col))
elev = elev.astype("float")
elev[elev == -32768] = np.nan

for i in range(0, end_row - start_row):
     for j in range(0, end_col - start_col):
            if T[0][i][j] >= -300:
                kop.append(Koppen((prec[0][i][j], prec[1][i][j], prec[2][i][j], prec[3][i][j], prec[4][i][j], prec[5][i][j], prec[6][i][j], prec[7][i][j], prec[8][i][j], prec[9][i][j], prec[10][i][j], prec[11][i][j]), (T[0][i][j], T[1][i][j], T[2][i][j], T[3][i][j], T[4][i][j], T[5][i][j], T[6][i][j], T[7][i][j], T[8][i][j], T[9][i][j], T[10][i][j], T[11][i][j]), elev[0][i][j]))
            else:
                kop.append('Not Classified')

koppen_map = np.reshape(kop, (end_row - start_row, end_col - start_col))
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

# world = rasterio.open(r'C:\Dimos\database\Koppen\wc2.1_30s_elev\wc2.1_30s_elev.tif')
# plt.figure(figsize = (20, 20))
# plt.imshow(world.read(1), cmap = 'Paired')
# currentAxis = plt.gca()
# currentAxis.add_patch(Rectangle((start_row, start_col), end_row - start_row, end_col - start_col, fill = None, alpha = 1, color = 'r', lw = 2))
# currentAxis.add_patch(Rectangle((start_row, start_col), end_row - start_row, end_col - start_col, alpha = 0.25, color = 'r'))
# plt.grid(color = 'black', ls = '--', alpha = 0.8)
# plt.show();

end_time = datetime.now()
net_time = end_time - start_time
print(net_time)