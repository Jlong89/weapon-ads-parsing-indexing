Parsing and Indexing of firearm ads with Apache Tika and Elasticsearch
======================================================================

USC CS572 fall 2015 project. This is the second part of a series of assignments to crawl, index and visualize ads selling firearms on the internet. 

The following is a description of how we parsed and indexed crawled html and images, crawled with Apache Nutch, into an instance of Elastisearch. We leveraged Apache Tika
for content detection and parsing out text and metadata from crawled documents. We also used GeoTopicParser, a Tika Geo NER Tool, to 
identify the name of location of the ads as well as provide long/lat information about each ad. Lastly, we also used Tika-OCR to leverage
Tesseract OCR to obtain textual content from images. 

To use Tika parsing capabilities, we used Tika-python, A Python port of the Apache Tika library that makes Tika available using the Tika REST Server.
The GeoTopicParser was used in a similar way by accessing its capabilitites through a tika server started with the geo parser at another 
local port.

We also indexed already parsed weapon ads data in json documents provided to us by our professor Chris Mattman.

You can see the installation instructions for the technologies used:

Elasticsearch 1.7 at https://www.elastic.co/products/elasticsearch.

elasticsearch-py, python elasticsearch client, at https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html

Apache Tika and Tika server, built from trunk 1.11 at https://github.com/apache/tika/

Tika python, at https://github.com/chrismattmann/tika-python

Tika GeoTopicParser, at http://wiki.apache.org/tika/GeoTopicParser

Setup
=====

Elasticsearch 1.7, tika-server 1.12, and tika python, geo-parser and tika-OCR need to be installed as specified in their respective pages above.
We had a $TIKA_HOME pointing to our tika-trunk home dir. 

In a nutshell, we setup a tika-server running at localhost:9997 for parsing out regular text, and a 'geo' tika-server running at localhost:9998 to
parse out geo related information. We index into an instance of elasticsearch running at localhost:9200. The python scripts in parsing-indexing dir connect to the
tika-server endpoints for parsing and index the parsed out data into the elasticsearch endpoint.

-------------------------------------------------------------------------------------------------------------------------------------------------------

The following steps were performed to setup tika servers  

1. Navigate to home dir of elasticsearch 1.7.3 and start an instance of elastic search:

	`bin/elasticsearch`

	make sure elasticsearch is running by openning localhost:9200 in browser and seeing basic info of instance of elasticsearch

2. Start 'regular metadata' Tika-server in local port 9998:

	`java -jar $TIKA_HOME/tika-server/target/tika-server-1.12-SNAPSHOT.jar`

	make sure tika-server is running by openning localhost:9998 in browser and seeing tika-server welcoming message and commands description

3. Start 'geo metadata' Tika-server in local port 9997:
	```
	java -classpath $HOME/src/location-ner-model:$HOME/src/geotopic-mime:$TIKA_HOME/tika-server/target/tika-server-1.12-SNAPSHOT.jar  org.apache.tika.server.TikaServerCli --port=9997
	```

	make sure tika-server is running by openning localhost:9997 in browser and seeing tika-server welcoming message and commands description

Parsing and Indexing
====================

After the setup above, we can use the python scripts in the parsing-indexing dir to parse and index documents. The scripts use tika by connecting to the
tika-server endpoints setup at localhost:9997 and localhost:9998 to parse out regular text and geo information respectively. Then, parsed out
data is indexed into the elasticsearch instance running at localhost:9200.

-------------------------------------------------------------------------------------------------------------------------------------------------------

1. 	Create 'weapons_tika_index' and 'weapon_doc' mapping, and parse and index documents into the new index:

	
	```
	python Tika-ES-Index-Mapping.py
	python Tika-ES-Indexing.py <docs dir>
	```
	
	<docs dir> directory where html and images to be indexed are located

3. Index already parsed out json data files:
	
	
	```
	python weapon-ads-ES-Index-Mapping.py
	python weapon-ads-ES-Indexer.py <json data dir>
	```
	
	<json data dir> directory where provided .json files are located


Link-based Page Scoring
=======================
As an exercise to understand link based page ranking and relevancy in Information Retrieval, we wrote a program that computes relevancy
scores of our crawled documents, insipired by Google's Page Rank algorithm. Check that out in the link-based-ranking folder.

Dataset Interaction and Visualization
=====================================

The last part of this series of projects is the visualization part where we use AngularJS, D3 and Kibana to interact and visualize the dataset we indexed into Elasticsearch. Check that out! https://github.com/Jlong89/weapons-ads-vis.








	
