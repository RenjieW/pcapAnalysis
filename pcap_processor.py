import argparse
import os 
import sys
import math
import numpy as np
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP

FEATURE_DIR = 'feature_files'
TIMESTAMP_DIR = 'timestamp_files'
PCAP_DIR = 'pcap_files'


def feature_extractor(file_name):
    print('Opening {}...'.format(file_name))
    count = 0
    effective_packet_count = 0
    packets_feature = []
    for (pkt_data, pkt_metadata,) in RawPcapReader(os.path.join(PCAP_DIR, file_name)):
        count += 1
        ether_pkt = Ether(pkt_data)
        # discard llc frames
        if 'type' not in ether_pkt.fields:
            continue
        # discard non-ipv4 packets
        if ether_pkt.type != 0x0800:
            continue
        # discard non-tcp packets
        ip_pkt = ether_pkt[IP]
        if ip_pkt.proto != 6:
            continue

        tcp_pkt = ip_pkt[TCP]
        if (ip_pkt.flags == 'MF') or (ip_pkt.frag != 0):
            continue

        effective_packet_count += 1
        packet_feature = []

        tcp_payload_len = ip_pkt.len - (ip_pkt.ihl * 4) - (tcp_pkt.dataofs * 4)

        if effective_packet_count == 1:
            first_pkt_timestamp = pkt_metadata.sec + pkt_metadata.usec / 1000000
            first_pkt_ordinal = count

        last_pkt_timestamp = pkt_metadata.sec + pkt_metadata.usec / 1000000
        last_pkt_ordinal = count

        this_pkt_relative_timestamp = last_pkt_timestamp - first_pkt_timestamp

        packet_feature.append(this_pkt_relative_timestamp)
        packet_feature.append(ip_pkt.src)
        packet_feature.append(ip_pkt.dst)
        packet_feature.append(tcp_pkt.sport)
        packet_feature.append(tcp_pkt.dport)
        packet_feature.append(tcp_payload_len)
        packet_feature.append(tcp_pkt.seq)
        packet_feature.append(tcp_pkt.ack)
        packet_feature.append(tcp_pkt.flags)
        packet_feature.append(tcp_pkt.window)

        packets_feature.append(packet_feature)
        # print(packet_feature)
        # print(packets_feature.shape)

    packets_feature = np.array(packets_feature)
    print(packets_feature.shape)

    prefix = file_name.split('.')[0]
    np.save(os.path.join(FEATURE_DIR, prefix+'_feature.npy'), packets_feature)
    # np.save('./feature_files/%s_feature.npy' % file_name.split('.')[0], packets_feature)

def timestamp_arr_generator(file_name, host_ip):
    print('Opening {}...'.format(file_name))
    count = 0
    effective_packet_count = 0
    timestamp_arr = []
    pull_arr = []
    push_arr = []
    for (pkt_data, pkt_metadata,) in RawPcapReader(os.path.join('./pcap_files', file_name)):
        count += 1
        ether_pkt = Ether(pkt_data)
        # discard llc frames
        if 'type' not in ether_pkt.fields:
            continue
        # discard non-ipv4 packets
        if ether_pkt.type != 0x0800:
            continue
        # discard non-tcp packets
        ip_pkt = ether_pkt[IP]
        if ip_pkt.proto != 6:
            continue

        tcp_pkt = ip_pkt[TCP]
        if (ip_pkt.flags == 'MF') or (ip_pkt.frag != 0):
            continue

        # discard packets without payload
        tcp_payload_len = ip_pkt.len - (ip_pkt.ihl * 4) - (tcp_pkt.dataofs * 4)
        if (tcp_payload_len == 0):
            continue

        effective_packet_count += 1

        if effective_packet_count == 1:
            first_pkt_timestamp = pkt_metadata.sec + pkt_metadata.usec / 1000000
            first_pkt_ordinal = count

        last_pkt_timestamp = pkt_metadata.sec + pkt_metadata.usec / 1000000
        last_pkt_ordinal = count

        this_pkt_relative_timestamp = last_pkt_timestamp - first_pkt_timestamp

        timestamp_arr.append(this_pkt_relative_timestamp)

        if (ip_pkt.src != host_ip):
            pull_arr.append(this_pkt_relative_timestamp)
        else:
            push_arr.append(this_pkt_relative_timestamp)

    timestamp_arr = np.array(timestamp_arr)
    pull_arr = np.array(push_arr)
    push_arr = np.array(push_arr)
    np.save('./timestamp_files/%s_timestamp_arr.npy' % file_name.split('.')[0], timestamp_arr)
    np.save('./timestamp_files/%s_pull_arr.npy' % file_name.split('.')[0], pull_arr)
    np.save('./timestamp_files/%s_push_arr.npy' % file_name.split('.')[0], push_arr)
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PCAP reader')
    parser.add_argument('--pcap', metavar='<pcap file name>',
                        help='pcap file to parse', required=True)
    parser.add_argument('--ip', metavar='<ip of host>',
    					help='ip of host', required=True)
    args = parser.parse_args()
    
    pcap_file_name = args.pcap
    host_ip = args.ip
    pcap_file_path = os.path.join(PCAP_DIR, pcap_file_name)
    
    features_filename = '%s_feature.npy' % pcap_file_name.split('.')[0]
    timestamp_arr_filename = '%s_timestamp_arr.npy' % pcap_file_name.split('.')[0]
    pull_arr_filename = '%s_pull_arr.npy' % pcap_file_name.split('.')[0]
    push_arr_filename = '%s_push_arr.npy' % pcap_file_name.split('.')[0]

    feature_Flag = os.path.isfile(os.path.join(FEATURE_DIR, features_filename))
    timestamp_Flag = os.path.isfile(os.path.join(TIMESTAMP_DIR, timestamp_arr_filename)) \
                and os.path.isfile(os.path.join(TIMESTAMP_DIR, pull_arr_filename)) \
                and os.path.isfile(os.path.join(TIMESTAMP_DIR, push_arr_filename))
                
    if feature_Flag:
        print('Extracted files already exist.')
        sys.exit(0)
    # if timestamp_Flag:
    #     print('Extracted files already exist.')
    #     sys.exit(0)
    elif not os.path.isfile(pcap_file_path):
        print('"{}" does not exist'.format(pcap_file_name))
        sys.exit(-1)
    else:
        feature_extractor(pcap_file_name)
        # timestamp_arr_generator(pcap_file_name, host_ip)
        sys.exit(0)