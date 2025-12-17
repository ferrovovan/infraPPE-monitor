#!/usr/bin/env python3
import pathlib

# Старый и новый текст лицензии
old_license = """# SPDX-License-Identifier: GPL-3.0-only"""
new_license = """# SPDX-License-Identifier: AGPL-3.0-only"""

# Корневая папка проекта
root = pathlib.Path("source")

# Идём рекурсивно по всем *.py
for path in root.rglob("*.py"):
    if path.name == "__init__.py":
        continue  # пропускаем пустые __init__.py
    content = path.read_text(encoding="utf-8")
    # Если файл начинается со старой лицензии — заменяем
    if content.startswith(old_license):
        new_content = new_license + content[len(old_license):]
        path.write_text(new_content, encoding="utf-8")
        print(f"Updated license: {path}")
