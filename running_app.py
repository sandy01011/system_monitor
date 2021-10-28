import psutil
import pandas as pd
import time
import numpy as np
import multiprocessing


def get_running_apps():
    df = pd.DataFrame(columns=['pid', 'name', 'username', 'status', 'cpu_percent'])

    # this is t0 (start of interval)
    for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'cpu_percent']):
        pass

    # interval time waiting
    #for i in range(interval):
    #    print("#" * (interval - i))
    #    time.sleep(1)

    # measure a second time, now save the results
    for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'cpu_percent']):
        df = df.append(proc.info, ignore_index=True)
    
    # divide by the number of cpu's
    df.cpu_percent = df.cpu_percent/multiprocessing.cpu_count()

    df = df.sort_values(['cpu_percent'], ascending=False)
    df = df.head(5)
    df.index = np.arange(1,len(df)+1)
    #Converting the dataframe to dictionary
    df = df.to_dict()
    return df


#if __name__ == "__main__":
    #df = get_running_aps()
    #print(df.head())
