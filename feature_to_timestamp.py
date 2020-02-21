import argparse
import os 
import sys
import math
import numpy as np
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP

TIMESTAMP_DIR = './timestamp_files'
FEATURE_DIR = './feature_files'

def featuer_to_timestamp(feature_filename, host_ip, src_dir, dst_dir):
    feature_arr = np.load(os.path.join(src_dir, feature_filename), allow_pickle=True)
    arr_len = feature_arr.shape[0]
    info_len = feature_arr.shape[1]
    
    timestamp_arr = []
    pull_arr = []
    push_arr = []

    pull_len = 0
    push_len = 0

    if info_len == 10:
        index = 5
    elif info_len == 8:
        index = 3

    for i in range(arr_len):
        if feature_arr[i][index] == 0:
            continue
        # print(feature_arr[i][index])
        timestamp_arr.append(feature_arr[i, 0])
        src_ip = feature_arr[i, 1]

        if src_ip == host_ip:
            push_arr.append(feature_arr[i, 0])
            push_len += feature_arr[i][index]
        else:
            pull_arr.append(feature_arr[i, 0])
            pull_len += feature_arr[i][index]

    print(pull_len)
    print(push_len)
    timestamp_arr = np.array(timestamp_arr)
    pull_arr = np.array(pull_arr)
    push_arr = np.array(push_arr)

    prefix = ''
    for i in range(len(feature_filename.split('_'))-1):
        prefix = prefix + feature_filename.split('_')[i] + '_'

    timestamp_arr_path = os.path.join(dst_dir, prefix + 'timestamp.npy')  
    pull_arr_path = os.path.join(dst_dir, prefix + 'pull.npy')
    push_arr_path = os.path.join(dst_dir, prefix + 'push.npy')
    np.save(timestamp_arr_path, timestamp_arr)
    np.save(pull_arr_path, pull_arr)
    np.save(push_arr_path, push_arr)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='feature files reader')
    parser.add_argument('--filename', metavar='<feature filename>',
                        help='files to parse', required=True)
    parser.add_argument('--ip', metavar='<ip of host>',
                        help='ip of host', required=True)
    args = parser.parse_args()

    feature_filename = args.filename
    host_ip = args.ip

    file_Flag = os.path.isfile(os.path.join(FEATURE_DIR, feature_filename))

    if file_Flag:
        featuer_to_timestamp(feature_filename, host_ip, FEATURE_DIR, TIMESTAMP_DIR)

        sys.exit(0)
    else:
        print('File does not exist.')
        sys.exit(-1)