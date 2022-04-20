arr_dim1s = {
	'sml': 10,
	'med': 400
	'lrg': 1000
}

arr_dim2s = {
	'sml': 5
        'med': 200
        'lrg': 500
}

arr_dim3s = {
	'sml': 8,
        'med': 300
        'lrg': 750
}


# number of input and output buckets
def buckets_count():
	return (0,0)

def generate_input(data_dir, size, input_buckets, output_buckets, upload_func):
	return { 'arr_dim1': arr_dim1s[size], 'arr_dim2': arr_dim2s[size], 'arr_dim3': arr_dim3s[size], 'num_loops': 50 }

