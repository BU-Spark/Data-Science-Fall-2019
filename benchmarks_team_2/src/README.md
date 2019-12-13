
## Directory structure

1. Jupyter :Notebook demos
2. Scraping : Code for scraping
3. requirements.txt : library requirements to run model

For scraping the masscases, you need to:
- enter fetch('url to website') in the Scrapy Console
- find the urls in the HTML via Xpath
- convert the list to a dataframe, and convert to a csv file.
- strip away the html tags to have all the urls to the opinions.

- now cd into the scraping directory and enter the following in the command prompt: `Scrapy name_of_spider spider.py`
