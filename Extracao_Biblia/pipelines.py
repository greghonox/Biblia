# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class TjScrapyPipeline(object):
    def process_item(self, item, spider):
        sql = f"INSERT INTO BIBLIA(livro, capitulo, paragrafo, paragrafo_text) VALUES('{item['livro']}','{item['capitulo']}','{item['paragrafo']}','{item['paragrafo_text']}');"
        self.con.execute(sql)
        self.con.commit()

    def open_spider(self, spider): 
        self.con = sqlite3.connect('biblia.db')
        self.criarTabela()

    def criarTabela(self):
        sql = 'CREATE TABLE BIBLIA(codigo INTEGER PRIMARY KEY AUTOINCREMENT, livro TEXT, capitulo TEXT, paragrafo TEXT, paragrafo_text TEXT);'
        try:
            self.con.execute(sql)
            self.con.commit()
        except: pass

    def close_spider(self, item, spider): 
        try: self.con.close()
        except: pass