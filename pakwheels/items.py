import scrapy


class PakwheelsItem(scrapy.Item):
    
    Name = scrapy.Field()
    City = scrapy.Field()
    Price = scrapy.Field()
    Year = scrapy.Field()
    Ad_information = scrapy.Field()
    Picture = scrapy.Field()
    Car_type = scrapy.Field()
    Engine = scrapy.Field()
    
