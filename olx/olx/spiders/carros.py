#import scrapy
import abc

class CarrosSpider(scrapy.Spider):
    name = 'carros'
    start_urls = ['https://rn.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/']

    def parse(self, response):
        itens = response.xpath('//ul[@id="ad-list"]/li')
        for item in itens:
            url = item.xpath('./a/@href').extract_first()        
            if isinstance(url,str):
                yield scrapy.Request( url = url, callback= self.parse_detail)
        
        next_page = response.xpath(
            '//div/a[contains(@data-lurker-detail,"next_page")]/@href'
        )

        if next_page:
            self.log('PROXIMA PAGINA: {} '.format(next_page.extract_first()))
            yield scrapy.Request(
                url = next_page.extract_first(), callback= self.parse
            )

# self.log(item.xpath('./a[not(contains(@class, "OLXad-list-link"))]/@href').extract_first())


    def parse_detail(self,response):

        modelo = response.xpath(
            '//span[contains(text(),"Modelo")]/following-sibling::a/text()'
        ).extract_first()

        marca = response.xpath(
            '//span[contains(text(),"Marca")]/following-sibling::a/text()'
        ).extract_first()

        Direção = response.xpath(
            '//span[contains(text(),"Direção")]/following-sibling::span/text()'
        ).extract_first()

        ano = response.xpath(
            '//span[contains(text(),"Ano")]/following-sibling::a/text()'
        ).extract_first()

        yield {
            'modelo' : modelo,
            'marca' : marca,
            'Direção' : Direção,
            'ano' : ano,
        }