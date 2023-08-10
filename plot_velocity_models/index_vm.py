#Script for navigating through velocity models in NETCDF format and plotting it according to different limits given by the user
#Felix Rodriguez Cardozo. August 9th 2023
#Use mtuq_j environment 
#https://github.com/rmodrak/mtuq/blob/c605632b265ba1bb6d7fec7af47a4b703c0aca88/mtuq/graphics/uq/double_couple.py#L178
#https://docs.xarray.dev/en/stable/generated/xarray.DataArray.where.html
#https://xarray.pydata.org/en/v0.8.0/generated/xarray.DataArray.where.html
#https://github.com/rmodrak/mtuq/blob/c605632b265ba1bb6d7fec7af47a4b703c0aca88/mtuq/graphics/uq/double_couple.py#L178
#https://github.com/rmodrak/mtuq/blob/c605632b265ba1bb6d7fec7af47a4b703c0aca88/mtuq/grid/moment_tensor.py
#https://uafgeotools.github.io/mtuq/user_guide/05/gallery_mt.html
#https://stackoverflow.com/questions/40179593/how-to-get-the-coordinates-of-the-maximum-in-xarray
#https://mom6-analysiscookbook.readthedocs.io/en/latest/notebooks/Plotting.html

from pandas import DataFrame
from xarray import DataArray
import xarray as xr
import glob
import numpy as np
import os
import os.path
#import pygmt
import netCDF4 as nc
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


def get_array(var,netcdf_file):
    #da = xr.open_dataarray(netcdf_file)
    ds = xr.open_dataset(netcdf_file)
    lat = ds.latitude.values
    #print(lat)
    lon = ds.longitude.values
    depth = ds.depth.values
    data_array = ds[var]
    return(lat,lon,depth,data_array)


def make_dictionary_index(latitude,longitude,depth):
    dict_lat = {}
    dict_lon = {}
    dict_depth = {}

    for l,lat in enumerate(latitude):
        dict_lat[np.round(lat,1)] = l

    for l,lon in enumerate(longitude):
        dict_lon[np.round(lon,1)] = l
    
    for i,d in enumerate(depth):
        dict_depth[np.round(d)] = i
    
    return(dict_lat,dict_lon,dict_depth)

def print_vm_boundaries(lat,lon,depth):
    print("\nVelocity model boundaries:")
    dlat = (np.max(lat)-np.min(lat))/len(lat)
    dlat = round_to_1(dlat)
    print("Latitude min/max/step {}/{}/{}".format(np.min(lat),np.max(lat),dlat))

    dlon = (np.max(lon)-np.min(lon))/len(lon)
    dlon = round_to_1(dlon)
    print("Longitude min/max/step {}/{}/{}".format(np.min(lon),np.max(lon),dlon))

    ddepth = (np.max(depth)-np.min(depth))/len(depth)
    ddepth= round_to_1(ddepth)
    print("Depth min/max/step {}/{}/{}".format(np.min(depth),np.max(depth),ddepth))

def round_to_1(x):
   #https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
   number = np.round(x, -int(np.floor(np.log10(np.abs(x)))))
   return (number)

def get_boundaries(dict_lat,dict_lon,dict_depth):
    
    d = int(input("\nChoose a depth for plotting an slice of the velocity model: "))
    depth_index = dict_depth.get(d)
    print(depth_index)

    lim_lat = input("\nChoose min/max latitude for the slice (eg., 10/50). Just enter if limits are the model boundaries: ")
    if lim_lat == '':
        lim_lat = '{}/{}'.format(np.min(lat),np.max(lat))

    #Here there is an issue because the latitude arrays are inverted, they started with maximum and end with minimun, so we have to reverse the indexes
    aux_lat = lim_lat.split('/')
    lat_index = [dict_lat.get(float(aux_lat[1])),dict_lat.get(float(aux_lat[0]))]


    lim_lon = input("\nChoose min/max longitude for the slice (eg., 24/76). Just enter if limits are the model boundaries: ")
    if lim_lon == '':
        lim_lon = '{}/{}'.format(np.min(lon),np.max(lon))

    aux_lon = lim_lon.split('/')
    lon_index = [dict_lon.get(float(aux_lon[0])),dict_lon.get(float(aux_lon[1]))]

    depth_index = dict_depth.get(d)

    #print(lat_index)
    #print(lon_index)
    #print(depth_index)

    return(aux_lat,aux_lon,d,lat_index,lon_index,depth_index)

def plot_slice(aux_lat,aux_lon,d,lat_index,lon_index,depth_index,data_array,var):


    data_slice = data_array.isel(depth=depth_index,latitude=slice(lat_index[0],lat_index[1]),longitude=slice(lon_index[0],lon_index[1]))
    print(data_slice)
    data_slice.plot()
    plt.savefig('Rodgers_{}_LAT_{}-{}_LON_{}-{}_Z_{}.pdf'.format(var,aux_lat[0],aux_lat[1],aux_lon[0],aux_lon[1],d))


def search_nan(lon,lat,d,data_array):
    for x in lon:
        for y in lat:
            vs = data_array.loc[y,x,d].item()
            if np.isnan(vs):
                print('We have an NAN in lat:{},lon:{},depth:{}'.format(y,x,d))
            else:
                print('The VS is {} in lat:{},lon:{},depth:{}'.format(vs,y,x,d))


if __name__=='__main__':

    netcdf_file = 'MESWA.nc'
    #ds = nc.Dataset(netcdf_file)
    ds = xr.open_dataset(netcdf_file)
    #print(ds)
    print (ds.data_vars)
    
    #Define the variable you want to retrieve. Use the information printed above for selection the variable (case sensitive)
    var = input("Type variable to retrieve from the database (CASE SENSITIVE, vs is not VS): ")

    #Retrieve data_array
    lat,lon,depth,data_array = get_array(var,netcdf_file)

    #Make a dictionary for coordinates, because (as far as I know) the data arrays are indexed with indexes rather with the coordinates itself.
    #For instance, for choosing an slice of 10km the user would have to provide the index corresponding with such depth (eg.,data_array.isel(depth=1)).
    #This could be complicated for any user, so, if the user types the depth, we use the dictionary for converting the depth into the index. 
    dict_lat,dict_lon,dict_depth = make_dictionary_index(lat,lon,depth)

    #Show velocity model boundaries
    print_vm_boundaries(lat,lon,depth)

    #Choosing the section of the velocity model to be plot
    aux_lat,aux_lon,d,lat_index,lon_index,depth_index = get_boundaries(dict_lat,dict_lon,dict_depth)

    #Plot the VM
    plot_slice(aux_lat,aux_lon,d,lat_index,lon_index,depth_index,data_array,var)

    #print(lat,lon,depth)
    #d = 30
    #search_nan(lon,lat,d,data_array)
