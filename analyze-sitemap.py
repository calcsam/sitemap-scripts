#!/usr/bin/env python3

import sys
import os
import csv

com_pages = []
org_pages = []

# READ SITEMAPS
com_filepath = 'com-sitemap.xml'
with open(com_filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        # print("Line {}: {}".format(cnt, line.strip()))
        com_pages.append(line.strip())
        line = fp.readline()
        cnt += 1

org_filepath = 'org-sitemap.xml'
with open(org_filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        # print("Line {}: {}".format(cnt, line.strip()))
        org_pages.append(line.strip())
        line = fp.readline()
        cnt += 1


# REMOVE XML
def remove_tags(pages, text_to_split="<loc>"):
    pages = pages[2:-1]
    parsed_pages = []
    for page in pages:
        path = page.split(text_to_split)[1].split("</loc>")[0]
        path = path.lower()
        if path[-1] != "/":
            path = path + "/"
        parsed_pages.append(path)
    return parsed_pages


com_pages = remove_tags(com_pages, ".com")
org_pages = remove_tags(org_pages, ".org")

# SORT ALPHABETICALLY
com_pages.sort()
org_pages.sort()

# WRITE TO FILES
com_paths = open("com_paths.txt", "w", newline="")
for page in com_pages:
    com_paths.write(page + "\n")
com_paths.close()

org_paths = open("org_paths.txt", "w", newline="\n")
for page in org_pages:
    org_paths.write(page + "\n")
org_paths.close()

# FIND PATHS FROM ORG THAT ARE ALREADY ON COM
# https://www.kite.com/python/answers/how-to-find-the-intersection-of-two-lists-in-python
intersection_set = set.intersection(set(org_pages), set(com_pages))
intersection_list = list(intersection_set)
intersection_list.sort()
org_paths_on_com = open("org_paths_on_com.txt", "w", newline="\n")
for page in intersection_list:
    org_paths_on_com.write(page + "\n")

# FIND PATHS FROM ORG THAT ARE NOT ON COM
# https://stackoverflow.com/questions/3462143/get-difference-between-two-lists
org_paths_not_on_com = open("org_paths_not_on_com.txt", "w", newline="\n")
for org_page in org_pages:
    if org_page not in com_pages:
        org_paths_not_on_com.write(org_page + "\n")
