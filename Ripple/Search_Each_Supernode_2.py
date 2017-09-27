import Dataset_To_Graph_1 as ntg
import networkx as nx
import copy
import timeit

"""
find all "out" neighboring vertices of a group
and group them by direction, entity type and edge type
"""
def find_out_neighs(node, grouptype):
    if node in ntg.OutAdlist:
        for OutNeigh in ntg.OutAdlist[node]:
            nodetype = ntg.D.node[OutNeigh]['node_type']
            edgetype = ntg.D.get_edge_data(node, OutNeigh)
            if grouptype in Supernodes:
                if nodetype in set(Supernodes).difference(set(grouptype)):
                    if [nodetype] not in LocalGroups:
                        LocalGroups.append([nodetype])
                if nodetype not in Supernodes:
                    if OutNeigh not in set(Iter_SearchVertices).intersection(set(FoundNodes)):
                        Iter_SearchVertices.append(OutNeigh)
                    if nodetype not in OutAd['CurrentGroup']:
                        OutAd['CurrentGroup'][nodetype] = dict()
                    if edgetype not in OutAd['CurrentGroup'][nodetype]:
                        OutAd['CurrentGroup'][nodetype][edgetype] = list()
                    if OutNeigh not in OutAd['CurrentGroup'][nodetype][edgetype]:
                        OutAd['CurrentGroup'][nodetype][edgetype].append(OutNeigh)
            else:
                if nodetype == grouptype:
                    if OutNeigh not in Buffer:
                        Buffer.append(OutNeigh)
                        if OutNeigh not in set(Iter_SearchVertices).intersection(set(FoundNodes)):
                            Iter_SearchVertices.append(OutNeigh)
                if nodetype != grouptype:
                    if nodetype in Supernodes:
                        if [nodetype] not in LocalGroups:
                            LocalGroups.append([nodetype])
                    if nodetype not in Supernodes:
                        if OutNeigh not in set(Iter_SearchVertices).intersection(set(FoundNodes)):
                            Iter_SearchVertices.append(OutNeigh)
                        if nodetype not in OutAd['CurrentGroup']:
                            OutAd['CurrentGroup'][nodetype] = dict()
                        if edgetype not in OutAd['CurrentGroup'][nodetype]:
                            OutAd['CurrentGroup'][nodetype][edgetype] = list()
                        if OutNeigh not in OutAd['CurrentGroup'][nodetype][edgetype]:
                            OutAd['CurrentGroup'][nodetype][edgetype].append(OutNeigh)

"""
find all "in" neighboring vertices of a group
and group them by direction, entity type and edge type
"""
def find_in_neighs(node, grouptype):
    if node in ntg.InAdlist:
        for InNeigh in ntg.InAdlist[node]:
            nodetype = ntg.D.node[InNeigh]['node_type']
            edgetype = ntg.D.get_edge_data(InNeigh, node)
            if grouptype in Supernodes:
                if nodetype in set(Supernodes).difference(set(grouptype)):
                    if [nodetype] not in LocalGroups:
                        LocalGroups.append([nodetype])
                if nodetype not in Supernodes:
                    if InNeigh not in set(Iter_SearchVertices).intersection(set(FoundNodes)):#
                        Iter_SearchVertices.append(InNeigh)
                    if nodetype not in InAd['CurrentGroup']:
                        InAd['CurrentGroup'][nodetype] = dict()
                    if edgetype not in InAd['CurrentGroup'][nodetype]:
                        InAd['CurrentGroup'][nodetype][edgetype] = list()
                    if InNeigh not in InAd['CurrentGroup'][nodetype][edgetype]:
                        InAd['CurrentGroup'][nodetype][edgetype].append(InNeigh)
            else:
                if nodetype == grouptype:
                    if InNeigh not in Buffer:
                        Buffer.append(InNeigh)
                        if InNeigh not in set(Iter_SearchVertices).intersection(set(FoundNodes)):
                            Iter_SearchVertices.append(InNeigh)
                if nodetype != grouptype:
                    if nodetype in Supernodes:
                        if [nodetype] not in LocalGroups:
                            LocalGroups.append([nodetype])
                    if nodetype not in Supernodes:
                        if InNeigh not in set(Iter_SearchVertices).intersection(set(FoundNodes)):
                            Iter_SearchVertices.append(InNeigh)
                        if nodetype not in InAd['CurrentGroup']:
                            InAd['CurrentGroup'][nodetype] = dict()
                        if edgetype not in InAd['CurrentGroup'][nodetype]:
                            InAd['CurrentGroup'][nodetype][edgetype] = list()
                        if InNeigh not in InAd['CurrentGroup'][nodetype][edgetype]:
                            InAd['CurrentGroup'][nodetype][edgetype].append(InNeigh)

