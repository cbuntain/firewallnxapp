import sys

import pandas as pd
import networkx as nx

# list of dataframes
dfs = []

# Read the CSV files
print("Reading files...")
for f in sys.argv[1:]:
    print("\tReading file: [%s]" % f)
    local_df = pd.read_csv(f, low_memory=False)

    dfs.append(local_df)

# Merge any dataframes
full_df = pd.concat(dfs)

# How many rows did we see?
print("Rows:", full_df.shape)

# Create a directed graph to represent this data
g = nx.DiGraph()

# For each connection in this dataset, we create an edge.
#. if that edge already exists, we increase its weight
for row in full_df[["Source IP", "Destination IP"]].itertuples():

    if not g.has_edge(row[1], row[2]):
        g.add_edge(row[1], row[2], weight=1)
    else:
        g[row[1]][row[2]]["weight"] += 1

print("Internet Nodes:", len(g.nodes))

print("Graph Density:", nx.density(g))

print_count = 50

print("High-Degree Nodes:")
degree_cents = nx.degree_centrality(g)
for ip in sorted(degree_cents, key=lambda x: degree_cents[x], reverse=True)[:print_count]:
    print(ip, degree_cents[ip], g.degree(ip))

print("Authoritative Nodes:")
node_ranks = nx.pagerank(g)
for ip in sorted(node_ranks, key=lambda x: node_ranks[x], reverse=True)[:print_count]:
    print(ip, node_ranks[ip])