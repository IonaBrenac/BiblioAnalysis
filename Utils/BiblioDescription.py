NMAX_NODES = 100 # maximum number of nodes to keep

DIC_FREQ_FILES = {'AU':'freq_authors.dat',
                  'AK':'freq_authorskeywords.dat',
                  'CU':'freq_countries.dat',
                  'DT':'freq_doctypes.dat',
                   'I':'freq_institutions.dat',
                   'J':'freq_journals.dat',
                  'IK':'freq_keywords.dat',
                  'LA':'freq_languages.dat',
                   'R':'freq_references.dat',
                  'RJ':'freq_refjournals.dat',
                   'S':'freq_subjects.dat',
                  'S2':'freq_subjects2.dat',
                  'TK':'freq_titlewords.dat',
                   'Y':'freq_years.dat'}

LABEL_MEANING = {'AU' :'co-authors',
                 'AK' :'authors_keywords',
                  'CU':'countries',
                  'DT':'doc_type',
                   'I':'institution',
                   'J':'journal',
                  'IK':'journal_keywords',
                  'LA':'languages',
                   'R':'reference',
                  'RJ':'refjournal',
                   'S':'subjects',
                  'S2':'subjects2',
                  'TK':'title_words',
                   'Y':'year'}


# Buids a cooccurrence graph only for thes labels
VALID_LABEL_GRAPH = ['AU', 'CU', 'S', 'S2', 'K', 'R', 'RJ', 'I', 'AK', 'TK']

def frequency_analysis(df):

    '''Builds the dataframe "df_freq" and the arrays "q_item" and "p_item" from the dataframe "df".
    The dataframe "df" consists in two columns named "pub_id" and "item":

     ex_a:              pub_id   item
                    0     0     item_a
                    1     0     item_b
                    2     1     item_c
                    3     2     item_a

    The dataframe "df" consists in three columns named "pub_id" "item" and "f" as (for ex_a):

                        item   count    f
                    0  item_a    2      50
                    1  item_b    1      25
                    2  item_c    1      25

    where : "count" is the total number of occurrence of the item (ex_a: count=2 for item_a )
            "f" is the frequency occurrence (100*count/total number of items) (ex_a: f=50% for item_a )

    "q_item" is array of two arrays: [array1,array2] where:
        array1 = [list of possible number of items per articles] = [#item1, #item2,..]
        array2 = [number of articles with a number of items #item1,
                  number of articles with a number of items #item2,...]
    for ex_a we have: [[1,2],[2,1]]

    "p_item" is an array of two arrays: [array1,array2] where:
        array1 = [list of possible number of occurrences of an item in the articles corpus ] = [#1, #2,..]
        array2 = [number of articles with a number of items #1, #2,...]
    for ex_a we have: [[1,2],[4,2]]

    '''

    def p_iterator(lst):
        c1 = sum(lst)
        for x  in  lst:
            yield c1
            c1 -=x

    df_freq = df.groupby('item').count().reset_index()
    df_freq.sort_values(by=['pub_id'],ascending=False,inplace=True)
    df_freq["f"] = df_freq['pub_id']/len(df)*100
    df_freq.columns = ['item','count','f']

    df_freq_stat = df.drop_duplicates().\
                      groupby('pub_id').count().reset_index().\
                      groupby('item').count().reset_index()
    q_item = [df_freq_stat['item'] .astype(int).to_list(),df_freq_stat['pub_id'].to_list()]

    df_freq_stat = df.drop_duplicates().\
                      groupby('item').count().reset_index().\
                      groupby('pub_id').count().reset_index()
    p_item = [df_freq_stat['pub_id'].to_list(), list(p_iterator(df_freq_stat['item'].to_list()))]

    return df_freq, q_item, p_item

