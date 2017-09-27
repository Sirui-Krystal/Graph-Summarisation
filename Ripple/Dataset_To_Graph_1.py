import csv
import networkx as nx
from collections import Counter

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


# build up adjacent lists for each node in data graph
def builtAdList(node1, node2):
    if node1 not in OutAdlist:
            OutAdlist[node1] = list()
            OutAdlist[node1].append(node2)
    if node1 in OutAdlist:
            if node2 not in OutAdlist[node1]:
                OutAdlist[node1].append(node2)
    if node2 not in InAdlist:
            InAdlist[node2] = list()
            InAdlist[node2].append(node1)
    if node2 in InAdlist:
            if node1 not in InAdlist[node2]:
                InAdlist[node2].append(node1)


# find vertices which meet the input requirement for entity sets
def find_selectedSN():
    for _iter in xrange(0, int(num_supernodes)):
        select_attr["S"+str(_iter+1)] = dict()
        num_attrs = raw_input('the number of attrs for supernode '+str(_iter+1)+': ')
        mylist = list()
        for attr in xrange(0, int(num_attrs)):
            attributes = raw_input('the attribute ' + str(attr + 1) + ' for supernode ' + str(_iter + 1) + ', use = to assign value: ')
            for each_node in D.nodes():
                if attributes.split('=')[0] in D.node[each_node]:
                    if attributes.split('=')[1] in D.node[each_node][attributes.split('=')[0]]:
                        mylist.append(each_node)
                        select_attr["S"+str(_iter+1)][attributes.split('=')[0]] = attributes.split('=')[1]
        result = list()
        counter = Counter(mylist)
        for node, num in counter.iteritems():
            if num == int(num_attrs):
                result.append(node)
        if not result:
            print "There may exist typo in your input!!"
        supernodes_set["S"+str(_iter+1)] = result


"""
typeEqualSupernode and typeNotEqualSupernode are used to
group vertices in the data graph based on entity types,
save the result in node_set.
"""
def typeEqualSupernode():
    for key in select_attr:
        buffer = list()
        node_set["M"+key.split('S')[1]] = list()
        node_type = select_attr[key]['node_type']
        for node in D.nodes():
            if 'node_type' in D.node[node]:
                if D.node[node]['node_type'] == node_type:
                    buffer.append(node)
        node_set["M"+key.split('S')[1]] = [x for x in buffer if x not in supernodes_set["S"+key.split('S')[1]]]
def typeNotEqualSupernode():
    chosen_node_type = list()
    for key in select_attr:
        chosen_node_type.append(select_attr[key]['node_type'])
    for type in all_node_type:
        if type not in chosen_node_type:
            node_set[type] = list()
            node_set[type] = Type_Map_Nodes[type]


# data graph built from the datast
D = nx.DiGraph()
#OutAdlist and InAdlist are adjacent lists
# edge 1->2, OutAdlist {1:[2]}, InAdlist{2:[1]}
OutAdlist = dict()
InAdlist = dict()
# supernodes_set record nodes who are chosen as supernodes
supernodes_set = dict()
select_attr = dict()
node_set = dict()
Type_Map_Nodes = {"author": list(), "journal": list(), "paper": list(), "proceeding": list(), "publisher": list()}
all_node_type = ['author', 'journal', 'paper', 'proceeding', 'publisher']


# build data graph from the dataset in CSV format
f1 = csv.reader(open('./files/author.csv'))
for row in f1:
    if RepresentsInt(row[0]):
        D.add_node(row[0], node_type='author', aid=row[0], personid=row[1], authorprofileid=row[2], fname=row[3], mname=row[4], lname=row[5], affiliation=row[6], email=row[7])
        Type_Map_Nodes['author'].append(row[0])

f2 = csv.reader(open('./files/journal.csv'))
for row in f2:
    if RepresentsInt(row[0]):
        D.add_node(row[0], node_type='journal', joid=row[0], journalid=row[1], name=row[2], periodical_type=row[3], publication_year=row[4].split('-')[0], puid=row[5])
        D.add_edge(row[5], row[0])
        D[row[5]][row[0]] = 'publish'
        Type_Map_Nodes['journal'].append(row[0])
        builtAdList(row[5], row[0])

f3 = csv.reader(open('./files/paper.csv'))
for row in f3:
    if RepresentsInt(row[0]):
        D.add_node(row[0], node_type='paper', pid=row[0], articleid=row[1], title=row[2], publication_year=row[3].split('-')[0], joid=row[4], prid=row[5])
        Type_Map_Nodes['paper'].append(row[0])
        if row[5]:
            D.add_edge(row[0], row[5])
            D[row[0]][row[5]] = 'belongs_to_prid'
            builtAdList(row[0], row[5])
        if row[4]:
            D.add_edge(row[0], row[4])
            D[row[0]][row[4]] = 'belongs_to_joid'
            builtAdList(row[0], row[4])

f4 = csv.reader(open('./files/proceeding.csv'))
for row in f4:
    if RepresentsInt(row[0]):
        D.add_node(row[0], node_type='proceeding', prid=row[0], proceedingid=row[1], title=row[2], subtitle=row[3], proc_desc=row[4], con_city=row[5], con_state=row[6], con_country=row[7], con_start_date=row[8], con_end_date=row[9], publication_year=row[10].split('-')[0], puid=row[11])
        Type_Map_Nodes['proceeding'].append(row[0])
        D.add_edge(row[11], row[0])
        D[row[11]][row[0]] = 'publish'
        builtAdList(row[11], row[0])

f5 = csv.reader(open('./files/publisher.csv'))
for row in f5:
    if RepresentsInt(row[0]):
        D.add_node(row[0], node_type='publisher', puid=row[0], publisherid=row[1], name=row[2], zipcode=row[3], city=row[4], state=row[5], country=row[6])
        Type_Map_Nodes['publisher'].append(row[0])

f6 = csv.reader(open('./files/writes.csv'))
for row in f6:
    if RepresentsInt(row[0]):
        D.add_edge(row[0], row[1])
        D[row[0]][row[1]] = 'writes'
        builtAdList(row[0], row[1])

f7 = csv.reader(open('./files/cites.csv'))
for row in f7:
    if RepresentsInt(row[0]):
        D.add_edge(row[0], row[1])
        D[row[0]][row[1]] = 'cites'
        builtAdList(row[0], row[1])

num_supernodes = raw_input('the number of input supernodes: ')
find_selectedSN()
typeEqualSupernode()
typeNotEqualSupernode()
for key in supernodes_set:
    node_set[key] = supernodes_set[key]

"""
 update node_type, here "M" refers to groups that have the same entity type
 with user-specified supernodes
"""
for i in xrange (1,int(num_supernodes)+1):
    for type in node_set:
        if type == "M" + str(i):
            for node in node_set["M" + str(i)]:
                D.node[node]["node_type"] = type
        if type == "S" + str(i):
            for node in node_set["S"+str(i)]:
                D.node[node]["node_type"] = type
