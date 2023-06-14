#!/usr/bin/env bash

for month in 01 #02 03 04 05 06 07 08 09 10 11 12 
do

cdo expr,'WIND=sqrt(u^2+v^2)' meteocloud_${month}.nc temp.nc

cdo -f nc4c const,10,download${month}.nc.regrid.nc const.nc

ncpdq -U download${month}.nc.regrid.nc temp2.nc

cdo merge const.nc temp2.nc temp.nc temp3.nc

ncrename -v sp,PSRF -v msdwswrf,FSDS -v msdwlwrf,FLDS -v mtpr,PRECTmms -v const,ZBOT -v t,TBOT -v q,SHUM temp3.nc

ncap2 -O -s 'where(FSDS<0.) FSDS=0' 2017_${month}.nc

ncatted -O -a units,ZBOT,m,c,"m" 2017_${month}.nc

rm temp*

done
