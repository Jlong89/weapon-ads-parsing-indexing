Link-Based Page Relevancy Scoring Python Program
================================================

We developed a link-based algorithm for computing relevancy page scoring based on similar metadata of documents. The program takes json documents, which
already contain weapon ad document metadata in its fields, and makes a node object of each document containing metadata of the documents as object properties, and stores nodes in a graph structure. Nodes are linked based on common metadata attributes and the nodes with higher number of links get higher scores. The algorithm is similar to Google's Page Rank, 
except that our edges are connections between shared metadata features and not hrefs between html pages, also our edges are undirected. 
This program was used to find patterns in the dataset, such as finding temporal and spatial trend of buyers.
The following is the equation used for computing the scores:

```
	S(A) = (1-d) + d*(S(N1)/C(N1) + ... + S(Nn)/C(Nn))

	S(A) = score of node A
	S(Nn) = score Node n, which shares edge with Node A; is neighbor of node A
	C(Nn) = number of edges from node A
	d = damping factor

```

The algorithm needs starting scores for the nodes, which are initiated to 0.5. The algorithm runs in a loop until the euclidian vector distance between the
node scores between one iteration and the next is smaller than a user input delta value. 

------------------------------------------------------------------------------------------------------

Setup and commands to run program
=================================

First, need to import networkx, which is used for storing nodes of the graph

	`$pip install networkx`

CLI to run the program:
======================

`$python link_based_ranker.py /path/to/json_files_collection_folder/ '["keywords1","keywords",...]' "field1" "field2"... `

All the fields in the index mapping of the documents are available for linking.

sample(use sample_json_collection in the same folder): 

	`$python link_based_ranker.py sample_json_collection/ '["grenade","rocket","explosive"]' "description"`

if no keywords provided, the keywords list still need to be argument with empty value

	`$python link_based_ranker.py sample_json_collection/ '[]' "availableDate" "itemCategory" "location"`

The scored query result "sorted.txt" will be generated after executing the code, showing 50 top scored files 

Examples
========

The following are the commands we use to run our link based algorithm to find temporal and spatial trend in the dataset:

`python link_based_ranker.py set/ '["looking to buy"]' "location" "description" "availableDate"`

The example_result1.txt contains the result scores of the above.

We can also use this to find temporal trends of the firearm manufacturers, shown in example_result2.txt.

