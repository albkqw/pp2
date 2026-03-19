import shutil
import os

# копия файла
shutil.copy("data.txt", "data_copy.txt")
print("file copied")

# бэкап
shutil.copy("data.txt", "backup_data.txt")
print("backup created")

# удаление
file_to_delete = "data_copy.txt"

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print("file deleted safely")
else:
    print("file not found")