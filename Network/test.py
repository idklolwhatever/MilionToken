#g = read_adjustlist('./data/Holders/export-tokenholders-for-contract-0x6b4c7a5e3f0b99fcd83e9c089bddd6c7fce5c611.csv',delimeter=',', create_using = nx.DiGraph())
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

import pandas as pd
import pdb
date_list = list(range(1,30,1))

df = pd.DataFrame()
for date in date_list:
    data_file = f'./data/Transfers/7_{str(date)}_2021_export-token-0x6b4c7a5e3f0b99fcd83e9c089bddd6c7fce5c611.csv'
    df_date = pd.read_csv(data_file)
    df= df.append(df_date)
    #pdb.set_trace()
    print(f'Read csv for {date}')



Graphtype = nx.Graph()
pdb.set_trace()
G = nx.from_pandas_edgelist(df.head(1000), "From","To", edge_attr=['Quantity'])

#pos = graphviz_layout(G, prog='dot')
pos = nx.spring_layout(G)
edge_labels = nx.get_edge_attributes(G, 'Quantity')
nx.draw(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
nx.draw_networkx_edges(G, pos)
#nx.draw_networkx_labels(G, pos, font_size=10)
plt.xticks([])
plt.yticks([])
plt.show() 


# nx.draw(G,with_labels=True)
# plt.show()