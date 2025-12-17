#!/usr/bin/env bash
set -euo pipefail

# Проверка, что есть папка assets в текущей директории
if [ ! -d "assets" ]; then
    echo "Error: directory 'assets' not found in current folder."
    echo "Please run this script from the project root."
    exit 1
fi

# Имя выходного видео
OUTPUT="assets/assets_compilation.mp4"

# Создаём видео из всех JPG в папке assets
ffmpeg -framerate 1/2 -pattern_type glob -i 'assets/*.jpg' -r 24 -pix_fmt yuv420p -y "$OUTPUT"

echo "Video created successfully: $OUTPUT"

