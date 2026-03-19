import shutil
import os

os.makedirs("test_dir", exist_ok=True)

# перемещение файла
if os.path.exists("data.txt"):
    shutil.move("data.txt", "test_dir/data.txt")
    print("file moved")

# копирование обратно
if os.path.exists("test_dir/data.txt"):
    shutil.copy("test_dir/data.txt", "data_restored.txt")
    print("file copied back")