"""
construct groups in "CombinedGroup" into graphs,
using the connected components to find groups which are
overlapping
obtained from http://stackoverflow.com/questions/4842613/merge-lists-that-share-common-elements
"""
def to_graph(CombinedGroup):
    C = nx.Graph()
    for group in CombinedGroup:
        C.add_nodes_from(group)
        C.add_edges_from(to_edges(group))
    return C


def to_edges(l):
    it = iter(l)
    last = next(it)
    for current in it:
        yield last, current
        last = current

"""
merge groups in GG which are in the same type and they are connected by the same group with the same edge
"""
def comb_groups(GG):
    node_map_index = dict() # use it to find which group gives this edge
    allset = set()
    type_map_index = dict()
    MergeIndex = list()
    for group in GG:
        if ntg.RepresentsInt(group[0]):
            allset = allset.union(group)
            index = GG.index(group)
            for node in group:
                node_map_index[node] = index
            if ntg.D.node[node]['node_type'] not in type_map_index:
                type_map_index[ntg.D.node[node]['node_type']] = list()
            type_map_index[ntg.D.node[node]['node_type']].append(index)
        else:
            allset = allset.union(ntg.node_set[group[0]])
            index = GG.index(group)
            for node in ntg.node_set[group[0]]:
                node_map_index[node] = index
            if group[0] not in type_map_index:
                type_map_index[group[0]] = list()
            type_map_index[group[0]].append(index)
    for grouptype in type_map_index:
        if len(type_map_index[grouptype]) > 1:
            IndexMapEdge = dict()
            for EachIndex in type_map_index[grouptype]:
                IndexMapEdge[EachIndex] = dict()
                for node in GG[EachIndex]:
                    if node in ntg.OutAdlist:
                        for OutN in set(ntg.OutAdlist[node]).intersection(allset):
                            ConnectIndex = node_map_index[OutN]
                            EdgeData = ntg.D.get_edge_data(node, OutN)
                            if ConnectIndex not in IndexMapEdge[EachIndex]:
                                IndexMapEdge[EachIndex][ConnectIndex] = list()
                            if EdgeData not in IndexMapEdge[EachIndex][ConnectIndex]:
                                IndexMapEdge[EachIndex][ConnectIndex].append(EdgeData)
                    if node in ntg.InAdlist:
                        for InN in set(ntg.InAdlist[node]).intersection(allset):
                            ConnectIndex = node_map_index[InN]
                            EdgeData = ntg.D.get_edge_data(InN, node)
                            if ConnectIndex not in IndexMapEdge[EachIndex]:
                                IndexMapEdge[EachIndex][ConnectIndex] = list()
                            if EdgeData not in IndexMapEdge[EachIndex][ConnectIndex]:
                                IndexMapEdge[EachIndex][ConnectIndex].append(EdgeData)
            Y = nx.Graph()
            for i in IndexMapEdge:
                Y.add_node(i)
            for k in IndexMapEdge:
                for j in IndexMapEdge:
                    if k != j:
                        if IndexMapEdge[k] == IndexMapEdge[j]:
                            Y.add_edge(k,j)
            connects = nx.connected_components(Y)
            for connect in connects:
                if len(connect)>1:
                    MergeIndex.append(list(connect))

    buffergroups = list()
    useindex = list()
    for m in MergeIndex:
        g = list()
        for i in m:
            useindex.append(i)
            g = list(set(g).union(set(GG[i])))
        buffergroups.append(g)
    for NotUseIndex in xrange(0, len(GG)):
        if NotUseIndex not in useindex:
            buffergroups.append(GG[NotUseIndex])
    return buffergroups


