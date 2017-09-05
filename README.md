DeafVariationDownloader
=======================

Download deaf variation data from http://deafnessvariationdatabase.org

Download data by API from http://deafnessvariationdatabase.org. Please do not use for commercial purpose or service attack.

# Dependency
pymongo if use mongodb to store data

# Usage
## Download gene files
```
python deafvariation_downloader.py
```

Workflow is as below:

1. Download genelist file (default genelist.json, can be set by --genelist option).
2. Download each gene file in genelist to output directory (default data, can be set by --output option), default format is tab (can be set by --format option)

## Transform tsv format to json format
Because json format is larger than tab format, we download tab format and then transform to json format.
```
python tsv2json.py data
```

## Store data to Mongodb
```
python store2mongo.py out
```

Set mongodb connection by --host, --port, --database and --collection
