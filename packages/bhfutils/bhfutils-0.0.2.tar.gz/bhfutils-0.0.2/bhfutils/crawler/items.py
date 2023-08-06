# -*- coding: utf-8 -*-

# Define here the models for your scraped items

from scrapy import Item, Field


class RawResponseItem(Item):
    appid = Field()
    crawlid = Field()
    url = Field()
    response_url = Field()
    status_code = Field()
    success = Field()
    exception = Field()
    encoding = Field()
    playground_id = Field()
    attrs = Field()


class MenuResponseItem(RawResponseItem):
    groupCategoryName = Field()
    groupName = Field()
    groupUrl = Field()


class ProductResponseItem(RawResponseItem):
    productUrl = Field()
    groupId = Field()
    imageUrl = Field()
    name = Field()
    details = Field()
    price = Field()


class ProductDetailsResponseItem(RawResponseItem):
    productUrl = Field()
    groupId = Field()
    imageUrl = Field()
    name = Field()
    details = Field()
