"""
Logic for the CLI.
"""

import click

from emulandice.emulandice_preprocess import emulandice_preprocess
from emulandice.emulandice_AIS_fit import emulandice_fit_AIS
from emulandice.emulandice_AIS_project import emulandice_project_AIS
from emulandice.emulandice_AIS_postprocess import emulandice_postprocess_AIS
from emulandice.emulandice_GrIS_fit import emulandice_fit_GrIS
from emulandice.emulandice_GrIS_project import emulandice_project_GrIS
from emulandice.emulandice_GrIS_postprocess import emulandice_postprocess_GrIS
from emulandice.emulandice_glaciers_fit import emulandice_fit_glaciers
from emulandice.emulandice_glaciers_project import emulandice_project_glaciers
from emulandice.emulandice_glaciers_postprocess import emulandice_postprocess_glaciers


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main():
    """
    The emulandice family of modules wrap around the Edwards et al. (2021) Gaussian process emulators of the ISMIP6 and GlacierMIP2 models.
    """
    pass


@main.command
@click.option(
    "--input-data-file",
    envvar="EMULANDICE_INPUT_DATA_FILE",
    help="Full path for temperature trajectory input file.",
    type=str,
    required=True,
)
@click.option(
    "--pipeline-id",
    envvar="EMULANDICE_PIPELINE_ID",
    help="Unique identifier for this instance of the module.",
    required=True,
)
@click.option(
    "--scenario",
    envvar="EMULANDICE_SCENARIO",
    help="SSP scenario (i.e ssp585).",
    default="ssp585",
)
@click.option(
    "--output-gslr-file",
    envvar="EMULANDICE_OUTPUT_GSLR_FILE",
    help="Path to write output global SLR file.",
    required=True,
    type=str,
)
@click.option(
    "--output-lslr-file",
    envvar="EMULANDICE_OUTPUT_LSLR_FILE",
    help="Path to write output local SLR file.",
    required=True,
    type=str,
)
@click.option(
    "--baseyear",
    envvar="EMULANDICE_BASEYEAR",
    help="Base year to which projections should be referenced.",
    default=2005,
)
@click.option(
    "--chunksize",
    envvar="EMULANDICE_CHUNKSIZE",
    help="Number of locations to process at a time [default=50].",
    default=50,
)
@click.option(
    "--location-file",
    envvar="EMULANDICE_LOCATION_FILE",
    help="File containing name, id, lat, and lon of points for localization.",
    type=str,
    required=True,
)
@click.option(
    "--output-gslr-eais-file",
    envvar="EMULANDICE_OUTPUT_GSLR_EAIS_FILE",
    help="Path to write output global SLR EAIS file.",
    type=str,
    default=None,
)
@click.option(
    "--output-gslr-wais-file",
    envvar="EMULANDICE_OUTPUT_GSLR_WAIS_FILE",
    help="Path to write output global SLR WAIS file.",
    type=str,
    default=None,
)
@click.option(
    "--output-gslr-pen-file",
    envvar="EMULANDICE_OUTPUT_GSLR_PEN_FILE",
    help="Path to write output global SLR PEN file.",
    type=str,
    default=None,
)
@click.option(
    "--output-lslr-eais-file",
    envvar="EMULANDICE_OUTPUT_LSLR_EAIS_FILE",
    help="Path to write output local SLR EAIS file.",
    type=str,
    default=None,
)
@click.option(
    "--output-lslr-wais-file",
    envvar="EMULANDICE_OUTPUT_LSLR_WAIS_FILE",
    help="Path to write output local SLR WAIS file.",
    type=str,
    default=None,
)
def ais(
    input_data_file,
    pipeline_id,
    scenario,
    output_gslr_file,
    output_lslr_file,
    baseyear,
    chunksize,
    location_file,
    output_gslr_eais_file,
    output_gslr_wais_file,
    output_gslr_pen_file,
    output_lslr_eais_file,
    output_lslr_wais_file,
):
    """
    Project sealevel rise from Antarctic Ice Sheet (AIS)
    """
    click.echo("Hello from emulandice AIS")
    preprocessed = emulandice_preprocess(
        input_data_file, baseyear, pipeline_id, scenario
    )
    fitted = emulandice_fit_AIS(pipeline_id)
    projected = emulandice_project_AIS(
        pipeline_id,
        preprocess_data=preprocessed,
        fit_data=fitted,
        output_gslr_file=output_gslr_file,
        output_eais_file=output_gslr_eais_file,
        output_wais_file=output_gslr_wais_file,
        output_pen_file=output_gslr_pen_file,
    )
    emulandice_postprocess_AIS(
        my_data=projected,
        locationfile=location_file,
        chunksize=chunksize,
        pipeline_id=pipeline_id,
        output_lslr_file=output_lslr_file,
        output_eais_file=output_lslr_eais_file,
        output_wais_file=output_lslr_wais_file,
    )


