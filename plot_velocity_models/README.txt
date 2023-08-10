This python script intends to read a velocity model in NetCDF format and plotting it according to the limits given by the user. 

It has been tested for the MESW velocity model (Rodgers, 2023: https://zenodo.org/record/8212589). So you need to download the velocity model from the repository. 

The following instructions are given assuming you have installed Anaconda.


1. Create and activate a new environment in Anaconda

The general recommendation is to create a new environment for installing the packages needed to use this script. You can skip this step if you consider that you have all the packages installed and it is not necessary to create a new environment.

conda create --name netcdf
conda activate netcdf

2. Packages needed for using this script

Once the netcdf environment is activated, then install the following packages:

* cartopy, pip, and pyproj: conda install pip cartopy pyproj
* pandas: conda install -c anaconda pandas
* xarray: conda install -c anaconda xarray
* netcdf4: conda install netcdf4

3. Run the script:

Type in the terminal "python  index_vm.py" and follow the instructions as they appear during the script execution.

Depending of the options you have chosen, you must see a file named: Rodgers_VS_LAT_20-40_LON_30-60_Z_30.pdf

This example, is a plot where is shown the VS values for a region from 20 to 40 latitude, 30 to 60 longitude and a depth of 30km. 


