# Iterative Graph Summarization based on Grouping
This project proposes two algorithms (Path-based Algorithm and Ripple Algorithm). Both of them produce a summary graph based on user-identified supernodes, finding intermediate supernodes between them. Ripple Algorithm further allows users to control the resolution of a summary graph.


## Getting Started
This project was written and tested in macOS Sierra. So the commands shown in this Readme are in mac style.

###Prerequisites
1. Python 2.x version. The algorithms were implemented using Python 2.7.10.
2. There should be a "files" folder in "Path-based" and "Ripple" directory and test dataset (ACM network) in the folder.
3. networkx, csv, Counter, copy, groupby, timeit as well as itemgetter python modules are required. They can be installed by running "pip install module name".
4. There should be 1 python file in “Path-based” directory, 3 python files in “Ripple” directory.


## Running the tests
This section will introduce how to run these two algorithms, respectively.

###Path-based Algorithm
1. Go into the "Path-based" directory in the terminal.
2. Run: python path-based.py
3. Give input as the program requires. For each attribute value, you can just give the keyword. The attribute you can choose is in the
```
D.add_node()
```
statement.

**Example**

```
> cd ~/Path-based
> python path-based.py
> the number of attrs for supernode 1: 2
> the attribute 1 for supernode 1, use = to assign value: node_type=author
> the attribute 2 for supernode 1, use = to assign value: affiliation=Duke
> the number of attrs for supernode 2: 2
> the attribute 1 for supernode 2, use = to assign value: node_type=author
> the attribute 2 for supernode 2, use = to assign value: affiliation=IBM
> threshold of path lengths: 3
```
The detail about the summary graph will be shown.

###Ripple Algorithm
1. Go into the "Ripple" directory in the terminal.
2. Run: python Resolution\_Control\_3.py
3. Give input as the program requires. For each attribute value, you can just give the keyword. The attribute you can choose is in the
```
D.add_node()
```
statement in "Dataset\_To\_Graph\_1.py".

**Example**

```
> cd ~/Ripple
> python Resolution_Control_3.py
> the number of input supernodes: 3
> the number of attrs for supernode 1: 2
> the attribute 1 for supernode 1, use = to assign value: node_type=author
> the attribute 2 for supernode 1, use = to assign value: affiliation=Duke
> the number of attrs for supernode 2: 2
> the attribute 1 for supernode 2, use = to assign value: node_type=author
> the attribute 2 for supernode 2, use = to assign value: affiliation=IBM
> the number of attrs for supernode 3: 2
> the attribute 1 for supernode 3, use = to assign value: node_type=paper
> the attribute 2 for supernode 3, use = to assign value: title=algorithms
> threshold of path lengths: 2
```
The detail about the summary graph will be shown.

```
> specify the resolution:15
```
The detail about the split summary graph will be shown.

## Project Structure
Functions in each algorithm program are introduced in this section.

### Path-based Algorithm
Codes in **"Path-based" directory** implemented the Path-based Algorithm. There is only one python file named **path-based.py** in this directory. Functions are:

1. RepresentsInt(s): check if a string "s" represents an integer, codes of this function obtained from [here](http://stackoverflow.com/questions/1265665/python-check-if-a-string-represents-an-it-without-using-try-except).
2. find_selectedSN(): find vertices which meet the input requirement for entity sets.
3. find_allpaths(L): find paths (length is not greater than L) between 2 input supernodes.
4. cate_type(listOfPaths): group vertices on paths based on entity type.
5. build_adlist(paths): build adjacent list based on found paths.
6. build_SG(nodeset): build a summary graph.

### Ripple Algorithm
Codes in **"Ripple" directory** implemented the Ripple Algorithm. There are three python files in this directory, i.e. "Dataset\_To\_Graph\_1.py", "Search\_Each\_Supernode\_2.py" and "Resolution\_Control\_3.py".

##### Dataset\_To\_Graph\_1.py
This python file is used to build the dataset into a data graph D. Functions are:

1. RepresentsInt(s): check if a string "s" represents an integer, codes of this function obtained from [here](http://stackoverflow.com/questions/1265665/python-check-if-a-string-represents-an-it-without-using-try-except).
2. buildAdlist(node1, node2): build adjacent lists if there is an edge between node1 and node2 in data graph D.
3. find_selectedSN(): find vertices which meet the input requirement for entity sets.
4. typeEqualSupernode() + typeNotEqualSupernode(): two functions are used to group vertices in the data graph D based on entity types. Here, user-identified supernodes are regarded as new entity types (Si)

##### Search\_Each\_Supernode_2.py
This python file is used to do Breadth-First-Search from each input supernode and merge groups. Functions are:

1. find\_out\_neighs(node, grouptype): find all "out" neighboring vertices of a group and group them based on direction, entity type and edge type.
2. find\_in\_neighs(node, grouptype): find all "in" neighboring vertices of a group and group them based on direction, entity type and edge type.
3. to\_graph(CombinedGroup) + to\_edge(l): construct groups in "CombinedGroup" into graphs. Using the connected components to find groups which are overlapping. Codes of this function obtained from [here](http://stackoverflow.com/questions/4842613/merge-lists-that-share-common-elements).
4. comb\_groups(GG): (1) find groups in "GG" which are in the same type and have the same neighbors. (2) For each same neighbor, check whether they are connected by the same edge type. If groups meet (1) and (2) requirements, merging them into one group.
5. find_finaledges(nodeset): find the relationships between groups in "nodeset".

##### Resolution\_Control\_3.py
This python file is used to allow users to control the resolution of the summary graph which is built in "Search\_Each\_Supernode\_2.py". Functions are:

1. NodesetMapAttr(): find distinct attribute values for each attribute.
2. AttrMapNum(): calculate the number of distinct values for each attribute.
3. FindSplitAttr() + FindMinNum(): find splitting attribute and splitting group.
4. find\_relationship(Groups): find the relationships between groups in "Groups".

## Known Issues
1. To find all paths between two input entity sets, Path-based Algorithm does not consider about the direction, so it may take a long time if users specify a large value for threshold. Solution is to restart the program with a smaller threshold value.
2. There is no space when you assign values to attributes. 
3. Capitalization of attribute values does matter! Please make sure the attribute value you chosen follows the dataset in "files" folder. If the program says: 
```
There may exist typo in your input!!
```
Check the input again and restart the program with correct input.
4. In the result of Ripple Algorithm, it may contain supernodes whose name start with "M". Supernodes start with "M" refer to nodes who have the same entity type (node_type) with input supernodes. For example, "S1" is a supernode which contains authors work for Duke University; therefore, "M1" is a supernode which contains authors who do not work for Duke University.
5. If there exist some supernodes which end with number, it means there exist supernodes who have the same entity type (node_type) with them, but they have different superedges. For example, there may exist "paper" and "paper1" in the result. It means these two supernodes are all papers but they are connected by different superedges, so they cannot be merged into one group.

## Author
Codes and this README are written by Sirui Li (u5831882).

Mail: u5831882@anu.edu.au

## Acknowledgments
Two functions in this project are others' works and they have been cited in this README. I really appreciate the guidance from my supervisor Qing Wang.


