# NAACP MEDIA RESEARCH

CS506 Spark! project

Yufeng Chen, yufeng72@bu.edu

Jiaqi Sun, sjq@bu.edu

Ruotian Liu, rtliu@bu.edu

## SOME INSTRUCTIONS ON HOW TO RUN OUR CODE:

PS: to successfully run our codes, please install all tools and packages we used using pip, and make sure to follow our project structure (or you can change all target directories in our codes into your own valid path).

### Collect data
Run [get_links.py](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/get_links.py) first to get 3 txt files ([bostonglobe.txt](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/bostonglobe.txt), [wbur.txt](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/wbur.txt) and [wgbh.txt](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/wgbh.txt)) for 3 websites. Our Scrapy spider is [globespider.py](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/globe/globe/spiders/globeSpider.py). To run Scrapy for data collecting, you should open terminal, locate the [spiders](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/tree/master/globe/globe/spiders) folder and run:

```
scrapy runspider globeSpider.py -o resultname.json
```

You need to change the filename in [line 11](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/globe/globe/spiders/globeSpider.py#L11) and use different xpath filter ([line 29](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/globe/globe/spiders/globeSpider.py#L29) for Boston Globe, [line 30](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/globe/globe/spiders/globeSpider.py#L30) for WGBH and WBUR) in our code to get all three websites' results. For more instructions on hwo to use Scrapy, you can check [A primer on web scraping and the Wayback machine by John C. Merfeld](https://github.com/johncmerfeld/wayback). We really thank John for his excellent work, and it really helped us a lot.


The whole data collecting process will take a long time, days, or even weeks if there are other server problems, so we splitted these 3 txts into more small sub files when we did this step. We stored our data in [raw data](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/tree/master/raw%20data) folder, and suggest you simply download it to see what we've collected.

### Filter news about black people
Make sure you've already generated (by run [combine.py](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/combine.py) on [raw data](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/tree/master/raw%20data) or downloaded [classified data](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/tree/master/classified%20data), then run [keywords_filter_black.py](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/keywords_filter_black.py). The results should be generated in [relevent data](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/tree/master/relevant%20data) folder.

Calculate coverage: make sure you've already generated (by run [combine.py](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/combine.py) on [raw data](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/tree/master/raw%20data)) or downloaded [classified data](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/tree/master/classified%20data), then run [coverage.py](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/coverage.py). The result should be printed on your screen. It's also recorded in [statistics_final.xlsx](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/statistics_final.xlsx) sheet one.

### Sentiment analysis
Make sure you've already generated (by run [combine.py](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/combine.py) on [raw data](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/tree/master/raw%20data) and [keywords_filter_black.py](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/keywords_filter_black.py) on [classified data](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/tree/master/classified%20data) or downloaded [classified data](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/tree/master/classified%20data) and [relevent data](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/tree/master/relevant%20data), then run [sentiment_analysis_black.py](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/sentiment_analysis_black.py) and [sentiment_analysis_all.py](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/sentiment_analysis_all.py). The results should be stored in [sentiment_analysis_black.csv](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/sentiment_analysis_black.csv) and [sentiment_analysis_all.csv](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/sentiment_analysis_all.csv). The results are also recorded in [statistics_final.xlsx](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/statistics_final.xlsx) sheet one.

### Look for popular topics
Make sure you've already generated (by run [combine.py](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/combine.py) on [raw data](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/tree/master/raw%20data)) or downloaded [classified data](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/tree/master/classified%20data), then run [get_topics.py](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/get_topics.py) to get popular topics and see visulization results like [topic_crime_black.png](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/topic_crime_black.png) and [topic_crime_all.png](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/topic_crime_all.png). you can change code to get all popular topics for the past five years. The results are stored in [5topics_black.txt
](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/5topics_black.txt) and [5topics_all.txt
](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/5topics_all.txt), The results are also stored in [statistics_final.xlsx](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/statistics_final.xlsx) sheet two.

## FOR NON-TECHNICAL AUDIANCE

If you are non-technical audiance who just want to see what we've achieved, please have a look at our project [report](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/Report%26Poster/NAACP%20Final%20Report.pdf) and [poster](https://github.com/AllenChenGH/NAACP_MEDIA_RESEARCH/blob/master/Report%26Poster/NAACP%20Poster.pdf). This should give you an basic idea of what we've done.
