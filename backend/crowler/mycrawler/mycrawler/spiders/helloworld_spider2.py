import scrapy
from urllib.parse import urlparse
import re
import logging


class HelloWorldSpider(scrapy.Spider):
    print("hello world____________________________________________________________________________________________________________________")
    name = "extract"
    city_names = ["Kegalle", "Deraniyagala", "warakapola", "yatiyanthota", "bulathkopitiya"]

    """def __init__(self, city_name, *args, **kwargs):
        super(HelloWorldSpider, self).__init__(*args, **kwargs)
        self.start_url = start_url
"""

    def __init__(self, start_url=None, *args, **kwargs):
        super(HelloWorldSpider, self).__init__(*args, **kwargs)
        self.start_url = start_url

    def start_requests(self):
        if self.start_url:

            yield scrapy.Request(url=self.start_url, callback=self.parse)
        else:
            for city in self.city_names:

                yield scrapy.Request(url=f"http://{city}.cn/", callback=self.parse)

        #[
            #'https://doa.gov.lk/',
            #'https://en.wikipedia.org/wiki/List_of_towns_in_Sri_Lanka',
            #'https://en.wikipedia.org/wiki/Districts_of_Sri_Lanka',
            #'https://en.wikipedia.org/wiki/List_of_Sri_Lanka',
            #'https://en.wikipedia.org/wiki/List_of_villages_in_Sri_Lanka'
        #]

        # Initiate crawl
        #for url in start_url:
         #   yield scrapy.Request(url=url, callback=self.parse)
        #yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        # Extract the title of the current page
        title = response.css('title::text').extract_first().strip()
        page_text = response.css('body').get()
        text_content = re.sub(r'<[^>]+>', '', page_text)
        lines = text_content.splitlines()

        relevant_lines = []
        data = {}

        for line in lines:
            for city in self.city_names:
                if city.lower() in line.lower():  # Case-insensitive search
                    relevant_lines.append(line.strip())

        patterns = {
            'year_month_day': r"\b(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])\b",

            #'year': r"\b(19|20)\d{2}\b",  # Matches years like 2020, 1995, etc.
            'area': r"\d+\s*(hectares|acres|square meters|sq km|km2)",  # Matches area (e.g., 10 hectares)
            'yield': r"\b(\d+(?:\.\d+)?\s*(tons?|kg|metric tons?|bushels?))\b",  # Matches yield (e.g., 200 kg, 30 tons)
            'price': r"\b(\$\d+(?:\.\d{2})?|₹\d+(?:\.\d{2})?|€\d+(?:\.\d{2})?|£\d+(?:\.\d{2})?|¥\d+(?:\.\d{2})?|₣\d+(?:\.\d{2})?|₨\d+(?:\.\d{2})?|₽\d+(?:\.\d{2})?|₹\d+(?:\.\d{2})?|₹\d+(?:\.\d{2})?|A\$\d+(?:\.\d{2})?|C\$\d+(?:\.\d{2})?|₲\d+(?:\.\d{2})?|₴\d+(?:\.\d{2})?|₾\d+(?:\.\d{2})?|₡\d+(?:\.\d{2})?|₱\d+(?:\.\d{2})?|₺\d+(?:\.\d{2})?|S\$?\d+(?:\.\d{2})?|KSh\d+(?:\.\d{2})?|₺\d+(?:\.\d{2})?|₹\d+(?:\.\d{2})?)\b",
            'crop': r"\b(wheat|rice|corn|soybeans?|barley|oats|cotton|potatoes?|sweet potatoes?|tomatoes?|carrots?|onions?|lettuce|spinach|cabbage|broccoli|cauliflower|cucumber|bell peppers?|peas?|beans?|lentils|chickpeas?|garlic|pumpkin|squash|zucchini|eggplant|radishes?|leeks|asparagus|artichokes|turnips|beets|parsley|cilantro|basil|rosemary|thyme|oregano|chives|dill|mint|sage|coriander|pumpkin|okra|cantaloupe|watermelon|strawberries?|blueberries?|raspberries?|blackberries?|grapes|apples?|pears?|peaches?|plums?|cherries?|apricots?|mangoes?|oranges?|lemons?|bananas?|kiwi|avocados?|pineapple|papaya|figs?|dates?|pomegranates?|almonds?|cashews?|walnuts?|pecans?|hazelnuts?|macadamia nuts?|pine nuts?|peanuts?|sesame seeds?|sunflower seeds?|flax seeds?|hemp seeds?|canola|mustard|safflower|soybean|flax|sunflower|rapeseed|chili peppers?|tobacco|cotton|coconut|olive|sorghum|millet|teff|rye|spelt|quinoa|amaranth|buckwheat|triticale|chia|mustard greens|collard greens|sweet corn|taro|chayote|bamboo|ginseng|ginger|turmeric|wasabi|bamboo shoots|fennel|sorghum|cassava|yams|arrowroot|kale|brussels sprouts|rutabaga|chili peppers|hops|lucerne|alfalfa|clover|switchgrass|timothy hay|bermudagrass|bluegrass|ryegrass|fescue|cottonseed|tobacco|industrial hemp|soybean|poppy|ginseng|peanuts|quinoa|millets|chia|saffron|kale|hemp|rubber|tea|cinnamon|cardamom|cloves?|pepper|nutmeg|vanilla|turmeric|sri lanka tea|cinnamon leaf|cinnamon bark|betel leaf|areca nut|papaya|mango|jackfruit|banana|king coconut|cashew|sri lankan coconut|spices|growing tea|cinnamon sri lanka|sri lanka rubber|clove|coconut oil|pulses|sri lankan herbs|sri lankan rice|jaggery|curry leaves|turmeric sri lanka|kohlrabi|pumpkin sri lanka|sri lankan peppers|sri lankan vegetables|curry plants|sri lankan fruits|sri lankan spices|curry leaf|coconut sugar|tamarind|liquid tamarind|sri lankan vanilla)\b",

            'fertilizer': r"\b(fertilizer|manure|compost|urea|potash|ammonium nitrate|ammonium sulfate|calcium nitrate|sodium nitrate|aqua ammonia|anhydrous ammonia|UAN|superphosphate|triple superphosphate|monoammonium phosphate|diammonium phosphate|rock phosphate|bone meal|fish meal|fish emulsion|seaweed extract|alfalfa meal|green manure|peat moss|coffee grounds|rice hulls|mushroom compost|worm castings|blood meal|green waste compost|lime|gypsum|osmocote|polymer-coated urea|sulfur-coated urea|controlled-release fertilizers|NPK|foliar fertilizers|liquid fertilizers|hydroponic fertilizers|magnesium sulfate|potassium chloride|potassium sulfate|potassium nitrate|sodium molybdate|cobalt sulfate|borax|zinc sulfate|iron sulfate|manganese sulfate|copper sulfate|boron|calcium nitrate|molybdenum fertilizers|cobalt nitrate|potassium magnesium sulfate|plant food|organic plant food|organic fertilizer|NPK 10-10-10|NPK 15-15-15|NPK 20-20-20|NPK 16-8-8|fertilizer spikes|fertilizer tablets|ammonium phosphate|ammonium carbonate|ammonium chloride|calcium ammonium nitrate|calcium phosphate|magnesium nitrate|magnesium chloride|nitrogen fixers|humus|dolomitic lime|lime sulfur|seaweed powder|worm tea|guano|bat guano|guano fertilizer|kelp meal|liquid kelp|compost tea|perlite|vermiculite|micronutrient blends|granular fertilizers|slow-release fertilizer|microbe inoculants|nitrogen-rich fertilizers|phosphorus-rich fertilizers|potassium-rich fertilizers|organic fertilizers|bio-fertilizers|composted manure|humic acid|fulvic acid|biochar|cattle manure|chicken manure|sheep manure|duck manure|horse manure|rabbit manure|goat manure|earthworm humus|guano|seaweed liquid|bio-compost|bone char|blood and bone|fish hydrolysate|fish protein|organic NPK|pelleted fertilizer|fertilizer solution|synthetic fertilizers|liquid plant food|fertilizer salts|nitrogenous fertilizers|phosphatic fertilizers|potassic fertilizers|mineral fertilizers|trace element fertilizers|potassium nitrate|monoammonium sulfate|potassium silicate|micronutrient foliar|fertilizer formulations|foliar spray|agricultural chemicals|nitrogen fertilizer|phosphorus fertilizer|potassium fertilizer|urea-ammonium nitrate solution)\b"

        }

        for field, pattern in patterns.items():
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                data[field] = match.group(0)
        # Yield the current page's title and URL

        date_pattern = r"\d{4}-\d{2}-\d{2}.*\b(farming|harvest|season)\b"
        date_match = re.search(date_pattern, page_text, re.IGNORECASE)
        if date_match:
            data['date'] = date_match.group(0)
        yield {
            'title': title,
            'url': response.url,
            'relevant_lines': relevant_lines,
            'data': data,
        }

        # Extract all links from the current page
        links = response.css('a::attr(href)').extract()
        #print(f"Scraping URL: {response.url} ______________________________________________________________________________________________________________________")  # This will print the URL being processed

        dom = response.url
        #print(dom, "**********************************************************************************")
        domains = urlparse(response.url).netloc
        print(domains, "(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((")
        # Follow links to other pages
        for link in links:

            absolute_url = response.urljoin(link)

            # Follow the link if it's within the same domain
            if any(domain in absolute_url for domain in [domains]):
                yield scrapy.Request(url=absolute_url, callback=self.parse)
