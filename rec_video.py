# Progetto di Tesi su:
# Classificazione su base audio del traffico con algoritmi di TinyML su dispositivi embedded
# Autore: Francesco Maccantelli
# Data: 20/05/2022
# Università degli Studi di Siena
# Software per creazione TrainingSet - Registrazione video

""" 
  _____                            _   
 |_   _|                          | |  
   | |  _ __ ___  _ __   ___  _ __| |_ 
   | | | '_ ` _ \| '_ \ / _ \| '__| __|
  _| |_| | | | | | |_) | (_) | |  | |_ 
 |_____|_| |_| |_| .__/ \___/|_|   \__|
                 | |                   
                 |_|                    """

import cv2
import time
import sys


""" 
  _____                               _                
 |  __ \                             | |               
 | |__) |_ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __ ___ 
 |  ___/ _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__/ __|
 | |  | (_| | | | (_| | | | | | |  __/ ||  __/ |  \__ /
 |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|  |___/
                                                       
 """    

fps = 15.0    # Define FPS of video Recording    
sample_length = 20      # Define numers of secods for each samples 

def record_video(time_stamp,sec,webcam_number,fps):
    
    cap = cv2.VideoCapture(webcam_number,cv2.CAP_DSHOW)

    # Define the codec and create VideoWriter object
    #fourcc = cv2.VideoWriter_fourcc(*'MP42')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    path = "video/" + time_stamp + ".avi"

    out = cv2.VideoWriter(path, fourcc, fps, (640, 480))

    # loop runs if capturing has been initialized.
    starting_time = time.time()
    print("Start video recording...")
    while((time.time()-starting_time)<sec):
        # reads frames from a camera
        # ret checks return at each frame
        ret, frame = cap.read()
        
        # output the frame
        out.write(frame)
        time.sleep(1/fps)
    
    print("STOP video recording.")
    #report=open("report.txt","w")
    #report.write("Video recording: ",time.time()-starting_time,"\n")
    print("video:",time.time()-starting_time)
    #report.close()
    # Close the window / Release webcam
    cap.release()

    # After we release our webcam, we also release the output
    out.release()

    # De-allocate any associated memory usage
    cv2.destroyAllWindows()

if __name__ == '__main__':
    #record_video(time_stamp,sec,webcam_number,fps):
    #Importing sys parameters
    par_time_stamp = sys.argv[1]
       
    if par_time_stamp == "linux":
        print("TEST MODE video !")
        par_sec = 10
        par_webcam_number = 0
        par_fps = 20.0
    elif par_time_stamp == "win":
        print("TEST MODE video !")
        par_webcam_number = 0
        par_fps = 20.0
        par_sec = 10
    else:
        par_sec = float(sys.argv[2])
        par_webcam_number = int(sys.argv[3])
        par_fps = float(sys.argv[4])

    print("webcam",par_webcam_number)

    record_video(par_time_stamp,par_sec,par_webcam_number,par_fps)