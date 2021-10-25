from scrapy import Spider
from scrapy.crawler import CrawlerProcess


class CountriesSpider(Spider):
    name = 'countries'
    start_urls = ['https://www.scrapethissite.com/pages/simple/']

    def parse(self, response):

        for country in response.xpath("//div[@class='row']/div[contains(@class,'country')]"):
            name = country.xpath(
                "normalize-space(./h3[@class='country-name']/i/following-sibling::text())").get()
            capital = country.xpath(
                ".//span[@class='country-capital']/text()").get()
            population = country.xpath(
                ".//span[@class='country-population']/text()").get()
            area_in_sq_km = country.xpath(
                ".//span[@class='country-area']/text()").get()

            yield {
                'name': name,
                'capital': capital,
                'population': population,
                'area_in_sq_km': area_in_sq_km
            }


if __name__ == '__main__':
    process = CrawlerProcess(
        settings={
            'FEEDS': {
                'items.csv': {
                    'format': 'csv',
                    'encoding': 'utf8',
                }
            }
        }
    )
    process.crawl(CountriesSpider)
    process.start()
