# Progetto di Tesi su:
# Classificazione su base audio del traffico con algoritmi di TinyML su dispositivi embedded
# Autore: Francesco Maccantelli
# Data: 20/05/2022
# Università degli Studi di Siena
# Software di Calibrazione - Acquisizione dati


import cv2 
#import pandas as pd
import numpy as np
import imutils


#Definizioni pesi traffic_index per categoria
#PCU: Passenger Car Unit
weight_car = 1
weight_bus = 2
weight_motorcycle = 0.4
weight_motorbike = 0.4
weight_truck = 2
weight_bicycle = 0.2

video_resize = 400    #Resize input video



def count_veichle(video_path,model,show_bool,cover_box,print_found):
    traffic_index = 0

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Video not opened correctly")
        print("ERROR ON VIDEO: ",video_path)
        return None

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        #frame = imutils.resize(frame,640,480)
        
        #censura
        if not ret:
            #print("Can't receive frame (stream end?). Exiting ...")
            break

        #frame = imutils.resize(frame,video_resize) #Resizing input video

        h_frame, w_frame, channels = frame.shape
        if (cover_box):
            
            #contours1 = np.array( [ [0,200], [w_frame,h_frame-50], [w_frame, h_frame], [0,h_frame] ] )

            #contours2 = np.array( [ [w_frame,0], [w_frame,318], [395,245],[421, 0]  ] )

            #contours3 = np.array( [ [0,160], [411,130], [420,0],[0, 0]  ] )

            pts  = np.array([[0, 308], [503, 460], [503, 480], [0, 480]])
            pts2 = np.array([[0, 260], [465, 210], [479, 0], [0, 0]])
            pts3 = np.array([[453, 358], [477, 0], [640, 0], [640, 408]])
            
            
            
            
            

            #contours3 = np.array( [[w_frame * 0.623, h_frame * 0.508], [w_frame * 0.653, 0], [w_frame, 0], [w_frame, h_frame * 0.658]])

            cv2.fillPoly(frame, pts =[pts], color=(0,0,0))
            cv2.fillPoly(frame, pts =[pts2], color=(0,0,0))
            cv2.fillPoly(frame, pts =[pts3], color=(0,0,0))
        
        # if frame is read correctly ret is True
        if not ret:
            #print("Can't receive frame (stream end?). Exiting ...")
            break
        
        results = model(frame)

        df = results.pandas().xyxy[0]
        #print(df)
        car_found = (df.name.values == "car").sum()
        bus_found = (df.name.values == "bus").sum()
        motorcycle_found = (df.name.values == "motorcycle").sum()
        motorbike_found = (df.name.values == "motorbike").sum()
        truck_found = (df.name.values == "truck").sum()
        bicycle_found = (df.name.values == "bicycle").sum()

        traffic_index = traffic_index + (car_found * weight_car) + (bus_found * weight_bus) + (motorcycle_found * weight_motorcycle) + (truck_found * weight_truck) + (bicycle_found * weight_bicycle)

        if (print_found):
            if (car_found > 0 ):
                print("cars: ",car_found)
            if (bus_found > 0 ):
                print("bus: ",bus_found)
            if (motorcycle_found > 0 ):
                print("motorcycle: ",motorcycle_found)
            if (truck_found > 0 ):
                print("truck: ",truck_found)
            if (motorbike_found > 0 ):
                print("motorbike: ",motorbike_found)
            if (bicycle_found > 0 ):
                print("bicycle: ",bicycle_found)


        if (show_bool):
            for index, row in df.iterrows():
                x_min = int(row['xmin'])
                y_min = int(row['ymin'])
                x_max = int(row['xmax'])
                y_max = int(row['ymax'])
                name = str(row['name'])
                conf = round(row['confidence'],2)
                conf = str(conf)
                w = x_max - x_min
                h = y_max - y_min

                if (name == "car"):
                    color = [255,0,0]
                elif (name == "truck"):
                    color = [0,255,0]
                elif (name == "bus"):
                    color = [0,0,255]
                elif (name == "motorbike"):
                    color = [255,255,0] 
                elif (name == "motorcycle"):
                    color = [0,255,255] 
                elif (name == "person"):
                    color = [125,255,125]
                elif (name == "bicycle"):
                    color = [125,0,255]
                else:
                    color = [0,0,0]

                cv2.rectangle(frame,(x_min,y_min), (x_min+w, y_min+h), color, (2))
                cv2.putText(frame, name, (x_max,y_min), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2)
                cv2.putText(frame, conf, (x_max,y_max), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)
                text_t_i = "T I: " + str(traffic_index)
                cv2.putText(frame, text_t_i, (0,h_frame-30), cv2.FONT_HERSHEY_PLAIN, 3, (125,125,125), 3 )

            cv2.imshow('frame', frame)
            
            if cv2.waitKey(1) == ord('q'):
                break
               
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    return traffic_index




def main():
    import torch
    # Modello YOLO
    url = "INSERT HERE A PATH OF A TRAFFIC VIDEO FOR TESTING"
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom
    _ = count_veichle(url,model,True,True,False)
    #                           Show,Cover,Print

if __name__ == "__main__":
    main()




