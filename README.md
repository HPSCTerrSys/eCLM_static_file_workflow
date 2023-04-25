# EU_11_eCLM_curvilinear

This repository shows the workflow for creating curvilinear surface and domain fields for eCLM simulations. The workflow follows the official clm-workflow but makes a few adaptions. 


## Cloning the necessary repositories

To follow the workflow it is necessary to clone:

```
git clone https://github.com/ESCOMP/CTSM.git
cd CTSM
git checkout release-clm5.0
git clone https://github.com/ESMCI/cime.git
```

The repository contains folders analog to the ones of CTSM and cime. So, you can add the files to the right folders.

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

There should already be netcdf files for your grid or you can creatte them according to Niklas Wagner's workflow for creating static files.
 
## Creation of mapping files

For the creation of the mapping files of CLM inputdata to our grid use mkmapdata/runscript_mkmapdata.sh. Adapt the script to your previously created SCRIP file, to your compute time project and to the path to the CLM mappingdata. The script is tailored to JURECA but can easily changed to JUWELS. If you don't have access to the CLM mappingdata you have to download it. Use:

```
wget --no-check-certificate -i  clm_mappingfiles.txt
```
Then start the creation of the weights with
```
sbatch runscript_mkmapdata.sh
```

## Creation of domain files

The CIME submodule under `cime/tools/mapping/gen_domain_files` generates the domain files for CLM. This repository contains a simplified version of `gen_domain` which is easier to compile on JSC machines and you do not need the CIME repository. To compile it go to  the `src/` directory with the loaded modules ifort, imkl, netCDF and netCDF-Fortran. Then compile with 

```
ifort -o ../gen_domain gen_domain.F90 -mkl -lnetcdff -lnetcdf
```

After the compilation you can execute `gen_domain` with $MAPFILE being of the mapping files created before and $GRIDNAME being a sting with the name of your grid. The choice of $MAPFILE does not influence the lat- and longitude values in the domain file but can influence the land/sea mask. 

```
./gen_domain -m $MAPFILE -o $GRIDNAME -l $GRIDNAME
```

The created domain file will later be modified.



## Creation of surface file

The surface creation tool is found under CTSM/tools/mksurfdata_map/. You have to compile it with make. Replace mksurfdat.F90 with the version found in this repository. The only difference is that 'regional' is set as a standard compared to global. The essential modules you need to load are intel and netCDF-Fortran. You still need to export(for jureca stage 2022 in this case)


```
export LIB_NETCDF=/p/software/jurecadc/stages/2022/software/netCDF-Fortran/4.5.3-GCCcore-11.2.0-serial/lib

export INC_NETCDF=/p/software/jurecadc/stages/2022/software/netCDF-Fortran/4.5.3-GCCcore-11.2.0-serial/include
```
After compilation execute

```
./mksurfdata.pl -r usrspec -usr_gname $GRIDNAME -usr_gdate $CDATE -l $CSMDATA -allownofile -y 2005 -hirespft
```
to create a real domain with hires pft. Again, you need to have set a $GRIDNAME, a current date $DATE in yymmdd and the path where the raw data of CLM is stored $CSMDATA. You have to download the data from https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/ if you have no access.

Also make sure that mksurdata and mkmdapdata have the same parent directory.

PS: There are many versions mksurfdata.pl in the CTSM github. Stick to the clm5-release version! Other versions use other mapping files and are not compatible with negative longitudes.

## Modification of the surface and domain file

The created surface and domain file have negative longitudes that CLM5 does not accept and inherently has no landmask. To modify the longitudes and to add a landmask use `mod_domain.sh` after inserting the paths to your files.

## Creation of forcing data from ERA5

A possible source of atmospheric forcing for CLM5 is ERA5. `prepare_ERA5.sh` prepares ERA as an input by changing names and modifying units. ERA5 has to be downloaded and regridded to your resolution beforehand.









