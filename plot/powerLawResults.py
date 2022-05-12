import matplotlib.pyplot as plt
import pandas as pd

# LOCAL TOPOLOGY INFO

# FIGURE 1: SIMULATION TIME

values = [13863, 13059, 11815, 19042]
y_values = ['Random', 'Bayesian Inference', 'Relayed Messages', 'Hop Count']
data = {'Simulation Time': values}
df = pd.DataFrame(data, columns=['Simulation Time'],index=y_values)
color_list = ['tab:blue', 'tab:blue', 'tab:orange',  'tab:blue']
ax = df.plot.barh(legend=False)
ax.bar_label(ax.containers[0])
ax.barh(y=y_values, width=values, color=color_list, edgecolor='black')
plt.title("Time required to discover the entire network topology")
plt.ylabel("Node selection method")
plt.xlabel("Simulation Time")
plt.show()


# FIGURE 2: TRANSMITTED BYTES
values = [0.18, 0.17, 0.07, 0.41]
y_values = ['Random', 'Bayesian Inference', 'Relayed Messages', 'Hop Count']
data = {'Transmitted bytes [MB]': values}
df = pd.DataFrame(data, columns=['Transmitted bytes [MB]'], index=y_values)
color_list = ['tab:blue', 'tab:blue', 'tab:orange', 'tab:blue']
ax = df.plot.barh(legend=False)
ax.bar_label(ax.containers[0])
ax.barh(y=y_values, width=values, color=color_list, edgecolor='black')
plt.title("Transmitted bytes used to discover the entire network topology")
plt.ylabel("Node selection method")
plt.xlabel("Transmitted bytes [MB]")
plt.show()


# FIGURE 3: NUMBER OF MESSAGES
data = {'Received Messages': [59.07, 57.88, 49.23, 78.1],
        'Update Messages': [30.74, 29.76, 28.88, 33]
        }
df = pd.DataFrame(data, columns=['Update Messages', 'Received Messages'],
                  index=['Random', 'Bayesian Inference', 'Relayed Messages', 'Hop Count'])

color_list = ['tab:green', 'tab:blue']
ax = df.plot.barh(color=color_list, edgecolor='black')
for container in ax.containers:
    ax.bar_label(container)

plt.title('Topology Discovery Received and Update Messages')
plt.ylabel('Node selection method')
plt.xlabel('Number of messages')

plt.show()
