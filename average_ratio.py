import argparse
import os 
import sys
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

RATIO_DIR = './batch256/ratio_files'
TIMESTAMP_DIR = './batch256/timestamp_files'

patterns = [ "|" , "\\" , "/" , "+" , "-", ".", "*","x", "o", "O" ]

legend_font = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 18,
}

label_font = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 26,
}

text_font = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 10,
}

def interval_arr_generator(model_name, arr):
    interval_arr = np.zeros(len(arr)-1)
    for i in range(len(arr)-1):
        interval_arr[i] = arr[i+1] - arr[i]

    print('Len of interval_arr: %d.' % len(interval_arr))
    # np.save(os.path.join(RATIO_DIR, model_name+'_interval_arr.npy'), interval_arr)
    return interval_arr 

def calculate_phase_time(model_name, timestamp_arr, slice_num):
	interval_arr_Flag = os.path.isfile(os.path.join(RATIO_DIR, '%s_interval_arr.npy' % model_name))
	indices_Flag = os.path.isfile(os.path.join(RATIO_DIR, '%s_max%s_indices.npy' % (model_name, slice_num)))

	if indices_Flag and interval_arr_Flag:
		interval_arr = np.load(os.path.join(RATIO_DIR, '%s_interval_arr.npy' % model_name))
		indices = np.load(os.path.join(RATIO_DIR, '%s_max%s_indices.npy' % (model_name, slice_num)))
		# print(True)
	else:
		interval_arr = interval_arr_generator(model_name, timestamp_arr)
		indices = np.argpartition(-interval_arr, slice_num)
		indices = indices[0:slice_num]
		# np.save(os.path.join(RATIO_DIR, '%s_max%s_indices.npy'%(model_name, slice_num)), indices)
	
	indices.sort()
	# print(interval_arr[indices])
	# print(indices[0:500])
	# print(indices[500])

	comm_time = np.zeros(len(indices)-1)
	comp_time = np.zeros(len(indices)-1)

	for i in range(len(indices)-1):
	  comp_time[i] = interval_arr[indices[i]]
	  comm_time[i] = timestamp_arr[indices[i+1]] - timestamp_arr[indices[i]+1]
	
	aver_comm = np.mean(comm_time)
	aver_comp = np.mean(comp_time)

	# print("%s's average computation time: %.2f: " % (model_name, aver_comp))
	# print("%s's average communication time: %.2f: " % (model_name, aver_comm))
	# print("{}'s average communication time: {:.2%}: ".format(model_name, aver_comp/(aver_comp+aver_comm)))
	return aver_comp, aver_comm

def stacked_bar_plot(figure_name, comm, comp, xticks_name):
	ratio_comp = comp / (comp+comm)
	ratio_comm = 1 - ratio_comp
	ind = np.arange(len(comm))
	width = 0.35

	plt.figure(figure_name)
	plt.subplot(2,1,1)
	p1 = plt.bar(ind, comm, width)
	p2 = plt.bar(ind, comp, width, bottom=comm)

	plt.ylabel('Time')
	plt.title('Comparison of average computation and communication time')
	plt.xticks(ind, xticks_name)
	plt.yticks(np.arange(0, 1.1, 0.1))
	plt.legend((p1[0], p2[0]), ('Communication', 'Computation'))

	plt.subplot(2,1,2)
	p1 = plt.bar(ind, ratio_comm, width)
	p2 = plt.bar(ind, ratio_comp, width, bottom=ratio_comm)

	plt.ylabel('Ratio')
	plt.title('Comparison of average computation and communication time')
	plt.xticks(ind, xticks_name)
	plt.yticks(np.arange(0, 1.1, 0.1))
	plt.legend((p1[0], p2[0]), ('Communication', 'Computation')) 
	plt.show()

