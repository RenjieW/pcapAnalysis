import argparse
import os 
import sys
import math
import numpy as np
from scapy.utils import RawPcapReader

SRC_DIR = './feature_files'
DST_DIR = './filtered_feature_files'

def packets_filter(src_path, dst_path, file_name):
    feature_arr = np.load(os.path.join(src_path, file_name), allow_pickle=True)
    arr_len = feature_arr.shape[0]
    info_len = feature_arr.shape[1]
    if info_len == 10:
        index = 5
    elif info_len == 8:
        index = 3
    filtered_feature_arr = []
    for i in range(arr_len):
        if feature_arr[i,index]:
            filtered_feature_arr.append(feature_arr[i,:])

    filtered_feature_arr = np.array(filtered_feature_arr)
    filtered_file_name = file_name.split('.')[0] + '_filterd.npy'
    np.save(os.path.join(dst_path, filtered_file_name), filtered_feature_arr)
    print(arr_len)
    print(len(filtered_feature_arr))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='feature file reader')
    parser.add_argument('--file', metavar='<feature file name>',
                        help='feature file to parse', required=True)
    args = parser.parse_args()
    
    file_name = args.file
    retran_num = packets_filter(SRC_DIR, DST_DIR, file_name)