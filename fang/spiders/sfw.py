# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import NewhouseItem,EsfhouseItem
import urllib.parse
from scrapy_redis.spiders import RedisSpider


class SfwSpider(RedisSpider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    # start_urls = ['https://www.fang.com/SoufunFamily.htm']
    redis_key = 'fang:start_url'

    def parse(self, response):
        trs=response.xpath('//div[@class="outCont"]//tr')
        province=None
        for tr in trs:
            tds=tr.xpath(".//td[not(@class='font01')]")
            province_td=tds[0]
            province_text=province_td.xpath(".//text()").extract_first()
            province_text=re.sub(r'\s',"",province_text)
            if province_text:
                province=province_text
            if province =='其它':
                continue
            city_td=tds[1]
            city_links=city_td.xpath('.//a')
            for city_link in city_links:
                city=city_link.xpath('.//text()').extract_first()
                city_url=city_link.xpath('.//@href').extract_first()
                # 构建新房的url链接
                url_module=city_url.split('.')

                scheme=url_module[0]
                domain=url_module[1]
                if 'https://bj' in scheme:
                    newhouse_url='https://newhouse.fang.com/house/s/'
                    esf_url=' https://esf.fang.com/'

                # elif  'https://world' in scheme or 'http://world' in scheme:
                #     country=city_url.split('com')[-1]
                #     newhouse_url=city_url+'m1/'
                #     esf_url=city_url+'m2/'

                else:
                    #新房链接
                    newhouse_url=scheme+".newhouse."+domain+'.com/'+'house/s/'
                    # 二手房链接
                    esf_url=scheme+'.esf.'+domain+'.com'
                # print(newhouse_url, esf_url)
                yield scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,
                                     meta={'info':(province,city)})
                yield scrapy.Request(url=esf_url, callback=self.parse_esf,
                                     meta={'info': (province, city)})

    def parse_newhouse(self,response):
        province,city=response.meta['info']
        lis=response.xpath('//div[@class="nl_con clearfix"]/ul/li')
        for li in lis:

            cell_name=li.xpath('.//div[@class="nlcd_name"]/a/text()').extract_first()
            if cell_name:
                cell_name=cell_name.strip()
            # print(cell_name)
            house_type_list=li.xpath('.//div[contains(@class,"house_type")]/a//text()').extract()
            house_type_list=list(map(lambda x:re.sub('\s','',x),house_type_list))
            # print(house_type_list)
            rooms=list(filter(lambda x:x.endswith('居'),house_type_list))
            rooms=''.join(rooms)
            address=li.xpath('.//div[contains(@class,"address")]//a/@title').extract_first()
            area=''.join(li.xpath(".//div[contains(@class,'house_type')]/text()").extract())
            area=re.sub(r'\s|－|/','',area)
            state=li.xpath("//div[contains(@class,'fangyuan pr')]/span/text()").extract_first()
            price=''.join(li.xpath(".//div[contains(@class,'nhouse_price')]//text()").extract())
            price=re.sub(r'\s|广告','',price)
            # origin_url='https:'+li.xpath(".//div[contains(@class,'nlcd_name')]/a/@href").extract_first()
            origin_url=li.xpath(".//div[contains(@class,'nlcd_name')]/a/@href").extract_first()

            item=NewhouseItem(province=province,city=city,cell_name=cell_name,rooms=rooms,address=address,state=state,area=area,price=price,origin_url=origin_url)
            print(item)
            yield item
        next_url=response.xpath("//a[@class='next']/@href").extract_first()

        # next_url=urllib.parse.urljoin(response.url,next_url)
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_newhouse,meta={'info':(province,city)})


    def parse_esf(self,response):
        province,city=response.meta['info']
        dls=response.xpath("//div[@class='shop_list shop_list_4']/dl")
        for dl in dls:
            item = EsfhouseItem(province=province,city=city)
            item['cell_name']=dl.xpath(".//p[@class='add_shop']/a/@title").extract_first()
            item['address']=dl.xpath(".//p[@class='add_shop']/span/text()").extract_first()
            infos=dl.xpath(".//p[@class='tel_shop']/text()").extract()
            item['year']=None
            infos=list(map(lambda x: re.sub(r'\s','',x),infos))
            for info in infos:
                    if '厅' in info:
                        item['rooms']=info
                    elif '层' in info:
                        item['floor']=info
                    elif '向' in info:
                        item['toward']=info
                    elif '㎡' in info:
                        item['area']=info

                    else:
                        item['year']=info
            price=dl.xpath(".//dd[@class='price_right']/span[1]//text()").extract()
            item['price']=''.join(price)
            item['unit']=dl.xpath(".//dd[@class='price_right']/span[2]//text()").extract()
            item['origin_url']=dl.xpath(".//h4/a/@href").extract_first()
            item['origin_url']=response.urljoin(item['origin_url'])
            yield item
        next_url=response.xpath("//div[@class='page_al']/p[1]/a/@href").extract_first()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_esf,meta={'info':(province,city)})