#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import requests
import cloudscraper
import time
from lxml import etree
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

# internet options
use_cloudscraper = False
use_mirror = True
pref = "mirror." if use_mirror else ""
headers = {'User-Agent': 'Mozilla/5.0'}
cookies_json_path = "cookies.json"
cookies = None              # if None, read from cookies_json_path
fetch_period = 10.0         # least interval time between two fetches in seconds
fetch_wait_heartbeat = 1    # heartbeat of interval time between two fetches in seconds
source_XPath = "/html/body/div[6]/div[5]/div/div[3]/pre"
source_selector = "#program-source-text"


# codeforces options
user_name = "tourist"
default_rating = 1500
count_limit = 1
only_cpp = True
only_AC = True



last_fetch_time = 0

if cookies is None:
    if not os.path.isfile(cookies_json_path):
        print(f"cookies json file {cookies_json_path} not found!")
        exit()

    with open("cookies.json", "r") as f:
        cookies = json.loads(f.read())
        print("cookies read successfully")
    
def fetch(url, **kwargs) -> str:
    if 'headers' not in kwargs:
        kwargs['headers'] = headers
    if 'cookies' not in kwargs:
        kwargs['cookies'] = cookies
    while time.time() - last_fetch_time < fetch_period:
        time.sleep(fetch_wait_heartbeat)
    if use_cloudscraper:
        return scraper.get(url, **kwargs).text
    else:
        s = requests.Session() 
        return s.get(url, **kwargs).text

def fetch_source(contest_id: int, submission_id: int) -> str:
    submission_url = f"https://{pref}codeforces.com/contest/{contest_id}/submission/{submission_id}"
    html_str = fetch(url= submission_url)
    html = BeautifulSoup(html_str, 'html.parser')
    data = html.select(source_selector)
    return str(data[0].text)
    # print(html_str)
    # html = etree.HTML(html_str)
    # print(html)
    # html_data = html.xpath(source_XPath)
    # ret = ""
    # for i in html_data:
    #     # print(i.text)
    #     ret += i.text
    # return ret
    

def fetch_status(user_name: str, count: int = -1) -> str:
    count_suf = "" if count_limit == -1 else f"&count={count_limit}"
    req_url = f"https://{pref}codeforces.com/api/user.status?handle={user_name}{count_suf}"
    return fetch(req_url)
    

if os.path.isfile(user_name):
    s = input("File {} already exists, remove it now? (y/n) ".format(user_name))
    if s[0].lower() == 'y':
        os.remove(user_name)
    else:
        exit()
        
if os.path.isdir(user_name):
    s = input("Folder {} already exists, remove it now? (y/n) ".format(user_name))
    if s[0].lower() == 'y':
        for root, dirs, files in os.walk(user_name, topdown = False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(user_name)
    else:
        exit()
        
os.mkdir(user_name)


context = json.loads(fetch_status(user_name, count_limit))
if context['status'] != "OK":
    print(f"API error, comment: {context['comment']}")
    exit()
for s in context['result']:
    if only_AC and s['verdict'] != 'OK':
        continue
    p = s['problem']
    if 'contestId' not in p:
        continue
    lang = s['programmingLanguage']
    if only_cpp and not '++' in lang:
        continue
    submission_id = s['id']
    contest_id = p['contestId']
    index = p['index']
    problem_id = str(contest_id) + index
    problem_name = p['name']
    problem_rating = p['rating'] if 'rating' in p else default_rating
    with open("./{}/{}+{}+{}+{}+{}"
                .format(user_name,
                        problem_name,
                        problem_id,
                        problem_rating,
                        user_name,
                        submission_id),"w") as f:
        f.write(fetch_source(contest_id, submission_id))
        