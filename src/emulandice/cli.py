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
def ais(input_data_file, pipeline_id, baseyear, chunksize, location_file):
    """
    Project sealevel rise from Antarctic Ice Sheet (AIS)
    """
    click.echo("Hello from emulandice AIS")
    emulandice_preprocess(input_data_file, baseyear, pipeline_id)
    emulandice_fit_AIS(pipeline_id)
    emulandice_project_AIS(pipeline_id)
    emulandice_postprocess_AIS(location_file, chunksize, pipeline_id)


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
def gris(input_data_file, pipeline_id, baseyear, chunksize, location_file):
    """
    Project sealevel rise from Greenland Ice Sheet (GrIS)
    """
    click.echo("Hello from emulandice GrIS")
    emulandice_preprocess(input_data_file, baseyear, pipeline_id)
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
def glaciers(input_data_file, pipeline_id, baseyear, chunksize, location_file):
    """
    Project sealevel rise from glaciers
    """
    click.echo("Hello from emulandice glaciers")
    emulandice_preprocess(input_data_file, baseyear, pipeline_id)
    emulandice_fit_glaciers(pipeline_id)
    emulandice_project_glaciers(pipeline_id)
    emulandice_postprocess_glaciers(location_file, chunksize, pipeline_id)
