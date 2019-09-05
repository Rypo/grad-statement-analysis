# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import csv
from scrapy.exporters import JsonLinesItemExporter, CsvItemExporter
from pathlib import Path


class JsonLinesDocumentPipeline(object):
    """Distribute items across multiple json files according to their 'url_id' field"""

    def open_spider(self, spider):
        self.url_id_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.url_id_to_exporter.values():
            exporter.finish_exporting()
            exporter.file.close()

    def _exporter_for_item(self, item):
        doc_id = item['url_id']
        dpath = Path('gradsop/data')
        if doc_id not in self.url_id_to_exporter:
            f = open(dpath/f'{doc_id}.json', 'wb')
            exporter = JsonLinesItemExporter(f)
            exporter.start_exporting()
            self.url_id_to_exporter[doc_id] = exporter
        return self.url_id_to_exporter[doc_id]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item


class CsvPipeline(object):
    def open_spider(self, spider):
        dpath = Path('gradsop/data')
        self.file = open(dpath/'data_posts_all2.csv', 'wb')
        self.exporter = CsvItemExporter(self.file)

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.start_exporting()
        self.exporter.export_item(item)
        return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class GradsopPipeline(object):
    def process_item(self, item, spider):
        return item
