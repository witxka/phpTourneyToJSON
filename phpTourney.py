#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import json
import datetime
from scrapy.crawler import CrawlerProcess
from operator import itemgetter

class PhpTourneySpider(scrapy.Spider):
    name = "phpTourney"

    start_urls = [
        "https://quake.su/?sid=155&mod=matches&act=view_all"
    ]

    def parse(self, response):
        for info in response.css(".largebox").xpath(".//tbody").xpath(".//tr"):
            matchLink = response.urljoin(info.xpath(".//a/@href").get())
            matchInfo = {}
            matchInfo["round"] = info.xpath(".//a/text()").get().strip()
            matchInfo["link"] = matchLink
            yield  response.follow(matchLink, self.parse_match,  cb_kwargs=matchInfo)

    def parse_match(self, response, round,link):
        confirmedTime = datetime.datetime.strptime(response.css(".largebox").css(".notice").re(r"confirmed: [0-9\-]+ [0-9:]+")[0].replace("confirmed: ",""),"%Y-%m-%d %H:%M:%S").isoformat() + "+00:00"
        yield {
            "players": response.css(".largebox").xpath(".//a/text()").getall()[1:],
            "round": round,
            "link": link,
            "info": response.css(".largebox").xpath(".//b/text()").getall(),
            "confirmed": confirmedTime 
        }

process = CrawlerProcess(settings={
    "FEEDS": {
        "phpTourney.json": {"format": "json", "overwrite": True},
    },
    "LOG_ENABLED": False
})

process.crawl(PhpTourneySpider)
process.start() # the script will block here until the crawling is finished

with open('phpTourney.json') as file:
    data = json.load(file)
    dataSorted = sorted(data, key=itemgetter('confirmed'))

with open('phpTourney.json', 'w') as outfile:
    json.dump(dataSorted, outfile) 
