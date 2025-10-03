import numpy as np
import os
import sys
import argparse
import re
from scipy.stats import truncnorm

from emulandice.r_helper import run_emulandice
from emulandice.io import WriteNetCDF


def ExtractProjections(emulandice_file):
    # Initialize
    # ice_sources = []
    # regions = []
    years = []
    samples = []
    sles = []

    # Open the emulandice_file for reading
    with open(emulandice_file, "r") as f:
        # Skip the header line
        _ = f.readline()

        # Load the rest of the data
        for line in f:
            lp = re.split(",", line)
            # ice_sources.append(lp[0])
            # regions.append(lp[1])
            years.append(int(lp[2]))
            samples.append(int(lp[3]))
            sles.append(float(lp[7]))

    # Convert to numpy arrays
    # ice_sources = np.array(ice_sources)
    # regions = np.array(regions)
    years = np.array(years)
    samples = np.array(samples)
    sles = np.array(sles)

    # Extract the target years
    targyears = np.unique(years)
    unique_samples = np.unique(samples)

    # Initialize the return data structure
    ret_data = np.full((len(unique_samples), len(targyears)), np.nan)

    # Loop over all the entries
    for i in np.arange(len(sles)):
        # This sample
        this_year = years[i]
        this_sample = samples[i]
        this_sle = sles[i]

        # Which index will this entry be filling?
        year_idx = np.flatnonzero(targyears == this_year)
        sample_idx = this_sample - 1

        # Put the data into the return data structure
        ret_data[sample_idx, year_idx] = this_sle * 10.0  # Convert cm to mm

    # Done
    return (ret_data, targyears)


def emulandice_project_GrIS(
    pipeline_id,
    preprocess_data: dict,
    fit_data: dict,
    output_dir,
    output_gslr_file: str,
    icesource="GrIS",
):
    preprocess_infile = preprocess_data["infile"]
    baseyear = preprocess_data["baseyear"]
    scenario = preprocess_data["scenario"]
    nsamps = preprocess_data["nsamps"]

    trend_mean = fit_data["trend_mean"]
    trend_sd = fit_data["trend_sd"]

    # Run the module using the FACTS forcing data

    emulandice_dataset = preprocess_data["facts_data_file"]
    run_emulandice(
        emulandice_dataset=emulandice_dataset,
        nsamps=nsamps,
        icesource=icesource,
        outdir=output_dir,
    )

    # Get the output from the emulandice run
    emulandice_file = os.path.join(output_dir, "projections_FAIR_FACTS.csv")
    samples, targyears = ExtractProjections(emulandice_file)

    # Make sure we get the number of samples we expected
    if nsamps != samples.shape[0]:
        raise Exception(
            "Number of SLC projections does not match number of temperature trajectories: {} != {}".format(
                samples.shape[0], nsamps
            )
        )

    # Generate samples for trends correlated among ice sheets
    # Note: Keep seed hard-coded and matched with AIS module within emulandice module set
    rng = np.random.default_rng(8071)
    trend_q = rng.random(nsamps)

    # Calculate the trend contributions over time for each ice sheet component
    gis_trend = (
        truncnorm.ppf(
            trend_q, a=0, b=99999, loc=trend_mean["GIS"], scale=trend_sd["GIS"]
        )[:, np.newaxis]
        * (targyears - baseyear)[np.newaxis, :]
    )

    # Add the trend to the samples
    samples += gis_trend

    # Save the global projections to a pickle
    output = {
        "gissamps": samples,
        "targyears": targyears,
        "scenario": scenario,
        "baseyear": baseyear,
        "preprocess_infile": preprocess_infile,
    }

    # Write the global projections to netcdf files
    WriteNetCDF(
        samples,
        targyears,
        baseyear,
        scenario,
        nsamps,
        pipeline_id,
        nc_filename=output_gslr_file,
        nc_description="Global SLR contribution from Greenland using the emulandice module",
    )

    return output


if __name__ == "__main__":
    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description="Run the projection stage for the emulandice GrIS SLR projection workflow",
        epilog="Note: This is meant to be run as part of the Framework for the Assessment of Changes To Sea-level (FACTS)",
    )

    # Add arguments for the resource and experiment configuration files
    parser.add_argument(
        "--pipeline_id",
        help="Unique identifier for this instance of the module",
        required=True,
    )

    # Parse the arguments
    args = parser.parse_args()

    # Run the preprocessing
    emulandice_project_GrIS(args.pipeline_id)

    # Done
    sys.exit()
