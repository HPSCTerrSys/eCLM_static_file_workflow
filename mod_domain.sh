#!/usr/bin/env bash

surface_file=/p/scratch/cjibg31/jibg3105/CESMDataRoot/InputData/lnd/clm2/surfdata_map/surfdata_EUR-0275_hist_78pfts_CMIP6_simyr2005_c230307.nc
domain_file=/p/scratch/cjibg31/jibg3105/CESMDataRoot/InputData/share/domains/EUR-0275/domain/domain.lnd.EUR-0275.230303.nc
#landmask_file=landmask.nc
ncap2 -O -s 'where(LONGXY<0) LONGXY=LONGXY+360' ${surface_file} temp.nc
mv temp.nc ${surface_file}

ncap2 -O -s 'where(xc<0) xc=xc+360' ${domain_file} temp.nc
ncap2 -O -s 'where(xv<0) xv=xv+360' temp.nc ${domain_file}

#ncrenam -v LANDMASK,mask -v FRAC,frac landmask_file

#ncks -A -v mask ${landmask_file} ${domain_file}

#ncks -A -v frac ${landmask_file} ${domain_file}




