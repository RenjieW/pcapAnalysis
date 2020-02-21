# -*- coding: utf-8 -*-
from multiprocessing import Process, Value, Array, Queue, Lock
import time
import socket

import sys
import struct

def sniff_process(msg_queue, queue_lock):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('', 8080))
	while True:
		recv_msg, addr = s.recvfrom(1024)
		msg = recv_msg.decode('utf-8') + ' ' + addr[0] + ' ' + str(addr[1])
		print('Packet received %s.' % msg)
		# queue_lock.acquire()
		msg_queue.put(msg)
		# queue_lock.release()
		

def queue_handler(msg_queue, queue_lock, progress_arr, performance):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	staleness_threshold = 5
	deteriorate_rate = 0.05
	training_flag = 1
	while training_flag:
		if msg_queue.empty():
			continue
		# elif queue.full():
		# 	for i in range(len(training_time)):
		# 		training_time[i] *= 2
		# 		flag = True
		# elif flag:
		# 	for i in range(len(training_time)):
		# 		training_time[i] /= 2
		# 		flag = False
	
		# queue_lock.acquire()

		time.sleep(150/512)
		msg = msg_queue.get()
		worker_nid = int(msg.split()[0])
		progress_arr[worker_nid] = int(msg.split()[1])
		training_time = float(msg.split()[2])
		client_ip = msg.split()[3]
		client_port = int(msg.split()[4])
		# queue_lock.release()

		client_addr = (client_ip, client_port)

		temp_fastest = max(progress_arr)
		temp_slowest = min(progress_arr)
		
		original_training_time = 1 + worker_nid
		if (temp_fastest == progress_arr[worker_nid]):
			performance.value += (1 + training_time / original_training_time)

			if ((temp_fastest - temp_slowest) > staleness_threshold):
				training_time *= 1.2
			elif training_time > (5 * original_training_time):
				training_time /= 1.2

		else:
			performance.value += (1 - (temp_fastest - progress_arr[worker_nid])*deteriorate_rate)

		time.sleep(150/512)
		if (performance.value >= 300):
			training_flag = 0

		msg = str(training_flag) + ' ' + str(training_time)
		send_msg = msg.encode('utf-8')
		s.sendto(send_msg, client_addr)

if __name__ == '__main__':
	performance = Value('d', 0.0)
	progress_arr = Array('i', [0, 0, 0])

	msg_queue = Queue()
	queue_lock = Lock()

	
	process_list = []
	process_list.append(Process(target=sniff_process, args=(msg_queue, queue_lock)))
	process_list.append(Process(target=queue_handler, args=(msg_queue, queue_lock, progress_arr, performance)))

	for i in range(2):
		process_list[i].start()

	process_list[1].join()
	process_list[0].terminate()

	print('Performance: %.2f.' % performance.value)
	for i in range(3):
		print('Worker %s trained %d iterations.' % (i, progress_arr[i]))

