__all__ = ['AUTHORIZED_ITEMS', 'AUTHORIZED_ITEMS_DICT', 'plot_cooc_graph', 'build_item_cooc']

from .BiblioGeneralGlobals import COUNTRIES_GPS

AUTHORIZED_ITEMS = ['AK','AU','CU','IK','S','S2','TK']

AUTHORIZED_ITEMS_DICT = {'Authors':'AU',
                         'Authors keywords':'AK',
                         'Title keywords':'TK',
                         'Journal keywords':'IK',
                         'Countries':'CU',
                         'Subjects':'S',
                         'Sub-subjects':'S2',
                        }




COLOR_NODES = { "Y": "255,255,0", # default color for gephi display
                "J": "150,0,150",
               "AU": "20,50,255",
               "IK": "255,0,255",
               "AK": "255,0,255",
               "TK": "205,0,205",
                "S": "50,0,150",
               "S2": "50,0,150",
                "R": "255,0,0",
               "RJ": "255,97,0",
                "I": "0,255,0",
               "CU": "0,255,255",
               "LA": "0,180,0",
               "DT": "0,180,0",}

PARSED_FILE = {'AU':'authors.dat',
               'AK':'keywords.dat',
               'TK':'keywords.dat',
               'IK':'keywords.dat',
                'I':'institutions.dat',
               'CU':'countries.dat',
                'S':'subjects.dat',
               'S2':'subjects2.dat',
                'Y':'years.dat'}


