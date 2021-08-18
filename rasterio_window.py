import pandas as pd
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from rasterio.windows import Window
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime
start_time = datetime.now()


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