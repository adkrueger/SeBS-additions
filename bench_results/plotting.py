import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_metrics(file_name, show_plots=False):
    df = pd.read_csv(file_name, header=0)
    
    warm128_iters = df.loc[(df["type"]=="warm") & (df["memory"]==128)]
    warm256_iters = df.loc[(df["type"]=="warm") & (df["memory"]==256)]
    cold128_iters = df.loc[(df["type"]=="cold") & (df["memory"]==128)]
    cold256_iters = df.loc[(df["type"]=="cold") & (df["memory"]==256)]

    file_no_ext =  os.path.splitext(file_name)[0] # remove the file extension
    plot_helper(file_no_ext, warm128_iters, cold128_iters, 128, show_plots=show_plots)
    plot_helper(file_no_ext, warm256_iters, cold256_iters, 256, show_plots=show_plots)

def plot_helper(plot_title, warm_df, cold_df, mem_size, show_plots=False):
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    warm_exec_time = warm_df["exec_time"]
    cold_exec_time = cold_df["exec_time"]
    plt.boxplot([warm_exec_time, cold_exec_time])
    title = plot_title + ": Exec. Time (" + str(mem_size) + "MB)"
    plt.title(title)
    ax.set_xticklabels(["Warm", "Cold"])

    plt.savefig("plots/" + plot_title + "_execTime_" + str(mem_size))

if __name__=="__main__":
    files = []
    files += [f for f in os.listdir() if os.path.isfile(f) and f != "plotting.py"]
    for f in files:
        plot_metrics(f, False)
