import scrapy


class WhoccSpider(scrapy.Spider):
    name = 'whocc'
    allowed_domains = ['www.whocc.no']
    start_urls = ['https://www.whocc.no/atc_ddd_index/?code=A&showdescription=no']

    def parse(self, response):
        # Extract the links to the second level pages
        links = response.xpath('//p/b/a[starts-with(@href, "./?code=")]/@href')
        category = response.xpath('//div[@id="content"]/b/a/text()')[0]
        for link in links:
            yield response.follow(link, callback=self.parse_second_level, meta={'category': category})

    def parse_second_level(self, response):
        # Extract the text nodes between <p> and <b> using Xpath
        texts = response.xpath('//p/text()[not(parent::b) and not(parent::a)]').getall()
        
        # Join the texts together into a single string
        text = ''.join(texts)
        
        # Split the string on the line breaks to get the codes and names
        lines = text.split('\n')
        
        # Iterate over the lines and yield as dictionary
        codes = [line.split(' ', 1)[0].strip() for line in lines if line.strip()]
        names = response.xpath('//b/a/text()').getall()
        category = response.meta['category']
        for code in codes:
            name = names[codes.index(code)]
            yield {
                'Code': code,
                'Nom': name,
            }

#scrapy crawl whooc -o whocc_data.csv
