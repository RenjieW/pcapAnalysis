import argparse
import os 
import sys
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

FIGURE_DIR = './figures/window_size'

legend_font = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 18,
}

label_font = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 26,
}

def window_size_plot(push_window_path, pull_window_path, model_name, figure_dir, packets_num):
    push_window_arr = np.load(push_window_path, allow_pickle=True)
    pull_window_arr = np.load(pull_window_path, allow_pickle=True)
    push_window_arr = push_window_arr[:, 0:packets_num]
    pull_window_arr = pull_window_arr[:, 0:packets_num]

    plt.figure(figsize=[12, 8])
    plt.plot(push_window_arr[0,:], push_window_arr[1,:], 'ro-', label=model_name+'_push')
    plt.plot(pull_window_arr[0,:], pull_window_arr[1,:], 'bo-', label=model_name+'_pull')
    plt.legend(loc='best', prop=legend_font)
    plt.tick_params(labelsize=20)
    plt.ylabel('TCP Window Size', label_font)
    plt.xlabel('Time', label_font)
    plt.show()
    figure_name = model_name + '_window_size.png'
    figure_path = os.path.join(figure_dir, figure_name)
    plt.savefig(figure_path, dpi = 150, quality = 95)



def window_size_arr(file_path, ip):
    feature_arr = np.load(file_path, allow_pickle=True)
    arr_len = feature_arr.shape[0]
    info_len = feature_arr.shape[1]

    push_window_arr = []
    pull_window_arr = []
    push_timestamp_arr = []
    pull_timestamp_arr = []

    if info_len == 10:
        index = 9
    else:
        index = 7

    for i in range(arr_len):
        if feature_arr[i][1] == ip:
            push_timestamp_arr.append(feature_arr[i][0])
            push_window_arr.append(feature_arr[i][index])
        elif feature_arr[i][2] == ip:
            pull_timestamp_arr.append(feature_arr[i][0])
            pull_window_arr.append(feature_arr[i][index])

    push_window_arr = np.array(push_window_arr)
    push_timestamp_arr = np.array(push_timestamp_arr)
    pull_window_arr = np.array(pull_window_arr)
    pull_timestamp_arr = np.array(pull_timestamp_arr)

    return np.array([push_timestamp_arr, push_window_arr]), np.array([pull_timestamp_arr, pull_window_arr])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='read feature files')
    parser.add_argument('--file', metavar='<file name>',
                        help='file to extract', required=True)
    parser.add_argument('--dir', metavar='<dir name>',
                        help='dir which stores files', required=True)
    parser.add_argument('--ip', metavar='<ip address>',
                        help='ip of the host')


    args = parser.parse_args()
    file_name = args.file
    dir_name = args.dir
    ip = args.ip

    # src_dir = os.path.join('.', dir_name, 'filtered_feature_files')
    src_dir = os.path.join('.', dir_name, 'feature_files')
    dst_dir = os.path.join('.', dir_name, 'window_files')

    name_arr = file_name.split('_')
    prefix = ''
    for i in range(3):
        prefix += name_arr[i] 
        prefix += '_'

    push_window_path = os.path.join(dst_dir, prefix + 'push_window.npy')
    pull_window_path = os.path.join(dst_dir, prefix + 'pull_window.npy')
    if not (os.path.isfile(push_window_path) and os.path.isfile(pull_window_path)):
        file_path = os.path.join(src_dir, file_name)
        push_window_arr, pull_window_arr = window_size_arr(file_path, ip)
        np.save(push_window_path, push_window_arr)
        np.save(pull_window_path, pull_window_arr)
    
    window_size_plot(push_window_path, pull_window_path, prefix[:-1], FIGURE_DIR, 20000)