import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


# FIGURE 1: SIMULATION TIME
data = {'Simulation Time': [3384, 3538, 2479, 3137, 3906, 3817, 5549, 8655, 11815]}

df = pd.DataFrame(data, columns=['Simulation Time'],
                  index=[120, 180, 240, 300, 360, 1800, 3600, 7200, 10800])

ax = df.plot.bar(edgecolor='black')
for container in ax.containers:
    ax.bar_label(container)

bars = (120, 180, 240, 300, 360, 1800, 3600, 7200, 10800)
x_pos = np.arange(len(bars))

# Create names on the x-axis
plt.xticks(x_pos, bars, rotation=0)

# plt.title('Topology Discovery Received and Update Messages')
plt.ylabel('Simulation Time [s]')
plt.xlabel('Normal flooding [s]')

plt.show()


# FIGURE 2: TRANSMITTED BYTES
data = {'Transmitted bytes': [155033, 136944, 151514, 189079, 159542, 143237, 61050, 67312]}

df = pd.DataFrame(data, columns=['Transmitted bytes'],
                  index=[60, 168, 338, 676, 1350, 2700, 5400, 10800])
color_list = ['tab:cyan', 'tab:olive', 'tab:brown', 'tab:purple', 'tab:red', 'tab:green', 'tab:orange', 'tab:blue']

ax = df.plot.bar(color=color_list, edgecolor='black')
for container in ax.containers:
    ax.bar_label(container)

bars = (60, 168, 338, 676, 1350, 2700, 5400, 10800)
x_pos = np.arange(len(bars))

# Create names on the x-axis
plt.xticks(x_pos, bars, rotation=0)

# plt.title('Topology Discovery Received and Update Messages')
plt.ylabel('Transmitted bytes [B]')
plt.xlabel('Normal flooding [s]')

plt.show()


# create a dataset
byte_values = [155033, 136944, 151514, 189079, 159542, 143237, 61050, 67312]
bars = (60, 168, 338, 676, 1350, 2700, 5400, 10800)
x_pos = np.arange(len(bars))

color_list = ['tab:cyan', 'tab:olive', 'tab:brown', 'tab:purple', 'tab:red', 'tab:green', 'tab:orange', 'tab:blue']


# Create bars with different colors
plt.bar(x_pos, byte_values, color=color_list)

# Create names on the x-axis
plt.xticks(x_pos, bars)
plt.ylabel('Transmitted bytes [B]')
plt.xlabel('Normal flooding [s]')

# Show graph
plt.show()
