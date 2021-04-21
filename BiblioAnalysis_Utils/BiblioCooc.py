__all__ = ['AUTHORIZED_ITEMS', 'plot_cooc_graph', 'build_item_cooc']

AUTHORIZED_ITEMS = ['AK','AU','CU','IK','S','S2','TK']

COUNTRIES_GPS_STRING = '''Aruba:12.5,-69.97;Afghanistan:33,65;Angola:-12.5,18.5;Anguilla:18.25,-63.17;
Albania:41,20;Andorra:42.5,1.5;United Arab Emirates:24,54;Argentina:-34,-64;Armenia:40,45;
American Samoa:-14.33,-170;Antarctica:-90,0;French Southern and Antarctic Lands:-49.25,69.167;
Antigua And Barbuda:17.05,-61.8;Australia:-27,133;Austria:47.3,13.3;Azerbaijan:40.5,47.5;
Burundi:-3.5,30;Belgium:50.83,4;Benin:9.5,2.25;Burkina Faso:13,-2;Bangladesh:24,90;Bulgaria:43,25;
Bahrain:26,50.55;Bahamas:24.25,-76;Bosnia And Herzegowina:44,18;Saint Barthélemy:18.5,-63.417;
Belarus:53,28;Belize:17.25,-88.75;Bermuda:32.3,-64.75;Bolivia:-17,-65;Brazil:-10,-55;
Barbados:13.16,-59.53;Brunei Darussalam:4.5,114.67;Bhutan:27.5,90.5;Bouvet Island:-54.43,3.4;
Botswana:-22,24;Central African Rep:7,21;Canada:60,-95;Switzerland:47,8;Chile:-30,-71;China:35,105;
IvoryCoast:8,-5;Cameroon:6,12;Congo:0,25;Republic of theCongo:-1,15;Cook Islands:-21.23,-159.77;
Colombia:4,-72;Comoros:-12.17,44.25;Cape Verde:16,-24;Costa Rica:10,-84;Cuba:21.5,-80;
Curacao:12.116667,-68.933333;Christmas Island:-10.5,105.66;Cayman Islands:19.5,-80.5;Cyprus:35,33;
Czech Republic:49.75,15.5;Germany:51,9;Djibouti:11.5,43;Dominica:15.416,-61.33;Denmark:56,10;
Dominican Republic:19,-70.7;Algeria:28,3;Ecuador:-2,-77.5;Egypt:27,30;Eritrea:15,39;Western Sahara:24.5,-13;
Spain:40,-4;Estonia:59,26;Ethiopia:8,38;Finland:64,26;Fiji:-18,175;Falkland Islands:-51.75,-59;
France:46,2;Faroe Islands:62,-7;Micronesia:6.917,158.25;Gabon:-1,11.75;United Kingdom:54,-2;
Georgia:42,43.5;Guernsey:49.46,-2.583;Ghana:8,-2;Gibraltar:36.13,-5.35;Guinea:11,-10;
Guadeloupe:16.25,-61.583;Gambia:13.47,-16.57;Guinea-bissau:12,-15;Equatorial Guinea:2,10;Greece:39,22;
Grenada:12.117,-61.67;Greenland:72,-40;Guatemala:15.5,-90.25;French Guiana:4,-53;Guam:13.47,144.783;
Guyana:5,-59;Hong Kong:22.267,114.188;Honduras:15,-86.5;Croatia:45.17,15.5;Haiti:19,-72.417;Hungary:47,20;
Indonesia:-5,120;Isle of Man:54.25,-4.5;India:20,77;British Indian Ocean Territory:-6,71.5;Ireland:53,-8;
Iran:32,53;Iraq:33,44;Iceland:65,-18;Israel:31.47,35.13;Italy:42.83,12.83;Jamaica:18.25,-77.5;
Jersey:49.25,-2.17;Jordan:31,36;Japan:36,138;Kazakhstan:48,68;Kenya:1,38;Kyrgyzstan:41,75;Cambodia:13,105;
Kiribati:1.417,173;Saint Kitts And Nevis:17.33,-62.75;South Korea:37,127.5;Kosovo:42.67,21.17;Kuwait:29.5,45.75;
Laos:18,105;Lebanon:33.83,35.83;Liberia:6.5,-9.5;Libya:25,17;Saint Lucia:13.883,-60.97;Liechtenstein:47.27,9.53;
Sri Lanka:7,81;Lesotho:-29.5,28.5;Lithuania:56,24;Luxembourg:49.75,6.16;Latvia:57,25;Macau:22.17,113.55;
Saint Martin:18.083,-63.95;Morocco:32,-5;Monaco:43.73,7.4;Moldova:47,29;Madagascar:-20,47;Maldives:3.25,73;
Mexico:23,-102;Marshall Islands:9,168;Macedonia:41.83,22;Mali:17,-4;Malta:35.83,14.583;Myanmar:22,98;
Montenegro:42.5,19.3;Mongolia:46,105;Northern Mariana Islands:15.2,145.75;Mozambique:-18.25,35;Mauritania:20,-12;
Montserrat:16.75,-62.2;Martinique:14.67,-61;Mauritius:-20.283,57.55;Malawi:-13.5,34;Malaysia:2.5,112.5;
Mayotte:-12.83,45.17;Namibia:-22,17;New Caledonia:-21.5,165.5;Niger:16,8;Norfolk Island:-29.03,167.95;
Nigeria:10,8;Nicaragua:13,-85;Niue:-19.03,-169.87;Netherlands:52.5,5.75;Norway:62,10;Nepal:28,84;
Nauru:-0.53,166.917;New Zealand:-41,174;Oman:21,57;Pakistan:30,70;Panama:9,-80;Pitcairn:-25.07,-130.1;
Peru:-10,-76;Philippines:13,122;Palau:7.5,134.5;Papua New Guinea:-6,147;Poland:52,20;Puerto Rico:18.25,-66.5;
North Korea:40,127;Portugal:39.5,-8;Paraguay:-23,-58;Palestine:31.9,35.2;French Polynesia:-15,-140;Qatar:25.5,51.25;
Reunion:-21.15,55.5;Romania:46,25;Russian Federation:60,100;Rwanda:-2,30;Saudi Arabia:25,45;Sudan:15,30;Senegal:14,-14;
Singapore:1.36,103.8;SouthGeorgia:-54.5,-37;Svalbard and Jan Mayen:78,20;Solomon Islands:-8,159;
Sierra Leone:8.5,-11.5;El Salvador:13.83,-88.916;San Marino:43.76,12.416;Somalia:10,49;
SaintPierreandMiquelon:46.83,-56.33;Serbia:44,21;SouthSudan:7,30;Sao Tome:1,7;
Suriname:4,-56;Slovakia:48.66,19.5;Slovenia:46.116,14.816;Sweden:62,15;Swaziland:-26.5,31.5;
Sint Maarten:18.03,-63.05;Seychelles:-4.583,55.66;Syrian Arab Republic:35,38;TurksandCaicosIslands:21.75,-71.583;
Chad:15,19;Togo:8,1.16;Thailand:15,100;Tajikistan:39,71;Tokelau:-9,-172;Turkmenistan:40,60;East Timor:-8.83,125.916;
Tonga:-20,-175;Trinidad And Tobago:11,-61;Tunisia:34,9;Turkey:39,35;Tuvalu:-8,178;Taiwan:23.5,121;Tanzania:-6,35;
Uganda:1,32;Ukraine:49,32;United States Minor Outlying Islands:19.2911437,166.618332;Uruguay:-33,-56;United States:38,-97;
Uzbekistan:41,64;Vatican City State:41.9,12.45;St Vincent/Grenadines:13.25,-61.2;Venezuela:8,-66;
Virgin Islands (British):18.431383,-64.62305;Virgin Islands (U.S.):18.35,-64.933333;Viet Nam:16.16,107.83;
Vanuatu:-16,167;Wallis and Futuna:-13.3,-176.2;Samoa:-13.583,-172.33;Yemen:15,48;South Africa:-29,24;
Zambia:-15,30;Zimbabwe:-20,30'''

