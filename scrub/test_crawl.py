
from UdesXMLBibliography import *

def test_dummy(cmdopt = "asdf"):
    if cmdopt == "type1":
        print("first")
    elif cmdopt == "type2":
        print("second")
    # to see what was printed
    #assert False


def test_print_records():

    offset = 0
    n = 10

    crawler = UdesXMLBibliography(xmlFile)
    recs = crawler.getRecords(offset, n)
    crawler.printTitles(recs, offset)

