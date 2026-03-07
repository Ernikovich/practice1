import os 

# create directory
os.mkdir("test_dir")

# create nested directories
os.makedirs("parent/child/grandchild")

# list files
print(os.listdir("."))
# listdir() — показывает список файлов и папок
# "." — означает текущую папку
# То есть команда выводит все файлы и папки в текущей директории.

# current directory
print(os.getcwd())
# getcwd() = get current working directory