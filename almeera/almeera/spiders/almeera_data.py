import json

import scrapy
from ..items import AlmeeraItem




class AlmeeraDataSpider(scrapy.Spider):
    name = "almeera_data"
    allowed_domains = ["almeera.online"]
    start_urls = ["https://almeera.online"]
    file_created=False


    def parse(self, response):
        i=1


        categories=response.xpath('//*[@id="sidebar-first"]/div/div[2]/div[1]/div/ul/li')

        for category in categories:
            category_name=category.xpath('//*[@id="content"]/div/div/div[3]/div/ul/li['+str(i)+']/a/span[2]/text()').extract_first()
            category_img_url=category.xpath('//*[@id="content"]/div/div/div[3]/div/ul/li['+str(i)+']/a/span[1]/img/@src').extract_first()
            category_pg_url=response.urljoin(category.xpath('//*[@id="content"]/div/div/div[3]/div/ul/li['+str(i)+']/a/@href').extract_first())






            yield  scrapy.Request(category_pg_url,callback=self.parse_subcategories,cb_kwargs={'category_name':category_name,'category_img_url':category_img_url})

            i+=1
            if i>5:
                break



    def parse_subcategories(self,response,category_name,category_img_url):

        i=1

        subcategories=response.xpath('//*[@id="content"]/div/div/div[3]/div/ul/li')

        for subcats in subcategories:
            if i>len(subcategories):
                break
            subcategory_name=subcats.xpath('//*[@id="content"]/div/div/div[3]/div/ul/li['+str(i)+']/a/span[2]/text()').extract_first()
            subcategory_url=response.urljoin(subcats.xpath('//*[@id="content"]/div/div/div[3]/div/ul/li['+str(i)+']/a/@href').extract_first())
            subcategory_img_url=subcats.xpath('//*[@id="content"]/div/div/div[3]/div/ul/li['+str(i)+']/a/span[1]/img/@src').extract_first()





            i+=1
            yield scrapy.Request(subcategory_url,callback=self.parse_products,cb_kwargs={'category_name':category_name,'category_img_url':category_img_url,'subcategory_name':subcategory_name,'subcategory_img_url':subcategory_img_url,'visited':False})

    def parse_products(self,response,**kwargs):
        i=1


        item = AlmeeraItem()





        products=response.css('li.product-cell.box-product')
        product_list=[]
        clean_image_urls=[]

        for product in products[6:]:
            if i > 5:
                break
            product_name=product.css('a.fn.url::attr(href)').extract_first()
            product_img_url=product.css('img.photo::attr(src)').extract_first()

            clean_image_urls.append(response.urljoin(product_img_url))

            product_price=product.css('span.price.product-price::text').extract_first()




            product_dict={
                'product_name':product_name,
                'product_img_url':product_img_url,
                'product_price':product_price,

            }

            product_list.append(product_dict)
            yield scrapy.Request(response.urljoin(product_name), callback=self.parse_SKU,cb_kwargs={'product_dict':product_dict})




            i += 1



        item['image_urls']=clean_image_urls
        item['category_name'] = kwargs.get('category_name')
        item['category_img_url'] = kwargs.get('category_img_url')
        item['subcategory_name'] = kwargs.get('subcategory_name')
        item['subcategory_img_url'] = kwargs.get('subcategory_img_url')
        item['products']=product_list
        yield item




        if kwargs.get('visited'):

            return





        next_page=response.css('a.page-2::attr(href)').extract_first()

        if next_page:
         yield scrapy.Request(response.urljoin(str(next_page)),callback=self.parse_products,cb_kwargs={'category_name':kwargs.get('category_name'),'category_img_url':kwargs.get('category_img_url'),'subcategory_name':kwargs.get('subcategory_name'),'subcategory_img_url':kwargs.get('subcategory_img_url'),'visited':True})

    def parse_SKU(self,response,product_dict):
        product_SKU=response.css('span.value::text').extract_first()
        check=True
        for char in product_SKU:
            if not char.isdigit():
                check=False
        if check:
            product_dict['products_SKU']=product_SKU
