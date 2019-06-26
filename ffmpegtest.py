import os
import shlex
import sys
import subprocess as sp
import logging
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
import time

start_time = time.time()
numThreads = cpu_count()
pathstr = os.path.join("/share","workhorse2","ankit","YFCC")
# opPathStr = r"G:\Audios"
codec = "aac"
input_file_type = "mp4"
fileCount = 0
fileNum = 0
fileList = []
errorFilePath = os.path.join("/share","workhorse3","vsanil","errorLog.txt")
fileFilePath = os.path.join("/share","workhorse3","vsanil","fileLog.txt")
start = True

errorFile = open(errorFilePath,"w+")
ipFile = open(fileFilePath,"w+")

for filename in os.listdir(path=pathstr):
    if filename.endswith(".{}".format(input_file_type)):
        #filename = '"'+filename+'"'
        fileList.append(filename)
        fileCount += 1
        if fileCount > 100:
            break
    else:
        errorFile.write("Warning: File found that is not of type: .{}\n"
                        "Name of file: {}\n".format(input_file_type, filename))
        continue


def ffmpegConvert(fileName):
    #if start == True:
    #    fileNum = 0
    #    start = False
    file_name = fileName.replace(".{}".format(input_file_type), "")
    input_file_name = os.path.join("/share","workhorse2","ankit","YFCC","{}".format(fileName))
    output_file_name = os.path.join("/share","workhorse3","vsanil","audio","Output_{}.{}".format(file_name, codec))
    cmd = "ffmpeg -i {0} {1}".format(input_file_name, output_file_name)
    try:
        output = sp.check_output(cmd, stderr=sp.STDOUT, shell=True)
    except sp.CalledProcessError as e:
        errorFile.write("Error detected while processing ffmpeg. \n"
                      "Filename: {} \n"
                      "Return Code: {} \n"
                      "Error Message: {} \n".format(fileName, e.returncode, e.output))
        #os.remove("{}".format(output_file_name))
    fileNum = sp.check_output("ls {} | wc -l".format(os.path.join("/share","workhorse3","vsanil","audio")), shell=True)
    ipFile.write("\nNumber of files converted: {}".format(fileNum))


def Main():
    pool = ProcessPoolExecutor(numThreads)
    result = pool.map(ffmpegConvert, fileList)


if __name__ == '__main__':
    Main()
    print("Final Execute")

#print(" \nExecution Time: {}\n".format(time.time()-start_time))