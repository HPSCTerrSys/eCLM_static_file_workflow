#!/usr/bin/env bash
for year in 2017
do
for month in 01 #02 03 04 05 06 07 08 09 10 11 12 
do
days_per_month=$(cal ${month} ${year} | awk 'NF {DAYS = $NF}; END {print DAYS}')
for my_date in $(seq -w 1 ${days_per_month})
do
for time in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23
do
cdo sellonlatbox,-48,74,20,69 /p/fastdata/slmet/slmet111/met_data/ecmwf/era5/grib/2017/${month}/2017${month}${my_date}${time}_ml.grb cut_domain_${month}${my_date}${time}.grb

cdo sellevel,137 cut_domain_${month}${my_date}${time}.grb lower_level_${month}${my_date}${time}.grb
#cdo -t ecmwf -f nc4 copy lower_level_${month}${my_date}${time}.grb lower_level_${month}${my_date}${time}.nc
cdo -t ecmwf selname,t,u,v,q lower_level_${month}${my_date}${time}.grb variables_lower_level_${month}${my_date}${time}.grb


done
done
cdo merge  variables_lower_level_*.grb meteocloud_${month}.grb
rm variables_lower_level_*.grb cut_domain* lower_level_* 
cdo -t ecmwf -f nc4 copy meteocloud_${month}.grb meteocloud_${month}.nc
done
done
