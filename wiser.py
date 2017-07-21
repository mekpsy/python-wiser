# -*- coding: utf-8 -*-

import wiserdb
import tokenizer
import postings
import InvertedIndex
from lxml import etree

class Wiser:
    @staticmethod
    def add_document(title, body, tmp_ii) :
        if title and body :
            # DBに文書を格納し、その文書IDを取得する
            wiserdb.db_add_document(title, body)
            document_id = wiserdb.db_get_document_id(title)

            # utf8 から utf32 へ変換する
            uni_body = unicode(body, 'utf_8')
            utf32_body = uni_body.encode('utf_32')

            # テンポラリ転置インデックスを作成する
            tmp_ii.ii_buffer = tokenizer.text_to_postings_list(document_id, utf32_body, 2, tmp_ii.ii_buffer)
            tmp_ii.ii_buffer_count = tmp_ii.ii_buffer_count + 1

        # 一定数溜まったら本体の転置インデックスとマージ
        if tmp_ii.ii_buffer_count > tmp_ii.ii_buffer_count_threshold or title is None :
            for token in tmp_ii.ii_buffer :
                postintgs.update_postings(token)

class TitleTarget(object):
    def __init__(self):
        self.tmp_ii = InvertedIndex.tmp_ii()
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
                #print self.text
                Wiser.add_document(self.title, self.text, self.tmp_ii);

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

    infile = './one-article.xml'
    results = etree.parse(infile, parser)
