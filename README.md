## Pathfinder Interview Exercise
Interviewee: Daniel Sim

## Overview
A web app that enables users to find University Courses offered in the UK by selecting UK SIC (Industry Classification) and Geographical Location

Both data sets are public domain:
- https://www.ons.gov.uk/methodology/classificationsandstandards/ukstandardindustrialclassificationofeconomicactivities/uksic2007
- https://www.hesa.ac.uk/collection/c17061/unistats_dataset_file_structure

## Requires
- Ubuntu 16.04 (and follwing service installed with apt-get)
  - NodeJS 4.2+
  - ElasticSearch 6+
- Python 3.6+ (and following modules installed with pip)
  - Pandas 0.22+
  - TQDM
  - googlemaps
  - nltk
  - gensim
- ReactiveSearch (https://reactjs.org/tutorial/tutorial.html)

## Run Instructions
- Get data (see README.md in ./data)
- Run NodeJS and Elasticsearch services
    - Add following lines in /etc/elasticsearch/elasticsearch.yml
```
http.cors.enabled : true
http.cors.allow-origin : "*"
http.cors.allow-headers: "X-Requested-With, Content-Type, Content-Length, Authorization"
```
- Wrangle and import data to Elasticsearch
  - run:
    - `./import_trees.py`
    - Run index put command found in `elastic_search_commands.txt`
    - `./import_data.py`
- Run nodejs server
  - `cd ./pf-react`
  - `npm start`
  - Browser opens with web app

## Approach used for this exercise
### Day 1 - Barely MVP
- Explored Django as backend
  - Thinking of doing most data wrangling and queries in Pandas
- Elasticsearch
  - Use current text search capabilities
- Explore preserving Unistats XML data relationships
  - Convert to JSON for upload to elasticsearch
  - Went with loading CSV instead of XML in the end for simplicity
- Find frontend widgets for Elasticsearch
  - Went with ReactiveSearch
- Use googlemaps API to get Geography from lat/lon
- UKPRN lookups skipped
  - https://www.ukrlp.co.uk/
- How to infer course industry?
  - Use Verbs, Nouns and Adjectives?
    - Looked at wordnet database
    - http://scrapmaker.com/dir/language
  - Look up course webpage and infer from text
    - A number of links are outdated
- Clean courses without location record
- Clean duplicate courses

### Day 2 - "Human-level?" Semantic Matching
- Wordnet qualitative review
  - Types of semantic path similarities
  - Wordnet synonyms,  hyponyms and hyperyms matching: https://sourcedexter.com/find-synonyms-and-hyponyms-using-python-nltk-and-wordnet%E2%80%8B/
- The above 2 topics are largely just for words,  as you know, Industry Headings and Course Titles are instead more like sentences at times. Word similarity fails to produce accurate results as highlighted here: https://stackoverflow.com/questions/22129943/how-to-calculate-the-sentence-similarity-using-word2vec-model-of-gensim-with-pyt
  - Abbreviations?
  - "Except", "Non-"
- Hence I moved on to document/sentence/paragraph classification:
  - Google Cloud Natural Language API (https://cloud.google.com/natural-language/) It classifies short paragraphs pretty well, the intuition is for us to get a short paragraph from the SIC website (which maps to an industry heading) and compare it's classification to the classification of the description of a Course. If both has matching classification then the probability is high that the course belongs to that industry.
  - Offline methods were also considered. Google has open-sourced it's word2vec trained model with "word vectors for a vocabulary of 3 million words and phrases that they trained on roughly 100 billion words from a Google News dataset" For offline document classification, spin-offs from word2vec like doc2vec (https://radimrehurek.com/gensim/models/doc2vec.html)
  - Feasibility of web scrapping/crawling through the course webpages of universities and the UK Standard Industrial Classification websites was explored with experiments involving off-the-shelf packages like BeautifulSoup (https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
  - Building our own document classifier system was explored. Some inspiration was taken from (https://medium.com/moosend-engineering-data-science/how-to-build-a-machine-learning-industry-classifier-5d19156d692f) Their methods are relatively simple and looks feasible for our use.
  - Named Entity Recognition was experimented with using NLTK - this allows us to tag each word in a sentence with its class which opens the door to much better sentence comprehension (https://pythonprogramming.net/named-entity-recognition-nltk-tutorial/) 

### Day 3 - Successful integration of Word2Vec
- Due to time pressure added basic string matching of courses to industry first
- Integrated Google's pre-trained word cosine similarity model: http://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/
- The current semantic matching is pretty alright (found here: http://damsim.ddns.net:3000/) it uses GenSim Word2Vec and Google's pre-trained neural net that was trained on Google News feeds with a vocabulary of over 3 million words. Cosine distance of the average of word vectors was used to judge relevancy between Course Title and Industry Classification. As Word2Vec only judges similarity between 2 words and both Course Titles and Industry Classification sentences have unique syntax, bespoke tokenization methods were used to convert sentences to words that can be feed into Word2Vec.
- Some human-level capabilities:
  - Selecting "Malt" will bring up courses on Brewing Beer
  - "Racing" brings up Equine Management
  - "Barite", Exploration and Resource Geology
  
### Day 4 - Improved Tokenization and Seperate Industry Division Filters
- Today, in attempts to improve the semantic matching further I've tried 2 more things: 1) Document Similarity With Word Movers Distance (http://jxieeducation.com/2016-06-13/Document-Similarity-With-Word-Movers-Distance/) and 2) A more generalized tokenization method.
- Word Movers Distance did not seem to improve performance, it looks like its tokenization routines were not suited for the task. It also increased processing time of data to upload to Elastic Search from 2 hours to over 30 hours (estimated)
- A more generalized tokenization method looks promising, though it increases the false positives, it also has the the effect of matching more relevant industries to courses. Data upload time was increased from 2 to around 10 hours


## Processing Optimizations
- GoogleMaps API lookups are cached in a pickled dictionary for reuse
- Industry categories tree structure is generated and pickled for reuse
- Similarity scores for Industry vs Course are also cached and pickled
  - This increases processing speed by up to 10 times