def generate_cooc_graph(df_corpus=None, size_min=1, item=None):
    
    '''Builds a coocurence networkx object G=(N,V) out of the dataframe df_corpus with two columns
    pub_id and item:

          pub_id     item
             0       item1
             0       item2
             1       item1
             1       item1
             1       item3 
             1       item3
             2       item4
             2       item5
             2       unknown
    
     First the df_corpus is cleaned by eliminating rows duplicated or with unkonwn item:
     
         pub_id     item
             0      item1
             0      item2
             1      item1
             1      item3 
             2      item4
             2      item5
             
     The set of nodes N is the set of the items {item1,item2,item3,...}
     The set of vertices V is the set of tuples {(item_i,item_j),...} where:   
          (i)   item_i and item_j are related to the same pub_id 
          (ii)  item_i != item_j 
          (iii) (item_i,item_j) is equivalent to (item_j,item_i).
     
     ex: N = {item1,item2,item3,item4,item5}, V={(item1,item2),(item1,item3), (item4,item5)}
     
     The size of the node associated with item_i is the number of occurrences of item_i 
     that should be >= than size_min
     ex: size node_item1=2, size node_item2=1
     
     
     The weight w_ij of a vertex is the number of occurrences of the tuple (item_i,item_j) in the
     list of tuples [(item_i,item_j),...] where item_i and item_j are 
         (i) related to the same pub_id 
         (ii) item_i != item_j 
         (iii) (item_i,item_j) is equivalent to (item_j,item_i).
     
     The nodes has one id and two attributes: the size of the node and its label. 
     
     The edges have two attributes: their weight w_ij and their Kessler similarity 

                                                        w_ij
                               kess_ij = ----------------------------------------
                                          sqrt(size(node_i) * sqrt(size(node_j)
    
    Args:
        df_corpus (dataframe): dataframe structured as |pub_id|item|
        size_min (int): minimum size of the node to be retained
        
    Return:
        The function returns G a networkx object. The function return G=None if the graph has less than
        two nodes
    '''
    
    # Standard library import
    from collections import defaultdict
    from more_itertools import distinct_combinations
    
    # 3rd party import
    import math
    import networkx as nx
    import numpy as np
    import pandas as pd

    #                           Cleaning of the dataframe
    #----------------------------------------------------------------------------------------------- 
    df_corpus.drop_duplicates(inplace=True)                           # Keeps unique occurrence of an item
                                                                      # per article
    df_corpus.drop(index=df_corpus[df_corpus['item'] == 'unknown'].index,
                            inplace=True)                             # Drops rows with "unknown" items

    dg = df_corpus.groupby('item').count().reset_index()              # Number of occurrences of an item
    dg.columns = ['item','count']
    labels_to_drop = dg.query('count<@size_min')['item'].to_list()    # List of items whith a number
                                                                      # of occurrences less than size_min
    index_to_drop = [x[0]  for x in zip(df_corpus.index ,df_corpus['item']) 
                           if x[1] in labels_to_drop]
    df_corpus.drop(index_to_drop, inplace = True)                     # Cleaning of the dataframe
   
    #                 Building the set of nodes and the set of edges
    #------------------------------------------------------------------------------------------------
    df_corpus.columns = ['pub_id','item' ]
    nodes_id = list(set(df_corpus['item']))                 # Attribution of an integer id to the different items
    dic_nodes = dict(zip(nodes_id,range(len(nodes_id))))    # Number of an item occurrence keyed by the
                                                            #   node id
    dic_size = dict(zip(dg['item'],dg['count']))
    nodes_size = {dic_nodes[x]:dic_size[x] for x in nodes_id}
    
    del dg, nodes_id, dic_size
    
    if len(nodes_size)<2: # Dont build a graph with one or zero node
        G = None
        del df_corpus, dic_nodes
        
    else:
        list_edges = []
        weight = defaultdict(int)
        for group_by_pub_id in df_corpus.groupby('pub_id'):
            for edges in list(distinct_combinations(group_by_pub_id[1]['item'].to_list(), 2)):
                if edges:
                    edge = (dic_nodes[edges[0]],dic_nodes[edges[1]])
                    if edge not in list_edges:
                        list_edges.append(edge)
                        weight[edge] = 1
                    else:
                        weight[edge] +=1 
        del df_corpus
        #                            Building the networx object graph G
        #------------------------------------------------------------------------------------------------
        G = nx.Graph()

        G.add_nodes_from(dic_nodes.values()) 
        nx.set_node_attributes(G,nodes_size, 'node_size')
        nodes_label = dict(zip(dic_nodes.values(), dic_nodes.keys()))
        del dic_nodes
        
        nx.set_node_attributes(G,nodes_label, 'label' )
        if item == 'CU':
            lat, lon = map(list, zip(*[COUNTRIES_GPS[nodes_label[node]] for node in G.nodes]))
            lat_dict = dict(zip(G.nodes,lat))
            lon_dict = dict(zip(G.nodes,lon))
            nx.set_node_attributes(G,lat_dict,'lat')
            nx.set_node_attributes(G,lon_dict,'lon')
            del lat_dict, lon_dict

        G.add_edges_from(list_edges)
        nx.set_edge_attributes(G, weight, 'nbr_edges')
        kess = {}
        for edge in list_edges: # Computes the Kessler similarity betwween node edge[0] and node edge[1]
                kess[edge] = weight[edge] / math.sqrt(nodes_size[edge[0]] * nodes_size[edge[1]])        
        nx.set_edge_attributes(G, kess, 'kessler_similarity')
        del list_edges, weight, nodes_label
    
    del nodes_size
    
    return G


def plot_cooc_graph(G,item,size_min=1,node_size_ref=30):
    
    '''Plots the cooccurrenre graph G .
    We fix the layout to be of type "spring_layout"
    
    Args:
     G (networkx ogject): Built using the function "generate_cooc_graph"
     item (str): Item name (ex: "Authors", "Country"...)
     size_min (int): Minimum size of the kept nodes
     Node_size_ref (int): The maximum size of a node
     
    '''
    
    # 3rd party import
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt
    import networkx as nx
    import numpy as np
    
    pos = nx.spring_layout(G)
    node_sizes = np.array(list(nx.get_node_attributes(G,'node_size').values()))
    nodes_sizes_normalized = node_sizes / max(node_sizes)
    node_sizes = (nodes_sizes_normalized*node_size_ref).astype(int)
    
    title_item_dict = {item: full_name for full_name,item in AUTHORIZED_ITEMS_DICT.items()}
    
    #cmap = cm.get_cmap('viridis', max(partition.values()) + 1) (for future use)
    fig = plt.figure(figsize=(15,15))
    _ = nx.draw_networkx_nodes(G, pos, node_size=node_sizes) #, partition.keys(),(for future use)
    #cmap=cmap, node_color=list(partition.values())) (for future use)
    _ = nx.draw_networkx_edges(G, pos, alpha=0.9,width=1.5, edge_color='k', style='solid',)
    labels = nx.draw_networkx_labels(G,pos=pos,font_size=8,
                                       font_color='w')
    plt.title('Cooccurrence graph for item ' + title_item_dict[item] + '\nNode minimum size: '+ str(size_min),
              fontsize=23,fontweight="bold")
    
    plt.show()

