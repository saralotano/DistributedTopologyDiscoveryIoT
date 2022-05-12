import matplotlib.pyplot as plt

labels = list(range(0, 100))
neigh = [2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2]

normal_edges = [152, 160, 169, 163, 173, 170, 173, 173, 163, 156, 158, 168, 171, 172, 177, 174, 172, 172, 165, 161, 169, 172, 178, 177, 176, 178, 175, 175, 168, 167, 162, 174, 179, 179, 176, 179, 178, 178, 177, 173, 168, 174, 179, 177, 180, 180, 180, 179, 173, 172, 169, 175, 173, 179, 180, 180, 176, 177, 176, 171, 165, 174, 179, 177, 180, 180, 179, 177, 171, 169, 152, 175, 177, 179, 178, 177, 178, 178, 172, 170, 149, 166, 170, 175, 173, 174, 171, 172, 171, 161, 152, 171, 160, 162, 165, 161, 161, 154, 153, 142]

advanced_edges = []
for e in normal_edges:
    advanced_edges.append(180 - e)

fig, ax = plt.subplots()

ax.bar(labels, normal_edges, color='#2980b9', label='Normal flooding edges')
ax.bar(labels, advanced_edges, color='#aed6f1', bottom=normal_edges, label='Advanced flooding edges')

'''
# Basic version with blue and orange bars
ax.bar(labels, normal_edges, label='Normal flooding edges')
ax.bar(labels, advanced_edges, bottom=normal_edges, label='Advanced flooding edges')
'''

ax.plot(labels, neigh, color='r', label='Number of neighbors')
ax.set_ylim(0, 180)
ax.set_ylabel('Discovered Edges')
ax.set_xlabel('Node ID')
ax.legend()

plt.show()
