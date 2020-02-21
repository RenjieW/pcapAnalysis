#!/usr/bin/env bash
cd /proj/distributed-ml-PG0/rjwu/

python3 window_size_extractor.py --file resnet18_4_256_w4_feature.npy --dir batch256 --ip 10.10.1.6
# python3 window_size_extractor.py --file resnet18_8_256_w4_feature.npy  --dir batch256 --ip 10.10.1.6
python3 window_size_extractor.py --file resnet50_4_256_w4_feature.npy --dir batch256 --ip 10.10.1.6
python3 window_size_extractor.py --file resnet50_8_256_w4_feature.npy --dir batch256 --ip 10.10.1.6
python3 window_size_extractor.py --file resnet101_4_256_w3_feature.npy --dir batch256 --ip 10.10.1.5
python3 window_size_extractor.py --file resnet101_8_256_w3_feature.npy --dir batch256 --ip 10.10.1.5
python3 window_size_extractor.py --file vgg11_4_256_w0_feature.npy --dir batch256 --ip 10.10.1.1
python3 window_size_extractor.py --file vgg11_8_256_w0_feature.npy --dir batch256 --ip 10.10.1.1
python3 window_size_extractor.py --file vgg19_4_256_w1_feature.npy --dir batch256 --ip 10.10.1.2
python3 window_size_extractor.py --file vgg19_8_256_w1_feature.npy --dir batch256 --ip 10.10.1.2