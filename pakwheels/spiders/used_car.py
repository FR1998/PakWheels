import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from urllib.parse import urljoin
from ..items import PakwheelsItem


class PakWheelSpider(CrawlSpider):
    
    name = "used_car"
    allowed_domains = ["pakwheels.com"]
    start_urls = ["https://www.pakwheels.com/used-cars/search/-/"]
    base_url = "https://www.pakwheels.com"
    
    rules = [
        Rule(LinkExtractor(allow= "used-cars/", restrict_css = "a.car-name.ad-detail-path", attrs= "href"), callback="parse_product_page",follow=True),
        Rule(LinkExtractor(allow= "used-cars/search/", restrict_css= "ul.pagination.search-pagi li.next_page", attrs="href" ), follow=True)
    ]
           
                   
    def extract_car_name(self,response):
        name = response.css("h1::text").get()
        
        return name
    
    
    def extract_car_address(self,response):
        address = response.css(".detail-sub-heading a::text").get()
        
        return address
    
    
    def extract_car_price(self,response):
        pricing = response.css('script[type="application/ld+json"]::text').getall()
        for price in pricing:
            car_price = json.loads(price)
            price_of_car = car_price.get('offers', {}).get('price')
            
        return price_of_car

    
    def extract_car_description(self,response):
        car_description = response.css(".fs16 p::text, .fs16 a::text").getall()
        
        return car_description
    
    
    def extract_specs(self,response):
        specifications =response.css(".ad-data+ li::text").getall()
        
        return specifications 
    
    
    def extract_features(self,response):
        features = response.css("#scroll_car_info .nomargin li::text").getall()

        return features               
    
    
    def extract_images(self,response):
        car_imgages = response.css(" #myCarousel img::attr(src)").getall()
        
        return car_imgages
    
    
    def extract_seller_info(self,response):
        name = response.css(".owner-detail-main h5::text").get()
        time_on_app = response.css(".member::text").get()
        phone_num = response.css(".generic-green.fs16::text").get()
        info = {
            "name":name,
            "acc_information":time_on_app,
            "seller_phone_number":phone_num
        }
        
        return info
    
            
    def parse_product_page(self,response):
        item = PakwheelsItem()
        
        item["car_name"] = self.extract_car_name(response)
        item["car_address"] = self.extract_car_address(response)
        item["car_price"] = self.extract_car_price(response)
        item["description"] = self.extract_car_description(response)
        item["specifications"] = self.extract_specs(response)
        item["car_features"] = self.extract_features(response)
        item["car_image"] = self.extract_images(response)
        item["seller_info"] = self.extract_seller_info(response)
        
        yield item
        
