import scrapy

class WhoccSpider(scrapy.Spider):
    name = 'fourth'
    allowed_domains = ['www.whocc.no']
    start_urls = ['https://www.whocc.no/atc_ddd_index/?code=A&showdescription=no']

    def parse(self, response):
        
        # Extract the text nodes between <p> and <b> using Xpath
        texts = response.xpath('//p/text()[not(parent::b) and not(parent::a)]').getall()
        
        # Join the texts together into a single string
        text = ''.join(texts)
        
        # Split the string on the line breaks to get the codes and names
        lines = text.split('\n')
       
        # Iterate over the lines and yield as dictionary
        codes = [line.split(' ', 1)[0].strip() for line in lines if line.strip()]
        names = response.xpath('//p/b/a/text()').getall()
        for code in codes:
            name = names[codes.index(code)]
            yield {
                'Code': code,
                'Nom': name,
            }
        # Extract the links to the second level pages
        links = response.xpath('//p/b/a[starts-with(@href, "./?code=")]/@href')
        category = response.xpath('//div[@id="content"]/b/a/text()').get()
        for link in links:
            yield response.follow(link, callback=self.parse_second_level, meta={'category': category})

    def parse_second_level(self, response):
        # Extract the text nodes between <p> and <b> using XPath
        texts = response.xpath('//p/text()[not(parent::b) and not(parent::a)]').getall()

        # Join the texts together into a single string
        text = ''.join(texts)

        # Split the string on the line breaks to get the codes and names
        lines = text.split('\n')

        # Iterate over the lines and yield as dictionary
        codes = [line.split(' ', 1)[0].strip() for line in lines if line.strip()]
        names = response.xpath('//p/b/a/text()').getall()
        category = response.meta['category']
        for code in codes:
            name = names[codes.index(code)]
            yield {
                'Code': code,
                'Nom': name,
            }

            # Extract the links to the third level pages
            link = response.xpath(f'//a[starts-with(@href, "./?code={code}")]').attrib['href']
            yield response.follow(link, callback=self.parse_third_level, meta={'code': code, 'category': category})

    def parse_third_level(self, response):
        texts = response.xpath('//p/text()[not(parent::b) and not(parent::a)]').getall()
        # Join the texts together into a single string
        text = ''.join(texts)
        # Split the string on the line breaks to get the codes and names
        lines = text.split('\n')
        # Iterate over the lines and yield as dictionary
        codes = [line.split(' ', 1)[0].strip() for line in lines if line.strip()]
        names = response.xpath('//p/b/a/text()').getall()
        category = response.meta['category']
        for code, name in zip(codes, names):
            yield {
                'Code': code,
                'Nom': name,
            }

            # Extract the links to the fourth level pages
            link = response.xpath(f'//a[starts-with(@href, "./?code={code}")]').attrib['href']
            yield response.follow(link, callback=self.parse_fourth_level, meta={'code': code, 'category': category})

    def parse_fourth_level(self, response):
        texts = response.xpath('//p/text()[not(parent::b) and not(parent::a)]').getall()
        # Join the texts together into a single string
        text = ''.join(texts)
        # Split the string on the line breaks to get the codes and names
        lines = text.split('\n')
        # Iterate over the lines and yield as dictionary
        codes = [line.split(' ', 1)[0].strip() for line in lines if line.strip()]
        names = response.xpath('//p/b/a/text()').getall()
        for code, name in zip(codes, names):
            yield {
                'Code': code,
                'Nom': name,
            }

            # Extract the links to the fifth level pages
            link = response.xpath(f'//a[starts-with(@href, "./?code={code}")]').attrib['href']
            yield response.follow(link, callback=self.parse_fifth_level, meta={'code': code})

    def parse_fifth_level(self, response):
        rows = response.xpath('//ul/table/tbody/tr[position() > 1]')
        for row in rows:
            code = row.xpath('.//td[1]/text()').extract_first(default='').strip()
            name = row.xpath('.//td[2]/a/text()').extract_first(default='').strip()

            if code and name:
                yield {
                    'Code': code,
                    'Nom': name,
                }