def merge_group(to_mergedgroup):
    C = to_graph(to_mergedgroup)
    combs = nx.connected_components(C)
    to_mergedgroup = list()
    for comb in combs:
        to_mergedgroup.append(list(comb))
    result = comb_groups(to_mergedgroup)
    return result


# find the relationships between groups in the final summary graph
def find_finaledges(nodeset):
    node_map_key = dict()
    allset = set()
    relationship = dict()
    m = dict()
    for key in nodeset:
        allset = allset.union(nodeset[key])
        for node in nodeset[key]:
            node_map_key[node] = key
    for key in nodeset:
        relationship[key] = dict()
        relationship[key]["Out"] = dict()
        relationship[key]["In"] = dict()
        for node in nodeset[key]:
            if node in ntg.OutAdlist:
                for OutN in set(ntg.OutAdlist[node]).intersection(allset):
                    ConnectKey = node_map_key[OutN]
                    EdgeData = ntg.D.get_edge_data(node, OutN)
                    if key not in m:
                        m[key] = dict()
                    if ConnectKey not in m[key]:
                        m[key][ConnectKey] = dict()
                    if EdgeData not in m[key][ConnectKey]:
                        m[key][ConnectKey][EdgeData] = list()
                    if node not in m[key][ConnectKey][EdgeData]:
                        m[key][ConnectKey][EdgeData].append(node)
                    if ConnectKey not in relationship[key]['Out']:
                        relationship[key]['Out'][ConnectKey] = list()
                    if EdgeData not in relationship[key]['Out'][ConnectKey]:
                        relationship[key]['Out'][ConnectKey].append(EdgeData)
            if node in ntg.InAdlist:
                for InN in set(ntg.InAdlist[node]).intersection(allset):
                    ConnectKey = node_map_key[InN]
                    EdgeData = ntg.D.get_edge_data(InN, node)
                    if ConnectKey not in relationship[key]['In']:
                        relationship[key]['In'][ConnectKey] = list()
                    if EdgeData not in relationship[key]['In'][ConnectKey]:
                        relationship[key]['In'][ConnectKey].append(EdgeData)
    return relationship, allset, m

K_str = raw_input('threshold of path lengths: ')
start = timeit.default_timer()
K = int(K_str)
# GlobalGroups saves the groups after searching all previous user-selected supernodes
GlobalGroups = list()
Supernodes = list()
FirstFound = dict()
AllSet = set()
for i in xrange (1,int(ntg.num_supernodes)+1):
    Supernodes.append("S"+str(i))
