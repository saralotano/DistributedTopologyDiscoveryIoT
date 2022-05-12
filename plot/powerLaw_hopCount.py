import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [12.50, 3.50]
plt.rcParams["figure.autolayout"] = True

y = ['Neighbors', 'Local Topology']
x1 = [84.25, 99]
x2 = [119684, 19042]

fig = plt.figure()
color_list = ['tab:blue', 'tab:orange']

axe1 = plt.subplot(121)
axe1.barh(y, x1, height=0.3, align='center', color=color_list, edgecolor='black')
for index, value in enumerate(x1):
    plt.text(value, index,
             str(value))
plt.ylabel("Requested Info")
plt.xlabel("Discovered edges")

axe2 = plt.subplot(122, sharey=axe1)
axe2.barh(y, x2, height=0.3, align='center', color=color_list, edgecolor='black')
for index, value in enumerate(x2):
    plt.text(value, index,
             str(value))
plt.xlabel("Simulation Time")

plt.show()
