import argparse
import os 
import sys
import math
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

def interval_arr_generator(model_name, arr):
    interval_arr = np.array([])
    for i in range(len(arr)-1):
        adjacent_interval = arr[i+1] - arr[i]
        interval_arr = np.append(interval_arr, adjacent_interval)   

    np.save('%s_interval_arr.npy'%model_name, interval_arr)
    return interval_arr 

def norm_arr_processor(model_name, timestamp_arr):
	interval_arr = interval_arr_generator(model_name, timestamp_arr)

	indices = np.argpartition(-interval_arr, 6)
	indices = indices[0:6]
	np.save('%s_max6_indices.npy'%model_name, indices)
	indices.sort()
	print(interval_arr[indices])
	# print(indices[0:500])
	# print(indices[500])

	comm_time = []
	comp_time = []

	for i in range(len(indices)-1):
	  temp_comp = interval_arr[indices[i]]
	  temp_comm = timestamp_arr[indices[i+1]] - timestamp_arr[indices[i]+1]
	  comp_time.append(temp_comp)
	  comm_time.append(temp_comm)

	comm_time = np.array(comm_time)
	comp_time = np.array(comp_time)
	# aver_comm = np.mean(comm_time)
	# aver_comp = np.mean(comp_time)

	# norm_comp_time = aver_comp / (aver_comm+aver_comp)
	# norm_comm_time = 1 - norm_comp_time

	return comp_time, comm_time

if __name__ == '__main__':
	# resnet18_arr = np.load('./timestamp_files/w3_resnet18_v1_cifar10.pcap_timestamp_arr.npy')
	vgg11_arr = np.load('Training0.pcap_timestamp_arr.npy')
	# vgg19_arr = np.load('./timestamp_files/w3_vgg19_cifar10.pcap_timestamp_arr.npy')
	# resnet50_arr = np.load('./timestamp_files/w4_resnet50_v1_cifar10.pcap_timestamp_arr.npy')
	
	vgg11_comp, vgg11_comm = norm_arr_processor('vgg11', vgg11_arr)
	# print('Average computation:%f' % vgg11_comp)
	# print('Average communication:%f ' % vgg11_comm)
	# vgg19_comp, vgg19_comm = norm_arr_processor('vgg19', vgg19_arr)
	# resnet18_comp, resnet18_comm = norm_arr_processor('resnet18', resnet18_arr)
	# resnet50_comp, resnet50_comm = norm_arr_processor('resnet50', resnet50_arr)

	ratio_comp = vgg11_comp / (vgg11_comp+vgg11_comm)
	ratio_comm = 1 - ratio_comp
	ind = np.arange(len(ratio_comp))
	width = 0.35

	plt.figure('Comparision graph of several iterations')
	p1 = plt.bar(ind, ratio_comm, width, color='white', edgecolor='blue', hatch=patterns[1], label='Ratio of Communication')
	p2 = plt.bar(ind, ratio_comp, width, bottom=ratio_comm, color='red', edgecolor='red', label='Ratio of Computation')

	plt.ylabel('Communication/Compuation Ratio', label_font)
	plt.xlabel('Iterations', label_font)
	# plt.title('Comparison of computation and communication time', title_font)
	plt.xticks(ind, [str(i) for i in (ind+1)])
	plt.yticks(np.arange(0, 1.1, 0.1))
	# plt.legend((p1[0], p2[0]), ('Communication', 'Computation'), prop=lengend_font)
	plt.legend(loc='best', prop=legend_font)
	plt.tick_params(labelsize=20)
	plt.show()


