# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.utils.response import open_in_browser as opb

class BibliaSpider(scrapy.Spider):
    name = 'biblia'
    start_urls = ['http://pesquisa.biblia.com.br/pt-BR/NVI//']

    def parse(self, response):
        html = BeautifulSoup(response.text, 'lxml')
        livros = html.findAll(class_='buttonBooks')
        for capitulo in livros: 
            self.livro = {}
            yield scrapy.Request(url=capitulo['onclick'].split('href')[1][2:-1], callback=self.parseLivro)

    def parseLivro(self, response):
        html = BeautifulSoup(response.text, 'lxml')
        total_pagina = int(html.findAll(class_='page-link')[-2].text)
        for pagina in range(1, total_pagina):
            self.livro['capitulo'] =  re.sub('\n|\t', '', html.find('a', {'class': 'bold'}).text)

            yield scrapy.Request(url=html.findAll(class_='page-link')[-1]['href'][:-1] + str(pagina), callback=self.parseVersiculos)              


    def parseVersiculos(self, response):
        html = BeautifulSoup(response.text, 'lxml')
        for versiculo in html.findAll(class_='versiculoTexto'): 
                self.livro['livro'] = re.sub('\n|\r', '', html.find(class_='table-title').text)
                self.livro['paragrafo'] = re.sub('\s{1,}', ' ', versiculo.text).split('|')[1]
                self.livro['paragrafo_text'] = re.sub('\s{1,}', ' ', versiculo.text).split('|')[2]
                yield self.livro