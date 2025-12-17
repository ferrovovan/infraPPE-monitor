#!/bin/bash
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2025 ferrovovan

python -m build --wheel

# Проверка, что whl работает
# pip install dist/infrappe_monitor-0.1.2-py3-none-any.whl
# python3 -c "import source.web.app as app; print(app)"
