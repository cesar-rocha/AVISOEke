from netCDF4 import Dataset
import numpy as np
from scipy import ndimage
import cmocean
import gsw
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as basemap

# Change default value of latlon kwarg to True.m.latlon_default=True
#basemap.latlon_default=True

__figpath__ = "Figures/"

aviso = np.load("AVISO_EKE.npz")

# Create Basemap object
map_object=basemap.Basemap(lat_0=0, lon_0=-180, projection='robin' )

# Grid 
loni, lati = np.meshgrid(aviso['longitude'],aviso['latitude'])
xi, yi = map_object(loni,lati)

# SWOT Cal/Val orbit
#calval = np.load("SWOTCalValOrbit.npz")
#lons, lats = calval['lon'],calval['lat']
#xswot, yswot = map_object(lons,lats)

# f/h using etopo5 data
etopo = Dataset('etopo5.nc')
lont, latt = np.meshgrid(etopo['X'][:], etopo['Y'][:])
topo = - np.ma.masked_array(etopo['bath'][:], etopo['bath'][:]>0)
fonh = (gsw.f(latt)/gsw.f(45))/(topo/4000)
fonh[fonh.mask] = np.nan

lont, fonh = map_object.shiftdata(lont,fonh)
xt,yt = map_object(lont,latt)

# Smooth f/h using 8  by 8 point filter
fonh_filtered = ndimage.filters.gaussian_filter(fonh, [8,8], mode='constant')

# Plotting properties
levels = np.linspace(0,.15,30)
eke_ct_props = {'levels':levels, 'vmin':levels.min(),
                'vmax':levels.max(),'extend': 'max',
                'cmap': cmocean.cm.ice_r}

fig = plt.figure(figsize=(12,5.5))
ceke = map_object.contourf(xi,yi,aviso['eke'],**eke_ct_props)
map_object.drawmapboundary(fill_color=None, linewidth=0)
map_object.fillcontinents(color='k', alpha=.8, lake_color='white')
map_object.drawcoastlines(linewidth=0.1, color="white")
#map_object.contour(xt,yt,fonh_filtered,np.linspace(-2.5,2.5,20),colors='k',
#                   linewidths=1,linestyles='solid')
#map_object.plot(lons,lats,'k',linewidth=1)
plt.colorbar(ceke, orientation='horizontal',shrink=0.8,fraction=0.05,
            pad=0.05,ticks=[0,0.05,0.1,0.15,],label=r'Eddy Kinetic Energy [m$^2$ s$^{-2}]$')
plt.savefig(__figpath__+"AVISOEke.png", bbox_inches='tight', pad_inches=0)



