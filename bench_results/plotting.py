import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# plots the execution times of various applications
def plot_exec_time_metrics(file_name, show_plots=False):
    df = pd.read_csv(file_name, header=0)
    
    # split up our application into warm and cold and memory allocation
    warm128_iters = df.loc[(df["type"]=="warm") & (df["memory"]==128)]
    warm256_iters = df.loc[(df["type"]=="warm") & (df["memory"]==256)]
    cold128_iters = df.loc[(df["type"]=="cold") & (df["memory"]==128)]
    cold256_iters = df.loc[(df["type"]=="cold") & (df["memory"]==256)]

    file_no_ext =  os.path.splitext(file_name)[0] # remove the file extension

    # 128MB iterations
    plot_exec_time_helper(file_no_ext, warm128_iters, cold128_iters, 128, show_plots=show_plots)
    # 256NB iterations
    plot_exec_time_helper(file_no_ext, warm256_iters, cold256_iters, 256, show_plots=show_plots)
    plot_exec_time_multiple_helper(file_no_ext, warm128_iters, cold128_iters, warm256_iters, cold256_iters, show_plots=show_plots)

# helper for plotting execution times; creates box plots of cold vs. warm executions
def plot_exec_time_helper(plot_title, warm_df, cold_df, mem_size, show_plots=False):
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    
    # grab the execution time columns
    warm_exec_time = warm_df["exec_time"] / 1000000 # convert to seconds
    cold_exec_time = cold_df["exec_time"] / 1000000
    plt.boxplot([warm_exec_time, cold_exec_time])
    title = plot_title + ": Exec. Time (" + str(mem_size) + "MB)"
    plt.title(title)
    ax.set_xticklabels(["Warm", "Cold"])    # make sure the boxes are labelled properly
    plt.xlabel("Application Setting")
    plt.ylabel("End-to-End Latency (s)")

    if show_plots:
        plt.show()

    plt.savefig("plots/" + plot_title + "_execTime_" + str(mem_size))

def plot_exec_time_multiple_helper(plot_title, warm_df128, cold_df128, warm_df256, cold_df256, show_plots=False):
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    
    # grab the execution time columns
    warm128_exec_time = warm_df128["exec_time"] / 1000000 # convert to seconds
    cold128_exec_time = cold_df128["exec_time"] / 1000000
    warm256_exec_time = warm_df256["exec_time"] / 1000000
    cold256_exec_time = cold_df256["exec_time"] / 1000000
    plt.boxplot([warm128_exec_time, cold128_exec_time, warm256_exec_time, cold256_exec_time])
    title = plot_title + ": Execution Time"
    plt.title(title)
    ax.set_xticklabels(["Warm (128MB)", "Cold (128MB)", "Warm (256MB)", "Cold (256MB)"])    # make sure the boxes are labelled properly
    plt.xlabel("Application Setting")
    plt.ylabel("End-to-End Latency (s)")

    if show_plots:
        plt.show()

    plt.savefig("plots/" + plot_title + "_execTime_all")

# plots a bar chart of average memory usage across all benchmarks
def plot_mems(file_names, show_plots=False):
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)

    all_mems = []
    all_file_names = []
    # for each file, read the file, get its average memory usage, and keep track of its name
    for f in file_names:
        curr_df = pd.read_csv(f, header=0)
        # print(f"curr_df: {curr_df}")
        all_mems.append(np.mean(curr_df["mem_used"].dropna().to_numpy()))
        all_file_names.append(os.path.splitext(f)[0])
    # print(f"all mems: {all_mems}")
    # print(f"all_file_names: {all_file_names}")
    plt.bar(all_file_names, all_mems)
    plt.xlabel("Application Ran")
    plt.ylabel("Memory Usage (MB)")

    plt.title("Memory Usage Across Different Applications")
    
    if show_plots:
        plt.show()
    plt.savefig("plots/MemoryUsage")

if __name__=="__main__":
    files = []
    files += [f for f in os.listdir() if os.path.isfile(f) and f != "plotting.py"]
    for f in files:
        plot_exec_time_metrics(f, False)
    plot_mems(files)
