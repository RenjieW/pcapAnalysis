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

def window_plot(model_dict, prefix, figures_dir):
    plt.figure(figsize=[12, 8])
    shape_arr = ['ro-', 'g<-', 'b>-', 'k*-', 'y+-', 'ro-.', 'g<-.', 'b>-.', 'k*-.', 'y+-.']
    i = 0
    for key, value in model_dict.items():
        plt.plot(value[0,:], value[1,:], shape_arr[i], label=key)
        i += 1

    plt.legend(loc='best', prop=legend_font)
    plt.tick_params(labelsize=20)
    plt.ylabel('TCP Window Size', label_font)
    plt.xlabel('Time', label_font)
    plt.show()
    figure_name = prefix + '_window_size.png'
    figure_path = os.path.join(figures_dir, figure_name)
    plt.savefig(figure_path, dpi = 150, quality = 95)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='numpy files reader')
    parser.add_argument('--dir', metavar='<dir name>',
                        help='dir which store numpy files', required=True)
    args = parser.parse_args()
    
    window_dir = os.path.join(args.dir, 'window_files')

    model_dict = {}
    for f in os.listdir(window_dir):
        name_arr = f.split('_')
        model_name = name_arr[0] + '_' + name_arr[1]
        model_path = os.path.join(window_dir, f)
        model_arr = np.load(model_path, allow_pickle=True)
        model_arr = model_arr[:, :5000]

        model_dict[model_name] = model_arr

    window_plot(model_dict, args.dir, FIGURE_DIR)