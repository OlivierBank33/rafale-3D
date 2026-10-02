#!/bin/bash
# Usage : bash eleven_prep.sh <dossier> <nom>  -> <nom>_bed.mp4 (vidéo + musique/bruitages, sans voix) et <nom>_guide.mp3 (voix guide calée)
D=$1; N=$2
python3 $(dirname "$0")/noise_check.py $D/music.wav $D/sfx.wav || { echo "STOP: bruit blanc détecté dans la musique/les bruitages"; exit 1; }
ffmpeg -y -loglevel error -i $D/voice.wav -i $D/music.wav -i $D/sfx.wav -filter_complex "[0:a]aresample=48000,asplit=2[vsc][vg];[1:a]aresample=48000,volume=0.32[m];[m][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[md];[2:a]aresample=48000,volume=0.6[s];[md][s]amix=inputs=2:normalize=0,loudnorm=I=-30:TP=-6,aresample=48000[bed];[vg]highpass=f=70,loudnorm=I=-16:TP=-1.5,aresample=44100[g]" -map "[bed]" -c:a pcm_s16le $D/bed.wav -map "[g]" -c:a libmp3lame -b:a 192k ${N}_guide.mp3
WM=$(dirname "$0")/brand/filigrane_video.png
ffmpeg -y -loglevel error -i $D/video_noaudio.mp4 -i $WM -i $D/bed.wav -filter_complex "[1]scale=280:-1,format=rgba,colorchannelmixer=aa=0.8[w];[0][w]overlay=36:36[v]" -map "[v]" -map 2:a -c:v libx264 -preset medium -crf 21 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart ${N}_bed.mp4
ls -la ${N}_bed.mp4 ${N}_guide.mp3
