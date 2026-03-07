#  "w" (write mode)
with open("demofile.txt", "w") as f:
    f.write("Hello")

# Когда используем "a" (append)
with open("demofile.txt", "a") as f:
    f.write("New line\n")

# "x" - Create - will create a file, returns an error if the file exists
f = open("myfile.txt", "x")