def write_cooc_gexf(G,filename):
    
    '''Save the graph "G" at Gephy (.gexf) format using full path filename
    '''
    
    # Standard library imports
    from pathlib import Path
    
    # 3rd party imports
    import networkx as nx
    
    nx.write_gexf(G,filename)

def write_cooc_gdf(G,item,color,filename):
    
    '''Stores the cooccurrenre graph G as a .gdf file readable by Gephy. If item=CU we add
    to the node attribute the longitude and latitude (in °) of the country capital to be
    compatible with the Geo Layout of Gephy.
    
    Args:
        G (networkx object): graph for Gephy built using the function "generate_cooc_graph"
        item (str): name of the item 
        color (str): color of the nodes in rgb format ex: "150,0,150"
        filemame (str): full path of the .gdf file 
    
    '''
    
    # 3rd party import
    import math
    import networkx as nx
    
    assert(isinstance(G,nx.classes.graph.Graph)),'G should be networkx Graph'
    
    with open(filename, "w") as f_gephi:
        nodes_label = nx.get_node_attributes(G,'label')
        nodes_weight = nx.get_node_attributes(G,'node_size')
        label_columns_nodes = 'nodedef>name VARCHAR,label VARCHAR,type VARCHAR,width DOUBLE,'
        if item != 'CU':
            label_columns_nodes += 'height DOUBLE,size DOUBLE,color VARCHAR\n'
        else: #we add the node attributes lon and lat
            label_columns_nodes += 'height DOUBLE,size DOUBLE,color VARCHAR,lat DOUBLE,lon DOUBLE\n'
        f_gephi.write(label_columns_nodes)
        
        
        for node in G.nodes:
            size = nodes_weight[node]
            row = f"{node},'{nodes_label[node]}',{item},"
            if item != 'CU':
                row += f"{math.sqrt(size):.5f} ,{math.sqrt(size):.5f},{size},'{color}'\n"
            else:
                lat, lon = COUNTRIES_GPS[nodes_label[node]]
                row += f"{math.sqrt(size):.5f} ,{math.sqrt(size):.5f},{size},'{color}',"
                row += f'{lat},{lon}\n'
            f_gephi.write(row)

        edge_weight = nx.get_edge_attributes(G,'nbr_edges')
        edge_similarity = nx.get_edge_attributes(G,'kessler_similarity')
        f_gephi.write('edgedef>node1 VARCHAR,node2 VARCHAR,weight DOUBLE,nb_cooc DOUBLE\n')
        for edge in G.edges:
            row = f'{edge[0]},{edge[1]},{edge_similarity[edge]:.10f},{edge_weight[edge]}\n'
            f_gephi.write(row)
            
def build_item_cooc(item,in_dir,out_dir,size_min = 1,):
    
    # Standard library import
    import os
    from pathlib import Path
    
    # 3rd party imports
    import pandas as pd
    
    assert (item in AUTHORIZED_ITEMS), f'unknown item: {item}'
    
    filename_in = PARSED_FILE[item]

    if item in ['AK','IK','TK']:      # Deals with keywords
        df = pd.read_csv(in_dir / Path(filename_in),
                     sep='\t',
                     header=None,)
        df.columns = ['pub_id','type','item']
        df = df.query('type==@item')[["pub_id","item"]]
        df.fillna('unknown', inplace=True)

    else:
        df = pd.read_csv(in_dir / Path(filename_in),
                         sep='\t',
                         header=None,)

        if len(df.columns)>2:
            df = df[[0,2]]

        df.columns = ["pub_id","item"]


    G = generate_cooc_graph(df_corpus=df, size_min=size_min, item=item)
    del df
    
    if G is not None:
        filename_out_prefix = 'cooc_' + item + '_thr' + str(size_min) 
        write_cooc_gdf(G,item,COLOR_NODES[item],out_dir / Path(filename_out_prefix + '.gdf'))
        write_cooc_gexf(G,out_dir / Path(filename_out_prefix + '.gexf'))
    
    return G