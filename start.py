#encoding: utf-8
from scrapy import cmdline


cmdline.execute("scrapy crawl sfw -o aa.csv".split())