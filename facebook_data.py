from __future__ import division
import pandas as pd
import networkx as nx
import matplotlib.pylab as plt
import seaborn
import community
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

class facebook_graph():
    def __init__(self, data_path, own_name):
        self.own_name = own_name
        self.data = pd.read_csv(data_path, header = 0)
        self.graph_without_self = nx.DiGraph()
        for idx, row in self.data.iterrows():
            if row[0] != own_name and row[1] != own_name:
                r0 = row[0].decode('utf-8')
                r1 = row[1].decode('utf-8')
                self.graph_without_self.add_node(r0)
                self.graph_without_self.add_node(r1)
                self.graph_without_self.add_edge(r0, r1)
                self.graph_without_self.add_edge(r1, r0)
        self.graph_without_self = self.graph_without_self.to_undirected()
        self.communities = None
        self.communities_names = None
        self.colors = None
        self.community_to_color = None
        
    def _ego_find_self(self):
        return self.graph_with_self.node.keys().index(self.name)
    
    def _color_distance_self(self, graph, radius, name):
        colors = []
        for n in graph.node.keys():
            colors.append(len(nx.shortest_path(graph, name, n))/(radius+1))
        self.colors = colors
        return colors
    
    def _add_legend_self(self, radius, colors, name):
        x = [0.0, 0.022]
        for ix, color in enumerate(sort(list(set(colors)))):
            y = [1-0.002-ix/100, 1-0.002-ix/100]
            fill_between(x, 1-0.008-ix/100 , y, color = plt.cm.RdBu(color), alpha = 0.5)
            index_dict = {1: 'st', 2: 'nd', 3: 'rd'}
            if ix == 0:
                annotate(name, xy=(0.022, 1-0.007-ix/100), xytext=(0.022, 1-0.007-ix/100), size = 13)
            elif ix < 4:
                annotate(str(ix)+index_dict[ix]+' cirle of friends', xy=(0.022, 1-0.007-ix/100), xytext=(0.022, 1-0.007-ix/100), size = 13)
            else:
                annotate(str(ix)+'th cirle of friends', xy=(0.022, 1-0.007-ix/100), xytext=(0.022, 1-0.007-ix/100), size = 13)
    
    def ego_plot(self, radius, name):
        inter_graph = nx.ego_graph(self.graph_without_self, name, radius = radius)
        colors = self._color_distance_self(inter_graph, radius, name)
        figsize(20, 20)
        nx.draw(inter_graph, node_color = [plt.cm.RdBu(color) for color in colors], alpha = 0.5, edge_color='lightgrey', font_size=10) 
        self._add_legend_self(radius, colors, name)
        title(name + ' ego graph', size = 20, weight = 'bold')
        return plt.show()
    
    def common_friends_plot(self):
        plt.figure(figsize=(10, 6))
        ax = plt.subplot(111)
        ax.hist(self.graph_without_self.degree().values(), bins = 25)
        ax.set_title('Number of friends by number of common friends', size = 14, weight = 'bold')
        ax.set_xlabel('Number of friends')
        ax.set_ylabel('Number of common friends')
        return plt.show()
    
    def _size_community(self):
        sizes = {}
        dict_degree = self.graph_without_self.degree()
        max_degree = max(dict_degree.values())
        for name in dict_degree:
            sizes[name] = dict_degree[name]/max_degree*3000
        return sizes
    
    def _communities(self):
        self.communities = community.best_partition(self.graph_without_self)
    
    def _colors_community(self):
        self._communities()
        c = self.communities
        max_community = max(c.values())
        colors = {k: c[k]/max_community for k in self.graph_without_self.node.keys()}
        self.colors = colors
            
    def _find_community_members(self):
        return {v: [name for name in self.communities if self.communities[name] == v] for v in set(self.communities.values())}
 
    def _set_communities_names(self):
        communities_names = []
        rev_dict = self._find_community_members()
        print 'Please input different names for each category'
        for community in sort(list(set(self.communities.values()))):
            wordlist = rev_dict[community][:min(len(rev_dict[community]), 10)]
            communities_names.append(self._ask_community_name(wordlist))
        self.communities_names = communities_names
        self._colors_community()
        self.community_to_color = {community: self.colors[rev_dict[community][0]] for community in rev_dict}
        
    def _list_names(self, wordlist):
        result = ''
        for word in wordlist:
            result += str(word)+', '
        return (str(len(wordlist)), result[:-2])
                
    def _ask_community_name(self, wordlist):
        return raw_input("Please enter a category name defining the " + self._list_names(wordlist)[0] + " following names : "+ self._list_names(wordlist)[1] +'      ')
    
    def _add_legend_community(self):
        x = [0.0, 0.02]
        for community in set(self.communities.values()):
            y = [1-0.002-community/100, 1-0.002-community/100]
            fill_between(x, 1-0.008-community/100 , y, color = plt.cm.spectral(self.community_to_color[community]), alpha = 0.4)
            annotate(self.communities_names[community], xy=(0.022, 1-0.006-community/100), xytext=(0.022, 1-0.006-community/100), size = 13)
    
    def community_plot(self):
        plt.figure(figsize=(70, 70))
        self._communities()
        self._set_communities_names()
        sizes = [self._size_community()[k] for k in self.graph_without_self.node.keys()]
        colors = [plt.cm.spectral(self.colors[k]) for k in self.graph_without_self.node.keys()]
        figsize(70, 70)
        nx.draw(self.graph_without_self, node_size=sizes, node_color=colors, edge_color='lightgrey', font_size=9, alpha = 0.2)
        self._add_legend_community()
        plt.title(self.own_name + ' Facebook network', size = 55, weight = 'bold')
        plt.show()