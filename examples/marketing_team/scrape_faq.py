import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json
import os
from unidecode import unidecode  # Importing Unidecode for sanitization

class OneLinkDeepSpider(CrawlSpider):
    name = 'onelinkdeep'
    start_urls = ['https://docs.aelf.com/about-aelf']  # Replace with your start URL

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[contains(@class, 'menu__link')]"), 
             callback='parse_item', follow=False),
    )

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        # Extract the page slug from the URL
        url_parts = response.url.rstrip('/').split('/')
        page_slug = url_parts[-1] or 'index'  # Use 'index' if the URL ends with a trailing slash

        # Extracting each question and answer
        sections = response.xpath('//div[@itemscope and @itemtype="https://schema.org/Question"]')
        
        for index, section in enumerate(sections, start=1):
            question = section.xpath('.//span[@itemprop="name"]/text()').get()
            answer = ''.join(section.xpath('.//div[@itemprop="text"]//text()').getall()).strip()

            # Sanitize the question and answer
            sanitized_question = unidecode(question)
            sanitized_answer = unidecode(answer)

            # Create a structured JSON object for each question-answer pair
            qa_data = {
                "text": sanitized_answer,    # Store the answer in the "text" field
                "title": sanitized_question, # Store the question in the "title" field
                "article_id": f"{page_slug}_{index}", # Construct the article_id
                "url": response.url,
            }
            
            # Ensure output directory exists
            os.makedirs('data', exist_ok=True)

            # Save each question-answer pair to a separate JSON file
            page_filename = f"data/{page_slug}_{index}.json"
            with open(page_filename, 'w', encoding='utf-8') as f:
                json.dump(qa_data, f, ensure_ascii=False, indent=4)

            self.log(f'Saved file {page_filename}')