from lxml import etree
from pprint import pprint
import wiserdb

class TitleTarget(object):
    def __init__(self):
        self.titleout = open('title.txt', 'w')
        self.textout = open('text.txt', 'w')
        self.in_page = False
        self.in_title = False
        self.in_revision = False
        self.in_text = False
        self.title = None
        self.text = None

    def start(self, tag, attrib):
        if tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
            self.in_page = True
            self.title = None
        if self.in_page :
            if tag == '{http://www.mediawiki.org/xml/export-0.10/}title':
                self.in_title = True
            elif tag == '{http://www.mediawiki.org/xml/export-0.10/}revision' :
                self.in_revision = True
                self.text = None
        if self.in_revision :
            if tag == '{http://www.mediawiki.org/xml/export-0.10/}text':
               self.in_text = True

    def end(self, tag):
        if tag == '{http://www.mediawiki.org/xml/export-0.10/}title' :
            self.in_title = False
            self.in_page = True
        if tag == '{http://www.mediawiki.org/xml/export-0.10/}revision' :
            self.in_page = True
            self.in_revision = False
        if tag == '{http://www.mediawiki.org/xml/export-0.10/}text' :
            self.in_text = False
            self.in_revision = True
            if self.text is not None:
                print "title " + self.title
                print self.text
                wiserdb.db_insert_wiki(self.title, self.text)

    def data(self, data):
        if self.in_title:
            if self.title is not None :
                self.title = self.title + data.encode('utf-8')
            else :
                self.title = data.encode('utf-8')
        if self.in_text:
            if self.text is not None :
                self.text = self.text + data.encode('utf-8')
            else :
                self.text = data.encode('utf-8')

    def close(self):
        self.titleout.close()
        self.textout.close()

if __name__ == '__main__':
    parser = etree.XMLParser(target = TitleTarget())

    infile = './jawiki-latest-pages-articles.xml'
    results = etree.parse(infile, parser)
