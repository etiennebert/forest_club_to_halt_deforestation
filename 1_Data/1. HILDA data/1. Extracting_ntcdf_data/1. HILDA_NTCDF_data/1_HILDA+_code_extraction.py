# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 00:02:20 2023

@author: etber
"""
import numpy as np
import pandas as pd
import netCDF4

# We define two configurations:
# 1) 'States': netCDF file path, variable name, filter codes [22, 23, 24, 33]
# 2) 'Transition': netCDF file path, variable name, filter codes [2222, 2323, ..., 5555]
files = [
    {
        "prefix": "States", #Land Use/Cover categories (**__states__**)
        "nc_path": "hildaplus_GLOB-2-1-crop_states.nc",
        "var_name": "LULC_states",
        "filter_codes": [22, #22 annual crops 
                         23, #23 tree crops 
                         24, #24 agroforestry  
                         33] #33 pasture/rangeland    
    },
    {
        "prefix": "Transition", 
        "nc_path": "hildaplus_GLOB-2-1-crop_transitions.nc", #Transitions between Land Use/Cover categories (**__transitions__**) with 4-digit codes (XXYY, where XX is LULC category of previous year and YY is LULC category of reference year)
        "var_name": "LULC_transitions",
        "filter_codes": [
            2222, # annual crops (stable)
            2323, # tree crops (stable)
            2424, # agroforestery (stable) 
            3333, # pasture (stable)
            4022, 4023, 4024, 4033, 4040, # Forest to annual crops, tree crops, agroforestery, pasture and stable
            4122, 4123, 4124, 4133, 4141, # etc
            4222, 4223, 4224, 4233, 4242,
            4322, 4323, 4324, 4333, 4343,
            4422, 4423, 4424, 4433, 4444,
            4522, 4523, 4524, 4533, 4545,
            5522, 5523, 5524, 5533, 5555
        ]
    }
]

# Bounding boxes for your three regions
list_lat_min = [-60, -30, -15]
list_lat_max = [ 13,  20,  15]
list_lon_min = [-80, -20,  90]
list_lon_max = [-35,  60, 150]
list_name    = ["South_America", "Africa", "South_East_Asia"]

def slicer(nc_dataset, year, lat_min, lat_max, lon_min, lon_max, var_name="LULC_states"):
    """
    Extract a subset of the LULC data for a given year and bounding box 
    from an open netCDF dataset. 
    """
    # Read arrays
    time = nc_dataset.variables['time'][:]
    lat  = nc_dataset.variables['latitude'][:]
    lon  = nc_dataset.variables['longitude'][:]
    lulc_var = nc_dataset.variables[var_name]

    # Find index of the requested year
    time_idx = np.where(time == year)[0]
    if len(time_idx) == 0:
        raise ValueError(f"Year {year} not found in dataset.")
    time_idx = time_idx[0]

    # Identify the lat/lon indices for slicing
    lat_indices = np.where((lat >= lat_min) & (lat <= lat_max))[0]
    lon_indices = np.where((lon >= lon_min) & (lon <= lon_max))[0]

    a, b = min(lat_indices), max(lat_indices) + 1
    c, d = min(lon_indices), max(lon_indices) + 1

    # Slice the lulc data: shape is (time, lat, lon)
    lulc_subset = lulc_var[time_idx, a:b, c:d]

    # Convert to DataFrame
    lat_subset = lat[a:b]
    lon_subset = lon[c:d]
    df = pd.DataFrame(lulc_subset, index=lat_subset, columns=lon_subset)

    # Insert an "id" column to help with melting
    df.insert(0, "id", lat_subset, True)
    return df

# Main processing loop
for file_conf in files:
    prefix       = file_conf["prefix"]          # "States" or "Transition"
    nc_path      = file_conf["nc_path"]         # netCDF path
    var_name     = file_conf["var_name"]        # e.g., "LULC_states"
    filter_codes = file_conf["filter_codes"]    # list of codes to keep

    # Open the netCDF dataset
    with netCDF4.Dataset(nc_path, 'r') as nc_dataset:
        for year in range(2008, 2020):
            for i in range(3):
                # Slice the data for (year, bounding box)
                df_sliced = slicer(
                    nc_dataset=nc_dataset,
                    year=year,
                    lat_min=list_lat_min[i],
                    lat_max=list_lat_max[i],
                    lon_min=list_lon_min[i],
                    lon_max=list_lon_max[i],
                    var_name=var_name
                )

                # Melt from wide to long format
                df_unpivot = pd.melt(df_sliced, id_vars='id')
                df_unpivot.columns = ["latitude", "longitude", "LULC"]

                # Filter out rows that do not match desired LULC codes
                df_unpivot = df_unpivot.loc[df_unpivot["LULC"].isin(filter_codes)]

                # Insert the year column
                df_unpivot.insert(0, "year", year, True)

                # Construct output filename
                # e.g., "HILDA_V2_1_All_States_South_America_2008.csv"
                output_filename = f"HILDA_V2_1_Selected_{prefix}_{list_name[i]}_{year}.csv"

                # Save to CSV
                df_unpivot.to_csv(output_filename, index=False, header=True)

    print(f"Done processing {prefix} data from '{nc_path}'.")
