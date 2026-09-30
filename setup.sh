#!/bin/bash
# Installation de l'atelier minuteaero dans /home/claude
set -e
cd /home/claude
pip install --break-system-packages -q bpy kokoro-onnx soundfile pycairo scipy pillow numpy 2>&1 | grep -v WARNING || true
mkdir -p tts qa tn mc/v r3d fg
[ -f tts/kokoro.onnx ] || curl -sSL -o tts/kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -f tts/voices.bin ] || curl -sSL -o tts/voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
# Modèles 3D : ne cloner que ceux dont on a besoin -> bash setup.sh Concorde A-10 ...
cd fg
for r in "$@"; do [ -d "$r" ] || GIT_TERMINAL_PROMPT=0 git clone -q --depth 1 https://github.com/FGMEMBERS/$r; done
echo "setup ok"
