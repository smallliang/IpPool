# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Request
from collectips.items import CollectipsItem


class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn/1']
    link_url = 'http://www.xicidaili.com'
    ip_count = 0

    def parse(self, response):
        ip_list = response.xpath('//*[@id="ip_list"]/tr')

        for ip in ip_list[1:]:
            item = CollectipsItem()
            try:
                item['IP'] = ip.xpath('td[2]/text()')[0].extract()
                item['PORT'] = ip.xpath('td[3]/text()')[0].extract()
                item['POSITION'] = ip.xpath('td[4]/a/text()')[0].extract()
                item['TYPE'] = ip.xpath('td[6]/text()')[0].extract()
                item['SPEED'] = ip.xpath('td[7]/div/@title').re('\d{0,}\.\d{0,}')[0]
                item['LAST_CHECK_TIME'] = ip.xpath('td[10]/text()')[0].extract()
                yield item
            except:
                pass
        #获取下一页链接
        next_page_nums = response.xpath('//*[@class="next_page"]/@href')
        if(next_page_nums):
            next_page = self.link_url + next_page_nums[0].extract()
            print(next_page)
            yield Request(url=next_page, callback=self.parse)
        else:
            print("爬取完成")