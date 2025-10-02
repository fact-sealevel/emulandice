# emulandice

The emulandice family of modules wrap around the Edwards et al. (2021) Gaussian process emulators of the ISMIP6 and GlacierMIP2 models.

## Example

```shell
mkdir -p ./data/input

curl -sL https://zenodo.org/record/7478192/files/grd_fingerprints_data.tgz | tar -zx -C ./data/input

echo "New_York	12	40.70	-74.01" > ./data/input/location.lst

mkdir -p ./data/output
  
```

for AIS

```shell
docker run --rm \
  -v ./data/input:/input/:ro \
  -v ./data/output:/output \
  emulandice:dev ais \
  --pipeline-id=1234 \
  --fprint-wais-file="/input/FPRINT/fprint_wais.nc" \
  --fprint-eais-file="/input/FPRINT/fprint_eais.nc" \
  --input-data-file="/input/gsat.nc" \
  --location-file="/input/location.lst" \
  --output-gslr-file="/output/gslr.nc" \
  --output-lslr-file="/output/lslr.nc"
```

for GrIS

```shell
docker run --rm \
  -v ./data/input:/input/:ro \
  -v ./data/output:/output \
  emulandice:dev gris \
  --pipeline-id=1234 \
  --fprint-gis-file="/input/FPRINT/fprint_gis.nc" \
  --input-data-file="/input/gsat.nc" \
  --location-file="/input/location.lst" \
  --output-gslr-file="/output/gslr.nc" \
  --output-lslr-file="/output/lslr.nc"
```
for glaciers

```shell
docker run --rm \
  -v ./data/input:/input/:ro \
  -v ./data/output:/output \
  emulandice:dev glaciers \
  --pipeline-id=1234 \
  --fprint-glacier-dir="/input/FPRINT" \
  --fprint-map-file="/input/fingerprint_region_map.csv" \
  --input-data-file="/input/gsat.nc" \
  --location-file="/input/location.lst" \
  --output-gslr-file="/output/gslr.nc" \
  --output-lslr-file="/output/lslr.nc" \
  --output-glacier-dir="/output/glacier"
```

```shell
docker build -t emulandice:dev . --platform="linux/amd64"
```

```shell
tar -cz --no-xattrs --exclude ".DS_Store" -f emulandice_1.1.0.tar.gz emulandice/
```
