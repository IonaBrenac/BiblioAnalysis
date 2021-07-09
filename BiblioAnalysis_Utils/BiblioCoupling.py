__all__ = ['build_coupling_graph','build_louvain_partition',
          'plot_coupling_graph','save_communities_xls','save_communities_gexf']

from .BiblioParsingGlobals import DIC_OUTDIR_PARSING
           
BCTHR = 1 # minimum number of shared references to keep a link (default 1)

RTUTHR = 2 # minimum time of use in the corpus to count a reference in the 
           #shared references (default 2)

WTHR = 0 # minimum weight to keep a link (default 0)

NRTHR = 1 # minimum number of references to keep a node (default 1)

NRUNS = 1 # number of time the louvain algorithm is run for a given network, 
          # the best partition being kept (default 1)
       
SIZECUT = 10
verbose = True

FILENAME_GEXF = 'biblio_network.gexf'
FILENAME_XLSX = 'biblio_network.xlsx'

def build_coupling_graph(in_dir):
    
    '''Builds a graph G(N,V) where:
            - N is the set of nodes with two attributes: article id and number of references
            - V is the set of vertices. A vertex links two articles if and only if:
                   (i)   they share at least "BCTHR" references
                   (ii)  each article has at least "NRTHR" references
                   (iii) their Kessler similarity w_ij is >= "WTHR"
              A vertex has two attributes: number of shared references 
                                           and the Kessler similarity     
    The Kessler similarity is defined as: 
                       
                  # of common references between pub_id_i and pub_id_j
         w_ij = ---------------------------------------------------------
                sqrt(# references of pub_id_i * # references of pub_id_j)
                                 
    It returns the networkx object G
    '''
     
    # Standard library import
    from collections import defaultdict
    from more_itertools import distinct_combinations
    from pathlib import Path
    
    # 3rd party import
    import math
    import networkx as nx
    import pandas as pd


    # The references and their ids are extracted from the file articles.dat (tsv format)
    # ---------------------------------------------------------------------------------------

    df_article = pd.read_csv(in_dir / Path(DIC_OUTDIR_PARSING['A']),
                 sep='\t',
                 header=None,
                 usecols=[0,1,2,3,4,5]).fillna(0).astype(str)
    df_article.columns = ['pub_id','first_author','year','journal','volume','page']

    table_art = df_article.apply(lambda row : ", ".join(row[1:]),axis=1) # Builds ref: "author, year, journal, volume, page"
                                                                     # ex:"Gordon P, 2004, SCIENCE, 306, 496"
    table_art = [x.replace(', 0','') for x in table_art] # takes care of the unknown volume and/or page number
                                                 # ex: "Ahn H., 2010,THESIS"
    df_article['label_article'] = table_art

    df_article['pub_id'] = pd.to_numeric(df_article['pub_id'])



    # 1- Creates the dict named ref_table = {ref A: [list of article id (pub_id) citing ref A]}
    # ex : ref_table = {'Bellouard Q, 2017, INT. J. HYDROG. ENERGY, 42, 13486': [0, 50],...}
    # 2- creates the dict named nR = {pub_id: number of references of pub_id}
    # ---------------------------------------------------------------------------------------

    df_reference = pd.read_csv(in_dir / Path(DIC_OUTDIR_PARSING['R']),
                               sep='\t',
                               header = None,
                               usecols=[0,1,2,3,4,5],
                               na_filter=False).astype(str)
    df_reference.columns = ['pub_id','first_author','year','journal','volume','page']

    table = df_reference.apply(lambda row : ", ".join(row[1:]), axis=1) # Builds ref: "author, year, journal, volume, page"
                                                                        # ex:"Gordon P, 2004, SCIENCE, 306, 496"
    table = [x.replace(', 0','') for x in table] # takes care of the unknown volume and/or page number
                                                 # ex: "Ahn H., 2010,THESIS"
    df_reference['label_ref'] = table

    df_reference['pub_id'] = pd.to_numeric(df_reference['pub_id'])

    nR = df_reference.groupby('pub_id').count().to_dict()['first_author']

    ref_table = {x[0]:x[1].tolist() for x in df_reference.groupby('label_ref')['pub_id']}


    # Builds the dict of dicts BC_table such as:
    #   BC_table = {pub_id_i:{pub_id_j: number of common references of pub_id_i and pub_id_j,...},...}
    # ex : BC_table = {0: {50: 8, 55: 2, 121: 2, 10: 2},...}
    #   pub_id 0 has 8 common references with pub_id 50; pub_id 0 has 2 common references with pub_id 55
    #----------------------------------------------------------------------------------------------

    BC_table = {}
    for reference in ref_table:
        if len(ref_table[reference]) >= RTUTHR:  # The reference is cited more than RTUTHR-1 times
            for pub_id_i,pub_id_j  in distinct_combinations(ref_table[reference], 2):
                if pub_id_i not in BC_table:
                    BC_table[pub_id_i] = dict()
                if pub_id_j not in BC_table[pub_id_i]:
                    BC_table[pub_id_i][pub_id_j] = 0
                BC_table[pub_id_i][pub_id_j] += 1   
                
    # Builds the graph netwokx objet G with edge atributes:
    #    1-   the Kessler similarity  w_ij
    #    2-   the number of common references between pub_id_i and pub_id_j                                 
    #----------------------------------------------------------------------------------------------

    G = nx.Graph()
    for pub_id_i in BC_table:
        for pub_id_j in BC_table[pub_id_i]:
            w_ij = (1.0 * BC_table[pub_id_i][pub_id_j]) \
                   / math.sqrt(nR[pub_id_i] * nR[pub_id_j]) # Kessler similarity
            if (
                (BC_table[pub_id_i][pub_id_j] >= BCTHR) # Number of common references 
                                                        #   between id_i and id_j>=BCTHR
                and (nR[pub_id_i] >= NRTHR)             # Number of references of id_i>=NRTHR (default=1)
                and (nR[pub_id_j] >= NRTHR)             # Number of references of id_j>=NRTHR (default=1)
                and (w_ij >= WTHR)                      # Kessler similarity >=WTHR (default=0)
            ):
                G.add_edge(pub_id_i, pub_id_j, weight=w_ij, nc=BC_table[pub_id_i][pub_id_j])
    
    nx.set_node_attributes(G,nR,'nbr_references')
    
    node_label = {x:df_article.loc[df_article['pub_id'] == x,'label_article'].tolist()[0] for x in G.nodes}
    nx.set_node_attributes(G,node_label,'label')
    
    node_first_author = {x:df_article.loc[df_article['pub_id'] == x,'first_author'].tolist()[0] for x in G.nodes}
    nx.set_node_attributes(G,node_first_author,'first_author')
    
    node_year = {x:df_article.loc[df_article['pub_id'] == x,'year'].tolist()[0] for x in G.nodes}
    nx.set_node_attributes(G,node_year,'year')
    
    node_journal = {x:df_article.loc[df_article['pub_id'] == x,'journal'].tolist()[0] for x in G.nodes}
    nx.set_node_attributes(G,node_journal,'journal')

    return G

