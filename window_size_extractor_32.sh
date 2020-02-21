#!/usr/bin/env bash
cd /proj/distributed-ml-PG0/rjwu/

python3 window_size.py --file resnet18_4_32_w3_feature_filterd.npy --dir batch32
# python3 window_size.py --file resnet18_8_32_w0_feature_filterd.npy --dir batch32
python3 window_size.py --file resnet50_4_32_w4_feature_filterd.npy --dir batch32
python3 window_size.py --file resnet50_8_32_w1_feature_filterd.npy --dir batch32
python3 window_size.py --file resnet101_4_32_w0_feature_filterd.npy --dir batch32
python3 window_size.py --file resnet101_8_32_w0_feature_filterd.npy --dir batch32
python3 window_size.py --file vgg11_4_32_w0_feature_filterd.npy --dir batch32
python3 window_size.py --file vgg11_8_32_w3_feature_filterd.npy --dir batch32
python3 window_size.py --file vgg19_4_32_w3_feature_filterd.npy --dir batch32
python3 window_size.py --file vgg19_8_32_w4_feature_filterd.npy --dir batch32