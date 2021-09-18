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
    dic_node_label = {str(node['id']):str(node['node_size'])+ '-'\
                      + node['label'] for node in nt.nodes}
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
    

def coupling_graph_html_plot(G,html_file,community_id,attr_dic,colored_attr,
                             colored_values,shaped_attr,color_nodes,heading):
    
    from pyvis.network import Network
    import json
    import networkx as nx
    
    SG = G.__class__()
    if community_id != 'all':
        # Builds a sub-graph from G limited to the community 'community_id'
        selected_nodes = {n:d['community_id'] for n,d in G.nodes().items() \
                          if d['community_id'] == int(community_id)}
        nodes_list = list(selected_nodes.keys())
        SG.add_nodes_from((n, G.nodes[n]) for n in nodes_list)
        SG.add_edges_from((n, nbr, d)
                for n, nbrs in G.adj.items() if n in nodes_list
                for nbr, d in nbrs.items() if nbr in nodes_list)
        SG.graph.update(G.graph)
    else:
        SG = G
    
    # sets colored attributes keys  
    attr_nbr = attr_dic[colored_attr]
    attr_keys = [colored_attr + '_' + str(i) for i in range(attr_nbr)]
     
    def map_algs(g,alg='barnes'):
        if alg == 'barnes':
            g.barnes_hut()
        if alg == 'forced':
            g.force_atlas_2based()
        if alg == 'hr':
            g.hrepulsion()

    
    nt = Network(height=1000, width=1000, 
                 bgcolor='#EAEDED', 
                 font_color='black',notebook=False, heading= heading)        

    # populates the nodes data structures
    nt.from_nx(SG)
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
        
        node['label'] = str(node['id'])

        attr_labels = [node[attr_keys[i]][:node[attr_keys[i]].find('(')] for i in range(attr_nbr)]
        if attr_labels[0] in colored_values.keys():
            node['color'] = color_nodes[int(colored_values[attr_labels[0]])]
        else:
            node['color'] = color_nodes['uncolor']
        
        if shaped_attr in attr_labels :
            node['shape'] = 'triangle'
        else:
            node['shape'] = 'dot'
    
    nt.show_buttons(filter_=['physics'])
    nt.show(html_file)