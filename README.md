# EU_11_eCLM_curvilinear

This repository shows the workflow for creating curvilinear surface and domain fields for eCLM simulations. The workflow follows the official clm-workflow but makes a few adaptions. 

It is not necessary to clone CTSM and cime, as this workflow is independent. However, the basis is the clm5.0 release and there might be newer developments in the official repositories below

```
https://github.com/ESCOMP/CTSM.git
https://github.com/ESMCI/cime.git
```
## Creation of gridfile

First, we need to create a gridfile that describes our simulation domain. The repository contains the ncl-script `produce_scrip_from_griddata.ncl` that can create a SCRIP-file from a netcdf that contains the lat- and lon-center coordinates 

To use `mksurfdata.pl` regridding weights have to be created. For this the grid has to be properly defined in one of the following formats:

- SCRIP 
- ESMF-Mesh 
- CF-convention-file

SCRIP is a very old format not maintained anymore but is still the most effective solution. it can be easily created with curvilinear_to_SCRIP from NCL. Unfortunately, NCL is also not maintained anymore, so this could lead to problems in the future.

ESMF-Mesh files are able to describe unstructured grids. A solution to create them is again found in a CTSM branch: `subset_mesh_dask` under `tools/site_and_regional/mesh_maker.py` I had to rewrite part of the script for it to accept 2d lat / lon. The main caveat is that the resulting surface files are in 1D which makes them harder to handle.

ESMF is able to basically handle any netcdf-file that follows the CF-conventions version 1.6 and includes lat /lon values and corners. Still, it is not the easy to correctly produce a correct description. I had the most success by mapping any grid to the desired grid by ncremap. NCO then produces lat and lon values and the vertices according to the CF-convention. However, I had to manually correct the grid corners at the most outer northside.

At the moment SCRIP generation is easiest with ncl. In `mkmapgrids/` you find produce_scrip_from `griddata.ncl`. To use it you need a netcdf file with the lat/lon centers in 2D. It is not necessary to provide the corners because the internal routine of ncl seems to calculate them correctly for the later steps. Adapt the input in `produce_scrip_from_griddata.ncl` to your gridfile and execute:

```
ncl produce_scrip_from_griddata.ncl
```

There should already be netcdf files for your grid or you can create them according to Niklas Wagner's workflow for creating static files.
 
## Creation of mapping files

For the creation of the mapping files of CLM inputdata to our grid use mkmapdata/runscript_mkmapdata.sh. Adapt the script to your previously created SCRIP file, to your compute time project and to the path to the CLM mappingdata. The script can be used on JURECA and JUWELS but it is advisable to use the large memory partitions for larger domains. If you don't have access to the CLM mappingdata you have to download it. Use:

```
wget --no-check-certificate -i  clm_mappingfiles.txt
```
Then start the creation of the weights with
```
sbatch runscript_mkmapdata.sh
```

## Creation of domain files

The CIME submodule under `./gen_domain_files/` generates the domain files for CLM. This repository contains a simplified version of `gen_domain` which is easier to compile on JSC machines and you do not need the CIME repository. To compile it go to  the `src/` directory with the loaded modules ifort, imkl, netCDF and netCDF-Fortran. Then compile with 

```
ifort -o ../gen_domain gen_domain.F90 -mkl -lnetcdff -lnetcdf
```

After the compilation you can execute `gen_domain` with $MAPFILE being of the mapping files created before and $GRIDNAME being a sting with the name of your grid. The choice of $MAPFILE does not influence the lat- and longitude values in the domain file but can influence the land/sea mask. 

```
./gen_domain -m $MAPFILE -o $GRIDNAME -l $GRIDNAME
```

The created domain file will later be modified.



## Creation of surface file

The surface creation tool is found under `./mksurfdata_map/`. You have to compile it with make. The essential modules you need to load are intel and netCDF-Fortran. You still need to export (e.g. for jsc machines)

```
export LIB_NETCDF=${EBROOTNETCDFMINFORTRAN}/lib
export INC_NETCDF=${EBROOTNETCDFMINFORTRAN}/include

```
After compilation modify corresponding pathes and execute 
```
export GRIDNAME=EUR-11
export CDATE=`date +%y%m%d`
export CSMDATA=/p/scratch/cslts/hartick1/CTSM/tools/mkmapdata/

# generate surfdata
./mksurfdata.pl -r usrspec -usr_gname $GRIDNAME -usr_gdate $CDATE -l $CSMDATA -allownofile -y 2005 -hirespft
```
to create a real domain with hires pft. Again, you need to have set a $GRIDNAME, a current date $DATE in yymmdd and the path where the raw data of CLM is stored $CSMDATA. You have to download the data from https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/ if you have no access.

Also make sure that mksurdata and mkmdapdata have the same parent directory.

PS: There are many versions mksurfdata.pl in the CTSM github. Stick to the clm5-release version! Other versions use other mapping files and are not compatible with negative longitudes.

## Modification of the surface and domain file

The created surface and domain file have negative longitudes that CLM5 does not accept and inherently has no landmask. To modify the longitudes and to add a landmask use `mod_domain.sh` after inserting the paths to your files.

## Creation of forcing data from ERA5

A possible source of atmospheric forcing for CLM5 is ERA5. The folder `mkforcing/` contains two scripts that assist the ERA5 retrieval. `download_ERA5.py` contains a prepared retrieval for the cdsapi python module. By modifying the two loops inside the script it is possible to download ERA5 for any timerange. However, the script requires that cdsapi is installed with an user specific key. More information about the installation can be found [here](https://cds.climate.copernicus.eu/api-how-to). 
`prepare_ERA5.sh` prepares ERA5 as an input by changing names and modifying units. ERA5 has to be regridded to your resolution before the script can be used.









