from matplotlib import pyplot as plt

power_law = {0: 2.08, 300: 10.68, 600: 15.28, 900: 19.38, 1200: 23.78, 1500: 26.25, 1800: 28.81, 2100: 31.06, 2400: 33.51, 2700: 35.69, 3000: 37.08, 3300: 38.58, 3600: 40.03, 3900: 41.3, 4200: 43.03, 4500: 44.35, 4800: 45.78, 5100: 47.2, 5400: 48.4, 5700: 49.81, 6000: 51.01, 6300: 52.09, 6600: 53.06, 6900: 53.98, 7200: 55.02, 7500: 55.86, 7800: 56.63, 8100: 57.49, 8400: 58.34, 8700: 59.09, 9000: 59.86, 9300: 60.42, 9600: 61.18, 9900: 61.92, 10200: 62.65, 10500: 63.29, 10800: 63.88, 11100: 80.51, 11400: 90.36, 11700: 93.65, 12000: 95.13, 12300: 96.21, 12600: 96.62, 12900: 98.59, 13200: 99, 13500: 99, 13800: 99, 14100: 99, 14400: 99, 14700: 99, 15000: 99, 15300: 99}
grid = {0: 3.66, 300: 34.78, 600: 57.56, 900: 77.09, 1200: 91.5, 1500: 102.09, 1800: 109.66, 2100: 117.6, 2400: 123.39, 2700: 130.5, 3000: 134.49, 3300: 138.93, 3600: 142.88, 3900: 145.11, 4200: 147.44, 4500: 151.04, 4800: 152.33, 5100: 154.18, 5400: 155.69, 5700: 157.08, 6000: 158.24, 6300: 160.29, 6600: 161.59, 6900: 162.71, 7200: 164, 7500: 164.95, 7800: 165.76, 8100: 166.52, 8400: 167.01, 8700: 167.48, 9000: 168.11, 9300: 168.61, 9600: 169.2, 9900: 169.7, 10200: 170.37, 10500: 170.73, 10800: 171, 11100: 177.26, 11400: 179.51, 11700: 179.93, 12000: 180, 12300: 180, 12600: 180, 12900: 180, 13200: 180, 13500: 180, 13800: 180, 14100: 180, 14400: 180, 14700: 180, 15000: 180, 15300: 180}

x = list(power_law.keys())
y1 = list(power_law.values())
y2 = list(grid.values())

# plot lines
plt.plot(x, y2, label="Grid topology")
plt.axhline(y=180, color='tab:blue', linestyle='--', label='180 Edges')
plt.plot(x, y1, label="Power Law topology")
plt.axhline(y=99, color='tab:orange', linestyle='dotted', label='99 Edges')

plt.annotate('SimulationTime = 11829', xy=(11829, 180),
             fontsize=9, xytext=(11830, 170),
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

plt.annotate('SimulationTime = 13059', xy=(13059, 99),
             fontsize=9, xytext=(13000, 105),
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

# plt.text(13059, 99, 'This text starts at point (2,4)')
plt.axvline(x=10800, color='r', linestyle='dashdot', label='Normal flooding')
plt.annotate('SimulationTime = 10800', xy=(10800, 0),
             fontsize=9, xytext=(8000, 10),
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

plt.legend()
plt.xlabel('Simulation Time')
plt.xlim(0, 14000)
plt.ylabel('Discovered Edges')
plt.ylim(0, 200)
plt.show()

