import argparse
import os 
import sys
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

FILE_DIR = './timestamp_files'

label_font = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 20,
}

# count number of packets during each provided interval
def array_slice(arr, interval):
	arr_len = len(arr)
	num_packets = []
	min_time = 0
	max_time = interval
	temp_count = 0
	for i in range(arr_len):
		if (arr[i] < max_time) and (arr[i] >= min_time): 				
			temp_count += 1
		elif arr[i] >= max_time:
			min_time += interval
			max_time += interval
			num_packets.append(temp_count)
			temp_count = 1

	return num_packets

# generate interval (adjacent) time array 
def interval_arr_generator(arr):
    interval_arr = np.array([])
    for i in range(len(arr)-1):
        adjacent_interval = arr[i+1] - arr[i]
        interval_arr = np.append(interval_arr, adjacent_interval)   

    return interval_arr 

# plot packet rates vs. time figures
def plot_packet_rate(timestamp_arr, pull_arr, push_arr, xlim, interval):
    len_of_time = len(timestamp_arr)
    num_packets = array_slice(timestamp_arr, interval)
    pull_num_packets = array_slice(pull_arr, interval)
    push_num_packets = array_slice(push_arr, interval)
    rough_time = interval * np.array(list(range(len(num_packets))))

    pull_num_packets = list(pull_num_packets + [0] * (len(rough_time) - len(pull_num_packets)))
    push_num_packets = list(push_num_packets + [0] * (len(rough_time) - len(push_num_packets)))

    plt.figure("packet rates figure") 
    plt.subplot(3, 1, 1)
    plt.plot(rough_time, num_packets, marker='o', mec='r')
    # plt.xlabel('Time', label_font)
    plt.ylabel('Packets #/10ms', label_font)
    plt.xlim(0, xlim)
    plt.subplot(3, 1, 2)
    plt.plot(rough_time, pull_num_packets, marker='v', mec='b')
    # plt.xlabel('Time', label_font)
    plt.ylabel('Pull Packets #/10ms', label_font)
    plt.xlim(0, xlim)
    plt.subplot(3, 1, 3)
    plt.plot(rough_time, push_num_packets, marker='^', mec='g')
    plt.xlabel('Time', label_font)
    plt.ylabel('Push Packets #/10ms', label_font)
    plt.xlim(0, xlim)  
    plt.show()

# plot packets vs. time
def plot_packets(timestamp_arr, pull_arr, push_arr, xlim):
    plt.figure("01packets figure") 
    plt.subplot(3, 1, 1)
    plt.plot(timestamp_arr, np.ones(len(timestamp_arr)), marker='o', mec='r')
    plt.xlim(0, xlim)
    plt.subplot(3, 1, 2)
    plt.plot(pull_arr, np.ones(len(pull_arr)), marker='v', mec='b')
    plt.xlim(0, xlim)
    plt.subplot(3, 1, 3)
    plt.plot(push_arr, np.ones(len(push_arr)), marker='^', mec='g')
    plt.xlim(0, xlim)
    plt.show()

# plot stacked bar graph (computation time vs. communication time)
def plot_comparison_bar(timestamp_arr):
    interval_arr = interval_arr_generator(timestamp_arr)

    indices = np.argpartition(-interval_arr, 6)
    indices = indices[0:6]
    indices.sort()
    # print(interval_arr[indices])
    # print(indices[0:6])
    comp_time = []
    comm_time = []
    norm_comp_time = []
    norm_comm_time = []

    for i in range(len(indices)-1):
        temp_comp = interval_arr[indices[i]]
        temp_comm = timestamp_arr[indices[i+1]] - timestamp_arr[indices[i]+1]
        comp_time.append(temp_comp)
        comm_time.append(temp_comm)

        norm_temp_comp = temp_comp / (temp_comp+temp_comm)
        norm_temp_comm = temp_comm / (temp_comp+temp_comm)
        norm_comp_time.append(norm_temp_comp)
        norm_comm_time.append(norm_temp_comm)



    print(norm_comp_time)
    print(norm_comm_time)

    ind = np.arange(len(norm_comp_time))    
    width = 0.35

    plt.figure('Comparison graph')
    p1 = plt.bar(ind, norm_comm_time, width)
    p2 = plt.bar(ind, norm_comp_time, width, bottom=norm_comm_time)

    plt.ylabel('Ratio')
    plt.title('Comparison of computation and communication time')
    plt.xticks(ind, ('1', '2', '3', '4', '5'))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.legend((p1[0], p2[0]), ('Communication', 'Computation'))
    # plt.ylim(0, 1.1)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='file reader')
    parser.add_argument('--prefix', metavar='<file name>',
                        help='prefix of numpy files to parse', required=True)
    args = parser.parse_args()
    
    prefix = args.prefix
    timestamp_filename = '%s_timestamp.npy' % prefix
    pull_filename = '%s_pull.npy' % prefix
    push_filename = '%s_push.npy' % prefix

    File_Flag = os.path.isfile(os.path.join(FILE_DIR, timestamp_filename)) \
                and os.path.isfile(os.path.join(FILE_DIR, pull_filename)) \
                and os.path.isfile(os.path.join(FILE_DIR, push_filename))
    
    # if not os.path.isfile(os.path.join(data_dir, pcap_file_name)):
    if not File_Flag:
        print('Files do not exist')
        sys.exit(0)
    else:
        timestamp_arr = np.load(os.path.join(FILE_DIR, timestamp_filename))
        pull_arr = np.load(os.path.join(FILE_DIR, pull_filename))
        push_arr = np.load(os.path.join(FILE_DIR, push_filename))
        
    # print([len(timestamp_arr), len(pull_arr), len(push_arr)])
    timestamp_arr = timestamp_arr[np.where(timestamp_arr<=50)]
    pull_arr = pull_arr[np.where(pull_arr<=50)]
    push_arr = push_arr[np.where(push_arr<=50)]
    xlim = math.ceil(timestamp_arr[-1])

    # # plot_packets(timestamp_arr, pull_arr, push_arr, xlim)
    plot_packet_rate(timestamp_arr, pull_arr, push_arr, xlim, 0.01)
    # # plot_comparison_bar(timestamp_arr)
    
    sys.exit(0)
