import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'authors-xpath'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        author_page_links = response.xpath('//*[@class="author"]/following-sibling::a/@href')
        yield from response.follow_all(author_page_links, self.parse_author)
        pagination_links = response.xpath('//li[@class="next"]/a/@href')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).get(default='').strip()

        yield {
            'name': extract_with_xpath('//h3[@class="author-title"]/text()'),
            'birthdate': extract_with_xpath('//*[@class="author-born-date"]/text()'),
            'bio': extract_with_xpath('//*[@class="author-description"]/text()'),
        }
