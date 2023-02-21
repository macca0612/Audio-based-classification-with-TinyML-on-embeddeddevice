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
- the rerequirements.txt is not 100% tested, there may be some compatible problem

```
pip install -r rerequirements.txt
```

## **Analys folder** example

Is present an example of analysis folder to show how create it.

> **Warning**
> The video files in this folder are censored so the prediction of yolo may be not accurate

> **Warning**
> The audio files not corrispond to the video files in this folder, are used only to show how **analysis folder** is structurated

## Record Audio-Video

The videos are generated with _rec_video.py_, and the audios with _rec_audio.py_, in order to record audio and video at the same time is used the script _run.all.sh_ on Windows system.

## Analysis

The analysis is made by executing _main_analisi.py_ and following the instrauction on the script.

### Main funciton

1. Video analysys - [Select **analysis folder**], This function analyze all videos in /selected_folder/video and produce a file **save** file save\__date_.txt, where are saved the filename and the t_i computed
2. Print grph from save file - [Select **save** file], This function allow to print a graph of the previus generated **save** file.
   - If the graph not show, close and open again _main_analisi.py_
3. Export audio file based on threshold - [Select **save** file, INSERT traffic_threshold_1, traffic_threshold_2], This function allow to export audio files based on the two threshold, for traffic_detected={"PRESENTE"}, and high_traffic={"INTENSO"}