for EachSupernode in Supernodes:
    print "start to do BFS search from " + EachSupernode
    Iter_GlobalGroups = list()
    Iter_GlobalGroups.append([EachSupernode])
    # FoundNodes saves all vertices that have been found before current step
    FoundNodes = list()
    # SearchVertices saves new found nodes in current step
    SearchVertices = list()
    step = 1
    while step <= K:
        print "step " + str(step) + " starts."
        # CurrentGroupBuffer saves current searched group
        Buffer = list()
        LocalGroups = copy.copy(Iter_GlobalGroups)
        Iter_SearchVertices = list()
        """
        OutAd and InAd saves out neighbors and in neighbors of current searched group,
        these neighbors are grouped by node types and edge types
        """
        if step == 1:
            OutAd = {"CurrentGroup": dict()}
            InAd = {"CurrentGroup": dict()}
            for NodeInSN in ntg.node_set[EachSupernode]:
                find_out_neighs(NodeInSN, EachSupernode)
                find_in_neighs(NodeInSN, EachSupernode)
            if OutAd['CurrentGroup']:
                for NodeType in OutAd['CurrentGroup']:
                    for EdgeType in OutAd['CurrentGroup'][NodeType]:
                        LocalGroups.append(OutAd['CurrentGroup'][NodeType][EdgeType])
            if InAd['CurrentGroup']:
                for NodeType in InAd['CurrentGroup']:
                    for EdgeType in InAd['CurrentGroup'][NodeType]:
                        LocalGroups.append(InAd['CurrentGroup'][NodeType][EdgeType])
        if step != 1:
            for EachGroup in Iter_GlobalGroups:
                if ntg.RepresentsInt(EachGroup[0]):
                    OutAd = {"CurrentGroup": dict()}
                    InAd = {"CurrentGroup": dict()}
                    Buffer = copy.copy(EachGroup)
                    GroupType = ntg.D.node[EachGroup[0]]["node_type"]
                    for node in set(EachGroup).intersection(set(SearchVertices)):
                        find_out_neighs(node, GroupType)
                        find_in_neighs(node, GroupType)
                    index = LocalGroups.index(EachGroup)
                    LocalGroups[index] = copy.copy(Buffer)
                    if OutAd['CurrentGroup']:
                        for NodeType in OutAd['CurrentGroup']:
                            for EdgeType in OutAd['CurrentGroup'][NodeType]:
                                LocalGroups.append(OutAd['CurrentGroup'][NodeType][EdgeType])
                    if InAd['CurrentGroup']:
                        for NodeType in InAd['CurrentGroup']:
                            for EdgeType in InAd['CurrentGroup'][NodeType]:
                                LocalGroups.append(InAd['CurrentGroup'][NodeType][EdgeType])
        Iter_GlobalGroups = copy.copy(LocalGroups)
        SearchVertices = copy.copy(Iter_SearchVertices)
        Iter_GlobalGroups = merge_group(Iter_GlobalGroups)
        FoundNodes = copy.copy(FoundNodes + SearchVertices)
        for node in SearchVertices:
            if node not in FirstFound:
                FirstFound[node] = EachSupernode+" step: ", step
        print "step " + str(step) + " ends."
        step += 1
    ToAddGroups = [x for x in Iter_GlobalGroups if x not in GlobalGroups]
    GlobalGroups = GlobalGroups + ToAddGroups
    GlobalGroups = merge_group(GlobalGroups)

new_nodeset = dict()
i = 1
for group in GlobalGroups:
    if ntg.RepresentsInt(group[0]):
        if ntg.D.node[group[0]]['node_type'] not in new_nodeset:
            new_nodeset[ntg.D.node[group[0]]['node_type']] = copy.copy(group)
        else:
            new_nodeset[ntg.D.node[group[0]]['node_type'] + str(i)] = copy.copy(group)
            i += 1
    else:
        new_nodeset[group[0]] = copy.copy(ntg.node_set[group[0]])
result = find_finaledges(new_nodeset)
relationships = result[0]
AllSet = result[1]
NeiBuffer = result[2]
print "These supernodes are in summary graph:"
for key in new_nodeset:
    print key
    print "size: " + str(len(new_nodeset[key]))
    print "vertices are:"
    print new_nodeset[key]
    if key not in Supernodes:
        if len(new_nodeset[key]) < 3:
            print "This group only contains a few vertices"
            for e in new_nodeset[key]:
                print e + " is found in: " + str(FirstFound[e])
    print "##############################################"
stop = timeit.default_timer()
print "It takes " + str(stop-start) + " seconds."
for g in relationships:
    print "The relationships about " + g + " are:"
    if relationships[g]["Out"]:
        print g + " points to:"
        gsize = len(new_nodeset[g])
        for eachgroup in relationships[g]["Out"]:
            print eachgroup
            print "edge is: "
            print relationships[g]["Out"][eachgroup]
            for edge in relationships[g]['Out'][eachgroup]:
                csize = len(NeiBuffer[g][eachgroup][edge])
                ratio = float(csize)/float(gsize)
                print "participant ratio is: " + str(ratio)

    if relationships[g]["In"]:
        print "These groups point to " + g
        for eachgroup in relationships[g]["In"]:
            print eachgroup
            print "edge is: "
            print relationships[g]['In'][eachgroup]
    print "--------------------------------------------"


