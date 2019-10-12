import numpy as np
import cmocean
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

__figpath__ = "Figures/"

aviso = np.load("AVISO_EKE.npz")

# Create Basemap object
map_object=Basemap(lat_0=0, lon_0=-180, projection='robin' )

# Grid to map object
loni, lati = np.meshgrid(aviso['longitude'],aviso['latitude'])
x,y = map_object(loni,lati)

# SWOT Cal/Val orbit
#calval = np.load("SWOTCalValOrbit.npz")
#xswot, yswot = map_object(calval['lon'],calval['lat'])

# Plotting properties
levels = np.linspace(0,.15,30)
eke_ct_props = {'levels':levels, 'vmin':levels.min(),
                'vmax':levels.max(),'extend': 'max',
                'cmap': cmocean.cm.ice_r}

fig = plt.figure(figsize=(12,5.5))
map_object.contourf(x,y,aviso['eke'],**eke_ct_props)
map_object.drawmapboundary(fill_color=None, linewidth=0)
map_object.fillcontinents(color='k', alpha=.8, lake_color='white')
map_object.drawcoastlines(linewidth=0.1, color="white")
#map_object.plot(xswot[:],yswot[:],'k')
plt.colorbar(orientation='horizontal',shrink=0.8,fraction=0.05,
            pad=0.05,ticks=[0,0.05,0.1,0.15,],label=r'Eddy Kinetic Energy [m$^2$ s$^{-2}]$')
plt.savefig(__figpath__+"AVISOEke.png", bbox_inches='tight', pad_inches=0)







