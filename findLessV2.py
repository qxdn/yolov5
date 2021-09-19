import os
import argparse


def getFileList(dir: str, extract: str) -> list:
    fileList = []
    filenames = os.listdir(dir)
    for filename in filenames:
        ext = os.path.splitext(filename)[-1]
        if ext == extract:
            fileList.append(filename)
    return fileList


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--dataset", help="dataset path", type=str, default="./dataset/train"
    )
    parser.add_argument("-s", "--size", help="image size", type=int, default=640)
    parser.add_argument("-l", "--limit", help="limit of pixels", type=int, default=8)
    args = parser.parse_args()
    path = args.dataset
    size = args.size
    limit = args.limit
    fileList = getFileList(path, ".txt")
    #limit = limit * limit
    counter = 0
    labelcounter = 0
    # change dir
    os.chdir(path)
    for file in fileList:
        with open(file) as f:
            for line in f:
                labelcounter += 1
                temp = line.split(" ")
                cls = int(temp[0])
                w = float(temp[3]) * size
                h = float(temp[4]) * size
                #pixels = round(w * h)
                if (w < limit or h< limit) and cls == 2:
                    counter += 1
    print(counter)
    print(labelcounter)
    print(len(fileList))
    print(limit)
