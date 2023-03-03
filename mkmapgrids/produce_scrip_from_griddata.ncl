load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/esmf/ESMF_regridding.ncl" 
;
OutFileName = "SCRIP_EU3.nc"
;Adjust the filename/path to your gridfile and the variable names of lon lat if needed
;

p     = "/p/scratch/cjibg31/jibg3105/CESMDataRoot/InputData/share/domains/"

print(p + "EUR-0275_1600x1552_grid_inclbrz_v2.nc")
f     = addfile(p+"EUR-0275_1600x1552_grid_inclbrz_v2.nc", "r")
lat2d = f->lat                        
lon2d = f->lon
;
;
 
Opt                      = True
Opt@InterpMethod         = "conserve"     ; default conserve
Opt@ForceOverwrite       = True
Opt@PrintTimings         = True
;
curvilinear_to_SCRIP(OutFileName,lat2d,lon2d,Opt)


