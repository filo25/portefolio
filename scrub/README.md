
A tool to filter xml records from a bibliography of 6k results
It colors results in console based on criterias and produces csv output
UDES stands for Universite de Sherbrooke

Uses pandas and colorama - see requirements.txt
xml is typically already included

Use decompress first to generate the xml file

Command options are

- compress
- decompress
- getamountrecords
- printrecords
- printrecordsbyword
- printrecordsnomatch
- exportrecordstopandas

It's possible to run basic tests using

`py.test.exe .\test_crawl.py`

