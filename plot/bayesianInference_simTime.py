from matplotlib import pyplot as plt

local = {10800: 63.88, 11100: 80.51, 11400: 90.36, 11700: 93.65, 12000: 95.13, 12300: 96.21, 12600: 96.62, 12900: 98.59, 13200: 99, 13500: 99, 13800: 99, 14100: 99, 14400: 99, 14700: 99, 15000: 99, 15300: 99}
neigh = {10800: 63.88, 11100: 64.72, 11400: 65.43, 11700: 66.29, 12000: 66.85, 12300: 67.52, 12600: 68.05, 12900: 68.54, 13200: 69.11, 13500: 69.63, 13800: 70.19, 14100: 70.68, 14400: 71.28, 14700: 71.78, 15000: 72.36, 15300: 72.68}
x = list(local.keys())
y1 = list(local.values())
y2 = list(neigh.values())

# plot lines
plt.plot(x, y1, label="Local Topology")
plt.plot(x, y2, label="Neighbors")
plt.axhline(y=99, color='r', linestyle='--', label='99 Edges')

plt.annotate('SimulationTime = 13059', xy=(13059, 99),
             fontsize=9, xytext=(13062, 96),
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

# plt.text(13059, 99, 'This text starts at point (2,4)')
# plt.axvline(x=13059, color='g', linestyle='--', label='99 Edges')
plt.legend()
plt.xlabel('Simulation Time')
plt.xlim(10800, 15300)
plt.ylabel('Discovered Edges')
plt.ylim(63.88, 100)
plt.show()

