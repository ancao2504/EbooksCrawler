import scrapy
import os
class SachVuiSpider(scrapy.Spider):
    name = 'sachvui'

    def start_requests(self):
        urls = [
            'https://sachvui.com/the-loai/tat-ca.html'
        ]
        for url in urls:
            yield scrapy.Request(url = url, callback=self.parsePage)

    def parsePage(self, response):
        for page in response.xpath("//div[contains(@class,'ebook')]/a"):
            page_url = page.xpath('./@href').extract_first()
            yield scrapy.Request(url = page_url, callback=self.parse)

        nextButtonUrl = response.xpath("//a[@rel='next']/@href").extract_first()
        if nextButtonUrl is not None:
            yield scrapy.Request(url = nextButtonUrl, callback=self.parsePage)

    def parse(self, response):
        epubUrl = response.xpath("//a[@class='btn btn-primary']/@href").extract_first()
        mobiUrl = response.xpath("//a[@class='btn btn-success']/@href").extract_first()
        pdfUrl = response.xpath("//a[@class='btn btn-danger']/@href").extract_first()
        
        if mobiUrl is not None:
            yield scrapy.Request(url = mobiUrl, callback=self.download)

        
    def download(self, response):
        path = response.url.split('/')[-1]
        dirf = r"../sachvui/"
        if not os.path.exists(dirf):os.makedirs(dirf)
        os.chdir(dirf)
        with open(path, 'wb') as f:
            f.write(response.body)