import scrapy
from bianb.items import BianbItem
from scrapy import Request
import re
from urllib.parse import quote


class BbpaperSpider(scrapy.Spider):
    current_page = 1
    search_keyword = ""#这里输入需要搜索的区，空的话就是所有文章
    encoded_keyword = quote(search_keyword)
    name = 'bbpaper'
    allowed_domains = ['*']#允许的地址，防止侵权给删除了

    start_urls = ['https://*/search_%d.jspx?q=%s&searchType=1' % (current_page, encoded_keyword)]


    def parse(self, response):
        paper_list =response.xpath('//ul[@class="list"]//li')
        total_page_res = response.xpath('//div[@style="float: right;margin-right: 10px"]//text()').get()
        pattern = r"(?<=/)\d+"
        match = re.search(pattern, total_page_res)
        if match:
            total_page = match.group()
        else:
            total_page = 1

        item = BianbItem()
        for paper in paper_list:
            url =paper.xpath('a/@href').get()
            url = re.sub(r':80', '', url) #删除：80端口，不然get url报错
            url = re.sub(r'http', 'https', url)#上面搞错了，是http访问不了要https
            item['url'] = url
            yield Request(url,meta={'item':item},callback=self.content_parse)
        self.current_page+=1
        if self.current_page <= int(total_page):
            next_url = 'https://*/search_%d.jspx?q=%s&searchType=1' % (self.current_page, self.encoded_keyword)
            yield Request(next_url,callback=self.parse)

    #获取来源和内容
    def content_parse(self, response):
        name = response.xpath('//span[@class="title"]/text()').extract_first()
        subtitle = response.xpath('//span[@class="sub_title"]/text()').extract_first()
        item = response.meta['item']
        item['name'] = name
        # 提取时间
        time_match = re.search(r'(\d{4}-\d{2}-\d{2})', subtitle) #要是没有匹配就返回none
        time = time_match.group(1)
        item['time'] = time

        # 提取来源
        source_match = re.search(r'来源：\s*(\S+)', subtitle)
        area = source_match.group(1)
        item['area'] = area

        content = response.xpath('//div[@class="newsCon"]').get()
        item['content']=content

        yield item
