import scrapy
from scrapy.loader import ItemLoader
from ..items import FlatDoc
from scrapy.loader.processors import TakeFirst
from ..settings import ST_URL


class SopSpider(scrapy.Spider):
	name = "gradsop"
	start_urls = [ST_URL]

	def parse(self, response):
		# for each thread on the thread list
		for a in response.css('div.mbot.pbot a'):
			yield response.follow(a, callback=self.parse_thread)

		# for each page in page list
		for a in response.css('nav a'):
			yield response.follow(a, callback=self.parse)

	def parse_thread(self, response):
		articles = response.css('div.dbg.br.AR article')

		for i, article in enumerate(articles):
			doc_loader = ItemLoader(item=FlatDoc(), response=response, selector=article, default_output_processor=TakeFirst())

			doc_loader.add_value('url_id', response.url.split("/")[-2].split('-')[-1])
			doc_loader.add_value('slug', response.url.split("/")[-2])
			doc_loader.add_value('thread_title', response.css('main h1::text').get())

			# Content
			doc_loader.add_css('post_date', 'div.fr::text', TakeFirst(), lambda x: x.strip())
			doc_loader.add_value('seqnum', int(i))
			# raw html, post processing will be required. If ::text selector is used, styled text is omitted
			doc_loader.add_css('post_content', 'div.pTx')

			# author meta-data
			doc_loader.add_css('user_id', 'div.fl a::attr(href)')
			doc_loader.add_css('name', 'div.fl a::attr(title)')
			doc_loader.add_css('username', 'div.fl a b::text')

			nthread_post = article.css('div.fl span::text').get().split(' / ')
			doc_loader.add_value('user_threads', nthread_post[0])
			doc_loader.add_value('user_posts', nthread_post[1])
			doc_loader.add_css('user_likes', 'div.fl span i::text')

			yield doc_loader.load_item()