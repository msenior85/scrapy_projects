import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse
import re


class AgentsSpider(scrapy.Spider):
    name = 'agents'
    allowed_domains = ['kw.com']

    def start_requests(self):
        url = 'https://www.kw.com/agent/search/NY/New%20York'
        yield scrapy.Request(url, meta={"playwright": True, "playwright_include_page": True})

    async def parse(self, response):
        page = response.meta.get('playwright_page')

        await page.wait_for_selector("div.KWLoader__bullet", state='hidden')
        total_string = await page.inner_text("//*[contains(@class,'FindAgentRoute__totalCount')]/div")
        total_count = re.match(r"Showing (\d+) Agents", total_string).group(1)

        if total_count:
            total_count = int(total_count)
            pages = total_count // 50

            for _ in range(pages):
                await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                await page.wait_for_selector("div.KWLoader__bullet", state='hidden')

        content = await page.content()

        response = HtmlResponse(url=page.url, body=content, encoding='utf-8')

        for agent in response.xpath("//*[contains(@class,'FindAgentRoute__agentCard')]"):
            yield {
                'name': agent.xpath(".//*[@class='AgentCard__name']/text()").get(),
                'market_center': agent.xpath(".//*[@class='AgentCard__marketCenter']/text()").get(),
                'license': agent.xpath(".//*[@class='AgentCard__license']/text()").re_first(r"License #(.*)"),
                'email': agent.xpath(".//*[@class='AgentCard__contact' and contains(@href, 'mailto')]/@href").re_first(r"mailto:(.*)"),
                'phone': agent.xpath(".//*[@class='AgentCard__contact' and contains(@href, 'tel')]/@href").re_first(r"tel:(.*)"),
            }

        await page.close()

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        'DOWNLOAD_HANDLERS': {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        'FEEDS': {
            'items.csv': {
                'format': 'csv',
            }
        }
    })
    process.crawl(AgentsSpider)
    process.start()
