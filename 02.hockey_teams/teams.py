from scrapy import Spider
from scrapy.crawler import CrawlerProcess


class HockeySpider(Spider):
    name = 'teams'
    start_urls = ['https://www.scrapethissite.com/pages/forms/']

    def parse(self, response):

        for row in response.xpath("//tr[@class='team']"):
            yield {
                'name': row.xpath("normalize-space(./td[@class='name']/text())").get(),
                'year': row.xpath("normalize-space(./td[@class='year']/text())").get(),
                'wins': row.xpath("normalize-space(./td[@class='wins']/text())").get(),
                'losses': row.xpath("normalize-space(./td[@class='losses']/text())").get(),
                'ot-losses': row.xpath("normalize-space(./td[@class='ot-losses']/text())").get(),
                'pct_text_success': row.xpath("normalize-space(./td[@class='pct text-success']/text())").get(),
                'gf': row.xpath("normalize-space(./td[@class='gf']/text())").get(),
                'ga': row.xpath("normalize-space(./td[@class='ga']/text())").get(),
                'diff_text_success': row.xpath("normalize-space(./td[@class='diff text-success']/text())").get(),
            }

            next_page = response.xpath("//a[@aria-label='Next']/@href").get()
            if next_page:
                yield response.follow(next_page)


if __name__ == '__main__':
    process = CrawlerProcess(
        settings={
            'FEEDS': {
                'teams.csv': {
                    'format': 'csv',
                    'encoding': 'utf8',
                }
            }
        }
    )
    process.crawl(HockeySpider)
    process.start()
