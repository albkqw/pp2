import os

# вложенные директории
os.makedirs("test_dir/sub_dir", exist_ok=True)
print("directories created")

# список файлов и папок
items = os.listdir("test_dir")
print("contents of test_dir:", items)