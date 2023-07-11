import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from pakwheels.items import CarItem


class PakWheelSpider(CrawlSpider):
    name = "pak_wheel_spider"
    allowed_domains = ["pakwheels.com"]
    start_urls = ["https://www.pakwheels.com/used-cars/search/-/"]
    base_url = "https://www.pakwheels.com"
    
    rules = [
        Rule(
            LinkExtractor(
                allow="used-cars/", 
                restrict_css="a.car-name.ad-detail-path", 
                attrs="href"
            ), 
            callback="parse_product_page",
            follow=True
        ),
        Rule(
            LinkExtractor(
                allow="used-cars/search/", 
                restrict_css="ul.pagination.search-pagi li.next_page", 
                attrs="href" 
            ), 
            follow=True
        )
    ]
                        
    def extract_car_name(self, response):
        return response.css("h1::text").get()
    
    def extract_car_address(self, response):
        return response.css(".detail-sub-heading a::text").get()
    
    def extract_car_price(self, response):
        pricing = response.css("script[type='application/ld+json']::text").getall()
        for price in pricing:
            car_price = json.loads(price)
            price_of_car = car_price.get("offers", {}).get("price")
            
        return price_of_car

    def extract_car_description(self, response):
        return response.css(".fs16 p::text, .fs16 a::text").getall()
    
    def extract_specs(self, response):
        return response.css(".ad-data+ li::text").getall()
        
    def extract_features(self, response):
        return response.css("#scroll_car_info .nomargin li::text").getall()

    def extract_images(self, response):
        return response.css("#myCarousel img::attr(src)").getall()
    
    def extract_seller_info(self, response):
        name = response.css(".owner-detail-main h5::text").get()
        time_on_app = response.css(".member::text").get()
        phone_num = response.css(".generic-green.fs16::text").get()
        info = {
            "name":name,
            "acc_information":time_on_app,
            "seller_phone_number":phone_num
        }

        return info
    
    def extract_seller_comments(self, response):
        return response.css("#scroll_seller_comments+ div::text").getall()
                   
    def parse_product_page(self, response):
        item = CarItem()
        
        item["car_name"] = self.extract_car_name(response)
        item["car_address"] = self.extract_car_address(response)
        item["car_price"] = self.extract_car_price(response)
        item["description"] = self.extract_car_description(response)
        item["specifications"] = self.extract_specs(response)
        item["car_features"] = self.extract_features(response)
        item["car_image"] = self.extract_images(response)
        item["seller_info"] = self.extract_seller_info(response)
        item["seller_comments"] = self.extract_seller_comments(response)
        
        yield item
        
