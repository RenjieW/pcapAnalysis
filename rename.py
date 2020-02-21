import os
import argparse

def rename_files(file_dir, insert_string, position):
    for f in os.listdir(file_dir):
        name_list = f.split('_')
        src = file_dir +'/' + f
        dst = file_dir + '/'
        for i in range(len(name_list)):
            dst = dst + name_list[i] + '_'
            if (i+1) == position:
                dst = dst + insert_string + '_'
        dst = dst[:-1]
        os.rename(src, dst)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dir name')
    parser.add_argument('--dir', metavar='<path>',
                        help='path of dir', required=True)

    args = parser.parse_args()
    files_dir = args.dir
    rename_files(files_dir, '32', 2)