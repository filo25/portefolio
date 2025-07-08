
import sys
import argparse
import gzip

from UdesXMLBibliography import *

# use alt + middle-click in powershell to copy-paste
# with new lines

def compress():
    with open(xmlFile, 'r', encoding='utf-8') as f:
        buf = f.read()

    compressed = gzip.compress(bytes(buf, 'utf-8'))

    with open(xmlFileGz, 'wb') as f2:
        f2.write(compressed)


def decompress():
    with open(xmlFileGz, 'rb') as f:
        buf = f.read()

    decompressed = gzip.decompress(buf).decode('utf-8')

    with open(xmlFileSafe, 'w', encoding='utf-8') as f2:
        f2.write(decompressed)


def getamountrecords():
    crawler = UdesXMLBibliography(xmlFile)
    recs = crawler.getRecords(0, 99999)
    print(len(recs))


def printrecords(n, offset, noPrettyPrint):
    noPrettyPrint = False if noPrettyPrint == None else True

    if not noPrettyPrint:
        print("Showing {} records with offset {}".format(n, offset))

    crawler = UdesXMLBibliography(xmlFile)
    recs = crawler.getRecords(offset, n)
    crawler.printTitles(recs, offset, noPrettyPrint)


def printrecordsbyword(n, offset, noPrettyPrint, word):

    word = "" if not len(word) else word[0]
    noPrettyPrint = False if noPrettyPrint == None else True

    if not noPrettyPrint:
        print("Showing {} records with offset {}".format(n, offset))

    crawler = UdesXMLBibliography(xmlFile)
    recs = crawler.getRecords(offset, n)
    crawler.printTitlesByWord(recs, offset, noPrettyPrint, word=word)


def printrecordsnomatch(n, offset, noPrettyPrint):

    noPrettyPrint = False if noPrettyPrint == None else True

    if not noPrettyPrint:
        print("Showing {} records with offset {}".format(n, offset))

    crawler = UdesXMLBibliography(xmlFile)
    recs = crawler.getRecords(offset, n)
    crawler.printTitlesNoMatch(recs, offset, noPrettyPrint)


def exportrecordstopandas(n, offset):
    crawler = UdesXMLBibliography(xmlFile)
    recs = crawler.getRecords(offset, n)
    crawler.exportToPandas(recs)


parser = argparse.ArgumentParser(description ='A tool to filter records from a bibliography of 8k results efficiently')
subparsers = parser.add_subparsers(dest='subparser')

parserCompress = subparsers.add_parser('compress')
parserCompress = subparsers.add_parser('decompress')

parserGetAmountRecs = subparsers.add_parser('getamountrecords')

parserPrintRecs = subparsers.add_parser('printrecords')
parserPrintRecs.add_argument(
    '-n',
    dest='n',
    default=3,
    type=int,
    help='fetch n records'
)
parserPrintRecs.add_argument(
    '-o',
    dest='offset',
    default=0,
    type=int,
    help='offset by n records'
)
parserPrintRecs.add_argument(
    '-p',
    dest='noPrettyPrint',
    default=None,
    nargs='*',
    help='human-readable'
)

parserPrintRecsByWord = subparsers.add_parser('printrecordsbyword')
parserPrintRecsByWord.add_argument(
    '-n',
    dest='n',
    default=3,
    type=int,
    help='fetch n records'
)
parserPrintRecsByWord.add_argument(
    '-o',
    dest='offset',
    default=0,
    type=int,
    help='offset by n records'
)
parserPrintRecsByWord.add_argument(
    '-p',
    dest='noPrettyPrint',
    default=None,
    nargs='*',
    help='human-readable'
)
parserPrintRecsByWord.add_argument(
    '-w',
    dest='word',
    type=str,
    default=None,
    nargs='*',
    help='keyword to search'
)

parserPrintRecsNoMatch = subparsers.add_parser('printrecordsnomatch')
parserPrintRecsNoMatch.add_argument(
    '-n',
    dest='n',
    default=3,
    type=int,
    help='fetch n records'
)
parserPrintRecsNoMatch.add_argument(
    '-o',
    dest='offset',
    default=0,
    type=int,
    help='offset by n records'
)
parserPrintRecsNoMatch.add_argument(
    '-p',
    dest='noPrettyPrint',
    default=None,
    nargs='*',
    help='human-readable'
)

parserExportToPandas = subparsers.add_parser('exportrecordstopandas')
parserExportToPandas.add_argument(
    '-n',
    dest='n',
    default=3,
    type=int,
    help='fetch n records'
)
parserExportToPandas.add_argument(
    '-o',
    dest='offset',
    default=0,
    type=int,
    help='offset by n records'
)


if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

kwargs = vars(parser.parse_args())
globals()[kwargs.pop('subparser')](**kwargs)


