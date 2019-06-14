import os
import shlex
import subprocess as sp
import logging
import logging.handlers
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

numThreads = cpu_count()
pathstr = r"C:\Users\Vedant\Desktop\Python\Music"
codec = "m4a"
input_file_type = "mp3"
fileCount = 0
fileList = []

for filename in os.listdir(path=pathstr):
    if filename.endswith(".{}".format(input_file_type)):
        filename = '"'+filename+'"'
        fileList.append(filename)
        fileCount += 1
    else:
        logging.warning("File found that is not of type: .{}\n".format(input_file_type))
        continue


def ffmpegConvert(fileName):
    output_file_name = fileName.replace(".{}".format(input_file_type), "")
    try:
        output = sp.check_output(
            shlex.split("ffmpeg -y -loglevel error -i {0} output_{1}.{2}".format(fileName, output_file_name, codec)),
            stderr=sp.STDOUT, shell=True)
    except sp.CalledProcessError as e:
        logging.error("Error detected while processing ffmpeg. \n"
                      "Filename: {} \n"
                      "Return Code: {} \n"
                      "Error Message: {} \n".format(fileName, e.returncode, e.output))
        os.remove(r"{}\output_{}.{}".format(pathstr, output_file_name, codec))


def Main():
    pool = ProcessPoolExecutor(numThreads)
    result = pool.map(ffmpegConvert, fileList)


if __name__ == '__main__':
    Main()
