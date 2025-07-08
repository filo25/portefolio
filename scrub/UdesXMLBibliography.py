
import xml.etree.ElementTree
from colorama import Fore, Back, Style
import pandas as pd
import re


# with >= 2015
xmlFile = '4f2e5af9-8077-4cf1-8d8c-7b18f9f46b88.xml'
xmlFileGz = '4f2e5af9-8077-4cf1-8d8c-7b18f9f46b88.xml.gz'
xmlFileSafe = '4f2e5af9-8077-4cf1-8d8c-7b18f9f46b88_2.xml'

#xmlFile = '73477566-11a7-438d-ae8c-6332559ee001.xml'
#xmlFileGz = '73477566-11a7-438d-ae8c-6332559ee001.xml.gz'
#xmlFileSafe = '73477566-11a7-438d-ae8c-6332559ee001_2.xml'


class UdesXMLBibliography:

    def __init__(self, xmlFile):

        self.xmlFile = xmlFile
        tree = xml.etree.ElementTree.parse(xmlFile)
        self.root = tree.getroot()

        # attitudes
        # Tissutal and Fluidic Aspects in Osteopathic Manual Therapy: A Narrative Review.

        self.filters = {
                        #'GOOD': ['somatic dysfunction', 'assessment', 'palpat']
                        'GOOD': ['somatic dysfunction', 'palpat', 'evidence', 'allosta', 'interexamin', 'reliab', 'biomech', 'palpatory finding'],

                        #'AVG': ['technique', 'report', 'study', 'manipu', 'impact']
                        'AVG': ['technique', 'report', 'study', 'manipu', 'case'],

                        'BAD': ['treat', 'modalit', 'effect', 'interven', 'injury', 'surgery', 'prevalence']
                    }


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


    def highlightWords(self, title, words, color, upper=False):
        A = [s for s in words if s in title.lower()]
        for a in A:
            #title = title.replace(a, color + a + Style.RESET_ALL)
            comp = re.compile(re.escape(a), re.IGNORECASE)
            if upper:
                title = comp.sub(color + a.upper() + Style.RESET_ALL, title)
            else:
                title = comp.sub(color + a.capitalize() + Style.RESET_ALL, title)
        return title


    def printTitles(self, records, offset = 0, noPrettyPrint = False, limit = None):
                    #filteredBad = ['treat', 'modalit', 'effect', 'interven', 'injury', 'surgery', 'prevalence'],
                    ## attitudes
                    ## Tissutal and Fluidic Aspects in Osteopathic Manual Therapy: A Narrative Review.
                    ##filteredAverage = ['technique', 'report', 'study', 'manipu', 'impact'],
                    #filteredAverage = ['technique', 'report', 'study', 'manipu'],
                    ##filteredGood = ['somatic dysfunction', 'assessment', 'palpat']):
                    #filteredGood = ['somatic dysfunction', 'palpat', 'evidence', 'allosta', 'reliab', 'biomech', 'palpatory finding']):

        #records2 = self.mangleRecords(records, offset, limit)
        records2 = self.mangleRecords(records, None, None)

        for i, d in enumerate(records2):

            # the ordering is important, if bad or average are present,
            # they overrule good
            if any(s in d['title'].lower() for s in self.filters['BAD']):
                if noPrettyPrint:
                    print("{},BAD,\"{}\",\"{}, {}\",{}".format(offset + i, d['title'], d['author1'], d['author2'], d['year']))
                else:
                    print("[{}] BAD \"".format(offset + i) + self.colorTitle(d['title'], Fore.RED) + "\" ({}, {}, {})".format(d['author1'], d['author2'], d['year']))
            elif any(s in d['title'].lower() for s in self.filters['AVG']):
                if noPrettyPrint:
                    print("{},AVG,\"{}\",\"{}, {}\",{}".format(offset + i, d['title'], d['author1'], d['author2'], d['year']))
                else:
                    #print("[{}] AVG \"".format(offset + i) + self.colorTitle(d['title'], Fore.YELLOW) + "\" ({}, {}, {})".format(d['author1'], d['author2'], d['year']))
                    print("[{}] AVG \"".format(offset + i) + self.highlightWords(d['title'], self.filters['AVG'], Fore.YELLOW) + "\" ({}, {}, {})".format(d['author1'], d['author2'], d['year']))
            elif any(s in d['title'].lower() for s in self.filters['GOOD']):
                if noPrettyPrint:
                    print("{},GOOD,\"{}\",\"{}, {}\",{}".format(offset + i, d['title'], d['author1'], d['author2'], d['year']))
                else:
                    print("[{}] GOOD \"".format(offset + i) + self.highlightWords(d['title'], self.filters['GOOD'], Fore.GREEN) + "\" ({}, {}, {})".format(d['author1'], d['author2'], d['year']))
            else:
                if noPrettyPrint:
                    print("{},NONE,\"{}\",\"{}, {}\",{}".format(offset + i, d['title'], d['author1'], d['author2'], d['year']))
                else:
                    print("[{}] NONE \"{}\" ({}, {}, {})".format(offset + i, d['title'], d['author1'], d['author2'], d['year']))


    def printTitlesByWord(self, records, offset = 0, noPrettyPrint = False, limit = None, word = None):

        records2 = self.mangleRecords(records, None, None)

        for i, d in enumerate(records2):

            if any(s in d['title'].lower() for s in [ word ]):
                if noPrettyPrint:
                    print("{},WORD,\"{}\",\"{}, {}\",{}".format(offset + i, d['title'], d['author1'], d['author2'], d['year']))
                else:
                    # MAGENTA, LIGHTCYAN_EX
                    print("[{}] WORD \"".format(offset + i) + self.highlightWords(d['title'], [ word ], Fore.LIGHTCYAN_EX, True) + "\" ({}, {}, {})".format(d['author1'], d['author2'], d['year']))


    def printTitlesNoMatch(self, records, offset = 0, noPrettyPrint = False, limit = None):

        F = []
        for k,v in self.filters.items():
            F.extend(v)

        records2 = self.mangleRecords(records, None, None)

        for i, d in enumerate(records2):

            if not any(s in d['title'].lower() for s in F):
                print("{},\"{}\",\"{}, {}\",{}".format(offset + i, d['title'], d['author1'], d['author2'], d['year']))


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

