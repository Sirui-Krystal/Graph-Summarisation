import csv
import networkx as nx
import sys
from collections import Counter
import timeit
import copy


"""
check if a string s represents an integer
this function obtained from
http://stackoverflow.com/questions/1265665/python-check-if-a-string-represents-an-int-without-using-try-except
"""
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# find vertices which meet the input requirement for entity sets
def find_selectedSN():
    for j in xrange(0, 2):
        num_attrs = raw_input('the number of attrs for supernode '+str(j+1)+': ')
        mylist= list()
        for m in xrange(0,int(num_attrs)):
            attributes = raw_input('the attribute '+str(m+1)+ ' for supernode '+str(j+1)+', use = to assign value: ')
            for each_node in D.nodes():
                if attributes.split('=')[0] in D.node[each_node]:
                    save_attr.append(attributes.split('=')[0])
                    if attributes.split('=')[1] in D.node[each_node][attributes.split('=')[0]]:
                        mylist.append(each_node)
        result = list()
        counter=Counter(mylist)
        for node, num in counter.iteritems():
            if num == int(num_attrs):
                result.append(node)
        input_SN.append(result)
        if not result:
            print "There may exist typo in your input!!"

# find paths (lengths are not great than L) between two input supernodes
def find_allpaths(L):
    for m in xrange(0,1):
        for n in xrange(m+1, 2):
            for node_f in input_SN[m]:
                for node_s in input_SN[n]:
                    for path_1 in nx.all_simple_paths(D, source=node_f, target=node_s,cutoff=L):
                        if path_1 not in chosen_path:
                            chosen_path.append(path_1)


# group vertices on paths based on entity types
def cate_type(listOfPaths):
    type_map_nodes["S1"] = input_SN[0]
    type_map_nodes["S2"] = input_SN[1]
    for path in listOfPaths:
        for vertex in path:
            v_type = D.node[vertex]['node_type']
            if v_type not in ["S1","S2"]:
                if v_type not in type_map_nodes:
                    type_map_nodes[v_type] = list()
                if vertex not in type_map_nodes[v_type]:
                    type_map_nodes[v_type].append(vertex)


# build adjacent list based on found paths
def build_adlist(paths):
    for path in paths:
        length = len(path)
        for i in xrange(0,length-1):
            if path[i] not in Adlist:
                Adlist[path[i]] = list()
            if path[i+1] not in Adlist[path[i]]:
                Adlist[path[i]].append(path[i+1])
            if path[i+1] not in Adlist:
                Adlist[path[i+1]] = list()
            if path[i] not in Adlist[path[i+1]]:
                Adlist[path[i+1]].append(path[i])


# build the summary graph
def build_SG(nodeset):
    for key in nodeset:
        if key not in summary_graph:
            summary_graph[key] = dict()
    for key in type_map_nodes:
        for node in type_map_nodes[key]:
            if node in Adlist:
                for outN in Adlist[node]:
                    outN_type = D.node[outN]['node_type']
                    edge_type = D.get_edge_data(node, outN)
                    if outN_type not in summary_graph[key]:
                        summary_graph[key][outN_type] = list()
                    if edge_type not in summary_graph[key][outN_type]:
                        summary_graph[key][outN_type].append(edge_type)

# save vertices who are chosen as user input supernodes
input_SN = list()
# save attributes of input supernodes
save_attr = list()
# adjacent list of vertices on paths
Adlist = dict()
# save paths chosen by users
chosen_path = list()
# map entity type to vertices on chosen_path
type_map_nodes = dict()
summary_graph = dict()
# data graph build from the dataset
D = nx.Graph()


# build data graph from the dataset in CSV format
f1 = csv.reader(open('./files/author.csv'))
for row in f1:
    if RepresentsInt(row[0]):
        D.add_node(row[0], node_type='author', aid=row[0], personid=row[1], authorprofileid=row[2], fname=row[3], mname=row[4], lname=row[5], affiliation=row[6], email=row[7])

f2 = csv.reader(open('./files/journal.csv'))
for row in f2:
    if RepresentsInt(row[0]):
        D.add_node(row[0], node_type='journal', joid=row[0], journalid=row[1], name=row[2], periodical_type=row[3], publication_year=row[4].split('-')[0], puid=row[5])
        D.add_edge(row[5], row[0],label='publishes')

f3 = csv.reader(open('./files/paper.csv'))
for row in f3:
    if RepresentsInt(row[0]):
        D.add_node(row[0], node_type='paper', pid=row[0], articleid=row[1], title=row[2], publication_year=row[3].split('-')[0], joid=row[4], prid=row[5])
        if row[5]:
            D.add_edge(row[0], row[5],label='belongs_to_prid')
        if row[4]:
            D.add_edge(row[0], row[4],label='belongs_to_joid')

f4 = csv.reader(open('./files/proceeding.csv'))
for row in f4:
    if RepresentsInt(row[0]):
        D.add_node(row[0], node_type='proceeding', prid=row[0], proceedingid=row[1], title=row[2], subtitle=row[3], proc_desc=row[4], con_city=row[5], con_state=row[6], con_country=row[7], con_start_date=row[8], con_end_date=row[9], publication_year=row[10].split('-')[0], puid=row[11])
        D.add_edge(row[11], row[0],label='publishes')

f5 = csv.reader(open('./files/publisher.csv'))
for row in f5:
    if RepresentsInt(row[0]):
        D.add_node(row[0], node_type='publisher', puid=row[0], publisherid=row[1], name=row[2], zipcode=row[3], city=row[4], state=row[5], country=row[6])

f6 = csv.reader(open('./files/writes.csv'))
for row in f6:
    if RepresentsInt(row[0]):
        D.add_edge(row[0], row[1],label='writes')

f7 = csv.reader(open('./files/cites.csv'))
for row in f7:
    if RepresentsInt(row[0]):
        D.add_edge(row[0], row[1],label='cites')


find_selectedSN()
startime = timeit.default_timer()

# change the entity type of nodes who are in input supernodes
for EachNode in input_SN[0]:
    D.node[EachNode]["node_type"] = "S1"
for Node in input_SN[1]:
    D.node[Node]["node_type"] = "S2"

selected_interval = raw_input('threshold of path lengths: ')
find_allpaths(int(selected_interval))

if not chosen_path:
    print "There is no path between two entity sets"
    sys.exit()

cate_type(chosen_path)
build_adlist(chosen_path)
build_SG(type_map_nodes)

endtime = timeit.default_timer()
print "It takes " + str(endtime - startime) + " seconds."

# print details about the summary graph
print "These supernodes are in summary graph:"
for key in type_map_nodes:
    print key
    print "size: " + str(len(type_map_nodes[key]))
    print "vertices are: "
    print type_map_nodes[key]
    print "--------------------------------------------------------------------"
for key in summary_graph:
    print "The neighbors of " + key + " are:"
    for SN in summary_graph[key]:
        print SN
        print "Superedge between " + key + " and " + SN + " is: " + str(summary_graph[key][SN])
    print "===================================================================="














