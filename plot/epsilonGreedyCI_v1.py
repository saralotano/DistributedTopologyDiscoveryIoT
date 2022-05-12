import numpy as np
import scipy.stats as st
from matplotlib import pyplot as plt

sim_time = [60, 168, 338, 676, 1350, 2700, 5400, 10800]
edges = {}
times = {}
byte = {}

edges['edge_10800'] = [63.88, 63.82, 63.33, 62.65, 64.16, 63.64, 63.3, 63.25, 64.43, 62.7]
times['time_10800'] = [11815, 12495, 11809, 12169, 12211, 12316, 11874, 11812, 12526, 12526]
byte['byte_10800'] = [67312, 68620, 62258, 74479, 66044, 63103, 63225, 62908, 69574, 71094]

edges['edge_5400'] = [48.39, 48.06, 48.06, 47.58, 47.84, 48.32, 47.65, 48.25, 48.18, 47.84]
times['time_5400'] = [7594, 7598, 7412, 7521, 7567, 7553, 7593, 7378, 7290, 7547]
byte['byte_5400'] = [95050, 95367, 94313, 94509, 95341, 95799, 94718, 97832, 90189, 95574]

edges['edge_2700'] = [35.72, 34.75, 34.75, 34.43, 34.45, 34.59, 34.29, 34.07, 35.31, 34.11]
times['time_2700'] = [5305, 4910, 5031, 5005, 4981, 4994, 5013, 4956, 4945, 4988]
byte['byte_2700'] = [103237, 105469, 108418, 108584, 100932, 102993, 105620, 103054, 107270, 104307]

edges['edge_1350'] = [25.25, 23.81, 23.81, 24.43, 24.97, 24.45, 23.81, 24.03, 25.05, 24.54]
times['time_1350'] = [4017, 4193, 4357, 4007, 4034, 4179, 4112, 4471, 4073, 4135]
byte['byte_1350'] = [139542, 131173, 133363, 136882, 132932, 139729, 135972, 136101, 137917, 134051]

edges['edge_676'] = [16.46, 16.29, 16.29, 16.65, 16.75, 16.85, 16.72, 16.81, 17.03, 16.88]
times['time_676'] = [3754, 3664, 3960, 4172, 3913, 4209, 3967, 3913, 3866, 4221]
byte['byte_676'] = [209079, 209130, 202482, 200978, 200479, 203806, 206900, 200632, 210528, 210539]

edges['edge_338'] = [11.37, 10.69, 10.69, 10.83, 11.63, 11.51, 10.34, 11.33, 10.91, 11.53]
times['time_338'] = [3320, 3322, 3301, 3341, 3006, 2963, 3347, 3383, 3347, 3353]
byte['byte_338'] = [191514, 193413, 199578, 202748, 194656, 196188, 199920, 202957, 201340, 199352]

edges['edge_168'] = [7.82, 7.05, 7.05, 6.93, 7.78, 7.63, 7.52, 7.29, 6.91, 7.55]
times['time_168'] = [2907, 3140, 2864, 3042, 3085, 2920, 3270, 3342, 3337, 2935]
byte['byte_168'] = [186944, 188425, 183898, 189381, 184080, 183294, 184012, 181286, 185625, 182231]

edges['edge_60'] = [4.14, 3.69, 3.69, 3.91, 4.04, 3.68, 3.79, 4.06, 3.6, 3.84]
times['time_60'] = [2879, 3153, 2961, 3008, 3035, 3198, 2989, 3074, 2991, 3034]
byte['byte_60'] = [175033, 179104, 171757, 177687, 175255, 172946, 170458, 177711, 172838, 174715]

yerr_edge = []
mean_edge = []

yerr_time = []
mean_time = []

yerr_byte = []
mean_byte = []


for s in sim_time:
    key = 'edge_' + str(s)
    values = edges[key]
    interval = st.t.interval(alpha=0.95, df=len(values)-1, loc=np.mean(values), scale=st.sem(values))
    yerr_edge.append(interval[1] - interval[0])
    mean_edge.append(np.mean(values))

    key = 'time_' + str(s)
    values = times[key]
    interval = st.t.interval(alpha=0.95, df=len(values) - 1, loc=np.mean(values), scale=st.sem(values))
    yerr_time.append(interval[1] - interval[0])
    mean_time.append(np.mean(values))

    key = 'byte_' + str(s)
    values = byte[key]
    # create 95% confidence interval for population mean weight
    interval = st.t.interval(alpha=0.95, df=len(values) - 1, loc=np.mean(values), scale=st.sem(values))
    yerr_byte.append(interval[1] - interval[0])
    mean_byte.append(np.mean(values))


color_list = ['tab:cyan', 'tab:olive', 'tab:brown', 'tab:purple', 'tab:red', 'tab:green', 'tab:orange', 'tab:blue']

# FIGURE 1
barWidth = 0.5
r1 = np.arange(len(mean_edge))
plt.bar(r1, mean_edge, width=barWidth, color=color_list, edgecolor='black', yerr=yerr_edge, capsize=7)
x_pos = np.arange(len(sim_time))
plt.xticks(x_pos, sim_time, rotation=0)
plt.ylabel('Discovered edges')
plt.xlabel('Normal flooding [s]')
plt.show()


# FIGURE 2
barWidth = 0.5
r1 = np.arange(len(mean_time))
plt.bar(r1, mean_time, width=barWidth, color=color_list, edgecolor='black', yerr=yerr_time, capsize=7)
x_pos = np.arange(len(sim_time))
plt.xticks(x_pos, sim_time, rotation=0)
plt.ylabel('Total Simulation time [s]')
plt.xlabel('Normal flooding [s]')
plt.show()


# FIGURE 3
barWidth = 0.5
r1 = np.arange(len(mean_byte))
plt.bar(r1, mean_byte, width=barWidth, color=color_list, edgecolor='black', yerr=yerr_byte, capsize=7)
x_pos = np.arange(len(sim_time))
plt.xticks(x_pos, sim_time, rotation=0)
plt.ylabel('Transmitted bytes [B]')
plt.xlabel('Normal flooding [s]')
plt.show()


