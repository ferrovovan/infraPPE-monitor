#!/bin/bash

# Рекурсивно удаляет все __pycache__ директории в source/
find source/ -type d -name "__pycache__" | while read dir; do
	echo "Удаление: $dir"
	rm -rf "$dir"
done

echo "__pycache__ директории удалены!"
