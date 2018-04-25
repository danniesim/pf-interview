## Pathfinder Interview Exercise
Interviewee: Daniel Sim

## Requires
- Ubuntu 16.04 (and follwing service installed with apt-get)
  - NodeJS 4.2+
  - ElasticSearch 6+
- Python 3.6+ (and following modules installed with pip)
  - Pandas 0.22+
  - TQDM
  - googlemaps
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
  - run python ./import_data.py
- Run nodejs server
  - `cd ./pf-react`
  - `npm start`
  - Browser opens with web app

## Approach used for this exercise
### Day 1 - Barely MVP Webapp
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
- Abbreviations?
- "Except", "Non-"
 
