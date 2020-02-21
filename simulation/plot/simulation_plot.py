import numpy as np
import matplotlib
import matplotlib.pyplot as plt

legend_font = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 26,
}

label_font = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 30,
}

title_font = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 22,
}

patterns = [ "|" , "\\" , "/" , "+" , "-", ".", "*","x", "o", "O" ]

comp_arr1 = np.load('arr1.npy')
# normal_arr2 = np.load('arr2.npy')
# normal_arr3 = np.load('arr3.npy')

comm_time = 4 * 150 / 51.2
comm_arr1 = [comm_time] * len(comp_arr1)
# comm_arr2 = [comm_time] * len(arr2)
# comm_arr3 = [comm_time] * len(arr3)

norm_comp_arr = []
norm_comm_arr = []

for i in range(len(comp_arr1)):
	temp_comp_time = comp_arr1[i] / (comp_arr1[i]+comm_arr1[i])
	norm_comp_arr.append(temp_comp_time)
	norm_comm_arr.append(1-temp_comp_time)

# ind = np.arange(len(norm_comp_arr))
ind = np.arange(20)
width = 0.35

plt.figure('Comparison graph')
p1 = plt.bar(ind, norm_comm_arr[0:20], width, color='white', edgecolor='blue', hatch=patterns[1], label='Ratio of Communication')
p2 = plt.bar(ind, norm_comp_arr[0:20], width, bottom=norm_comm_arr[0:20], color='red', edgecolor='red', label='Ratio of Computation')

plt.xlabel('Iteration', label_font)
plt.ylabel('Communication/Computation Ratio', label_font)
# plt.title('Comparison of computation and communication time in the simulation experiment', title_font)
plt.xticks(ind, [str(i) for i in (ind+1)])
plt.yticks(np.arange(0, 1.1, 0.1))
# plt.legend((p1[0], p2[0]), ('Communication', 'Computation'), prop=lengend_font)
plt.legend(loc='best', prop=legend_font)
plt.tick_params(labelsize=20)
# plt.ylim(0, 1.1)
plt.show()