import scrapy


class PakwheelsItem(scrapy.Item):
    
    car_name = scrapy.Field()
    car_address = scrapy.Field()
    car_price = scrapy.Field()
    description = scrapy.Field()
    specifications = scrapy.Field()
    car_features = scrapy.Field()
    car_image = scrapy.Field()
    seller_info = scrapy.Field()
    
