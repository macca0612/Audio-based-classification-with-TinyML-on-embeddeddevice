Progetto di tesi triennale su:
Classificazione su base audio del traffico con algoritmi di TinyML su dispositivi embedded

di Maccantelli Francesco

Ingegneria informatica e dell'informazione
Università degli studi di Siena

---

Three-year thesis project on:
Audio-based traffic classification with TinyML algorithms on embedded devices

by Maccantelli Francesco

Computer and information engineering
University of Siena

# Before starting

Attention!

- for run on GPU must be installed pytorch for cuda see: https://pytorch.org/
- the rerequirements.txt is not 100% tested, there may be some compatibility problem

```
pip install -r rerequirements.txt
```

## **Analys folder** example

It presents an example of an analysis folder to show how to create it.

> **Warning**
> The video files in this folder are censored so the prediction of yolo may be not accurate

> **Warning**
> The audio files do not correspond to the video files in this folder, and are used only to show how the **analysis folder** is structured

## Record Audio-Video

The videos are generated with _rec_video.py_, and the audios with _rec_audio.py_, in order to record audio and video at the same time is used the script _run.all.sh_ on Windows system.

## Analysis

The analysis is made by executing main_analisi.py and following the instructions in the script.

### Main funciton

1. Video analyses - [Select **analysis folder**], This function analyze all videos in /selected_folder/video and produces a file save file save_date.txt, where are saved the filename and the t_i computed
2. Print graph from save file - [Select **save file**], This function allows printing a graph of the previously generated **save file**.
   - If the graph does not show, close and open again _main_analisi.py_
3. Export audio file based on the threshold - [Select save file, INSERT traffic_threshold_1, traffic_threshold_2], This function allow exporting audio files based on the two thresholds, for traffic_detected={"PRESENTE"}, and high_traffic={"INTENSO"}
