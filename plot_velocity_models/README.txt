These python scripts intend to read a velocity model in NetCDF format and plotting it according to the limits given by the user. 

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

Type in the terminal "python  index_vm.py - h" and you will see the following menu:


options:
  -h, --help  show this help message and exit
  -mode MODE  If you run this script interactively (-mode 1), you will be guided through the steps for plotting.
              If not (-mode 2), you need to create a param.txt file with the input values like this:
               	Variable: VP
               	Depth: 10
               	Latitude_boundaries: 10/50
              	Longitude_boundaries: 24/76
              Latitude and longitude boundaries could be left in blank for using the model boundaries.
              If you are not familiar with the velocity model, it is recommended to use the interactive mode (-mode 1)
              for displaying the model boundaries and grid points.
  -file FILE  NetCDF file name (e.g., -file MESWA.nc)

That explains you have to provide the name of the NetCDF file and to choose between run the script iteratively or provide the input parameters for plotting the velocity model through an external txt file.

For instance, an example for running interactively the script would be: python index_vm.py -mode 1 -file MESWA.nc 
Then you will be prompted for typing the options for making the plot. 

Depending of the options you have chosen, you must see a file named: Rodgers_VS_LAT_20-40_LON_30-60_Z_30.pdf

This example, is a plot where is shown the VS values for a region from 20 to 40 latitude, 30 to 60 longitude and a depth of 30km

On the other Hand, if you run: python index_vm.py -mode 2 -file MESWA.nc , you must already have a param.txt file that contains the information that would be given by the user in the mode 1. 

4. Run index_vm.py many times:

With this script you can make several plots for a single parameter but with different depths. This is, you will create many files due to run automatically several times index_vm.py, each file will be the plot of the velocity model at different depths. It is hardcoded for  plot the velocity model for VP values in depths from 0 to 82.

