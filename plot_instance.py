
# 显示中文
from pylab import *  
mpl.rcParams['font.sans-serif'] = ['SIMSUN']

import matplotlib.pyplot as plt
import argparse
import os

names = ["person", "bike", "car", "motor", "bus", "truck"]

counter = {}
for name in names:
    counter[name] = 0


def index2name(index: int) -> str:
    return names[index]

def get_filelist(dir: str, extract: str,prefix=False) -> list:
    filelist = []
    filenames = os.listdir(dir)
    for filename in filenames:
        ext = os.path.splitext(filename)[-1]
        if ext == extract:
            if prefix:
                filename = os.path.join(dir,filename)
            filelist.append(filename)
    return filelist


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", help="dataset path", required=True, type=str)
    args = parser.parse_args()
    dataset_path = args.dataset
    if not os.path.exists(dataset_path):
        print("dataset path didn't exist")
        exit(1)
    label_list = get_filelist(dataset_path,'.txt',True)
    for file in label_list:
        with open(file) as f:
            for line in f:
                temp = line.split(" ")
                name = int(temp[0])
                counter[index2name(name)]+=1
    
    print(counter)
    labels = []
    data = []
    for k,v in counter.items():
        labels.append(k)
        data.append(v)
    
    plt.title("实例数量") 
    plt.xlabel("类别") 
    plt.ylabel("数量（个）") 
    plt.bar(range(len(data)),data,tick_label=labels)
    plt.show()
