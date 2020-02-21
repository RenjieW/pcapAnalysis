#!/usr/bin/env bash
cd /proj/distributed-ml-PG0/rjwu/
python3 feature_to_timestamp.py --filename resnet18_8_128_w4_feature.npy --ip 10.10.1.6
python3 feature_to_timestamp.py --filename resnet50_8_128_w4_feature.npy --ip 10.10.1.6
python3 feature_to_timestamp.py --filename resnet101_8_128_w3_feature.npy --ip 10.10.1.5
python3 feature_to_timestamp.py --filename vgg11_8_128_w0_feature.npy --ip 10.10.1.1
python3 feature_to_timestamp.py --filename vgg19_8_128_w1_feature.npy --ip 10.10.1.2