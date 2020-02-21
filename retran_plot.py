import argparse
import os 
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

DIR = './retran_results/all_files'

def file_reader(path):
    model_name = []
    total_num = []
    retran_num = []
    retran_ratio = []
    arr = [total_num, retran_num, retran_ratio]
    for f in os.listdir(path):
        if not f.split('.')[-1] == 'txt':
            continue
        with open(os.path.join(path, f), 'r') as fp:
            split_name = f.split('_')
            model_name.append(split_name[0]+'_'+split_name[1])
            cnt = 0 
            for line in fp:
                arr[cnt].append(line.strip('\n'))
                cnt += 1

    model_name = np.array(model_name)
    total_num = np.array(total_num).astype(int)
    retran_num = np.array(retran_num).astype(int)
    retran_ratio = np.array(retran_ratio).astype(float)

    index = np.argsort(model_name)
    # print(index)

    model_name = model_name[index]
    total_num = total_num[index]
    retran_num = retran_num[index]
    retran_ratio = retran_ratio[index]
    # print(model_name)
    return model_name, total_num, retran_num, retran_ratio

def retran_plot(model_name, retran_num, retran_ratio):
    ind = np.arange(len(model_name))    
    width = 0.35

    plt.figure('Retransmission Results')
    plt.subplot(2, 1, 1)
    plt.bar(ind, retran_num, width)
    plt.ylabel('Retransmission Packets')
    plt.xticks(ind, model_name)
    plt.subplot(2, 1, 2)
    plt.bar(ind, retran_ratio*1000, width)
    plt.ylabel('Retransmission Ratios (‰)')
    plt.xticks(ind, model_name)
    plt.show()

if __name__ == '__main__':
    model_name, total_num, retran_num, retran_ratio = file_reader(DIR)
    # retran_plot(model_name, retran_num, retran_ratio)
    for i in range(len(model_name)):
        print(model_name[i])
        print(np.around(retran_ratio[i]*1000, 2))