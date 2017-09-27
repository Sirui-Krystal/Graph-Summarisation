import Search_Each_Supernode_2 as ses
import Dataset_To_Graph_1 as ntg
from itertools import groupby
from operator import itemgetter
import copy


# define a function to find distinct attribute values in each supernode
def NodesetMapAttr():
    for key in nodeset_attribute_value:
        for node in NodeSet_Final[key]:
            for attr in ntg.D.node[node]:
                if attr != "node_type":
                    if attr not in nodeset_attribute_value[key]:
                        nodeset_attribute_value[key].setdefault(attr,[])
                    nodeset_attribute_value[key][attr].append(ntg.D.node[node][attr])
                    if ntg.D.node[node][attr] not in nodeset_attribute_value[key][attr]:
                        nodeset_attribute_value[key][attr].append(ntg.D.node[node][attr])


# define a function to calculate the number of distinct values for each attribute
def AttrMapNum():
    for key in nodeset_attribute_value:
        for k, value in nodeset_attribute_value[key].items():
            num = float(len([item for item in value if item]))/float(len(NodeSet_Final[key]))
            if num != 0 and num != 1:
                if key not in nodeset_disvalue_number:
                    nodeset_disvalue_number[key] = dict()
                if k not in nodeset_disvalue_number[key]:
                    nodeset_disvalue_number[key][k] = num

# define two functions to find splitting attribute and splitting group
def FindSplitAttr():
    for key in nodeset_disvalue_number:
        if key not in min_in_group:
            min_in_group[key] = dict()
            min_attr = [v for k,v in groupby(sorted((v,k) for k,v in nodeset_disvalue_number[key].iteritems()), key=itemgetter(0)).next()[1]]
            if nodeset_disvalue_number[key][min_attr[0]] not in min_in_group[key]:
                min_in_group[key][nodeset_disvalue_number[key][min_attr[0]]] = min_attr
def FindMinNum():
    for key in min_in_group:
        for k in min_in_group[key]:
            if k not in minv_map_groups:
                minv_map_groups[k] = dict()
            if key not in minv_map_groups[k]:
                minv_map_groups[k][key] = min_in_group[key][k]


# define a function to find the relationships between groups in Groups
def find_relationship(Groups):
    node_map_groupname = dict()
    for key in Groups:
        for node in Groups[key]:
            node_map_groupname[node] = key
    for key in Groups:
        relationship[key] = dict()
        relationship[key]['Out'] = dict()
        relationship[key]['In'] = dict()
        for node in Groups[key]:
            if node in ntg.OutAdlist:
                for OutN in set(ntg.OutAdlist[node]).intersection(ses.AllSet):
                    ConnectType = node_map_groupname[OutN]
                    EdgeData = ntg.D.get_edge_data(node, OutN)
                    if ConnectType not in relationship[key]['Out']:
                        relationship[key]['Out'][ConnectType] = list()
                    if EdgeData not in relationship[key]['Out'][ConnectType]:
                        relationship[key]['Out'][ConnectType].append(EdgeData)
            if node in ntg.InAdlist:
                for InN in set(ntg.InAdlist[node]).intersection(ses.AllSet):
                    ConnectType = node_map_groupname[InN]
                    EdgeData = ntg.D.get_edge_data(InN, node)
                    if ConnectType not in relationship[key]['In']:
                        relationship[key]['In'][ConnectType] = list()
                    if EdgeData not in relationship[key]['In'][ConnectType]:
                        relationship[key]['In'][ConnectType].append(EdgeData)

Resolution_Str = raw_input('specify the resolution:')
NodeSet_Final = copy.copy(ses.new_nodeset)
i = 0
while len(NodeSet_Final) < int(Resolution_Str):
    i += 1
    nodeset_attribute_value = dict()
    nodeset_disvalue_number = dict()
    min_in_group = dict()
    minv_map_groups = dict()
    NodeSet_Iter = dict()
    relationship = dict()
    for key in NodeSet_Final:
        if key not in ses.Supernodes:
            nodeset_attribute_value[key] = dict()
    NodesetMapAttr()
    AttrMapNum()
    FindSplitAttr()
    FindMinNum()
    min_key = min(minv_map_groups.keys())
    groups = minv_map_groups[min_key].keys()
    split_group = groups[0]
    split_attr = minv_map_groups[min_key][split_group][0]
    for value in nodeset_attribute_value[split_group][split_attr]:
        if value:
            node = split_group+"+"+value
            NodeSet_Iter[node] = list()
            for single_node in NodeSet_Final[split_group]:
                if ntg.D.node[single_node][split_attr] == value:
                    NodeSet_Iter[node].append(single_node)
        else:
            node = split_group+"+"+"MISSING!"
            NodeSet_Iter[node] = list()
            for single_node in NodeSet_Final[split_group]:
                if not ntg.D.node[single_node][split_attr]:
                    NodeSet_Iter[node].append(single_node)
    for group in NodeSet_Final:
        if group != split_group:
            NodeSet_Iter[group] = copy.copy(NodeSet_Final[group])
    NodeSet_Final = copy.copy(NodeSet_Iter)

    print "The group to be split is " + split_group + " based on " + split_attr
    print "The size of summary graph after splitting is: " + str(len(NodeSet_Final))
    print "Note that the string after '+' is the value of splitting attribute in current supernode"
    find_relationship(NodeSet_Final)
    for g in relationship:
        print "The relationships about " + g + " are:"
        print "size: " + str(len(NodeSet_Final[g]))
        if relationship[g]["Out"]:
            print g + " points to:"
            for eachgroup in relationship[g]["Out"]:
                print eachgroup
                print "edge is: "
                print relationship[g]["Out"][eachgroup]
        if relationship[g]["In"]:
            print "These groups point to " + g
            for eachgroup in relationship[g]["In"]:
                print eachgroup
                print "edge is: "
                print relationship[g]['In'][eachgroup]
        print "--------------------------------------------"
