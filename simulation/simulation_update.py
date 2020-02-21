# -*- coding: utf-8 -*-
from multiprocessing import Process, Value, Array, Queue, Lock
import time
import numpy as np

def training_task(nid, per, arr, training_time, queue, lock, send_nid, comp_arr):
	# nid = kw['nid']
	# per = kw['per']
	# arr = kw['arr']

	print('The id of subprocess is %s' % nid)
	staleness = 5
	deteriorate_rate = 0.05
	update_rate = 0.05
	# original_sigma = 0.1
	# sigma = original_sigma
	original_training_time = 1 + nid
	training_time[nid] = original_training_time

	while (per.value < 100):
		temp_fastest = max(arr)
		temp_slowest = min(arr)

		if (temp_fastest == arr[nid]) and ((temp_fastest - temp_slowest) > staleness):
			training_time[nid] *= 2
			# sigma *= 2
		elif (training_time[nid] > (original_training_time * 2)):
			training_time[nid] /= 2
			# sigma /= 2
		else:
			training_time[nid] = original_training_time
			# sigma = original_sigma

		# time.sleep(training_time[nid]+np.random.normal(0, sigma))
		time.sleep(training_time[nid])
		comp_arr[arr[nid]] = training_time[nid]

		# print('Worker %s: %.2f.' % (nid, per.value))
		lock.acquire()
		time.sleep(150 / 51.2)
		queue.put(nid)
		lock.release()
		# print('Worker %s: %.2f.' % (nid, per.value))
		while (send_nid.value != nid):
			continue
 
		time.sleep(150 / 51.2)

		per.value += 1 - (temp_fastest - arr[nid]) * deteriorate_rate + (training_time[nid] / original_training_time) * update_rate 
		arr[nid] += 1

# def control_process(training_time, queue, lock, nid):
def control_process(queue, lock, nid):
	# flag = False
	while True:
		if queue.empty():
			continue
		# elif queue.full():
		# 	for i in range(len(training_time)):
		# 		training_time[i] *= 2
		# 		flag = True
		# elif flag:
		# 	for i in range(len(training_time)):
		# 		training_time[i] /= 2
		# 		flag = False
	
		lock.acquire()
		nid.value = queue.get()
		time.sleep(2*150/51.2)
		lock.release()
		# print(nid.value)

if __name__ == '__main__':
	performance = Value('d', 0.0)
	send_nid = Value('i', -1)
	arr = Array('i', [0, 0, 0])
	training_time = Array('d', [1.0, 1.0, 1.0])
	# request_queue = Queue(6)
	request_queue = Queue()
	queue_lock = Lock()

	comp_arr1 = Array('d', [0]*200)
	comp_arr2 = Array('d', [0]*200)
	comp_arr3 = Array('d', [0]*200)
	comp_arr = [comp_arr1, comp_arr2, comp_arr3]

	process_list = []
	for i in range(3):
		process_list.append(Process(target=training_task, args=(i, performance, arr, training_time, request_queue, queue_lock, send_nid, comp_arr[i])))

	# process_list.append(Process(target=control_process, args=(training_time, request_queue, queue_lock, send_nid)))
	process_list.append(Process(target=control_process, args=(request_queue, queue_lock, send_nid)))

	start = time.time()
	for i in range(4):
		process_list[i].start()

	for i in range(3):
		process_list[i].join()

	process_list[3].terminate()

	end = time.time()
	training_time = end - start

	print('Performance: %.2f.' % performance.value)
	print('Training time: %.2f seconds.' % training_time)
	for i in range(3):
		print('Worker %s trained %d iterations.' % (i, arr[i]))

	normal_arr1 = []
	normal_arr2 = []
	normal_arr3 = []
	normal_arr = [normal_arr1, normal_arr2, normal_arr3]
	for i in range(3):
		for j in range(200):
			if (comp_arr[i][j] != 0):
				normal_arr[i].append(comp_arr[i][j])

	normal_arr1 = np.array(normal_arr1)
	normal_arr2 = np.array(normal_arr2)
	normal_arr3 = np.array(normal_arr3)

	print(len(normal_arr1))
	print(len(normal_arr2))
	print(len(normal_arr3))
	np.save('normal_arr1.npy', normal_arr1)
	# np.save('normal_arr2.npy', normal_arr2)
	# np.save('normal_arr3.npy', normal_arr3)


