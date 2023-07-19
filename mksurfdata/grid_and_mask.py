import xarray as xr
import numpy as np
import sys

#path_clm_3_5 = sys.argv[1]
#path_clm_5 = sys.argv[2]


clm_3_5_source = xr.open_dataset("/p/scratch/cslts/hartick1/SDLTS_EUR-0011_ECMWF-ERA5_evaluation_r1i1p1_FZJ-COSMO5-01-CLM3-5-0-ParFlow3-12-0_vAdgrid/geo/TSMP_EUR-0011/clm/fracdata_CLM_EUR-0011_TSMP_FZJ-IBG3_CLMPFLDomain_3994x3874.nc")
cosmo_source = xr.open_dataset("/p/scratch/cslts/hartick1/TSMP_EUR-0275/static.resource/10_GatherCLM35/griddata_COSMO_EUR-0275_TSMP_FZJ-IBG3_COSMODomain_1600x1552.nc")

mask_clm = clm_3_5_source['LANDMASK']


grid_pfl_lon = clm_3_5_source['LONGXY']
grid_pfl_lat = clm_3_5_source['LATIXY']
grid_clm_lon = grid_pfl_lon.copy()
grid_clm_lat = grid_pfl_lat.copy()


grid_pfl_lon.name = "gpfl.lon"
grid_pfl_lat.name = "gpfl.lat"
ds_pfl_lon = xr.Dataset({grid_pfl_lon.name: (['x_gpfl','y_gpfl'], grid_pfl_lon.data)})
ds_pfl_lat = xr.Dataset({grid_pfl_lat.name: (['x_gpfl','y_gpfl'], grid_pfl_lat.data)})
ds_pfl_lon.to_netcdf('grids.nc', mode="w")
ds_pfl_lat.to_netcdf('grids.nc', mode="a")


lon_flatten = grid_clm_lon.values.flatten()
lat_flatten = grid_clm_lat.values.flatten()

lon_flatten_ds = xr.Dataset({'gclm.lon': (['x_gclm'], lon_flatten)})
lat_flatten_ds = xr.Dataset({'gclm.lat': (['x_gclm'], lat_flatten)})
lon_flatten_ds.to_netcdf('grids.nc',mode="a")
lat_flatten_ds.to_netcdf('grids.nc',mode="a")




grid_pfl_lone = clm_3_5_source['LONE']
grid_pfl_lonw = clm_3_5_source['LONW']
pfl_lon_sta = xr.concat([grid_pfl_lone, grid_pfl_lonw, grid_pfl_lonw, grid_pfl_lone], dim='crn_gpfl')
pfl_lon_sta.name = 'gpfl.clo'
ds_pfl_lon_sta = xr.Dataset({pfl_lon_sta.name: (['crn_gpfl','x_gpfl','y_gpfl'], pfl_lon_sta.data)})
ds_pfl_lon_sta.to_netcdf('grids.nc', mode="a")

grid_clm_lone = grid_pfl_lone.values.flatten() 
grid_clm_lonw = grid_pfl_lonw.values.flatten()
#grid_clm_lone = grid_pfl_lone.reduce(np.ravel)
#grid_clm_lonw = grid_pfl_lonw.reduce(np.ravel)
#clm_lon_sta = xr.concat([grid_clm_lone, grid_clm_lonw, grid_clm_lonw, grid_clm_lone], dim='crn_gclm')
clm_lon_sta = xr.Dataset({"gclm.clo": (["crn_gclm","x_gclm"], [grid_clm_lone, grid_clm_lonw, grid_clm_lonw, grid_clm_lone])})
#clm_lon_sta.name = 'gclm.clo'
#ds_clm_lon_sta = xr.Dataset({clm_lon_sta.name: ds_clm_lon_sta})
clm_lon_sta.to_netcdf('grids.nc', mode="a")

grid_pfl_lats = clm_3_5_source['LATS']
grid_pfl_latn = clm_3_5_source['LATN']
pfl_lat_sta = xr.concat([grid_pfl_lats, grid_pfl_lats, grid_pfl_latn, grid_pfl_latn], dim='crn_gpfl')
pfl_lat_sta.name = 'gpfl.cla'
ds_pfl_lat_sta = xr.Dataset({pfl_lat_sta.name: (['crn_gpfl','x_gpfl','y_gpfl'], pfl_lat_sta.data)})
ds_pfl_lat_sta.to_netcdf('grids.nc', mode="a")

