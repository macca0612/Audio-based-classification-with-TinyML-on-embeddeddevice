# Progetto di Tesi su:
# Classificazione su base audio del traffico con algoritmi di TinyML su dispositivi embedded
# Autore: Francesco Maccantelli
# Data: 20/05/2022
# Università degli Studi di Siena
# Software per creazione TrainingSet - Main Analisi


from ast import operator
from select import select
from socket import timeout
from cv2 import threshold
import count_car_yolo_02                         #script to analyze video and get traffic_index
from matplotlib import pyplot as plt    #lilbrary to plot
import os       #library for scroll to all file
import torch    #library for YOLO
import time     #library for time
import shutil   #limbrary for copy/paste
import serial
import cv2
from tqdm import tqdm
import numpy as np
from scipy import interpolate
import tkinter as tk
from tkinter import filedialog



def draw_black_box(path_video):
    video = cv2.VideoCapture(path_video)
    _ , frame = video.read()

    width  = video.get(3)  # float `width`
    height = video.get(4)  # float `height`

    list_position_past = []
    list_list = []    

    def draw(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("set")
            cv2.circle(frame,(x,y),5,(0,255,0),-1)

            if x < 10:
                x=0
            if y < 10:
                y=0
            if x > (width-10):
                x = int(width)
            if y > (height-10):
                y = int(height)

            list_position_past.append([x,y])
            if (len(list_position_past) == 4):
                list_list.append(list_position_past)
                print(list_position_past)
                list_position_past.clear()
                
            

    cv2.namedWindow(winname= "Title of Popup Window")
    cv2.setMouseCallback("Title of Popup Window", draw)

    while True:
        cv2.imshow("Title of Popup Window", frame)
        if cv2.waitKey(10) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


# function to analyze video and save t_i on file (generated automaticaly by year-month-day-hour-minutes-seconds)

def video_analyze(path_to_analyze):

    print("Folder: ",path_to_analyze)
    video_folder = path_to_analyze + "/video"
    audio_folder = path_to_analyze + "/audio"

    #import YOLO model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom

    my_data_prefix = time.strftime("%Y%m%d_%H%M%S")

    saving_path = path_to_analyze+"/save_"+my_data_prefix+".txt"

    saving = open(saving_path,"a")

    list_t_i = []

    #scroll to all video file
    for file in tqdm(os.listdir(video_folder)):
        path_2_video = video_folder+"/"+file
                                              #path_video #yolo #show#cover#print_found

        t_i = count_car_yolo_02.count_veichle(path_2_video,model,False,True,False)

        if t_i == None:
            continue

        list_t_i.append(t_i)

        saving.write(file + " " + str(t_i) + "\n")
        saving.flush()
    
    saving.close()


def video_test(path_to_analyze):

    video_folder = path_to_analyze + "/video"

    #import YOLO model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom
  

    #scroll to all video file
    for file in tqdm(os.listdir(video_folder)):
        path_2_video = video_folder+"/"+file
                                              #path_video #yolo #show#cover#print_found
        t_i = count_car_yolo_02.count_veichle(path_2_video,model,True,True,False)


# Function to print graph from save file   

def print_graph_from_file(path_file):

    list_file_name = []
    list_t_i = []
    
    with open(path_file) as file:
        lines = file.readlines()

    
    for line in tqdm(lines):
        list_file_name.append(line[:19])
        t_i = float(line[20:][:-1])
        #t_i = float(line[11:][:-1])
        list_t_i.append(t_i)
        
        
    x=range(len(list_t_i))

    plt.plot(x,list_t_i,color='green', linestyle='solid', linewidth = 1,
         marker='o', markerfacecolor='blue', markersize=3)
    plt.legend( [ 'Traffic_index' ] )
    plt.show()


# Function to export list_file_name and list_t_i

def Get_list_name_t_i_fromFile(path_save_file):

    list_file_name = []
    list_t_i = []

    with open(path_save_file) as file:
        lines = file.readlines()

    for line in lines:
        list_file_name.append(line[:19])
        t_i = float(line[20:][:-1])
        list_t_i.append(t_i)
    
    return list_file_name , list_t_i

def Get_list_name_t_i_class_fromFile(path_save_File):

    list_name = []
    list_t_i = []
    list_class = []

    with open(path_save_File) as file:
        lines = file.readlines()
    
    for line in lines:
        list_name.append(line[:19])
        list_t_i.append(line[20:-2])
        list_class.append(line[-2:][:1])

    # print ("name" + str(list_name))
    # print ("t_i" + str(list_t_i))
    # print ("class" + str(list_class))

    return list_name, list_t_i, list_class


# Function to export audio file based on thresholds [assente,presente,intenso]


def export_audio_file(path_save_file,thresholds):

    try:
        th_presente = thresholds[0]
        print("Th LOW = ",th_presente)
        th_intenso = thresholds[1]
        print("Th HIGH = ",th_intenso)
    except:
        print("ERROR! - threshold list not set propriely, must be a 2 dimension list with numbers e.g. [125.5,500]")
        quit()

    base_path_audio = path_save_file[:-24]+"audio"
    base_path_export = path_save_file[:-24]+"export"

    export_audio_log = base_path_export + "/export_audio_log.txt"
    audio_log = open(export_audio_log,"a")

    list_file_name , list_t_i = Get_list_name_t_i_fromFile(path_save_file)

    for i in tqdm(range(len(list_file_name))):
        t_i_selected = list_t_i[i]
        name_selected = list_file_name[i]

        if t_i_selected < th_presente:
            prefix = "ASSENTE."
        elif t_i_selected < th_intenso:
            prefix = "PRESENTE."
        else:
            prefix = "INTENSO."

        audio_log.write(str(name_selected) + " " + str(t_i_selected) + " " + str(prefix[0])+ "\n")
        #audio_log.flush()

        path_selected =  base_path_audio + "/" + name_selected[:-4] + ".json"
        path_destination = base_path_export + "/" + prefix + str(t_i_selected) + "." + name_selected[:-4] + ".json"

        try:
            # INFO:
            # if shutil.copyfile is slow is possible to use os.rename, but all audio file must be copied in export folder
            # os.rename(path_selected, path_destination)
            shutil.copyfile(path_selected, path_destination)
        except:
            print("ERRORE ! - file: ",path_selected," NON TROVATO")

    audio_log.close()


def check_export(path_export_file):

    base_folder = path_export_file[:-27]
    list_name, list_t_i, list_class = Get_list_name_t_i_class_fromFile(path_export_file)
    
    edit = 0

    selection = str(input("Select target to analyze I: Intenso, P: Presente, A: Assente: "))
    if selection not in ["A","P","I"] :
        print("Selezione non valida")
        return None

    video_folder = base_folder + "/video"

    for i in range(len(list_name)):
        # print(list_class[i])
        if list_class[i] == selection:
            Play_video(video_folder+"/"+str(list_name[i]))
        else:
            continue
        
        val = input("The video is " + selection + " ? : [y/n/] :")
       
        if val == "y":
            continue
        else:
            print("here")
            exit_value = True
            while (exit_value):
                edit = 1
                new_class = input("Select classification [I,P,A]: ")
                if new_class in ["I","P","A"]:
                    print("The new selected class is: ",new_class)
                    list_class[i] = new_class
                    exit_value = False
                else:
                    print("ERROR - Selected type not valid")
                    
        # Check if there was a change from original file
    if edit == 1:
        
        print("SAVING new export file")
        
        # make backup
        path_export_file_backup = path_export_file[:-4] + "_backup.txt"
        shutil.copyfile(path_export_file, path_export_file_backup)
        
        audio_log = open(path_export_file,"w")
        
        for entry_index in range(len(list_name)):
            audio_log.write(str(list_name[entry_index]) + " " + str(list_t_i[entry_index]) + " " + str(list_class[entry_index])+ "\n")
            
def change_validation(path_export_file):
    
    list_name, list_t_i, list_class = Get_list_name_t_i_class_fromFile(path_export_file)
    # print(list_name)
    folder_export = path_export_file[:-21]
    # print(folder_export)
    
    for filename in tqdm(os.listdir(folder_export)):
        # print("ultime 4:",filename[-4:])
        if filename[-4:] != "json":
            continue
        name_file = filename[-20:]
        name_file = name_file[:-5]
        name_file = name_file + ".avi"
        # print(name_file)
        index = list_name.index(name_file)
        if list_class[index] == "I":
            prefix = "INTENSO."
        elif list_class[index] == "A":
            prefix = "ASSTENTE."
        elif list_class[index] == "P":
            prefix = "PRESENTE."
        
        os.rename(folder_export+"/"+filename,folder_export+"/"+prefix+name_file[:-4]+".json")
        
    print("ALL FILES ARE DONE!")
    

def VideoTesting(webcam_number,serial_port,video_path,fps,record_time):
    """
    This function allow to test the system by a live capture of video with live prediction from Arduino
    """
    webcam = cv2.VideoCapture(webcam_number,cv2.CAP_DSHOW)
    input_serial = serial.Serial(serial_port,115200,timeout=None)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    video_out = cv2.VideoWriter(video_path,fourcc,fps,(640,480))

    start_time = time.time()
    print("Starting recording...")

    read_serial_1 = str("1")
    read_serial_2 = str("2")
    read_serial_3 = str("3")
    read_serial_4 = str("4")
    color_assente = (255,255,255)
    color_presente = (255,255,255)
    color_intenso = (255,255,255)
    number_classification = 0
    list_past_classification = ["Prestene","Intenso","Assente"]

    while(True):
        # reads frames from a camera
        # ret checks return at each frame
        ret, frame = webcam.read()
        
        # output the frame
        
        pause_time_start = time.time()

        
        if(input_serial.inWaiting()>1):
            number_classification = number_classification +1       
            read_serial_1 = str(input_serial.readline())[2:-3]
            read_serial_2 = str(input_serial.readline())[6:-3]
            value_assente = float(read_serial_2[9:])
            if value_assente > 0.5:
                color_assente = (0,255,0)
                list_past_classification.append("Assente")
            else:
                color_assente = (255,0,0)
            
            read_serial_3 = str(input_serial.readline())[6:-3]
            value_intenso = float(read_serial_3[9:])
            if value_intenso > 0.5:
                color_intenso = (0,255,0)
                list_past_classification.append("Intenso")
            else:
                color_intenso = (255,0,0)
           
            read_serial_4 = str(input_serial.readline())[6:-3]
            value_presente = float(read_serial_4[9:])
            if value_presente > 0.5:
                color_presente = (0,255,0)
                list_past_classification.append("Presente")
            else:
                color_presente = (255,0,0)
            
            input_serial.reset_input_buffer()
        
        """ read_serial_1 = str("1")
        read_serial_2 = str("2")
        read_serial_3 = str("3")
        read_serial_4 = str("4") """

        cv2.putText(frame,read_serial_1,(30,300), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,0), 1)
        cv2.putText(frame,read_serial_2,(30,350), cv2.FONT_HERSHEY_PLAIN, 2, color_assente, 2)
        cv2.putText(frame,read_serial_3,(30,400), cv2.FONT_HERSHEY_PLAIN, 2, color_intenso, 2)
        cv2.putText(frame,read_serial_4,(30,450), cv2.FONT_HERSHEY_PLAIN, 2, color_presente, 2)
        cv2.putText(frame,list_past_classification,(30,470), cv2.FONT_HERSHEY_PLAIN, 2, color_presente, 2)
        cv2.putText(frame,"# class:"+str(number_classification),(475,450), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1)

        video_out.write(frame)
        cv2.imshow('webcam', frame)
        if cv2.waitKey(1) == ord('q'):
                break

        #print(read_serial_1,read_serial_2,read_serial_3,read_serial_4)

    webcam.release()
    video_out.release()
    cv2.destroyAllWindows()

