import matplotlib.pyplot as plt

labels = list(range(0, 100))
neigh = [8, 10, 4, 12, 12, 1, 1, 4, 4, 4, 2, 3, 3, 2, 2, 6, 1, 2, 2, 3, 2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 4, 1, 3, 2, 3, 1, 2, 2, 1, 1, 1, 1, 5, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 3, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

normal_edges = [99, 99, 99, 99, 99, 47, 59, 99, 94, 97, 68, 90, 86, 91, 69, 94, 56, 81, 95, 87, 69, 70, 55, 70, 69, 50,
                74, 43, 81, 57, 48, 58, 59, 93, 42, 86, 69, 91, 63, 68, 72, 45, 44, 56, 55, 97, 49, 49, 50, 68, 50, 76,
                47, 51, 52, 53, 56, 77, 49, 58, 56, 43, 51, 50, 60, 93, 56, 41, 45, 62, 89, 47, 47, 43, 47, 70, 62, 80,
                64, 47, 52, 55, 46, 50, 71, 51, 47, 50, 57, 50, 53, 53, 60, 45, 49, 57, 63, 44, 49, 56]

advanced_edges = []
for e in normal_edges:
    advanced_edges.append(99 - e)

fig, ax = plt.subplots()

ax.bar(labels, normal_edges, color='#2980b9', label='Normal flooding edges')
ax.bar(labels, advanced_edges, color='#aed6f1', bottom=normal_edges, label='Advanced flooding edges')
'''
# Basic version with blue and orange bars
ax.bar(labels, normal_edges, label='Normal flooding edges')
ax.bar(labels, advanced_edges, bottom=normal_edges, label='Advanced flooding edges')
'''

ax.plot(labels, neigh, color='r', label='Number of neighbors')

ax.set_ylim(0, 100)
ax.set_ylabel('Discovered Edges')
ax.set_xlabel('Node ID')
ax.legend()

plt.show()