def group_stacked_bar_plot(figure_name, comm_4, comm_8, comp_4, comp_8, xticks_name):
	ratio_comp_4 = comp_4 / (comp_4+comm_4)
	ratio_comm_4 = 1 - ratio_comp_4
	ratio_comp_8 = comp_8 / (comp_8+comm_8)
	ratio_comm_8 = 1 - ratio_comp_8
	print(ratio_comp_4)
	print(ratio_comp_8)
	ind = np.arange(len(comm_4))
	width = 0.35

	plt.figure(figure_name)
	# plt.subplot(2,1,1)
	p1_4 = plt.bar(ind, comm_4, width, color='white', edgecolor='blue', hatch=patterns[1], label='Comm time of 4 nodes')
	p2_4 = plt.bar(ind, comp_4, width, bottom=comm_4, color='red', edgecolor='red', label='Comp time of 4 nodes')

	p1_8 = plt.bar(ind+width+0.05, comm_8, width, color='white', edgecolor='black', hatch=patterns[1], label='Comm time of 8 nodes')
	p2_8 = plt.bar(ind+width+0.05, comp_8, width, bottom=comm_8, color='orange', edgecolor='orange', label='Comp time of 8 nodes')

	plt.ylabel('Comm/Comp Time', label_font)
	# plt.title('Comparison of average computation and communication time')
	plt.xticks(ind+width/2+0.025, xticks_name)
	# plt.yticks(np.arange(0, 1.1, 0.1))
	# plt.legend()
	plt.legend(loc='best', prop=legend_font)
	label_4 = np.around(comm_4 + comp_4, 2)
	label_8 = np.around(comm_8 + comp_8, 2)
	for i in range(len(xticks_name)):
		plt.text(x = ind[i]-0.05 , y = label_4[i]+0.05, s = label_4[i], fontdict=text_font)
		plt.text(x = ind[i]+width, y = label_8[i]+0.05, s = label_8[i], fontdict=text_font)

	plt.tick_params(labelsize=20)
	# plt.subplot(2,1,2)
	# p1_4 = plt.bar(ind, ratio_comm_4, width, color='white', edgecolor='blue', hatch=patterns[1], label='Comm ratio of 4 nodes')
	# p2_4 = plt.bar(ind, ratio_comp_4, width, bottom=ratio_comm_4, color='red', edgecolor='red', label='Comp ratio of 4 nodes')

	# p1_8 = plt.bar(ind+width+0.05, ratio_comm_8, width, color='white', edgecolor='black', hatch=patterns[1], label='Comm ratio of 8 nodes')
	# p2_8 = plt.bar(ind+width+0.05, ratio_comp_8, width, bottom=ratio_comm_8, color='orange', edgecolor='orange', label='Comp ratio of 8 nodes')

	# plt.ylabel('Comm/Comp Ratio')
	# plt.title('Comparison of average computation and communication time ratio')
	# plt.xticks(ind+width/2+0.025, xticks_name)
	# # plt.yticks(np.arange(0, 1.1, 0.1))
	# # plt.legend((p1[0], p2[0]), ('Communication', 'Computation')) 
	# plt.legend(loc='best')
	plt.show()


def phase_time(model_name, arr, slice_num):
	interval_arr = interval_arr_generator(model_name, arr)
	indices = np.argpartition(-interval_arr, slice_num)
	indices = indices[0:slice_num]
	
	indices.sort()

	time = np.zeros(len(indices)-1)

	for i in range(len(indices)-1):
	  time[i] = arr[indices[i+1]] - arr[indices[i]+1]
	
	aver_time = np.mean(time)

	# print("%s's average computation time: %.2f: " % (model_name, aver_comp))
	# print("%s's average communication time: %.2f: " % (model_name, aver_comm))
	# print("{}'s average communication time: {:.2%}: ".format(model_name, aver_comp/(aver_comp+aver_comm)))
	return aver_time


