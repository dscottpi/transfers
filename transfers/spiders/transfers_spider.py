# -*- coding: utf-8 -*-
import scrapy
import json

class TransfersSpiderSpider(scrapy.Spider):
    json_player_name = "PLAYER"
    json_link = "LINK"
    json_team_from = "TEAM_FROM"
    json_team_to = "TEAM_TO"
    json_price = "PRICE"

    json_transfers = {}
    json_transfers["transfers"] = {}
    base_url = "http://bbc.co.uk"
    name = "transfers_spider"
    allowed_domains = ["bbc.co.uk"]
    start_urls = (
        'http://www.bbc.co.uk/sport/36681972',
    )

    def write_file(self):
        with open("transfers.json", 'w+') as output_file:
            json.dump(self.json_transfers, output_file, indent=4, sort_keys=True)

    def parse(self, response):
        transfers = response.xpath('//div[@id="story-body"]/p[not(@*) and a]').extract()
        transfers = [x for x in transfers if "<p><a" in x]
        for index, transfer in enumerate(transfers):
            json_transfer = {}
            transfer = transfer.replace("<p>", "")
            transfer = transfer.replace("</p>", "")
            import re
            url = re.findall(r'\"(.+?)\"', transfer)[0]
            name = re.findall(r'\>(.+?)\<', transfer)[0]
            teams = re.findall(r'\[(.+?)\]', transfer)[0].split(' - ')
            prev_team = teams[0]
            new_team = teams[1]
            price = transfer.split(']', 1)[-1]

            if self.base_url in url:
                url = url
            else:
                url = self.base_url + url

            json_transfer[self.json_player_name] = name
            json_transfer[self.json_link] = url
            json_transfer[self.json_team_from] = prev_team
            json_transfer[self.json_team_to] = new_team
            json_transfer[self.json_price] = price
            self.json_transfers["transfers"][index] = json_transfer

        self.json_transfers["SIZE"] = len(self.json_transfers["transfers"]) - 1
        self.write_file()
