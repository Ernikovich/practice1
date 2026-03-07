import shutil
import os

# copy file
shutil.copy("demofile.txt", "myfile.txt")

# delete file
if os.path.exists("backup_sample.txt"):
    os.remove("backup_sample.txt")
    print("File deleted")
else:
    print("File does not exist")