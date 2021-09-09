__all__ = ['coupling_graph_html_plot',
           'cooc_graph_html_plot']

def cooc_graph_html_plot(G,html_file):
    
    from pyvis.network import Network
    import networkx as nx

    def map_algs(g,alg='barnes'):
        if alg == 'barnes':
            g.barnes_hut()
        if alg == 'forced':
            g.force_atlas_2based()
        if alg == 'hr':
            g.hrepulsion()
    
    nt = Network(height=500, width=500, 
                 bgcolor='#222222', 
                 font_color='white',notebook=False)
    # populates the nodes and edges data structures
    nt.from_nx(G)
    map_algs(nt,alg='barnes')
    for node in nt.nodes:
        node['title'] = node['label']
        node['size'] = node['node_size']
    for edge in nt.edges:
        edge['title'] = str(edge['nbr_edges'])
        edge['value'] = edge['nbr_edges']
    neighbor_map = nt.get_adj_list()

    dic_label = {node['id']:node['label'] for node in nt.nodes}
    # add neighbor data to node hover data
    for node in nt.nodes:
        idd = node['id'] 
        title = '<b>'+dic_label[idd] + '</b>'+ '<br>' +'<br>'.join([dic_label[i] for i in neighbor_map[idd]])
        node['title'] = title
    nt.show_buttons()
    nt.show(html_file)

def coupling_graph_html_plot(G,html_file):
    
    from pyvis.network import Network
    import json
    import networkx as nx
    # Attention limited to 22 communities
    color_nodes = {0: '#B03A13',
                   1: '#B04513',
                   2: '#B05213',
                   3: '#B05F13',
                   4: '#B06913',
                   5: '#B07113',
                   6: '#B07E13',
                   7: '#B08E13', 
                   8: '#B09E13',
                   9: '#B0A313',
                   10: '#A6B013',
                   11: '#81B013',
                   12: '#6FB013',
                   13: '#52B013',
                   14: '#38B013',
                   15: '#13B01E',
                   16: '#13B0AB',
                   17: '#139EB0',
                   18: '#1389B0',
                   19: '#1374B0',
                   20: '#1367B0',
                   21: '#1357B0',
                   22: '#134DB0'}

    def map_algs(g,alg='barnes'):
        if alg == 'barnes':
            g.barnes_hut()
        if alg == 'forced':
            g.force_atlas_2based()
        if alg == 'hr':
            g.hrepulsion()

    nt = Network('500px', width='500px', 
                 bgcolor='#222222', 
                 font_color='white',notebook=False)
    # populates the nodes and edges data structures
    nt.from_nx(G)
    map_algs(nt,alg='barnes')

    for node in nt.nodes:
        node['title'] = 'community_id: ' + str(node['community_id'])+ '<br>'
        node['title'] += 'pub_id:'+ str(node['id'])+ '<br>'
        node['title'] += '<br>'.join([key + ': ' + str(node[key]) 
                                    for key in node.keys()
                                    if 'CU_' in key
                                    or 'TK_' in key
                                    or 'IK_' in key
                                    or 'AK_' in key
                                    or 'S_' in key
                                    or 'S2_' in key])
        node['size'] = node['nbr_references']
        node['color'] = color_nodes[node['community_id']]
        node['label'] = str(node['community_id'])
        if node['community_id']%2:
            node['shape'] = 'triangle'
        else:
            node['shape'] = 'dot'

    nt.show_buttons()
    nt.show(html_file)
