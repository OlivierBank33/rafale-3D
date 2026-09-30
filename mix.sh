#!/bin/bash
# Usage : bash mix.sh <dossier> <sortie.mp4>   (le dossier contient voice.wav, music.wav, sfx.wav, video_noaudio.mp4)
D=$1; OUT=$2
ffmpeg -y -loglevel error -i $D/voice.wav -i $D/music.wav -i $D/sfx.wav -filter_complex "[0:a]aresample=48000,asplit=2[v][vsc];[1:a]aresample=48000,volume=0.32[m];[m][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[md];[2:a]aresample=48000,volume=0.6[s];[v]highpass=f=70,acompressor=threshold=0.2:ratio=3:attack=5:release=80[vv];[vv][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]" -map "[out]" -c:a pcm_s16le $D/mix.wav
ffmpeg -y -loglevel error -i $D/video_noaudio.mp4 -i $D/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $OUT
ls -la $OUT
