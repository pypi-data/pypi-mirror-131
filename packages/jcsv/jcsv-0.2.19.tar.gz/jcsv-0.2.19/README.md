# JCSV (JSON2CSV and CSV2JSON converter)

Project developed in the Python for Data Science course - Artificial intelligence PUC-MG

## Requirements
- python ^3.7

## Install
```
pip install jcsv
or
pip3 install jcsv
```

## Usage



- convert csv to json

```
csv2json --input /path/to/csv/files --output /path/to/json/files --delimiter ,
```

- convert json to csv

```
json2csv --input /path/to/json/files --output /path/to/csv/files --delimiter ,
```

### Default
- input = "./"
- output = "./"
- delimiter = ","

## Help

```
csv2json --help
Usage: csv2json [OPTIONS]

Options:
  -i, --input TEXT      Path where to find CSV files to be contered to JSON.
  -o, --output TEXT     Path where the converted files will be saved.
  -d, --delimiter TEXT  Separator used to split files.
  --help                Show this message and exit.
```

```
json2csv --help
Usage: json2csv [OPTIONS]

Options:
  -i, --input TEXT      Path where to find JSON files to be contered to CSV.
  -o, --output TEXT     Path where the converted files will be saved.
  -d, --delimiter TEXT  Separator used to split files.
  --help                Show this message and exit.
```

