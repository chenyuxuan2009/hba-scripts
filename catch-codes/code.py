import requests
import json
import time
import bs4
import cyaron
import math
import os
import re
import base64
from urllib.parse import unquote
import matplotlib.pyplot as plt

sleepTime = 1
defaultTimes = 5
JID = "71458BD8FE3709659E01208F93214E5F"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4331.0 Safari/537.36",
    "cookie": f"JSESSIONID={JID};",
}


def getStandings(cid, cnt):
    time.sleep(sleepTime)
    url = f"https://codeforces.com/api/contest.standings?contestId={cid}&from=1&count=100&showUnofficial=true"
    data = requests.get(url, headers=headers).text
    # print(data)
    return json.loads(data)


def getUserSubmission(cid, handle):
    time.sleep(sleepTime)
    url = f"https://codeforces.com/api/contest.status?contestId={cid}&from=1&handle={handle}"
    data = requests.get(url, headers=headers).text
    # print(data)
    return json.loads(data)


def getSubmission(cid, id):
    time.sleep(sleepTime)
    url = f"https://mirror.codeforces.com/contest/{cid}/submission/{id}"
    data = requests.get(url, headers=headers).text
    # outf = open("res.html", "w")
    # print(data)
    # outf.writelines(data)
    # outf.close()
    return data


savepath = "./result"
with open("list.txt", "r") as file:
    line = file.readline()
    while line:
        line = line.replace("\n", "")
        cid = 0
        pid = 0
        pos = -1
        cnt = defaultTimes
        if " " in line:
            p = line.find(" ")
            cnt = int(line[p + 1 :])
            line = line[0:p]
        line = line.upper()
        # print(line)
        for i in range(len(line)):
            if "A" <= line[i] <= "Z":
                pos = i
                break
        if pos == -1:
            print("[ERROR]:", line)
            line = file.readline()
            continue
        cid = int(line[0:pos])
        pid = line[pos:]
        print("[QUERY]:", cid, pid, cnt)
        standings = getStandings(cid, cnt)
        num = 0
        found = 0
        for p in standings["result"]["problems"]:
            if p["index"] == pid:
                found = 1
                break
            num += 1
        if found == 0:
            print("[ERROR]:", pid, "No such problem.")
            line = file.readline()
            continue
        outf = open(f"./result/{cid}{pid}.md", "w+")
        tot = 0
        for user in standings["result"]["rows"]:
            if len(user["party"]["members"]) > 1:
                print("[TEAM]: Team", user["party"]["teamName"])
                continue
            handle = user["party"]["members"][0]["handle"]
            submission = getUserSubmission(cid, handle)
            oksub = 0
            for sub in submission["result"]:
                if sub["problem"]["index"] != pid:
                    continue
                if sub["verdict"] != "OK":
                    continue
                if (("G++" in sub["programmingLanguage"]) == False) and (
                    ("C++" in sub["programmingLanguage"]) == False
                ):
                    continue
                id = sub["id"]
                print("[SUBMISSION]:", handle, id)
                sbm = getSubmission(cid, id)
                instr = '<pre id="program-source-text" class="prettyprint lang-cpp linenums program-source" style="padding: 0.5em;">'
                # print(instr)
                # outf.writelines(sbm)
                stpos = sbm.find(instr) + len(instr)
                edpos = stpos + sbm[stpos:].find("</pre>")
                # print(stpos, edpos)
                code = sbm[stpos:edpos]
                outf.writelines(handle)
                outf.writelines("\n\n```cpp\n")
                code = bs4.BeautifulSoup(code, "html.parser").text
                l = len(code)
                while code[l - 1] == "\n":
                    l -= 1
                outf.writelines(code[0:l])
                outf.writelines("\n```\n\n")
                tot += 1
                break
            if tot == cnt:
                break
        outf.close()
        line = file.readline()
# getSubmission(476, 9827315)
