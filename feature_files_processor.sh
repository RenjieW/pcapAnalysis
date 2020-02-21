#!/usr/bin/env bash
cd /proj/distributed-ml-PG0/rjwu/
python3 feature_files_processor.py --file resnet18_4_128_w4_feature.npy
python3 feature_files_processor.py --file resnet50_4_128_w4_feature.npy
python3 feature_files_processor.py --file resnet101_4_128_w3_feature.npy
python3 feature_files_processor.py --file vgg11_4_128_w0_feature.npy
python3 feature_files_processor.py --file vgg19_4_128_w1_feature.npy