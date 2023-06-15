#!/usr/bin/env bash

##This scripts replaces variables in the surface file of CLM5 with variables from a CLM3_5 file. This is easily doable for the variables handeled with nco, the pft-percentages need a special treatment. Because they are splittet into crop and natural pfts in CLM5.
##It is still under discussion whether the soillevels are identical but both CLM versions have 10 levles in the surface file. LAI and other plant parameters can only be replaced like this if there are the same number of them in both datasets. 

CLM_3_5_path=/p/scratch/cslts/hartick1/temp/surfdata_CLM_EUR-11_TSMP_FZJ-IBG3_CLMPFLDomain_444x432.nc
CLM5_path=/p/scratch/cslts/hartick1/temp/surfdata_EUR-11_hist_16pfts_Irrig_CMIP6_simyr2000_c230216.nc


ncks -A -v PCT_SAND,PCT_CLAY,MONTHLY_LAI,MONTHLY_SAI,MONTHLY_HEIGHT_TOP,MONTHLY_HEIGHT_BOT $CLM_3_5_path $CLM5_path

python replace.py $CLM_3_5_path $CLM5_path
