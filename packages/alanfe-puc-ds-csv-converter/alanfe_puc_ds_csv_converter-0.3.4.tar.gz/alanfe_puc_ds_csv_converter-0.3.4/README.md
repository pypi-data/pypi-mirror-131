IConverter
===

A simple module to make easy conversions between two type of files: `csv` and `json`.
<br>
It was created for a postgraduate assignment that had as objective to validate our knowledge about the use of basic structures of Python and the process of creating and publishing a Python module.


## Usage and Examples
To use this module you need to install that end use the convert script of this module:
```
pip install alanfe-puc-ds-csv-converter
python3 -m alanfe-puc-ds-csv-converter convert
```
You will set some arguments of this script like: **output path** (using -o or -ouput) and **input path**(using -i or -input). After that automatically it will parse all files in this path and will save it in output path. 
```
python3 -m alanfe-puc-ds-csv-converter convert -i /input/ -o /output/
# OR
python3 -m alanfe-puc-ds-csv-converter convert -i /input/teste.csv -o /output/
```
It will detect if files are csv or json and will convert them to another format, in the case o csv, will be converted to json and json, csv.
<br>
<br>
To more information about this function we cant use the help command:
```
python3 -m alanfe-puc-ds-csv-converter convert --help
```


