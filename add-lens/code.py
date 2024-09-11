import os

path = "./krk"
outf = open("len.txt", "w")
with open("list.txt", "r") as file:
    line = file.readline()
    while line:
        s = "+" + line + "+"
        s = s.replace("\n", "")
        # print(s)
        cnt = 0
        lenl = 0
        for filewalks in os.walk(path):
            for files in filewalks[2]:
                if s in files:
                    cnt += 1
                    stats = os.stat(os.path.join(filewalks[0], files))
                    lenl = stats.st_size
                    # print(s, " is in", os.path.join(filewalks[0], files))
        if cnt == 1:
            outf.writelines(str(lenl) + "\n")
        else:
            outf.writelines("Error\n")
        line = file.readline()
outf.close()
