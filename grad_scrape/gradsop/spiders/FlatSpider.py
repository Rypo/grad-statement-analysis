import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from ..items import FlatDoc
from scrapy.loader.processors import TakeFirst


class DocSpider(scrapy.Spider):
	name = "flatsop"
	# TODO: use beautful soup to strip out this element
	google_ad = '<div class="pTx"><div class="ads fr"><ins class="adsbygoogle iB" style="width:300px;height:250px" data-ad-client="ca-pub-4504722976547079" data-ad-slot="9016811480"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script><div class="cb"></div></div>'

	def start_requests(self):

		start_urls = ['']
		for url in start_urls:
			yield scrapy.Request(url=url, callback=self.parse_next)

	def parse_next(self, response):
		for a in response.css('div.mbot.pbot a'):
			yield response.follow(a, callback=self.parse)

	def parse(self, response):
		doc = FlatDoc()

		doc['slug'] = response.url.split("/")[-2]
		# doc['sup_title'] = response.css('main h1::text').get()  # main doc title

		# container = response.css('')
		articles = response.css('div.dbg.br.AR article')
		for i, article in enumerate(articles):
			doc['url_id'] = response.url.split("/")[-2].split('-')[-1]
			# Content
			# post['post_id'] = article.css('div.fr a::attr(href)').get()
			doc['seqnum'] = i
			doc['post_date'] = article.css('div.fr::text').get().strip()
			# raw html, post processing will be required. If ::text selector is used, styled text is omitted
			doc['post_content'] = article.css('div.pTx').get().strip(self.google_ad)

			# author meta-data
			doc['user_id'] = article.css('div.fl a::attr(href)').get().split('=')[-1]  # .attrib['href'].
			doc['name'] = article.css('div.fl a::attr(title)').get().strip('Author: ')  # Remove prefix "Author: "
			doc['username'] = article.css('div.fl a b::text').get()
			doc['user_threads'], doc['user_posts'] = article.css('div.fl span::text').get().split(' / ')
			doc['user_likes'] = article.css('div.fl span i::text').get()

			yield doc

