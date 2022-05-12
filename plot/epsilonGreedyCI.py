import numpy as np
import scipy.stats as st
from matplotlib import pyplot as plt

data = [12, 12, 13, 13, 15, 16, 17, 22, 23, 25, 26, 27, 28, 28, 29]
sim_time = [60, 168, 338, 676, 1350, 2700, 5400, 10800]

edges = {}
times = {}
byte = {}

edges['edge_10800'] = [63.88, 63.82, 63.33, 62.65, 64.16, 63.64, 63.3, 63.25, 64.43, 62.7]
times['time_10800'] = [11815, 12495, 11809, 12169, 12211, 12316, 11874, 11812, 12526, 12526]
byte['byte_10800'] = [67312, 88620, 62258, 74479, 76044, 83103, 63225, 62908, 89574, 91094]

edges['edge_5400'] = [48.39, 48.06, 48.06, 47.58, 47.84, 48.32, 47.65, 48.25, 48.18, 47.84]
times['time_5400'] = [6794, 7698, 7412, 7521, 7967, 7553, 7093, 7378, 7290, 7647]
byte['byte_5400'] = [61050, 110367, 94313, 100509, 136341, 102799, 79718, 97832, 93189, 108574]

edges['edge_2700'] = [35.72, 34.75, 34.75, 34.43, 34.45, 34.59, 34.29, 34.07, 35.31, 34.11]
times['time_2700'] = [5335, 4710, 5031, 5505, 4981, 4794, 5713, 4656, 4345, 4288]
byte['byte_2700'] = [143237, 95469, 128418, 168584, 120932, 112993, 175620, 93054, 77270, 74307]

edges['edge_1350'] = [25.25, 23.81, 23.81, 34.43, 24.97, 24.45, 23.81, 24.03, 25.05, 24.54]
times['time_1350'] = [4017, 3193, 3357, 5007, 2834, 2779, 3712, 3471, 3073, 5035]
byte['byte_1350'] = [159542, 111173, 123363, 236882, 92932, 89729, 135972, 136101, 97917, 224051]

edges['edge_676'] = [16.46, 16.29, 16.29, 16.65, 16.75, 16.85, 16.72, 16.81, 17.03, 16.88]
times['time_676'] = [3754, 3664, 3960, 4172, 4513, 4209, 3967, 4313, 2466, 4221]
byte['byte_676'] = [189079, 189130, 202482, 220978, 247479, 223806, 206900, 230632, 110528, 220539]

edges['edge_338'] = [11.37, 10.69, 10.69, 10.83, 11.63, 11.51, 10.34, 11.33, 10.91, 11.53]
times['time_338'] = [2820, 3322, 2801, 3641, 3006, 2963, 2847, 4083, 4047, 3553]
byte['byte_338'] = [151514, 173413, 149578, 202748, 164656, 156188, 149920, 232957, 231340, 199352]

edges['edge_168'] = [7.82, 7.05, 7.05, 6.93, 7.78, 7.63, 7.52, 7.29, 6.91, 7.55]
times['time_168'] = [2407, 3140, 2864, 3442, 4085, 2620, 3270, 3342, 3537, 2635]
byte['byte_168'] = [136944, 178425, 153898, 199381, 244080, 153294, 184012, 201286, 205625, 152231]

edges['edge_60'] = [4.14, 3.69, 3.69, 3.91, 4.04, 3.68, 3.79, 4.06, 3.6, 3.84]
times['time_60'] = [2579, 3053, 2861, 4008, 3035, 3198, 2789, 3574, 2691, 3634]
byte['byte_60'] = [155033, 179104, 171757, 227687, 175255, 192946, 160458, 107711, 162838, 204715]

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


# FIGURE 1
barWidth = 0.5
r1 = np.arange(len(mean_edge))
plt.bar(r1, mean_edge, width=barWidth, color='tab:blue', edgecolor='black', yerr=yerr_edge, capsize=7, label='Discovered edges')
x_pos = np.arange(len(sim_time))
plt.xticks(x_pos, sim_time, rotation=0)
plt.ylabel('Discovered edges')
plt.xlabel('Normal flooding [s]')
plt.legend()
plt.show()



# FIGURE 2
barWidth = 0.5
r1 = np.arange(len(mean_time))
plt.bar(r1, mean_time, width=barWidth, color='tab:blue', edgecolor='black', yerr=yerr_time, capsize=7, label='Total simulation time')
x_pos = np.arange(len(sim_time))
plt.xticks(x_pos, sim_time, rotation=0)
plt.ylabel('Total Simulation time [s]')
plt.xlabel('Normal flooding [s]')
plt.legend()
plt.show()


# FIGURE 3
barWidth = 0.5
r1 = np.arange(len(mean_byte))
plt.bar(r1, mean_byte, width=barWidth, color='tab:blue', edgecolor='black', yerr=yerr_byte, capsize=7, label='Transmitted bytes [B]')
x_pos = np.arange(len(sim_time))
plt.xticks(x_pos, sim_time, rotation=0)
plt.ylabel('Transmitted bytes [B]')
plt.xlabel('Normal flooding [s]')
plt.legend()
plt.show()
