import shutil 
# shutil — это модуль Python для копирования, перемещения и удаления файлов и папок.
shutil.move("sample.txt", "test_dir/sample.txt") #То есть файл перемещается из текущей папки в папку test_dir.
shutil.copy("test_dir/sample.txt", "copy_sample.txt")
# move = cut + paste
# copy = copy + paste