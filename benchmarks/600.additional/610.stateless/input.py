arr_dim1s = {
	'test': 10,
	'small': 400,
	'large': 1000
}

arr_dim2s = {
	'test': 5,
        'small': 200,
        'large': 500
}

arr_dim3s = {
	'test': 8,
        'small': 300,
        'large': 750
}


# number of input and output buckets
def buckets_count():
	return (0,0)

def generate_input(data_dir, size, input_buckets, output_buckets, upload_func):
	return { 'arr_dim1': arr_dim1s[size], 'arr_dim2': arr_dim2s[size], 'arr_dim3': arr_dim3s[size], 'num_loops': 50 }

