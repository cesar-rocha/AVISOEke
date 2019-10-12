import glob
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset

__datapath__ = "Data/"
__figpath__ = "Figures/"
__outputpath__ = 'Output/'

ncfiles = sorted(glob.glob(__datapath__ + "**/*.nc", recursive=True))

def kinetic_energy(data):
    
    return 0.5*( data['ugosa'][0]**2 + data['vgosa'][0]**2 )

# Get grid
filename = ncfiles[0]
data = Dataset(filename)
longitude, latitude =  data['longitude'][:], data['latitude'][:]

# Initialize kinetic energy array
ke = kinetic_energy(data)

# Need to consider potential gappy data
for filename in ncfiles[1:]:

    data = Dataset(filename)

    ke += kinetic_energy(data)

ke *= 1/len(ncfiles)

ke[ke.mask] = np.nan
np.savez("AVISO_EKE.npz",longitude=longitude,latitude=latitude,eke=ke)

# Create Basemap object
map_object=Basemap(lat_0=0, lon_0=-180, projection='robin' )

# Grid to map object
loni, lati = np.meshgrid(longitude,latitude)
x,y = map_object(loni,lati)

# SWOT Cal/Val orbit
calval = np.load("SWOTCalValOrbit.npz")
xswot, yswot = map_object(calval['lon'],calval['lat'])

# Plotting properties
levels = np.linspace(0,.15,30)
eke_ct_props = {'levels':levels, 'vmin':levels.min(),
                'vmax':levels.max(),'extend': 'max',
                'cmap': cmocean.cm.ice_r}

fig = plt.figure(figsize=(15,7.5))
map_object.contourf(x,y,ke,**eke_ct_props)
map_object.drawmapboundary(fill_color=None, linewidth=0)
map_object.fillcontinents(color='k', alpha=.8, lake_color='white')
map_object.drawcoastlines(linewidth=0.1, color="white")
map_object.plot(xswot,yswot,'k.')
plt.colorbar(orientation='horizontal',shrink=0.75,fraction=0.03,
            pad=0.05,ticks=[0,0.05,0.1,0.15,],label=r'Eddy Kinetic Energy [m$^2$ s$^{-2}]$')



