# -*- coding: utf-8 -*-
from multiprocessing import Process, Value, Array, Queue, Lock
import time
import numpy as np
import socket

def training_task(nid):
	# nid = kw['nid']
	# per = kw['per']
	# arr = kw['arr']

	print('The id of subprocess is %s' % nid)

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_port = 8080
	server_ip = '192.168.1.100'

	# s.connect((server_ip, server_port))
	
	sigma = 0.1
	original_training_time = 1 + nid
	training_flag = 1
	training_time = original_training_time
	iterations = 0

	while (training_flag):
		iterations += 1	
		
		# training phase
		time.sleep(training_time+np.random.normal(0, sigma))

		# synchronization phase
		msg = str(nid) + ' ' + str(iterations) + ' ' + str(training_time)
		send_msg = msg.encode('utf-8')
		s.sendto(send_msg, (server_ip, server_port))
		# s.send(send_msg)
		print('Process %s sent packet %s.' % (nid, msg))
		time.sleep(150/512)
		
		recv_msg, addr = s.recvfrom(1024)
		# recv_msg = s.recv(1024)
		msg = recv_msg.decode('utf-8')
		print('Process %s received packet %s.' % (nid, msg))
		training_flag = int(recv_msg.split()[0])
		training_time = float(recv_msg.split()[1])

	# s.close()

		
# def control_process(training_time, queue, lock, nid):
# 	flag = False
# 	while True:
# 		if queue.empty():
# 			continue
# 		elif queue.full():
# 			for i in range(len(training_time)):
# 				training_time[i] *= 2
# 				flag = True
# 		elif flag:
# 			for i in range(len(training_time)):
# 				training_time[i] /= 2
# 				flag = False
	
# 		lock.acquire()
# 		nid.value = queue.get()
# 		time.sleep(2*150/512)
# 		lock.release()
# 		# print(nid.value)

if __name__ == '__main__':
	process_list = []
	for i in range(2):
		process_list.append(Process(target=training_task, args=(i,)))

	start = time.time()
	for i in range(2):
		process_list[i].start()

	for i in range(2):
		process_list[i].join()

	print('Processes end.')
	# process_list[3].terminate()

	end = time.time()
	training_time = end - start
	
	print('Training time: %.2f seconds.' % training_time)
	# for i in range(3):
	# 	print('Worker %s trained %d iterations.' % (i, arr[i]))
