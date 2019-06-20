import os
import shlex
import sys
import subprocess as sp
import logging
import logging.handlers
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
import time
from pathlib import Path

start_time = time.time()
numThreads = cpu_count()
pathstr = r"G:\Python"
# opPathStr = r"G:\Audios"
codec = "aac"
input_file_type = "mp4"
fileCount = 0
fileList = []

for filename in os.listdir(path=pathstr):
    if filename.endswith(".{}".format(input_file_type)):
        filename = '"'+filename+'"'
        fileList.append(filename)
        fileCount += 1
        if fileCount > 100:
            break
    #else:
    #    logging.warning("File found that is not of type: .{}\n".format(input_file_type))
    #    continue


def ffmpegConvert(fileName):
    file_name = fileName.replace(".{}".format(input_file_type), "")
    output_file_name = os.path.join("G:\\","Audios","Output_{}.{}".format(file_name.replace('"',''), codec))
    strcmd = "ffmpeg -y -loglevel error -i {0} {1}".format(fileName, output_file_name)
    if sys.platform.startswith("win"):
        cmd = strcmd
    elif sys.platform.startswith("linux"):
        cmd = shlex.split(strcmd)
    try:
        output = sp.check_output(cmd, stderr=sp.STDOUT, shell=True)
    except sp.CalledProcessError as e:
        logging.error("Error detected while processing ffmpeg. \n"
                      "Filename: {} \n"
                      "Return Code: {} \n"
                      "Error Message: {} \n".format(fileName, e.returncode, e.output))
        os.remove("{}".format(output_file_name))


def Main():
    pool = ProcessPoolExecutor(numThreads)
    result = pool.map(ffmpegConvert, fileList)


if __name__ == '__main__':
    Main()

#print(" \nExecution Time: {}\n".format(time.time()-start_time))