__all__ = ['coupling_graph_html_plot',
           'cooc_graph_html_plot']

var_options = {
  "nodes": {
    "color": {
      "border": "rgba(11,22,127,1)",
      "background": "rgba(120,142,196,1)"
    }
  },
  "edges": {
    "color": {
      "color": "rgba(120,142,196,1)",
      "inherit": False
    },
    "smooth": False
  },
  "physics": {
    "enabled": False,
    "barnesHut": {
      "gravitationalConstant": -80000,
      "springLength": 250,
      "springConstant": 0.001
    },
    "minVelocity": 0.75
  }
}

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
    
    dic_tot_edges ={node:G.degree(node,'nbr_edges') for node in G.nodes}
    
    nt = Network(height=1000, width=1000, 
                 bgcolor='#EAEDED', 
                 font_color='black',notebook=False)

    # populates the nodes and edges data structures
    nt.from_nx(G)
    dic_node_label = {str(node['id']):node['label'] for node in nt.nodes}
    map_algs(nt,alg='barnes')
    
    for edge in nt.edges:
        edge['title'] = edge['nbr_edges']
        edge['value'] = edge['nbr_edges']
    
    for node in nt.nodes:     
        node['title'] = node['label']
        node['size'] = node['node_size']
        node['tot_edges'] = dic_tot_edges[node['id']]
        node['nbr_edges_to'] = {}
        for edge in nt.edges:
            if edge['from'] == node['id']:
                node_to_label = dic_node_label[str(edge['to'])]
                node['nbr_edges_to'][node_to_label] = edge['nbr_edges']
            if edge['to'] == node['id']:
                node_from_label = dic_node_label[str(edge['from'])]
                node['nbr_edges_to'][node_from_label]=edge['nbr_edges']
    
    
    neighbor_map = nt.get_adj_list()
    
    dic_label_main = {node['id']: str(node['node_size']) + '-' \
                                 + node['label'] + ' (' \
                                 + str(node['tot_edges']) + ')' for node in nt.nodes}
    dic_label_neighbors = {}
    for node in nt.nodes:
        dic_label_neighbors[node['id']] = []
        for key in node['nbr_edges_to'].keys():
            dic_label_neighbors[node['id']].append(key + ' (' + str(node['nbr_edges_to'][key]) + ')')
        dic_label_neighbors[node['id']].sort()    
    
    # add neighbor data to node hover data
    for node in nt.nodes:
        idd = node['id'] 
        title = '<b>'+dic_label_main[idd] + '</b>'+ '<br>' +'<br>'\
                .join([dic_label_neighbors[idd][i] for i in range(len(dic_label_neighbors[idd]))])
        node['title'] = title
    #nt.set_options(options)
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

    nt = Network(height=1000, width=1000, 
                 bgcolor='#EAEDED', 
                 font_color='black',notebook=False)        

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