# Open selected file based x progression

def open_video_file(path_save_file):

    while True:
        try:
            select = int(input("Select index for video: "))
        except:
            print("Index must be a number")
            continue

        if select == "q" :
            break

        list_file_name, _ = Get_list_name_t_i_fromFile(path_save_file)
        path_folder = path_save_file[:-25]
        # print("Path folder > ",path_folder)
        video_folder = path_folder + "/video"
        # print("Video folder > ",video_folder)
        try:
            video_path = video_folder + "/" +list_file_name[select]
        except:
            print("Index not correct")
            continue
        print("Video path > ",video_path)
        # Create a VideoCapture object and read from input file
        try:
            cap = cv2.VideoCapture(video_path)
        except:
            print("File not found")
            continue
        
        # Check if camera opened successfully
        if (cap.isOpened()== False): 
            print("Error opening video  file")
        
        # Read until video is completed
        while(cap.isOpened()):
            
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
            
                # Display the resulting frame
                cv2.imshow('Frame', frame)
            
                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            
            # Break the loop
            else: 
                break
    
        # When everything done, release 
        # the video capture object
        cap.release()
        
        # Closes all the frames
        cv2.destroyAllWindows()


def Play_video(video_path):
    try:
        Video_stream = cv2.VideoCapture(video_path)
    except:
        print("File not found")
        return None
        
        
    # Check if camera opened successfully
    if (Video_stream.isOpened()== False): 
        print("Error opening video  file")
    
    # Read until video is completed
    while(Video_stream.isOpened()):
        
        # Capture frame-by-frame
        ret, frame = Video_stream.read()
        if ret == True:
        
            # Display the resulting frame
            cv2.imshow('Frame', frame)
        
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        
        # Break the loop
        else: 
            break

    # When everything done, release 
    # the video capture object
    Video_stream.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()




