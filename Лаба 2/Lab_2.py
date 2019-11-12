# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 11:54:04 2019

@author: mag
"""


from bs4 import BeautifulSoup
import feedparser
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

class News():
    def __init__(self):
        self.news = list()
        self.tags = set()
        
        
        
    def get_News(self, url):
        feed = feedparser.parse(url)
        raw_News = feed['entries'] #  новости в формате списка словарей             
        for i in raw_News:
            try:
                self.news.append({'url' : i['id'],'tags' : (i['tags'][0]['term']),
                                  'data' : i['published'],'title' : i['title'],'summary' : BeautifulSoup(i['summary'], 'html.parser').get_text()})#запись словаря
            except:
                self.news.append({'url' : i['id'],'tags' : [0],
                                  'data' : i['published'],'title' : i['title'],'summary' : BeautifulSoup(i['summary'], 'html.parser').get_text()})#запись словаря
    
    def consider_Tags(self):
        try:
             #создание множества для того, чтобы не было повторных элементов
            for i in self.news:
                if i['tags'][0] != 0:
                    self.tags.add(i['tags'])                
            
            return 1
        except:
            return 0
    
    def get_Tagged_News(self, tag):
        mes = ""
        for i in self.news:
            if i['tags'].count(tag) > 0:
                mes = mes + i['url'] + '\n' + i['data'] + '\n' + i['title'] + '\n' + i['summary'] + '\n\n\n\n'
        
        return mes
    
    def get_KWorded_News(self, keywords):
        stemmer = SnowballStemmer("russian")
        kwords = [stemmer.stem(i) for i in keywords.split(" ")]
        mes = ""
        for i in self.news:
            word_list = [j for j in nltk.word_tokenize(i["summary"]) if j not in string.punctuation and j not in stopwords.words('russian')]
            word_list = set([stemmer.stem(i) for i in word_list])
            flag = 0
            for k in kwords:
                if flag == 0:
                    for j in word_list:
                        if k == j:
                            flag = 1
                            break
                else:
                    break
            if flag == 1:
                mes = mes + i['url'] + '\n' + i['data'] + '\n' + i['title'] + '\n' + i['summary'] + '\n\n\n\n'
        return mes

#for i in  ke:
#    print(feed[i])string indices must be integers
#print(ke)#'feed', 'entries', 'bozo', 'headers', 'etag', 'href', 'status', 'encoding', 'version', 'namespaces'

#feed = feedparser.parse('https://lenta.ru/rss/news')
#news = feed['entries'][0]

#print(news['tags'][0]['term'])
#print(news['tags'][0]['term'])
#print(feed['entries'][0].keys())#'id', 'guidislink', 'link', 'title', 'title_detail', 'links', 'summary', 'summary_detail', 'published', 'published_parsed', 'tags'
#print(news['id'], '\n', news['title'], '\n', news['summary'], '\n', news['published'])#, '\n', news['tags'][0]['term']


rss = News()
#https://news.yandex.ru/cyber_sport.rss
#https://lenta.ru/rss/news
rss.get_News("https://lenta.ru/rss/news")
#print(rss.consider_Tags())
#print(rss.news[1])
rss.consider_Tags()
print(rss.tags)
#print(rss.get_Tagged_News("Ценности"))
