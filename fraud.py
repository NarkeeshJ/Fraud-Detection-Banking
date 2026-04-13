import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("transactions.csv")
data.columns = data.columns.str.strip()

# Create graph
G = nx.from_pandas_edgelist(
    data,
    source='Sender',
    target='Receiver',
    edge_attr='Amount',
    create_using=nx.DiGraph()
)

# Centrality measures
degree = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)

# Identify suspicious nodes
suspicious = []
for node in G.nodes():
    if degree[node] > 0.3 or betweenness[node] > 0.05:
        suspicious.append(node)

# -------- OUTPUT --------
print("\n🔍 FRAUD ANALYSIS REPORT")
print("-" * 30)

print("\n📌 High Degree Accounts:")
for node, val in degree.items():
    if val > 0.3:
        print(f"{node} → {round(val,3)}")

print("\n📌 High Betweenness Accounts:")
for node, val in betweenness.items():
    if val > 0.05:
        print(f"{node} → {round(val,3)}")

print("\n🚨 Suspicious Accounts Detected:")
for node in suspicious:
    print(node)

# -------- GRAPH --------
plt.figure(figsize=(10,7))

pos = nx.spring_layout(G)

# Color nodes
node_colors = []
for node in G.nodes():
    if node in suspicious:
        node_colors.append('red')   # suspicious
    else:
        node_colors.append('lightblue')

# Draw graph
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000)

# Edge labels (Amount)
edge_labels = nx.get_edge_attributes(G, 'Amount')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title("Fraud Transaction Network Analysis")
plt.show()