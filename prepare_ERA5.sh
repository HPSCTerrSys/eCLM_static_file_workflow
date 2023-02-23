#!/usr/bin/env bash

for month in 01 02 03 04 05 06 07 08 09 10 11 12 
do
ncrename -v d2m,TDEW -v t2m,TBOT -v sp,PSRF -v ssrd,FSDS -v strd,FLDS -v tp,PRECTmms download${month}.nc.regrid.nc
cdo expr,'WIND=sqrt(u10^2+v10^2)' download${month}.nc.regrid.nc temp.nc


cdo selname,FSDS,FLDS download${month}.nc.regrid.nc temp_energy.nc

cdo selname,PRECTmms download${month}.nc.regrid.nc temp_rain.nc

cdo delname,FLDS,FSDS,PRECTmms,u10,v10 download${month}.nc.regrid.nc temp2.nc

cdo -b F64 divc,3600 temp_energy.nc temp_energy_watt.nc

ncap2 -s 'where(FSDS<0.) FSDS=0' temp_energy_watt.nc -O temp_energy_watt2.nc

ncatted -O -a units,FSDS,m,c,"W m-2" temp_energy_watt2.nc

ncatted -O -a units,FLDS,m,c,"W m-2" temp_energy_watt2.nc

cdo -b F64 -mulc,1000 -divc,3600 -chunit,m,mms**-1 temp_rain.nc temp_rain_mms.nc

cdo merge temp_energy_watt2.nc temp_rain_mms.nc temp2.nc temp.nc temp3.nc

ncpdq -U temp3.nc 2017-${month}.nc
rm temp3

done
