#!/bin/bash
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2025 ferrovovan

# Рекурсивно удаляет все __pycache__ директории в source/
find source/ -type d -name "__pycache__" | while read dir; do
	echo "Удаление: $dir"
	rm -rf "$dir"
done

echo "__pycache__ директории удалены!"
