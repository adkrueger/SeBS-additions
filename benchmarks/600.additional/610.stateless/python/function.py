import datetime
import numpy as np



def handler(event):
	arr_dim1 = event.get('arr_dim1')
	arr_dim2 = event.get('arr_dim2')
	arr_dim3 = event.get('arr_dim3')
	num_loops = event.get('num_loops')
	rand_arr1 = np.random.rand(arr_dim1, arr_dim2)
	rand_arr2 = np.random.rand(arr_dim2, arr_dim3)

	processing_begin = datetime.datetime.now()
	# perform a bunch of random processing, but no need to really keep track of the results
	for i in range(num_loops):
		np.random.shuffle(rand_arr1)
		np.random.shuffle(rand_arr2)
		temp = rand_arr1.dot(rand_arr2)
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

