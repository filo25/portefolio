
import xml.etree.ElementTree
from colorama import Fore, Back, Style
import pandas as pd
import re


# with >= 2015
xmlFile = '2a4c08fe-1438-44a3-b9ff-2ff84d48c3b8.xml'
xmlFileGz = '2a4c08fe-1438-44a3-b9ff-2ff84d48c3b8.xml.gz'
xmlFileSafe = '2a4c08fe-1438-44a3-b9ff-2ff84d48c3b8_2.xml'

#xmlFile = '73477566-11a7-438d-ae8c-6332559ee001.xml'
#xmlFileGz = '73477566-11a7-438d-ae8c-6332559ee001.xml.gz'
#xmlFileSafe = '73477566-11a7-438d-ae8c-6332559ee001_2.xml'


class UdesXMLBibliography:

    def __init__(self, xmlFile):

        self.xmlFile = xmlFile
        tree = xml.etree.ElementTree.parse(xmlFile)
        self.root = tree.getroot()


    def digNode(self, node, verbose=False):
        """
        crawls the nodes within a record node of the xml
        """

        J = []
        for child in node:
            if verbose:
                print(child.tag, child.attrib)
            J.append(child)
            J.extend(self.digNode(child))
        return J


    def getRecords(self, offset, limit):

        recs = []
        for i, node in enumerate(self.root):

            if i < offset:
                continue

            if i >= offset + limit:
                return recs

            rec = self.digNode(node)
            recs.append(rec)

        return recs


    def mangleRecords(self, records, offset = None, limit = None):
        """
        takes xml record nodes and mangles them into a list of dicts,
        easily used by further functions
        """

        Ds = []

        # possible to fetch n records and to print a subset
        # might be removed later

        for i, rec in enumerate(records):
            if offset and i < offset:
                continue
            if offset and limit and i >= offset + limit:
                break

            d = {"title": None, "author1": None, "author2": None, "author3": None}
            atl = [n for n in rec if n.tag == 'atl']
            d['title'] = atl[0].text
            aus = [n for n in rec if n.tag == 'au']
            d['author1'] = aus[0].text if len(aus) > 0 else ""
            d['author2'] = aus[1].text if len(aus) > 1 else ""
            d['author3'] = aus[2].text if len(aus) > 2 else ""

            dt = [n for n in rec if n.tag == 'dt']
            dt = dt[0] if len(dt) > 0 else None
            d['year'] = dt.get('year')

            Ds.append(d)

        return Ds


    def colorTitle(self, title, color):
        return color + title + Style.RESET_ALL


    def highlightWords(self, title, words, color):
        A = [s for s in words if s in title.lower()]
        for a in A:
            #title = title.replace(a, color + a + Style.RESET_ALL)
            comp = re.compile(re.escape(a), re.IGNORECASE)
            title = comp.sub(color + a.capitalize() + Style.RESET_ALL, title)
        return title


    def printTitles(self, records, offset = 0, limit = None, 
                    filteredBad = ['treatment', 'modalit'],
                    filteredAverage = ['technique', 'report'],
                    filteredGood = ['somatic dysfunction', 'assessment']):

        #records2 = self.mangleRecords(records, offset, limit)
        records2 = self.mangleRecords(records, None, None)

        for i, d in enumerate(records2):

            # the ordering is important, if bad or average are present,
            # they overrule good
            if any(s in d['title'].lower() for s in filteredBad):
                print("[{}] BAD \"".format(offset + i) + self.colorTitle(d['title'], Fore.RED) + "\" ({}, {}, {})".format(d['author1'], d['author2'], d['year']))
            elif any(s in d['title'].lower() for s in filteredAverage):
                print("[{}] AVG \"".format(offset + i) + self.colorTitle(d['title'], Fore.YELLOW) + "\" ({}, {}, {})".format(d['author1'], d['author2'], d['year']))
            elif any(s in d['title'].lower() for s in filteredGood):
                print("[{}] GOOD \"".format(offset + i) + self.highlightWords(d['title'], filteredGood, Fore.GREEN) + "\" ({}, {}, {})".format(d['author1'], d['author2'], d['year']))
            else:
                p = "[{}] NONE \"{}\" ({}, {}, {})".format(offset + i, d['title'], d['author1'], d['author2'], d['year'])
                print(p)


    def printCSVTitles(self, records, offset = 0, limit = None, 
                    filteredBad = ['treatment', 'modalit'],
                    filteredAverage = ['technique', 'report'],
                    filteredGood = ['somatic dysfunction', 'assessment']):

        #records2 = self.mangleRecords(records, offset, limit)
        records2 = self.mangleRecords(records, None, None)

        for i, d in enumerate(records2):

            # the ordering is important, if bad or average are present,
            # they overrule good
            if any(s in d['title'].lower() for s in filteredBad):
                print("\"{}\",\"BAD\",\"".format(offset + i) + self.colorTitle(d['title'], Fore.RED) + "\" ({}, {}, {})".format(d['author1'], d['author2'], d['year']))
            elif any(s in d['title'].lower() for s in filteredAverage):
                print("[{}] AVG \"".format(offset + i) + self.colorTitle(d['title'], Fore.YELLOW) + "\" ({}, {}, {})".format(d['author1'], d['author2'], d['year']))
            elif any(s in d['title'].lower() for s in filteredGood):
                print("[{}] GOOD \"".format(offset + i) + self.highlightWords(d['title'], filteredGood, Fore.GREEN) + "\" ({}, {}, {})".format(d['author1'], d['author2'], d['year']))
            else:
                p = "[{}] NONE \"{}\" ({}, {}, {})".format(offset + i, d['title'], d['author1'], d['author2'], d['year'])
                print(p)


    def exportToPandas(self, records, offset = None, limit = None):

        records2 = self.mangleRecords(records, offset, limit)

        df = pd.DataFrame(records2)
        print(df)

