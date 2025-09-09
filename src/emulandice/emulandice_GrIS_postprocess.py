import numpy as np
import time
import argparse
from emulandice.read_locationfile import ReadLocationFile
from emulandice.AssignFP import AssignFP

import xarray as xr
import dask.array as da

""" emulandice_postprocess_GrIS.py

"""


def emulandice_postprocess_GrIS(
    *,
    my_data: dict,
    locationfile,
    chunksize,
    pipeline_id,
    fprint_gis_file,
    output_lslr_file: str,
):
    gissamps = my_data["gissamps"]
    targyears = my_data["targyears"]
    scenario = my_data["scenario"]
    baseyear = my_data["baseyear"]
    preprocess_infile = my_data["preprocess_infile"]

    # Load the site locations
    (_, site_ids, site_lats, site_lons) = ReadLocationFile(locationfile)

    # Get some dimension data from the loaded data structures
    nsamps = gissamps.shape[0]

    # Get the fingerprints for all sites from all ice sheets
    gisfp = da.array(AssignFP(fprint_gis_file, site_lats, site_lons))

    # Rechunk the fingerprints for memory
    gisfp = gisfp.rechunk(chunksize)

    # Apply the fingerprints to the projections
    gissl = np.multiply.outer(gissamps, gisfp)

    # Define the missing value for the netCDF files
    nc_missing_value = np.nan  # np.iinfo(np.int16).min

    # Create the xarray data structures for the localized projections
    ncvar_attributes = {
        "description": "Local SLR contributions from icesheet according to emulandice GrIS workflow",
        "history": "Created " + time.ctime(time.time()),
        "source": "SLR Framework: emulandice workflow",
        "scenario": scenario,
        "baseyear": baseyear,
        "preprocess_infile": preprocess_infile,
    }

    gis_out = xr.Dataset(
        {
            "sea_level_change": (
                ("samples", "years", "locations"),
                gissl,
                {"units": "mm", "missing_value": nc_missing_value},
            ),
            "lat": (("locations"), site_lats),
            "lon": (("locations"), site_lons),
        },
        coords={
            "years": targyears,
            "locations": site_ids,
            "samples": np.arange(nsamps),
        },
        attrs=ncvar_attributes,
    )

    # Write the netcdf output files
    gis_out.to_netcdf(
        output_lslr_file,
        encoding={
            "sea_level_change": {
                "dtype": "f4",
                "zlib": True,
                "complevel": 4,
                "_FillValue": nc_missing_value,
            }
        },
    )

    return None


if __name__ == "__main__":
    # Initialize the command-line argument parser
    parser = argparse.ArgumentParser(
        description="Run the post-processing stage for the emulandice GrIS SLR projection workflow",
        epilog="Note: This is meant to be run as part of the Framework for the Assessment of Changes To Sea-level (FACTS)",
    )

    # Define the command line arguments to be expected
    parser.add_argument(
        "--locationfile",
        help="File that contains name, id, lat, and lon of points for localization",
        default="location.lst",
    )
    parser.add_argument(
        "--chunksize",
        help="Number of locations to process at a time [default=50]",
        type=int,
        default=50,
    )
    parser.add_argument(
        "--pipeline_id", help="Unique identifier for this instance of the module"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Run the postprocessing for the parameters specified from the command line argument
    emulandice_postprocess_GrIS(args.locationfile, args.chunksize, args.pipeline_id)

    # Done
    exit()
