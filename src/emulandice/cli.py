"""
Logic for the CLI.
"""

import click


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main():
    """
    The emulandice family of modules wrap around the Edwards et al. (2021) Gaussian process emulators of the ISMIP6 and GlacierMIP2 models.
    """
    pass


@main.command
def ais():
    """
    Project sealevel rise from Antarctic Ice Sheet (AIS)
    """
    click.echo("Hello from emulandice AIS")


@main.command
def gris():
    """
    Project sealevel rise from Greenland Ice Sheet (GrIS)
    """
    click.echo("Hello from emulandice GrIS")


@main.command
def glaciers():
    """
    Project sealevel rise from glaciers
    """
    click.echo("Hello from emulandice glaciers")
