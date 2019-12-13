# NAACP-Media-Research
This is a repository containing information about the NAACP Media Research Project our CS506 course in the fall of 2019.

To scrape The Boston Herald Website, use the HeraldSpiderCrawling.py and follow the instructions found at https://github.com/johncmerfeld/wayback. This will create a mongodb database with your files that you can then convert to
json, csv, etc.

To analyze the data, run the python file most-distinctive-word.py, updating the file pathway to be where you store the data 
files. This will give you an output of the 30 most common words relative to the articles discussing each particular neighborhood.