def generate_cooc(df,item):

    '''Builds a coocurence undirected graph (N,V) where:
            - the set N of nodes is the set of the NMAX_NODES prominent items in term of occurrence
       frequency (by default NMAX_NODES=100)
            - the set of edges connecting two items sitting in the the same article

        As input we use the dataframe "df" which consists in two columns named "pub_id" and "item":

     ex_a:              pub_id   item
                    0     0     item_a
                    1     0     item_b
                    2     1     item_c
                    3     2     item_a

       Args:

    '''

    from collections import defaultdict


    #                           Builds nodes
    #----------------------------------------------------------------------------
    liste_node = []
    dict_node={}
    dg = df.groupby('item').count()\
                      .reset_index()\
                      .sort_values(by='pub_id',ascending=False)\
                      .iloc[:NMAX_NODES,:] # Selects the n most prominent items
                                           # in term of rate occurrence

    for node,x in enumerate(dg.iterrows()):
        dict_node[x[1]["item"]] = node
        liste_node.append({"type":item,
                           "name":node,
                           "item":x[1]["item"],
                           "size":x[1]["pub_id"]})

    #                           Builds edges
    #----------------------------------------------------------------------------
    dic_item_to_keep = {}
    comm = defaultdict(int)

    item_to_keep = set(dg['item'].to_list()) # Buils the n-top list of the n items
                                             # with the higher occurrence rate

    for x in df.groupby('pub_id')['item']:   # For each article, keeps items in the n-top list
        item_publi = set(x[1].to_list())
        item_publi_to_keep = item_publi.intersection(item_to_keep)
        if len(item_publi_to_keep):
            dic_item_to_keep[x[0]] = item_publi_to_keep


    for item_to_keep in dic_item_to_keep.values() : # Builds a edge between two items if
                                                    # there are are in the same article item list
        for source in item_to_keep:
            for target in [x for x in item_to_keep if x > source]:
                comm[source,target] += 1

    liste_edge = []
    for edge,weight in comm.items():
        liste_edge.append({"type":item,
                           "source":dict_node[edge[0]],
                           "target":dict_node[edge[1]],
                           "Ncooc":weight})

    return liste_node, liste_edge

def describe_item(df,item,dic_distrib_item,list_cooc_nodes,list_cooc_edges ,freq_filename):

    '''Builds the dataframe "df_freq" and the arrays "q_item" and "p_item for :
    item = 'AU','AK','CU', 'DT', 'I', 'J', 'IK', 'LA', 'R', 'RJ', 'S', 'S2', 'TK', 'Y'
       Builds the coocurence undirected graph
    item = 'AU', 'CU', 'S', 'S2', 'K', 'R', 'RJ', 'I', 'AK', 'TK'
    '''


    df.columns = ['pub_id','item']
    df_freq, q_item, p_item = frequency_analysis(df)

    df_freq.to_csv(freq_filename,sep=',', index = False)

    dic_distrib_item["q"+item.capitalize()] = q_item
    dic_distrib_item["p"+item.capitalize()] = p_item

    if item in VALID_LABEL_GRAPH:
        liste_node, liste_edge = generate_cooc(df,item)

        list_cooc_nodes.extend(liste_node)
        list_cooc_edges.extend(liste_edge)


