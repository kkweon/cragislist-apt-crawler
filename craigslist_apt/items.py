# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import datetime as dt
import re

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst


def get_bedroom(value):
    try:
        return re.findall(r"(\d+)br", value)[0]

    except:
        return ""


def get_size(value):
    try:
        return re.findall(r"(\d+)ft", value)[0]

    except:
        return ""


def clean_price(value):
    if "$" in value:
        value = value.replace("$", "")
        return value.strip()


def format_date(value):
    format = "%Y-%m-%dT%H:%M:%S%z"
    date = dt.datetime.strptime(value, format)
    return date.strftime("%Y-%m-%d %H:%M")


def strip_value(value):
    value = re.sub(r"\\", " ", value)
    value = re.sub(r"\W", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip().lower()


def get_area_code(value):
    return re.findall(r".org/(\w+)/.+", value)[0]


class CraigslistAptItem(scrapy.Item):
    """
    title,
    price,
    pub_date,
    city,
    link,
    content,
    address
    """
    title = scrapy.Field(
        input_processor=MapCompose(strip_value),
        output_processor=Join(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(clean_price),
        output_processor=TakeFirst(),
    )
    pub_date = scrapy.Field(
        input_processor=MapCompose(format_date),
        output_processor=Join(),
    )
    city = scrapy.Field(
        input_processor=MapCompose(strip_value),
        output_processor=Join(),
    )
    link = scrapy.Field(
        output_processor=Join(),
    )
    content = scrapy.Field(
        input_processor=MapCompose(strip_value),
        output_processor=Join(),
    )

    area = scrapy.Field(
        input_processor=MapCompose(get_area_code),
        output_processor=Join(),
    )

    address = scrapy.Field(
        input_processor=MapCompose(strip_value),
        output_processor=Join(),
    )

    bedroom = scrapy.Field(
        input_processor=MapCompose(get_bedroom),
        output_processor=Join(),
    )
    size = scrapy.Field(
        input_processor=MapCompose(get_size),
        output_processor=Join(),
    )
