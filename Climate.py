path = r'C:\Users\owner\Google Drive 2\Additional Thesis'
import sys
sys.path.append(path)
from Climate_all import Climate

prec1 = r'C:\Users\owner\Google Drive 2\Additional Thesis\wc2.1_10m_prec\wc2.1_10m_prec_0{}.tif'
prec2 = r'C:\Users\owner\Google Drive 2\Additional Thesis\wc2.1_10m_prec\wc2.1_10m_prec_{}.tif'
temp1 = r'C:\Users\owner\Google Drive 2\Additional Thesis\wc2.1_10m_tavg\wc2.1_10m_tavg_0{}.tif'
temp2 = r'C:\Users\owner\Google Drive 2\Additional Thesis\wc2.1_10m_tavg\wc2.1_10m_tavg_{}.tif'
elev_raster = r'C:\Users\owner\Google Drive 2\Additional Thesis\wc2.1_10m_elev\wc2.1_10m_elev.tif'
  
# m = np.random.randint(0, cols) #Lenght (Χ) 
# n = np.random.randint(0, rows) #Width  (Υ)

m = 1195      #GREECE
n = 285       #GREECE

l = 5
k = 5

# m = 0           #X
# n = 0           #Y

# l = rows        #Lenght (Χ)
# k = cols        #Width  (Υ)

rot = 0
el = 60

df, time = Climate(path, prec1, prec2, temp1, temp2, elev_raster, m, n, k, l, rot, el, ter = True)
print(time)