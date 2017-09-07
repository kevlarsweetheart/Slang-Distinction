import scrapy
import jsonlines

class MeduzaSpider(scrapy.Spider):
    name = "meduza"
    allowed_domains = ['meduza.io']
    start_urls = ["http://meduza.io"]


    def parse_article(self, response):
        request_url = response.url.split("/")
        if 'cards' in request_url:
            article_title = response.xpath('//span[contains(@class, "CardMaterial-titleFirst")]/text()').extract()
            yield {'Article title': article_title}
            chapters = response.xpath('//div[contains(@class, "Card-chapter")]')
            for chapter in chapters:
                chapter_title = chapter.xpath('//h3[contains(@class, "CardChapter-title")]/text()').extraxt()
                chapter_text = chapter.xpath('//div[contains(@class, "CardChapter-body")]/p/text()').extract()
                yield {'Chapter title': chapter_title}
                yield {'Chapter text': chapter_text}
        elif 'feature' in request_url:
            feature_title = response.xpath('//span[contains(@class, "MediaMaterialHeader-first")]/text()').extract()
            yield {'Feature title': feature_title}
            feature_body = response.xpath('//div[contains(@class, "Body")]/p/text()').extract()
            yield {'Feature body': feature_body}
        elif 'news' in request_url or 'shapito' in request_url:
            news_title = response.xpath('//span[contains(@class, "NewsMaterialHeader-first")]/text()').extract()
            yield {'News title': news_title}
            news_body = response.xpath('//div[contains(@class, "Body")]/p/text()').extract()
            yield {'News body': news_body}


    def parse(self, response):
        with jsonlines.open('./meduza/articles_urls.jl') as urls:
            for page in urls:
                yield scrapy.Request(page, callback=self.parse_article)