def describe_corpus(in_dir, out_dir, verbose):

    '''Using the files xxxx.dat generated by the parsing function biblio_parser and stored in
    the folder parsing, the function describe_corpus generates the files freq_xxxx.dat and
    two .json files. These new files are stored in the folder freq.
    home path//BiblioAnalysis Data/
    |-- myprojectname/
    |   |-- freq/
    |   |   |-- coocnetworks.json, DISTRIBS_itemuse.json
    |   |   |-- freq_authors.dat, freq_authorskeywords.dat, freq_countries.dat
    |   |   |-- freq_doctypes.dat, freq_institutions.dat, freq_journals.dat
    |   |   |-- freq_keywords.dat, freq_languages.dat, freq_references.dat
    |   |   |-- freq_refjournals.dat, freq_subjects.dat, freq_subjects2.dat
    |   |   |-- freq_titlewords.dat, freq_years.dat
    |   |-- parsing/
    |   |   |-- addresses.dat, articles.dat, authors.dat, countries.dat, database.dat
    |   |   |-- institutions.dat, keywords.dat, references.dat, subjects.dat, subjects2.dat

    '''

    import json
    from pathlib import Path
    import re

    import pandas as pd

    dic_distrib_item = {}
    list_cooc_nodes = []
    list_cooc_edges = []



    with open(in_dir/Path("database.dat" ), "r") as file:
        dic_distrib_item["database"] = file.read().strip("\n")

    df_articles = pd.read_csv(in_dir/Path("articles.dat"),
                              sep='\t',
                              header=None,
                              usecols=[0,2,3,7,8])
    df_articles.rename (columns = {0:'pub_id',
                                  3:'Source title',
                                  2:'Year',
                                  7:'Document Type',
                                  8:'Language of Original Document',},
                       inplace = True)
    dic_distrib_item["N"] = len(df_articles)

    item = "Y"                       # Deals with years
    describe_item(df_articles[['pub_id','Year']],
                   item,
                   dic_distrib_item,
                   list_cooc_nodes,
                   list_cooc_edges,
                   out_dir/Path(DIC_FREQ_FILES[item]))

    item = "J"                     # Deals with journals title (ex: PHYSICAL REVIEW B)
    describe_item(df_articles[['pub_id','Source title']],
                  item,
                  dic_distrib_item,
                  list_cooc_nodes,
                  list_cooc_edges,
                  out_dir/Path(DIC_FREQ_FILES[item]))

    item = "DT"                    # Deal with doc type (ex: article, review)
    describe_item(df_articles[['pub_id','Document Type']],
                  item,
                  dic_distrib_item,
                  list_cooc_nodes,
                  list_cooc_edges,
                  out_dir/Path(DIC_FREQ_FILES[item]))

    item = "LA"                   # Deal with language
    describe_item(df_articles[['pub_id','Language of Original Document']],
                  item,
                  dic_distrib_item,
                  list_cooc_nodes,
                  list_cooc_edges,
                  out_dir/Path(DIC_FREQ_FILES[item]))

    item = 'AU'                   # Deals with authors
    df = pd.read_csv(in_dir / Path('authors.dat'),
                     sep='\t',
                     header=None,
                     usecols=[0,2])
    describe_item(df,
                  item,
                  dic_distrib_item,
                  list_cooc_nodes,
                  list_cooc_edges,
                  out_dir/Path(DIC_FREQ_FILES[item]))

    df = pd.read_csv(in_dir / Path('keywords.dat'),
                     sep='\t',
                     header=None,
                     usecols=[0,1,2])
    df.columns = ['pub_id','type','item']

    for item in ['AK','IK','TK']:      # Deals with keywords
        describe_item(df.query('type==@item')[['pub_id','item']],
                      item,
                      dic_distrib_item,
                      list_cooc_nodes,
                      list_cooc_edges,
                      out_dir/Path(DIC_FREQ_FILES[item]))


    item = 'S'                        # Deals with subjects
    df = pd.read_csv(in_dir / Path('subjects.dat'),
                     sep='\t',
                     header=None)
    describe_item(df,
                  item,
                  dic_distrib_item,
                  list_cooc_nodes,
                  list_cooc_edges,
                  out_dir/Path(DIC_FREQ_FILES[item]))

    item = 'S2'                      # Deals with subject2
    try:
        df = pd.read_csv(in_dir / Path('subjects2.dat'),
                         sep='\t',
                         header=None)
        describe_item(df,
                      item,
                      dic_distrib_item,
                      list_cooc_nodes,
                      list_cooc_edges,
                      out_dir/Path(DIC_FREQ_FILES[item]))
    except:
        print('no file subjects2.dat found')

    item = 'I'                       # Deals with institutions
    df = pd.read_csv(in_dir / Path('institutions.dat'),
                     sep='\t',
                     header=None,
                     usecols=[0,2] )
    describe_item(df,
                  item,
                  dic_distrib_item,
                  list_cooc_nodes,
                  list_cooc_edges,
                  out_dir/Path(DIC_FREQ_FILES[item]))

    item = 'CU'                     # Deals with countries
    df = pd.read_csv(in_dir / Path('countries.dat'),
                     sep='\t',
                     header=None,
                     usecols=[0,2] )
    describe_item(df,
                  item,
                  dic_distrib_item,
                  list_cooc_nodes,
                  list_cooc_edges,
                  out_dir/Path(DIC_FREQ_FILES[item]))

    item = 'RJ'
    try:
        df = pd.read_csv(in_dir / Path('references.dat'),
                         sep='\t',
                         header=None,
                         usecols=[0,1,2,3,4,5] ).astype(str)
        describe_item(df[[0,3]],
                      item,
                      dic_distrib_item,
                      list_cooc_nodes,
                      list_cooc_edges,
                      out_dir/Path(DIC_FREQ_FILES[item]))

        item = 'R'
        find_0 = re.compile(r',\s?0')
        df['ref'] = df.apply(lambda row:re.sub(find_0,'', ', '.join(row[1:-1]))
                                     ,axis=1)
        describe_item(df[[0,'ref']],
                      item,
                      dic_distrib_item,
                      list_cooc_nodes,
                      list_cooc_edges,
                      out_dir/Path(DIC_FREQ_FILES[item]))
    except:
        print('no file references.dat found')

    #                    creates json files
    #---------------------------------------------------------------------
    with open(out_dir / Path('DISTRIBS_itemuse.json'),'w') as file:
        json.dump(dic_distrib_item,file,indent=4)

    dic_cooc = {}
    dic_cooc['nodes'] = list_cooc_nodes
    dic_cooc['links'] = list_cooc_edges
    with open(out_dir / Path('coocnetworks.json'),'w') as file:
        json.dump(dic_cooc,file,indent=4)

