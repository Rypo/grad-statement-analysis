import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from gradsop.items import Author, Post, Document
from scrapy.loader.processors import TakeFirst


class DocSpider(scrapy.Spider):
	name = "graddocs"
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
		n_page_posts = response.css('td.CF.txtR b::text')
		# Page setup
		# container houses the original post and all subsequent responses

		doc = Document()
		doc_posts = []
		doc['url_id'] = response.url.split("/")[-2]
		doc['sup_title'] = response.css('main h1::text').get()  # main doc title

		container = response.css('div.dbg.br.AR')
		articles = container.css('article')
		for i, article in enumerate(articles):
			post = Post()
			author = Author()

			# Content
			post['post_id'] = article.css('div.fr a::attr(href)').get()
			post['is_sop'] = i == 0
			post['post_date'] = article.css('div.fr::text').get().strip()
			# post_loader.add_css('sub_title', 'div.pTx h2::text')  # May or may not have sub title(s)
			# raw html, post processing will be required. If ::text selector is used, styled text is omitted
			post['post_content'] = article.css('div.pTx').get().strip(self.google_ad)

			# author meta-data
			author['user_id'] = article.css('div.fl a::attr(href)').get().split('=')[-1]  # .attrib['href'].

			author['is_op'] = i == 0  # TODO: check for "OP" field on page
			author['name'] = article.css('div.fl a::attr(title)').get().strip('Author: ')  # Remove prefix "Author: "
			author['username'] = article.css('div.fl a b::text').get()
			author['n_threads'], author['n_posts'] = article.css('div.fl span::text').get().split(' / ')
			author['n_likes'] = article.css('div.fl span i::text').get()

			post['post_author'] = author.deepcopy()
			doc_posts.append(post)

		doc['posts'] = doc_posts
		yield doc
