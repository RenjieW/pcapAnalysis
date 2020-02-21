import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

legend_font = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 18,
}

label_font = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 26,
}

def time_plot(time_arr, model_name, xticks_name):
    plt.figure('Epoch Time vs. Batch Size')
    ind = np.arange(time_arr.shape[1])
    shape_arr = ['ro-', 'g<-', 'b>-', 'k*-', 'y+-']
    width = 0.35
    for i in range(time_arr.shape[0]):
        plt.plot(ind, time_arr[i], shape_arr[i], label=model_name[i])

    plt.xticks(ind, xticks_name)
    plt.legend(loc='best', prop=legend_font)
    plt.tick_params(labelsize=20)
    plt.ylabel('Time per Epoch', label_font)
    plt.xlabel('Batch Size', label_font)
    plt.show()


if __name__ == '__main__':
    resnet18_4 = [877, 402, 245, 142]
    resnet18_8 = [808, 256, 139, 76]
    resnet50_4 = [1734, 864, 437, 223]
    resnet50_8 = [1755, 462, 274, 131]
    resnet101_4 = [3109, 1500, 826, 378]
    resnet101_8 = [3263, 830, 457, 236]
    vgg11_4 = [2357, 1289, 676, 355]
    vgg11_8 = [1847, 672, 348, 181]
    vgg19_4 = [3002, 1550, 822, 452]
    vgg19_8 = [2604, 865, 474, 256]

    time_4 = np.array([resnet18_4, resnet50_4, resnet101_4, vgg11_4, vgg19_4])
    time_8 = np.array([resnet18_8, resnet50_8, resnet101_8, vgg11_8, vgg19_8])
    xticks_name = ['32', '64', '128', '256']
    model_name = ['resnet18', 'resnet50', 'resnet101', 'vgg11', 'vgg19']

    time_plot(time_8, model_name, xticks_name)
