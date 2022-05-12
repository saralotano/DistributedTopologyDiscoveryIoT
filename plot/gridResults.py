import matplotlib.pyplot as plt
import pandas as pd

# FIGURE 1: SIMULATION TIME
values = [12601, 11829, 11470, 12055]
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
values = [0.24, 0.18, 0.11, 0.14]
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
data = {'Received Messages': [64.33, 60.89, 57.45, 59.47],
        'Update Messages': [35.19, 35.02, 34.45, 35.27]
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

