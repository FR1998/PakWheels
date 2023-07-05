from ..items import PakwheelsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule


class UsedCarSpider(CrawlSpider):
    
    name = "used_car"
    page_num = 2
    allowed_domains = ["pakwheels.com"]
    start_urls = ["https://www.pakwheels.com"]
    
    rules = [
        Rule(LinkExtractor(allow="/used-cars/search/-/"), callback="parse"),
    ]

    def parse(self, response):

        items = PakwheelsItem()
        
        name = response.css(".ad-detail-path h3::text").getall()
        city = response.css(".search-vehicle-info li::text").getall()
        price = response.css(".price-details::text").getall()
        year = response.css(".search-vehicle-info-2 li:nth-child(1)::text").getall()
        car_type = response.css(".fs13 li:nth-child(5)::text").getall()
        engine = response.css(".fs13 li:nth-child(4)::text").getall()
        ad_info = response.css(".dated::text").getall()
        picture = response.css(".pic::attr(src)").getall()

        for name,city,price,year,car_type,engine,ad_info,picture in zip(
            name,city,price,year,car_type,engine,ad_info,picture
        ):
            items = {
            "Name": name.strip(),
            "City": city.strip(),
            "Price": price.strip(),
            "Year": year.strip(),
            "Car_type": car_type.strip(), 
            "Ad_information": ad_info.strip(),
            "Engine": engine.strip(),
            "Picture": picture.strip()
            }
        
            yield items
            
            next_page = f"{response.url}?page={UsedCarSpider.page_num}"
            if UsedCarSpider.page_num < 2000:
                UsedCarSpider.page_num += 1
                yield response.follow(next_page, callback = self.parse)
                
