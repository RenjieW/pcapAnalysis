# -*- coding: utf-8 -*-
from multiprocessing import Process, Value, Array, Queue, Lock
import time
import numpy as np

def training_task(nid, per, arr, queue, lock, send_nid, comp_arr):
	# nid = kw['nid']
	# per = kw['per']
	# arr = kw['arr']

	staleness = 5
	deteriorate_rate = 0.05
	# sigma = 0.1
	training_time = 1 + nid
	print('The id of subprocess is %s.\nTraining time per iteration: %.2f' % (nid, training_time))

	while (per.value < 100):
		temp_fastest = max(arr)
		temp_slowest = min(arr)

		while (temp_fastest == arr[nid]) and ((temp_fastest - temp_slowest) > staleness):
			time.sleep(training_time)
			temp_fastest = max(arr)
			temp_slowest = min(arr)

		# time.sleep(training_time+np.random.normal(0, sigma))
		time.sleep(training_time)
		comp_arr[arr[nid]] = training_time

		lock.acquire()
		time.sleep(150 / 51.2)
		queue.put(nid)
		lock.release()
		# print('Worker %s: %.2f.' % (nid, per.value))
		while (send_nid.value != nid):
			continue

		time.sleep(150 / 51.2)

		per.value += 1 - (temp_fastest - arr[nid]) * deteriorate_rate
		arr[nid] += 1

def control_process(queue, lock, nid):
	while True:
		if queue.empty():
			continue
	
		lock.acquire()
		nid.value = queue.get()
		time.sleep(2*150/51.2)
		lock.release()
		# print(nid.value)

if __name__ == '__main__':
	performance = Value('d', 0.0)
	send_nid = Value('i', -1)
	arr = Array('i', [0, 0, 0])
	# training_time = Array('d', [1.0, 1.0, 1.0])
	request_queue = Queue()
	queue_lock = Lock()
	comp_arr1 = Array('d', [0]*200)
	comp_arr2 = Array('d', [0]*200)
	comp_arr3 = Array('d', [0]*200)
	comp_arr = [comp_arr1, comp_arr2, comp_arr3]

	process_list = []
	for i in range(3):
		process_list.append(Process(target=training_task, args=(i, performance, arr, request_queue, queue_lock, send_nid, comp_arr[i])))

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