#export_audio_file("G:/Il mio Drive/AA TESI/win_code/analisi/analisi_test/save_20220620_214706.txt",[690,700])
#print_graph_from_file("G:/Il mio Drive/AA TESI/win_code/analisi/analisi_test/save_20220620_214706.txt")
#video_analyze()

def main():
    print("""   _____        __ _                                                 _           _     
  / ____|      / _| |                              /\               | |         (_)    
 | (___   ___ | |_| |___      ____ _ _ __ ___     /  \   _ __   __ _| |_   _ ___ _ ___ 
  \___ \ / _ \|  _| __\ \ /\ / / _` | '__/ _ \   / /\ \ | '_ \ / _` | | | | / __| |/ __|
  ____) | (_) | | | |_ \ V  V / (_| | | |  __/  / ____ \| | | | (_| | | |_| \__ | |\__ /
 |_____/ \___/|_|  \__| \_/\_/ \__,_|_|  \___| /_/    \_\_| |_|\__,_|_|\__, |___/_|___/
                                                                        __/ |          
                                                                       |___/           """)
    print("for thesis :")
    print("Classificazione su base audio del traffico con algoritmi di TinyML su dispositivi embedded")
    print("by:")
    print("Francesco Maccantelli")
    print("Università degli Studi di Siena - 20/05/2022")

    while True:

        print("############################################")
        print("Select function:\n1) Video analysys:\n[path_folder_to_analyze] (Attention! in this folder must be almost 3 folders audio,video,export)")
        print("2) Print grph from save file\n[path_save_file]\n3) Export audio file based on threshold\n[path_save_file,list_threshold] (Attention! list threshold must be 2 dimension list with numbers, like [50,500])")
        print("4) Draw black box")
        print("5) Video Testing prediction with webcam")
        print("6) Video test YOLO")
        print("7) Play video")
        print("8) check export")
        print("9) change validation export")
        print("10) Exit")
        selection = input("\n------------------------------------------\nSelect function [1,2,3,4,5,6,7,8,9,10] :")

        if selection == "1":
            print("## Video analysys ##")
            
            print("Selecet folder to analyze")

            root = tk.Tk()
            root.withdraw()

            path_to_analyze = filedialog.askdirectory()

            #JUST FOR TESTING PURPUSE
            if path_to_analyze == "test":
                path_to_analyze = "G:/Il mio Drive/AA TESI/win_code/analisi/analisi_test"

            video_analyze(path_to_analyze)
        elif selection == "2":
            print("## Print grph from save file ##")

            root = tk.Tk()
            root.withdraw()
            print("Select Save File")
            path_save_file = filedialog.askopenfilename()


            print_graph_from_file(path_save_file)
        elif selection == "3":
            print("## Export audio file based on threshold ##")

            root = tk.Tk()
            root.withdraw()
            print("Select Save File")
            path_save_file = filedialog.askopenfilename()

            threshold = []
            first_threshold = input("Insert FRST threshold :")
            threshold.append(float(first_threshold))
            second_threshold = input("Insert SECOND threshold :")
            threshold.append(float(second_threshold))
            export_audio_file(path_save_file,threshold)
        elif selection == "4":
            print("Select video for reference")
            root = tk.Tk()
            root.withdraw()
            path_video = filedialog.askopenfilename()
            draw_black_box(path_video)

        elif selection =="5":
            webcam_number = 1
            serial_port = "COM3"
            
            
            print("Select FOLDER where save video - ! Must be set serial-port and webcam_number (main_analisi.py) params before")
            root = tk.Tk()
            root.withdraw()

            video_path = filedialog.askdirectory()
            video_path = video_path + "/video_analysis_" + time.strftime("%Y%m%d_%H%M%S") + ".avi"
            fps = 30.0
            record_time = 15
            VideoTesting(webcam_number,serial_port,video_path,fps,record_time)

        elif selection == "6":
            print("## Video test ##")
            
            print("Selecet folder to analyze")

            root = tk.Tk()
            root.withdraw()

            path_to_analyze = filedialog.askdirectory()

            video_test(path_to_analyze)

        elif selection == "7":
            print("Selecte save file")
            root = tk.Tk()
            root.withdraw()
            path_save_file = filedialog.askopenfilename()
            print("press Q to exit")
            open_video_file(path_save_file)

        elif selection == "8":
            print("Selecte export file")
            root = tk.Tk()
            root.withdraw()
            path_export_file = filedialog.askopenfilename()
            check_export(path_export_file)
        
        elif selection == "9":
            print("Selecte export file")
            root = tk.Tk()
            root.withdraw()
            path_export_file = filedialog.askopenfilename()
            change_validation(path_export_file)

        elif selection == "9" or "q" or "Q" or "quit" or "QUIT":
            # print("Sono dentro qua!")
            print("Quitting...")
            quit()
        else:
            print("ERROR! - selection not valid")

if __name__ == "__main__":
    main()