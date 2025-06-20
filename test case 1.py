import matplotlib.pyplot as plt
import networkx as nx
from math import sqrt

# Posisi AP dimana setiap AP memiliki posisi yang berdekatan satu sama lain
ap_positions = {
    "AP1": (0, 0),
    "AP2": (5, 0),
    "AP3": (0, 5),
    "AP4": (5, 5),
    "AP5": (3, 2),
    "AP6": (2, 4)
}

# Fungsi interferensi berdasarkan threshold (15 meter)
def is_interfering(pos1, pos2, threshold=15):
    x1, y1 = pos1
    x2, y2 = pos2
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5 <= threshold

# Buat graf interferensi berbobot (hanya jika berjarak < threshold)
threshold = 15
G = nx.Graph()
for ap in ap_positions:
    G.add_node(ap)

for ap1 in ap_positions:
    for ap2 in ap_positions:
        if ap1 != ap2 and is_interfering(ap_positions[ap1], ap_positions[ap2], threshold):
            distance = round(((ap_positions[ap1][0] - ap_positions[ap2][0])**2 + (ap_positions[ap1][1] - ap_positions[ap2][1])**2) ** 0.5, 2)
            G.add_edge(ap1, ap2, weight=distance)

# Algoritma Welsh-Powell
def welsh_powell(graph):
    sorted_nodes = sorted(graph.nodes(), key=lambda x: len(graph[x]), reverse=True)
    color_assignment = {}
    color = 1
    for node in sorted_nodes:
        if node not in color_assignment:
            color_assignment[node] = color
            for other in sorted_nodes:
                if other not in color_assignment:
                    if all(color_assignment.get(n) != color for n in graph[other]):
                        color_assignment[other] = color
            color += 1
    return color_assignment


color_result = welsh_powell(G)
chromatic_number = len(set(color_result.values()))

print("Channel Assignments:")
for ap in sorted(color_result):
    print(f"{ap} → Channel {color_result[ap]}")
print(f"\nChromatic Number (Number of Channels Used): {chromatic_number}")

# Adjacency Matrix and List
nodes = sorted(G.nodes())
index_map = {node: i for i, node in enumerate(nodes)}
adj_matrix = [[0]*len(nodes) for _ in range(len(nodes))]

for u, v in G.edges():
    i, j = index_map[u], index_map[v]
    adj_matrix[i][j] = 1
    adj_matrix[j][i] = 1  

print("\nAdjacency Matrix:")
print("    " + "      ".join(nodes))
for i, row in enumerate(adj_matrix):
    print(f"{nodes[i]}  " + "        ".join(str(val) for val in row))

print("\nAdjacency List:")
adj_list = {node: sorted(list(G.neighbors(node))) for node in nodes}
for node in nodes:
    print(f"{node}: {adj_list[node]}")

# Visualisasi graf interferensi
plt.figure(figsize=(8, 6))
node_colors = [color_result[n] for n in G.nodes()]
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw(G, pos=ap_positions, with_labels=True, node_color=node_colors, cmap=plt.cm.Set3,
        node_size=1000, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos=ap_positions, edge_labels=edge_labels)
plt.title(f"Graph Coloring Based on Interference Threshold = {threshold} meters")
plt.show()
