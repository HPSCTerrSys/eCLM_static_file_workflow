#!/usr/bin/env bash

for year in 2017
do
for month in 01 #02 03 04 05 06 07 08 09 10 11 12 
do

cdo expr,'WIND=sqrt(u^2+v^2)' meteocloud_${year}_${month}.nc ${year}_temp.nc

cdo -f nc4c const,10,download${year}${month}.nc.regrid.nc ${year}_const.nc

ncpdq -U download${year}${month}.nc.regrid.nc ${year}_temp2.nc

cdo merge ${year}_const.nc ${year}_temp2.nc ${year}_temp.nc ${year}_temp3.nc

ncrename -v sp,PSRF -v msdwswrf,FSDS -v msdwlwrf,FLDS -v mtpr,PRECTmms -v const,ZBOT -v t,TBOT -v q,SHUM ${year}_temp3.nc

ncap2 -O -s 'where(FSDS<0.) FSDS=0' ${year}_${month}.nc

ncatted -O -a units,ZBOT,m,c,"m" ${year}_${month}.nc

rm ${year}_temp*nc ${year}_const.nc

done
done
