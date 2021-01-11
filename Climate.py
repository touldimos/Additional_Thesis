path = r'C:\Users\owner\Google Drive 2\MSc\TU DELFT - Water Managment\Additional Thesis\Scripts'
import sys
sys.path.append(path)
from Climate_all import Climate
import rasterio
import numpy as np 

prec1 = r'C:\Users\owner\Google Drive 2\MSc\TU DELFT - Water Managment\Additional Thesis\Scripts\wc2.1_10m_prec\wc2.1_10m_prec_0{}.tif'
prec2 = r'C:\Users\owner\Google Drive 2\MSc\TU DELFT - Water Managment\Additional Thesis\Scripts\wc2.1_10m_prec\wc2.1_10m_prec_{}.tif'
temp1 = r'C:\Users\owner\Google Drive 2\MSc\TU DELFT - Water Managment\Additional Thesis\Scripts\wc2.1_10m_tavg\wc2.1_10m_tavg_0{}.tif'
temp2 = r'C:\Users\owner\Google Drive 2\MSc\TU DELFT - Water Managment\Additional Thesis\Scripts\wc2.1_10m_tavg\wc2.1_10m_tavg_{}.tif'
elev_raster = r'C:\Users\owner\Google Drive 2\MSc\TU DELFT - Water Managment\Additional Thesis\Scripts\wc2.1_10m_elev\wc2.1_10m_elev.tif'

rast = (rasterio.open(prec1.format(1)))
rows = rast.shape[0]
cols = rast.shape[1]

# m = np.random.randint(0, cols) #Lenght (Χ)
# n = np.random.randint(0, rows) #Width  (Υ)

m = 1195      #GREECE
n = 285       #GREECE

# m = 1095      #NETHERLANDS
# n = 205       #NETHERLANDS

l = 15
k = 15

# m = 1169           #X
# n = 392           #Y

# l = rows        #Lenght (Χ)
# k = cols        #Width  (Υ)

rot = 0
el = 60

Climate(path, prec1, prec2, temp1, temp2, elev_raster, m, n, k, l, rot, el, ter = False)
