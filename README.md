# emulandice

Application projecting sea-level change from ice following the Gaussian process emulators of the ISMIP6 and GlacierMIP2 models described in Edwards et al. (2021).

## Example

This application can run on projected global surface air temperature data. For example, you can use the output `gsat.nc` file from the [the fair model container](https://github.com/facts-org/fair-temperature). Additional input data is also needed.

First, create a new directory and download required input data and prepare for the run, like

```shell
mkdir -p ./data/input

curl -sL https://zenodo.org/record/7478192/files/grd_fingerprints_data.tgz | tar -zx -C ./data/input

echo "New_York	12	40.70	-74.01" > ./data/input/location.lst

mkdir -p ./data/output
```

With using fair output as an example, drop the output `gsat.nc` file into `./data/input`.

Now run the containter, for example with Docker, like

```shell
docker run --rm \
  -v ./data/input:/input/:ro \
  -v ./data/output:/output \
  ghcr.io/facts-org/emulandice:latest ais \
  --pipeline-id=1234 \
  --fprint-wais-file="/input/FPRINT/fprint_wais.nc" \
  --fprint-eais-file="/input/FPRINT/fprint_eais.nc" \
  --input-data-file="/input/gsat.nc" \
  --location-file="/input/location.lst" \
  --output-gslr-file="/output/gslr.nc" \
  --output-lslr-file="/output/lslr.nc"
```

If the run is successful, the output projection will appear in `./data/output`. The `ais` subcommand we used here means we projected changes in the Antarctic ice sheet.

> [!TIP]
> For this example we use `ghcr.io/facts-org/emulandice:latest`. We do not recommend using `latest` for production runs because it is not reproducible. Instead, use a tag for a specific version of the image or an image's digest hash. You can find tagged image versions and digests [here](https://github.com/facts-org/emulandice/pkgs/container/emulandice).

Alternatively, we could project changes from the Greenland ice sheet (`gris`) like

```shell
docker run --rm \
  -v ./data/input:/input/:ro \
  -v ./data/output:/output \
  ghcr.io/facts-org/emulandice:latest gris \
  --pipeline-id=1234 \
  --fprint-gis-file="/input/FPRINT/fprint_gis.nc" \
  --input-data-file="/input/gsat.nc" \
  --location-file="/input/location.lst" \
  --output-gslr-file="/output/gslr.nc" \
  --output-lslr-file="/output/lslr.nc"
```

Yet another option is to project changes from glaciers, like

```shell
docker run --rm \
  -v ./data/input:/input/:ro \
  -v ./data/output:/output \
  ghcr.io/facts-org/emulandice:latest glaciers \
  --pipeline-id=1234 \
  --fprint-glacier-dir="/input/FPRINT" \
  --fprint-map-file="/input/fingerprint_region_map.csv" \
  --input-data-file="/input/gsat.nc" \
  --location-file="/input/location.lst" \
  --output-gslr-file="/output/gslr.nc" \
  --output-lslr-file="/output/lslr.nc" \
  --output-glacier-dir="/output/glacier"
```

## Features

Several options and configurations are available when running the container.

```
Usage: emulandice [OPTIONS] COMMAND [ARGS]...

  Application projecting sea-level change from ice following the Gaussian
  process emulators of the ISMIP6 and GlacierMIP2 models described in Edwards
  et al. (2021).

Options:
  --debug / --no-debug
  -h, --help            Show this message and exit.

Commands:
  ais       Project sealevel rise from Antarctic Ice Sheet (AIS)
  glaciers  Project sealevel rise from glaciers
  gris      Project sealevel rise from Greenland Ice Sheet (GrIS)
```

See this help by running

```shell
docker run --rm ghcr.io/facts-org/emulandice:latest --help
```

or for a specific subcommand, for example `glaciers` like

```shell
docker run --rm ghcr.io/facts-org/emulandice:latest glaciers --help
```

The various options and configurations can also be set with environment variables prefixed by EMULANDICE_*. For example, set `--chunksize` with `EMULANDICE_CHUNKSIZE`.

When run from the container, `EMULANDICE_FORCING_HEAD_PATH` is set by default to a data file included with the container image.

## Building the container image locally

You can build the container with Docker by cloning the repository and then running

```shell
docker build -t emulandice:dev . --platform="linux/amd64"
```

from the repository root.

> [!NOTE]
> The container will only build for the linux/amd64 platform. This is required because the application depends on an older version of R to run the original emulandice package. This older R image is only availble for linux/amd64.


## Support

Source code is available online at https://github.com/facts-org/emulandice. This software is open source, available under the MIT license.

Please file issues in the issue tracker at https://github.com/facts-org/emulandice/issues.

The R package in this repository is derived from Edwards et al. 2021 (https://doi.org/10.1038/s41586-021-03302-y) available at https://github.com/tamsinedwards/emulandice under the public domain.