@main.command
@click.option(
    "--input-data-file",
    envvar="EMULANDICE_INPUT_DATA_FILE",
    help="Full path for temperature trajectory input file.",
    type=str,
    required=True,
)
@click.option(
    "--pipeline-id",
    envvar="EMULANDICE_PIPELINE_ID",
    help="Unique identifier for this instance of the module.",
    required=True,
)
@click.option(
    "--scenario",
    envvar="EMULANDICE_SCENARIO",
    help="SSP scenario (i.e ssp585).",
    default="ssp585",
)
@click.option(
    "--baseyear",
    envvar="EMULANDICE_BASEYEAR",
    help="Base year to which projections should be referenced.",
    default=2005,
)
@click.option(
    "--chunksize",
    envvar="EMULANDICE_CHUNKSIZE",
    help="Number of locations to process at a time [default=50].",
    default=50,
)
@click.option(
    "--location-file",
    envvar="EMULANDICE_LOCATION_FILE",
    help="File containing name, id, lat, and lon of points for localization.",
    type=str,
    required=True,
)
def gris(input_data_file, scenario, pipeline_id, baseyear, chunksize, location_file):
    """
    Project sealevel rise from Greenland Ice Sheet (GrIS)
    """
    click.echo("Hello from emulandice GrIS")

    preprocessed = emulandice_preprocess(
        input_data_file, baseyear, pipeline_id, scenario
    )
    emulandice_fit_GrIS(pipeline_id)
    emulandice_project_GrIS(pipeline_id)
    emulandice_postprocess_GrIS(location_file, chunksize, pipeline_id)


@main.command
@click.option(
    "--input-data-file",
    envvar="EMULANDICE_INPUT_DATA_FILE",
    help="Full path for temperature trajectory input file.",
    type=str,
    required=True,
)
@click.option(
    "--pipeline-id",
    envvar="EMULANDICE_PIPELINE_ID",
    help="Unique identifier for this instance of the module.",
    required=True,
)
@click.option(
    "--scenario",
    envvar="EMULANDICE_SCENARIO",
    help="SSP scenario (i.e ssp585).",
    default="ssp585",
)
@click.option(
    "--baseyear",
    envvar="EMULANDICE_BASEYEAR",
    help="Base year to which projections should be referenced.",
    default=2005,
)
@click.option(
    "--chunksize",
    envvar="EMULANDICE_CHUNKSIZE",
    help="Number of locations to process at a time [default=50].",
    default=50,
)
@click.option(
    "--location-file",
    envvar="EMULANDICE_LOCATION_FILE",
    help="File containing name, id, lat, and lon of points for localization.",
    type=str,
    required=True,
)
def glaciers(
    input_data_file, pipeline_id, scenario, baseyear, chunksize, location_file
):
    """
    Project sealevel rise from glaciers
    """
    click.echo("Hello from emulandice glaciers")

    preprocessed = emulandice_preprocess(
        input_data_file, baseyear, pipeline_id, scenario
    )
    emulandice_fit_glaciers(pipeline_id)
    emulandice_project_glaciers(pipeline_id)
    emulandice_postprocess_glaciers(location_file, chunksize, pipeline_id)