import re
pattern = re.compile(r"^[\n]{0,1}(?P<country>[\w\s\-\(\)\./]+):(?P<long>[\d\.\-]+),(?P<lat>[\d\.\-]+)$",re.M)

COUNTRIES_GPS = {}
for country in COUNTRIES_GPS_STRING.split(';'):
    match = pattern.search(country)
    COUNTRIES_GPS[match.group("country")] = (float(match.group("long")),float(match.group("lat")))


COLOR_NODES = {"Y": "255,255,0", # default color for gephi display
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


def generate_cooc_graph(df_corpus=None, size_min=1):
    
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
     ex: size node_item1=2, size node_item2=1
     
     The weight w_ij of a vertex is the number of occurrences of the tuple (item_i,item_j) in the
     list of tuples [(item_i,item_j),...] where item_i and item_j are 
         (i) related to the same pub_id 
         (ii) item_i != item_j 
         (iii) (item_i,item_j) is equivalent to (item_j,item_i).
     
     The nodes has one id and two attributes: the size of the node and its label. 
     
     The edges have two attributes: their weight w_ij and their cosine similarity 

                                                        w_ij
                               cos_ij = ----------------------------------------
                                          sqrt(size(node_i) * sqrt(size(node_j)
    
    Args:
        df_corpus (dataframe): dataframe structured as |pub_id|item|
        min_size (int): minimum size of the node to be retained
        
    Return:
        The function returns G a networkx object.
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
                                                                      # of occurrrences less than size_min
    index_to_drop = [x[0]  for x in zip(df_corpus.index ,df_corpus['item']) 
                           if x[1] in labels_to_drop]
    df_corpus.drop(index_to_drop, inplace = True)                     # Cleaning of the dataframe
   
    #                 Building the set of nodes and the set of edges
    #------------------------------------------------------------------------------------------------
    df_corpus.columns = ['pub_id','item' ]
    nodes_id = list(set(df_corpus['item']))                 # Attribution of a integer id to the items
    dic_nodes = dict(zip(nodes_id,range(len(nodes_id))))    # Number of an item occurrence keyed by the
                                                            #   node id
    dic_size = dict(zip(dg['item'],dg['count']))
    nodes_size = {dic_nodes[x]:dic_size[x] for x in nodes_id}


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
                    
                    
    #                            Building the networx object graph G
    #------------------------------------------------------------------------------------------------
    G = nx.Graph()
    G.add_nodes_from(dic_nodes.values()) 
    G.add_edges_from(list_edges)
    nx.set_node_attributes(G,nodes_size, 'node_size')
    nx.set_node_attributes(G,dict(zip(dic_nodes.values(), dic_nodes.keys())), 'label' )
    nx.set_edge_attributes(G, weight, 'nbr_edges')
    cos = {}
    for edge in list_edges: # Computes the cosine similarity
            cos[edge] = weight[edge] / math.sqrt(nodes_size[edge[0]] * nodes_size[edge[1]])
            
    nx.set_edge_attributes(G, cos, 'cos_similarity')
    
    return G

def plot_cooc_graph(G,node_size_ref=30):
    
    '''Plots the cooccurrenre graph G .
    We fix the layout to be of type "spring_layout"
    
    Args:
     G (networkx ogject): Built using the function "generate_cooc_graph"
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
    
    #cmap = cm.get_cmap('viridis', max(partition.values()) + 1) (for future use)
    fig = plt.figure(figsize=(15,15))
    _ = nx.draw_networkx_nodes(G, pos, node_size=node_sizes) #, partition.keys(),(for future use)
    #cmap=cmap, node_color=list(partition.values())) (for future use)
    _ = nx.draw_networkx_edges(G, pos, alpha=0.9,width=1.5, edge_color='k', style='solid',)
    labels = nx.draw_networkx_labels(G,pos=pos,font_size=8,
                                       font_color='w')

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
        edge_similarity = nx.get_edge_attributes(G,'cos_similarity')
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


    G = generate_cooc_graph(df_corpus=df, size_min=size_min)
    
    filename_out = Path('cooc_' + item + '_thr' + str(size_min) + '.gdf')
    write_cooc_gdf(G,item,COLOR_NODES[item],out_dir / filename_out )
    
    return G