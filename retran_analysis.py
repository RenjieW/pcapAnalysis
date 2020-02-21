import argparse
import os 
import sys
import math
import numpy as np
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP

window_size = 5000
FILE_DIR = './batch64/filtered_feature_files'
RESULTS_DIR = './batch64/retran_results'
# FILE_DIR = '/proj/distributed-ml-PG0/rjwu/filtered_feature_files'

def packet_counter(path, file_name):
    feature_file = np.load(os.path.join(path,file_name), allow_pickle=True)
    arr_len = feature_file.shape[0]
    info_len = feature_file.shape[1]
    retran_counter = 0
    print('length of %s is %d' % (file_name, arr_len))

    seq_arr = np.zeros(arr_len)

    if info_len == 10:
        for i in range(0, arr_len):
            src_ip = feature_file[i, 1]
            dst_ip = feature_file[i, 2]
            sport = feature_file[i, 3]
            dport = feature_file[i, 4]
            seq = feature_file[i, 6]
            seq_arr[i] = seq

            # our of order detection
            # if (seq<seq_arr[i-1]):
            #     if i > 5000:
            #         index = (np.abs(seq_arr[i-5000:i]-seq)).argmin()
            #         time_interval = np.abs(feature_file[i,0]-feature_file[i-5000+index,0])
            #     else:
            #         index = (np.abs(seq_arr[0:i]-seq)).argmin()
            #         time_interval = np.abs(feature_file[i,0]-feature_file[index,0])
                
            #     if time_interval > 0.003:
            #         retran_counter += 1
            #         continue
            #     else:
            #         order_counter += 1

            size = i if i<window_size else window_size
            for j in range(-size, 0):
                flag1 = (src_ip == feature_file[i+j,1])
                flag2 = (dst_ip == feature_file[i+j,2])
                flag3 = (sport == feature_file[i+j,3])
                flag4 = (dport == feature_file[i+j,4])
                flag5 = (seq == feature_file[i+j,6])
                # use seq number to detect
                if flag1 and flag2 and flag3 and flag4 and flag5:
                    retran_counter += 1
                    break

    elif info_len == 8:
        for i in range(0, arr_len):
            src_ip = feature_file[i, 1]
            dst_ip = feature_file[i, 2]
            seq = feature_file[i, 4]
            seq_arr[i] = seq

            size = i if i<window_size else window_size
            for j in range(-size, 0):
                flag1 = (src_ip == feature_file[i+j,1])
                flag2 = (dst_ip == feature_file[i+j,2])
                flag3 = (seq == feature_file[i+j,4])
                # use seq number to detect
                if flag1 and flag2 and flag3:
                    retran_counter += 1
                    break

    print('Loop complete')
    return arr_len, retran_counter

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='feature file reader')
    parser.add_argument('--file', metavar='<feature file name>',
                        help='feature file to parse', required=True)
    args = parser.parse_args()
    
    file_name = args.file

    arr_len, retran_num = packet_counter(FILE_DIR, file_name)
    ratio = retran_num / arr_len
    print('Retransmission packets: %d' % retran_num)
    print('Ratio: {0:.3%}'.format(retran_num / arr_len))

    result_path = os.path.join(RESULTS_DIR, file_name.split('.')[0]+'_results.txt')
    f = open(result_path, 'w+')
    f.write(str(arr_len)+'\n')
    f.write(str(retran_num)+'\n')
    f.write(str(ratio))
    f.close()