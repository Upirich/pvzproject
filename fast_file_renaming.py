import os
import re


folder_path = "peashooter"
files = os.listdir(folder_path)

files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
for i in range(len(files) - 1):
    for j in range(len(files) - 1 - i):
        match1 = re.search(r"-(\d+).", files[j])
        match2 = re.search(r"-(\d+).", files[j + 1])
        digit1 = int(match1.group(1))
        digit2 = int(match2.group(1))
        if digit1 > digit2:
            files[j], files[j + 1] = files[j + 1], files[j]

for i in range(len(files)):
    new_name = f"frame-{i + 1}.gif"

    old_file = os.path.join(folder_path, files[i])
    new_file = os.path.join(folder_path, new_name)

    # ВНИМАНИЕ!!! НАДО ПРОВЕРИТЬ ПРАВИЛЬНО ЛИ ПРОИСХОДИТ ЗАМЕНА!!!
    # И ТОЛЬКО ПОТОМ ВКЛЮЧАТЬ СТРОКУ os.rename()
    # os.rename(old_file, new_file)

    print(f"Переименован: {files[i]} -> {new_name}")

print("Все файлы переименованы.")