def build_louvain_partition(G):
    
    '''Computes graph G partition into communities using Louvain algorithm.
    The attribute community is added to the nodes.
    '''
    
    # 3rd party import
    import community as community_louvain
    import networkx as nx
    
    # Compute the best partition : {pub_id:community_id}
    partition = community_louvain.best_partition(G)
    
    nx.set_node_attributes(G,partition,'community_id')
    
    return G,partition


def plot_coupling_graph(G,partition,nodes_number_max=1):
    
    
    # Plots the result coloring each node according to its community
    # nodes_number_max (default = 1): minimum number of nodes in a community 
    # to keep the community on the plot 
    # The layout is fixed to "spring_layout"
    # ----------------------------------------------------------------
    
    # 3rd party import
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt
    import networkx as nx
    import pandas as pd
    
    
    
    # Suppress communities with a number of nodes less than nodes_number_max
    df = pd.DataFrame(list(partition.items()),columns = ['pub_id','community_id']) 
    dg = df.groupby('community_id').count().reset_index()
    community_to_discard = list(dg[dg['pub_id']<nodes_number_max ] ['community_id'])
    nodes_to_dicard = list(df.query('community_id in @community_to_discard')['pub_id'])
    partition_number = max(partition.values()) - len(community_to_discard)
    G.remove_nodes_from(nodes_to_dicard)
    new_partition = {key:value for key,value in partition.items()
                 if value not in community_to_discard}
    
    # Draw the graph
    pos = nx.spring_layout(G)
    # color the nodes according to their partition
    
    cmap = cm.get_cmap('viridis',partition_number + 1)
    fig = plt.figure(figsize=(15,15))
    nx.draw_networkx_nodes(G, pos, new_partition.keys(), node_size=250,
                           cmap=cmap, node_color=list(new_partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.9,width=1.5, edge_color='k', style='solid',)

    labels = nx.draw_networkx_labels(G,pos=pos,font_size=8,
                                     font_color='w')
                                     
    node_degree = dict(G.degree).values()
    mean_degree = sum(node_degree) * 1.0 / len(node_degree)
    mean_weight = 2*sum([d[-1]['weight'] for d in G.edges(data=True)])/(len(G.nodes()) * (len(G.nodes()) - 1))
                                   
    plt.title(f'Coupling graph \nAverage degree: {mean_degree:.2f}\
                Average weight: {mean_weight:.5f}',fontsize=23,fontweight="bold")
    plt.show()
    

def save_communities_xls(partition,in_dir,out_dir):
    
    '''Saves the "articles.dat" file as a .xlsx file adding the column community_id
    of each article of the corpus after the Louvain partitioning.
    '''
    
    # Standard library imports
    from pathlib import Path
    
    # 3rd party import
    import pandas as pd
    
    df_articles = pd.read_csv(in_dir / Path(DIC_OUTDIR_PARSING['A']),sep="\t",header=None)

    df_articles['communnity'] = df_articles[0].map(partition) # Adds column community
    df_articles.sort_values(by=['communnity',0],inplace=True)
    df_articles.columns = ['pub_id','first_author','year','journal',
                           'volume','page','doi','pub_type','language','title','ISSN','community_id']
    df_articles.to_excel(out_dir / Path(FILENAME_XLSX))

    
def save_communities_gexf(G,save_dir):
    
    '''Save the graph "G" at Gephy (.gexf) format using full path "save_dir"
    '''
    
    # Standard library imports
    from pathlib import Path
    
    # 3rd party imports
    import networkx as nx
    
    nx.write_gexf(G,save_dir / Path(FILENAME_GEXF))
    

def runpythonlouvain(G):
    
    '''Used to analyse a corpus at level "len(foo_dendrogram) - 1)" of the graph G dendrogram.
    Author: Sebastian Grauwin (http://sebastian-grauwin.com/bibliomaps/)
    
    Args:
        G (networkx object): corpus graph
        
    Returns:
        dendrogram: see https://buildmedia.readthedocs.org/media/pdf/python-louvain/latest/python-louvain.pdf
        partition: see https://buildmedia.readthedocs.org/media/pdf/python-louvain/latest/python-louvain.pdf
        modularity: see https://buildmedia.readthedocs.org/media/pdf/python-louvain/latest/python-louvain.pdf
    '''
    
    # 3rd party import
    import community as community_louvain
    
    max_modularity = -1
    for run in range(NRUNS):
        if NRUNS > 1:
            print(f'......run {run + 1}/{NRUNS}')
        foo_dendrogram = community_louvain.generate_dendrogram(G, part_init=None)
        partition_foo = community_louvain.partition_at_level(foo_dendrogram, len(foo_dendrogram) - 1)
        modularity = community_louvain.modularity(partition_foo, G)
        if modularity > max_modularity:
            max_modularity = modularity
            partition = partition_foo.copy()
            dendrogram = foo_dendrogram.copy()
            
    return [dendrogram, partition, modularity]

def graph_community(G):
        
    '''Used to analyse a corpus at two levels of the graph G dendrogram in a way
    that the size of all the communities are <= SIZECUT 
    Author: Sebastian Grauwin (http://sebastian-grauwin.com/bibliomaps/)
    
    Args:
        G (networkx object): corpus graph
        
    Returns:
        louvain_partition (dict): partition of the corpus 
    '''
    
    import community as community_louvain

    dendrogram, part, max_mod = runpythonlouvain(G)
    part2 = part.copy()
    to_update = {}

    communities_id,nodes_id =set(part.values()), list(part.keys())
    for community_id in communities_id:
        list_nodes = [nodes for nodes in part.keys() if part[nodes] == community_id]

        if len(list_nodes) > SIZECUT: # split clusters of size > SIZECUT
            H = G.subgraph(list_nodes).copy()
            [dendo2, partfoo, mod] = runpythonlouvain(H)
            dendo2 = community_louvain.generate_dendrogram(H, part_init=None)
            partfoo = community_louvain.partition_at_level(dendo2, len(dendo2) - 1)
            # add prefix code
            for aaa in partfoo.keys():
                partfoo[aaa] = (community_id + 1) * 1000 + partfoo[aaa]
            nb_comm = len(set(partfoo.values()))
            if verbose:
                print(
                    "... ==> cluster %d (N=%d records) was split in %d sub-clusters, Q=%.3f"
                    % (community_id, len(list_nodes), nb_comm, mod)
                )
            part2.update(partfoo)
        else:  # for communities of less than SIZECUT nodes, shift the com label as well
            for n in list_nodes:
                to_update[n] = ""
    for n in to_update:
        part2[n] += 1

    # ... save partitions
    louvain_partition = dict()
    for lev in range(len(dendrogram)):
        louvain_partition[lev] = community_louvain.partition_at_level(dendrogram, lev)
    # .. I want communtity labels starting from 1 instead of 0 for top level
    for k in louvain_partition[len(dendrogram) - 1].keys():
        louvain_partition[len(dendrogram) - 1][k] += 1
    louvain_partition[len(dendrogram)] = part2
    
    return louvain_partition

def networkx_to_louvain_format(communities):
    
    '''Transforms the tuple ({pub_id_1.1,pub_id_1.2,pup_id_1.3,...},{pub_id_2.1,pub_id_2.2,pub_id_2.3,...},...) 
    generated by the networkx community algorithms into the set {pub_id:community_id} as generated by the Louvain
    algorithm.
    '''
    a = {idx:community for idx,community in enumerate(communities)}
    return {val:com_id for com_id in a.keys() for val in a[com_id]} 