#!/bin/bash
python rec_video.py audio 3.5 0 15 >> report_video.txt &
python rec_audio.py audio COM8 3.5 >> report_audio.txt &
wait