def plot_graph(in_dir,item):

    '''plot the communities graph which nodes and edges are extracted from
    the json file coocnetworks.json built by the function describe_corpus:

        {
        "nodes":[
            {"type":"AU","name":0,"item":"Abanades S","size":8},
            ...................................................
        ],
        "links":[
            {"type":"AU","source":0,"target":8,"Ncooc":5},
            ..............................................
        ]
        }

    where type = "AU", "S", "I", "CU", "S2", "K", "AK", "TK", "R", "RJ",
    '''

    import json
    from pathlib import Path
    import pprint


    import community as community_louvain
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt
    import networkx as nx
    import numpy as np
    import pandas as pd


    assert (item in VALID_LABEL_GRAPH),\
            f'unknown type {TYPE}: should be {", ".join(VALID_LABEL_GRAPH)}'

    # Extract nodes and edgesSets the graph  from the json coocnetworks.json
    # for type=TYPE
    # -----------------------------------------------------------
    file_coocnetworks = in_dir / Path('coocnetworks.json')
    with open(file_coocnetworks, "r") as read_file:
                cooc = json.load(read_file)

    df = pd.DataFrame( cooc['links']).query('type==@item')
    G = nx.from_pandas_edgelist(df,source='source',target='target' )
    dg = pd.DataFrame(cooc['nodes']).query('type==@item')
    G.add_nodes_from(dg['name'])
    for index, row in dg.iterrows():
        src_attr_dict = {k: row.to_dict()[k] for k in ['item','size']}
        G.nodes[row['name']].update(src_attr_dict)

    # compute the best partition
    partition = community_louvain.best_partition(G)


    # draw the graph
    pos = nx.spring_layout(G)
    node_size = np.array(list(nx.get_node_attributes(G,'size').values()))*70
    cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    fig = plt.figure(figsize=(15,15))
    nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=node_size,
                           cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.9,width=1.5, edge_color='k', style='solid',)

    labels = nx.draw_networkx_labels(G,pos=pos,font_size=8,
                                   font_color='w')

    plt.title(f'Graph partition using the {LABEL_MEANING[item]} and the Louvain algorithm')
    plt.show()

    node = nx.get_node_attributes(G,'item')
    pprint.pprint(node)

    df = pd.DataFrame({node_id:[num_partition, node[node_id] ]
                       for node_id,num_partition in partition.items()}).T

    for g in df.groupby([0]):
        print(f'N° partition:{g[0]}, items: {g[1][1].to_list()}')

    return

def plot_histo(in_dir,item):

    '''Plots the histograms of the p and q statistics (see frequency_analysis for more details).
    The data are extracted from the json file DISTRIBS_itemuse.json
    built by the funtion describe_corpus
    '''

    import json
    import matplotlib.pyplot as plt


    file_distrib_item = in_dir / Path('DISTRIBS_itemuse.json')
    with open(file_distrib_item, "r") as read_file:
                    distrib_item = json.load(read_file)

    #        Plots the q histogram
    #------------------------------------------------------
    q = distrib_item['q' + item.capitalize()]
    print("q",q)
    fig = plt.figure(figsize=(15,7))
    plt.subplot(1,2,1)
    _ =plt.bar(q[0], q[1] , width=0.8, bottom=None)
    plt.xlabel(f'# {LABEL_MEANING[item]}/article')
    plt.ylabel(f'# articles')
    plt.title(f'Histogram {LABEL_MEANING[item]}')

    #        Plots the p histogram
    #------------------------------------------------------
    p = distrib_item['p' + item.capitalize()]
    print("p",p)
    plt.subplot(1,2,2)
    _ = plt.bar(p[0], p[1] , width=0.8, bottom=None)
    plt.xlabel(f'# articles / {LABEL_MEANING[item]}')
    plt.ylabel(f'# {LABEL_MEANING[item]}')
    plt.title(f'Histogram {LABEL_MEANING[item]}')
