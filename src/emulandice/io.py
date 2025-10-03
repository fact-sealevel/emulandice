"""Common storage and IO logic"""

import time

from netCDF4 import Dataset
import numpy as np


def WriteNetCDF(
    slr,
    targyears,
    baseyear,
    scenario,
    nsamps,
    pipeline_id,
    nc_filename: str,
    nc_description: str,
):
    rootgrp = Dataset(nc_filename, "w", format="NETCDF4")

    # Define Dimensions
    _ = rootgrp.createDimension("years", len(targyears))
    _ = rootgrp.createDimension("samples", nsamps)
    _ = rootgrp.createDimension("locations", 1)

    # Populate dimension variables
    year_var = rootgrp.createVariable("years", "i4", ("years",))
    samp_var = rootgrp.createVariable("samples", "i8", ("samples",))
    loc_var = rootgrp.createVariable("locations", "i8", ("locations",))
    lat_var = rootgrp.createVariable("lat", "f4", ("locations",))
    lon_var = rootgrp.createVariable("lon", "f4", ("locations",))

    # Create a data variable
    samps = rootgrp.createVariable(
        "sea_level_change",
        "f4",
        ("samples", "years", "locations"),
        zlib=True,
        complevel=4,
    )

    # Assign attributes
    rootgrp.description = nc_description
    rootgrp.history = "Created " + time.ctime(time.time())
    rootgrp.source = "FACTS: {0}. ".format(pipeline_id)
    rootgrp.baseyear = baseyear
    rootgrp.scenario = scenario
    samps.units = "mm"

    # Put the data into the netcdf variables
    year_var[:] = targyears
    samp_var[:] = np.arange(nsamps)
    samps[:, :, :] = slr[:, :, np.newaxis]
    lat_var[:] = np.inf
    lon_var[:] = np.inf
    loc_var[:] = -1

    return None
