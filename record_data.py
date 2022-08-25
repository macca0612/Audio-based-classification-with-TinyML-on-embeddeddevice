# Progetto di Tesi su:
# Classificazione su base audio del traffico con algoritmi di TinyML su dispositivi embedded
# Autore: Francesco Maccantelli
# Data: 20/05/2022
# Università degli Studi di Siena
# Software per creazione TrainingSet - Main


import time
import sys
import os
import subprocess


def make_bash_file(time_stamp,serial_port_name,sample_length,sec_video,webcam_number,fps):
    
    file = open("run_all.sh","w")

    file.write("#!/bin/bash\n")
    file.write("python rec_video.py " + time_stamp + " " + sec_video + " " + webcam_number + " " + fps + " >> report_video.txt &"+ "\n")
    file.write("python rec_audio.py " + time_stamp + " " + serial_port_name + " " + sample_length + " >> report_audio.txt &" + "\n")
    file.write("wait")
    

if __name__ == '__main__':
    if sys.argv[1] == "win":
        print("WINDOWS DETECTED")
        time_stamp = "audio"
        serial_port_name = "COM8"
        sample_length = "5"
        sec_video = "5"
        webcam_number = "0"
        fps = "15"
    elif sys.argv[1] == "linux":
        print("LINUX DETECTED")
        time_stamp = "video"
        serial_port_name = "/dev/ttyACM0"
        sample_length = "10"
        sec_video = "10"
        webcam_number = "0"
        fps = "15"
    
    make_bash_file(time_stamp,serial_port_name,sample_length,sec_video,webcam_number,fps)
    os.chmod('run_all.sh', 0o755)
    

    num_sample = int(input("Number of samples to save: "))

    report = open("report.txt","a")

    for i in range(num_sample):
        print("Saving sample #",i,"of ",num_sample)
        my_time = time.strftime("%Y%m%d-%H%M%S")

        make_bash_file(str(my_time),serial_port_name,sample_length,sec_video,webcam_number,fps)
        subprocess.run(["run_all.sh"], shell=True)

    
    
    