if __name__ == '__main__':
	filedict = {'resnet18_4':'resnet18_4_256_w4', 
				'resnet18_8':'resnet18_8_256_w4', 
				'resnet50_4':'resnet50_4_256_w4', 
				'resnet50_8':'resnet50_8_256_w4', 
				'resnet101_4':'resnet101_4_256_w3', 
				'resnet101_8':'resnet101_8_256_w3', 
				'vgg11_4':'vgg11_4_256_w0', 
				'vgg11_8':'vgg11_8_256_w0', 
				'vgg19_4':'vgg19_4_256_w1', 
				'vgg19_8':'vgg19_8_256_w1'}

	# filedict = {'resnet18_4':'resnet18_4_32_w3', 
	# 			'resnet18_8':'resnet18_8_32_w0', 
	# 			'resnet50_4':'resnet50_4_32_w4', 
	# 			'resnet50_8':'resnet50_8_32_w1', 
	# 			'resnet101_4':'resnet101_4_32_w0', 
	# 			'resnet101_8':'resnet101_8_32_w0', 
	# 			'vgg11_4':'vgg11_4_32_w0', 
	# 			'vgg11_8':'vgg11_8_32_w3', 
	# 			'vgg19_4':'vgg19_4_32_w3', 
	# 			'vgg19_8':'vgg19_8_32_w4'}
				
	for key in filedict:
		filedict[key]+= '_timestamp.npy'
		# filedict[key]+= '_pull.npy'

	# print(filedict)

	vgg11_arr = np.load(os.path.join(TIMESTAMP_DIR, filedict['vgg11_4']))
	vgg19_arr = np.load(os.path.join(TIMESTAMP_DIR, filedict['vgg19_4']))
	resnet18_arr = np.load(os.path.join(TIMESTAMP_DIR, filedict['resnet18_4']))
	resnet50_arr = np.load(os.path.join(TIMESTAMP_DIR, filedict['resnet50_4']))
	resnet101_arr = np.load(os.path.join(TIMESTAMP_DIR, filedict['resnet101_4']))
	
	resnet18_comp, resnet18_comm = calculate_phase_time('resnet18_4', resnet18_arr, 65)
	resnet50_comp, resnet50_comm = calculate_phase_time('resnet50_4', resnet50_arr, 65)
	resnet101_comp, resnet101_comm = calculate_phase_time('resnet101_4', resnet101_arr, 65)
	vgg11_comp, vgg11_comm = calculate_phase_time('vgg11_4', vgg11_arr, 65)
	vgg19_comp, vgg19_comm = calculate_phase_time('vgg19_4', vgg19_arr, 65)
	
	comp_arr_4 = np.array([resnet18_comp, resnet50_comp, resnet101_comp, vgg11_comp, vgg19_comp])
	comm_arr_4 = np.array([resnet18_comm, resnet50_comm, resnet101_comm, vgg11_comm, vgg19_comm])
	
	# resnet18_time = phase_time('resnet18_4', resnet18_arr, 500)
	# resnet50_time = phase_time('resnet50_4', resnet50_arr, 500)
	# resnet101_time = phase_time('resnet101_4', resnet101_arr, 450)
	# vgg11_time = phase_time('vgg11_4', vgg11_arr, 500)
	# vgg19_time = phase_time('vgg19_4', vgg19_arr, 500)

	# time_arr_4 = np.array([resnet18_time, resnet50_time, resnet101_time, vgg11_time, vgg19_time])
	# print(time_arr_4)

	# xticks_name = ('vgg11', 'vgg19', 'resnet18', 'resnet50')
	# figure_name = 'Comparison graph of 4 nodes'
	# stacked_bar_plot(figure_name, comm_arr, comp_arr, xticks_name)

	vgg11_arr = np.load(os.path.join(TIMESTAMP_DIR, filedict['vgg11_8']))
	vgg19_arr = np.load(os.path.join(TIMESTAMP_DIR, filedict['vgg19_8']))
	resnet18_arr = np.load(os.path.join(TIMESTAMP_DIR, filedict['resnet18_8']))
	resnet50_arr = np.load(os.path.join(TIMESTAMP_DIR, filedict['resnet50_8']))
	resnet101_arr = np.load(os.path.join(TIMESTAMP_DIR, filedict['resnet101_8']))
	
	resnet18_comp, resnet18_comm = calculate_phase_time('resnet18_8', resnet18_arr, 33)
	resnet50_comp, resnet50_comm = calculate_phase_time('resnet50_8', resnet50_arr, 33)
	resnet101_comp, resnet101_comm = calculate_phase_time('resnet101_8', resnet101_arr, 33)
	vgg11_comp, vgg11_comm = calculate_phase_time('vgg11_8', vgg11_arr, 33)
	vgg19_comp, vgg19_comm = calculate_phase_time('vgg19_8', vgg19_arr, 33)
	
	comp_arr_8 = np.array([resnet18_comp, resnet50_comp, resnet101_comp, vgg11_comp, vgg19_comp])
	comm_arr_8 = np.array([resnet18_comm, resnet50_comm, resnet101_comm, vgg11_comm, vgg19_comm])

	# xticks_name = ('vgg11', 'vgg19', 'resnet18', 'resnet50', 'resnet101')
	# figure_name = 'Comparison graph of 8 nodes'
	# stacked_bar_plot(figure_name, comm_arr, comp_arr, xticks_name)
	xticks_name = ('resnet18', 'resnet50', 'resnet101', 'vgg11', 'vgg19')
	figure_name = 'Group comparision graph'
	group_stacked_bar_plot(figure_name, comm_arr_4, comm_arr_8, comp_arr_8, comp_arr_8, xticks_name)



