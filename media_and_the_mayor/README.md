# 506SentimentAnalysis

The objective of this project is to understand the media coverage (news and social media) and the public response to the to the legislative agenda of Martin J. Walsh, the 54th Mayor of Boston. This implies understanding which of the agenda’s priorities were covered by mainstream media, in what quantity, the time of response of mainstream media when covering them with respect to the press release, and the public’s general sentiment regarding such topics.

## Requirements:
nltk==3.4.5
Scrapy==1.8.0
scrapy_splash==0.7.2
mxnet==1.6.0b20191207
Keras==2.3.1
pandas==0.25.3
gluonnlp==0.8.1
numpy==1.17.4
gensim==3.8.1
scikit_learn==0.22
textblob==0.15.3

## A couple of disclaimers...

1. This file simply provides the steps required to run the mainstream media model and it's not the documentation of our project. If you want to find out more about our approach, our experiments and our results please check our _\_Poster.pdf_ (created by @FaizGanz) or our _\_Report.pdf_ file. 

2. No datasets are have been uploaded to this repo, but if you would like to test our model, without having to run our Scraper first, feel free to contact me. 

3. You may need to modify some file path in the code to make it run correctly.

## Code Structure:
* src folder includes all of the data about our project.
* Models includes some pre-train model files.
* Scraper is the scraper we used to scrape data.
* Statistic is the code for statistic analysis.
* data processing includes the code for filtering and cleaning the data.
* lstm folder includes lstm for twitter data, gluon LNP for mainstream media.


## Running the code

### Preparation

1. Clone or download the repo and _cd_ to its local directory. 

2. Run _pip3 install -r requirements.txt_ to download all the dependancies. 

3. In the _src_ folder create a folder named _Datasets_. 

4. Inside the _Datasets_ folder create another one named _Raw_. 

5. Place all the datasets you obtained, either by running the Scraper yourself or by contacting me, inside the _Raw_ folder. 


### Scraper

Scraping is always unpredictable; what ran perfectly yesterday may not work at all today... So, in order to save time and frustration, I would advice contacting me for the datasets. If on the other hand you want to test the Scraper yourself, you can execute it like any other _Scrapy_ project. 


### Running the model

To run the preprocessing and sentiment analysis model just _cd_ to the _src_ folder and run the following commands: 

1. _python3 clean.py_ to remove missing values and align the different datetime formats. 

2. _python3 preprocess.py_ to align the documents' columns, merge the _tags_, _summary_ and _body_ columns and lowercase, tokenize, remove stopwords and lemmatize all the texts _(it may take some time...)_. 

3. _python3 doc2vec.py_ to create the doc2vec model and vectorize the articles _(it may take some time too...)_. 

4. _python3 relevance\_classifier.py_ to create the Feed Forward Neural Network for the articles' relevance-based classification. 

5. _python3 filter\_irrelevant.py_ to filter out all the irrelevant articles from the corpus. 

6. _python3 get\_agenda.py_ to obtain the mayor's agenda topics, using NMF, and map all the articles of the corpus to their respective agenda topic. 

7. _python3 sentiment\_analysis.py_ to train the Gluon NLP sentiment analysis model and perform sentiment predictions on the corpus. 

8. _python3 data\_process.py to clean, tokenize, stemming and lemmatization the data.

9. _python3 lda.py using LDA and NMF algorithm to extract topics from text.

10. _python3 sentiment\_textblob.py sentiment analysis based on Textblob and Vader.

* To run code on LSTM:
  >1. Download data from <br>
     https://www.kaggle.com/kazanova/sentiment140#training.1600000.processed.noemoticon.csv <br>
     and add it under folder /lstm_model/data
  >2. If you want to train the model by you own, run 'python twitter_model.py' under folder /lstm_model.
  >3. If you want to use the model we have already trained, download them from <br>
      https://drive.google.com/file/d/1leABsjuNDAttt5MFwFGSK9vAVQe59bBv/view?usp=sharing <br>
      and add files under folder /lstm_model/model, then run 'python twitter_model.py'
