import datetime
import random

def handler(event):
	arr_dim1 = event.get('arr_dim1')
	arr_dim2 = event.get('arr_dim2')
	arr_dim3 = event.get('arr_dim3')
	num_loops = event.get('num_loops')
	rand_arr1 = [[random.randint(i-10, i+10) for i in range(arr_dim1)] for j in range(arr_dim2)]
	rand_arr2 = [[random.randint(i-10, i+10) for i in range(arr_dim2)] for j in range(arr_dim3)]
	# rand_arr1 = np.random.rand(arr_dim1, arr_dim2)
	# rand_arr2 = np.random.rand(arr_dim2, arr_dim3)

	processing_begin = datetime.datetime.now()
	# perform a bunch of random processing, but no need to really keep track of the results
	for i in range(num_loops):
		a = random.shuffle(rand_arr1)
		b = random.shuffle(rand_arr2)
	
	for i in range(len(rand_arr1)):
		for j in range(len(rand_arr1[0])):
			c = rand_arr1[i].pop(0)
	
	for i in range(len(rand_arr2)):
		for j in range(len(rand_arr2[0])):
			c = rand_arr2[i].pop(0)
	
	processing_end = datetime.datetime.now()

	processing_time = (processing_end - processing_begin) / datetime.timedelta(microseconds=1)
	num_entries = arr_dim1*arr_dim2 + arr_dim2*arr_dim3

	return {
		'result': 'success!',
		'measurement': {
			'processing_time': processing_time,
			'num_entries': num_entries
		}
	}