grid_clm_lats = grid_pfl_lats.values.flatten()
grid_clm_latn = grid_pfl_latn.values.flatten()
#clm_lat_sta = xr.concat([grid_clm_lats, grid_clm_lats, grid_clm_latn, grid_clm_latn], dim='crn_gclm')
clm_lat_sta = xr.Dataset({"gclm.cla": (["crn_gclm","x_gclm"], [grid_clm_lats, grid_clm_lats, grid_clm_latn, grid_clm_latn])})
#clm_lat_sta.name = 'gclm.cla'
#ds_clm_lat_sta = xr.Dataset({clm_lat_sta.name: clm_lat_sta})
clm_lat_sta.to_netcdf('grids.nc', mode="a")



#CLM/PFL mask

idx_zero = mask_clm == 0
idx_one = mask_clm == 1

new_clm_mask = mask_clm.copy()
new_clm_mask.values[idx_zero] = 1
new_clm_mask.values[idx_one] = 0

new_clm_mask.name = 'gpfl.msk'
new_clm_mask_ds = xr.Dataset({new_clm_mask.name: (['x_gpfl','y_gpfl'], new_clm_mask.data)})
new_clm_mask_ds.to_netcdf("masks.nc", mode="w")

new_clm_mask2 = new_clm_mask_ds['gpfl.msk'].values.flatten()

new_clm_mask2 = xr.Dataset({'gclm.msk': (['x_gclm'], new_clm_mask2)})

new_clm_mask2.to_netcdf('masks.nc', mode="a")



##COSMO grid

mask_cos = cosmo_source['LANDMASK']

idx_zero = mask_cos == 0
idx_one = mask_cos == 1

new_cos_mask = mask_cos.copy()
new_cos_mask.values[idx_zero] = 1
new_cos_mask.values[idx_one] = 0

new_cos_mask.name = 'gcos.msk'
new_cos_mask_ds = xr.Dataset({new_cos_mask.name: (['x_gcos','y_gcos'],new_cos_mask.data)})
new_cos_mask_ds.to_netcdf("masks.nc", mode="a")



grid_cos_lon = cosmo_source['LONGXY']
grid_cos_lat = cosmo_source['LATIXY']
grid_cos_lon.name = "gcos.lon"
grid_cos_lat.name = "gcos.lat"
ds_cos_lon = xr.Dataset({grid_cos_lon.name: (['x_gcos','y_gcos'], grid_cos_lon.data)})
ds_cos_lat = xr.Dataset({grid_cos_lat.name: (['x_gcos','y_gcos'], grid_cos_lat.data)})
ds_cos_lon.to_netcdf('grids.nc', mode="a")
ds_cos_lat.to_netcdf('grids.nc', mode="a")


grid_cos_lone = cosmo_source['LONE']
grid_cos_lonw = cosmo_source['LONW']

cos_lon_sta = xr.concat([grid_cos_lone, grid_cos_lonw, grid_cos_lonw, grid_cos_lone], dim='crn_gcos')
cos_lon_sta.name = 'gcos.clo'
ds_cos_lon_sta = xr.Dataset({cos_lon_sta.name: (['crn_gcos','x_gcos','y_gcos'],cos_lon_sta.data)})
ds_cos_lon_sta.to_netcdf('grids.nc', mode="a")


grid_cos_lats = cosmo_source['LATS']
grid_cos_latn = cosmo_source['LATN']

cos_lat_sta = xr.concat([grid_cos_lats, grid_cos_lats, grid_cos_latn, grid_cos_latn], dim='crn_gcos')
cos_lat_sta.name = 'gcos.cla'
ds_cos_lon_sta = xr.Dataset({cos_lat_sta.name: (['crn_gcos','x_gcos','y_gcos'],cos_lat_sta.data)})
ds_cos_lon_sta.to_netcdf('grids.nc', mode="a")





#mask_clm.to_netcdf('masks.nc')

#pft_3_5 = pft_3_5.to_numpy()


#pft_natural = pft_3_5[0:15,:,:]
#cft = pft_3_5[15:,:,:]


#clm5_dest = xr.open_dataset(path_clm_5, mode='a')

#clm5_dest["PCT_NAT_PFT"]=(['natpft', 'lsmlat', 'lsmlon'],  pft_natural)
#clm5_dest["PCT_CFT"]=(['cft', 'lsmlat', 'lsmlon'],  cft)

#clm5_dest.to_netcdf(path_clm_5)


clm_3_5_source.close()
cosmo_source.close()
