#!/usr/bin/env python3

import os
import subprocess
from csv import reader
from multiprocessing.pool import ThreadPool as Pool

pool_size = 20
base_path = "https://mini-org.netlify.app"
showcase_path = "https://build-779aae1b-53d4-4368-9d4a-b676393eec63.gtsb.io"
docs_path = "https://build-ac6abc5b-6906-4339-b14b-d8e8a8c41fb7.gtsb.io/"
path_to_verify_at = base_path
total_count = 0
broken_count = 0

org_paths = 'org_paths_short.txt'
broken_links = open("broken_links.txt", "w", newline="")
curl_redirect_results = open("curl_redirect_results.txt", "w", newline="")


def worker(line):
    global total_count
    global broken_count
    global path_to_verify_at
    path = line.strip()
    path_to_verify_at = base_path
    if "starters" in path:
        path_to_verify_at = showcase_path
    elif "showcase" in path:
        path_to_verify_at = showcase_path
    elif "docs" in path:
        path_to_verify_at = docs_path
    elif "contributing" in path:
        path_to_verify_at = docs_path
    elif "tutorial" in path:
        path_to_verify_at = docs_path
    print(path_to_verify_at)
    try:
        status_code = subprocess.check_output(
            f'curl -L -s -o /dev/null -w "%{{http_code}}" {path_to_verify_at}{path}', shell=True, universal_newlines=True).strip()
    except:
        print(f'Something failed curling the path: {path}')

    if (status_code == "404"):
        print(f'{status_code} response for {path}')
        broken_links.write(base_path + path + "\n")
        broken_count += 1
    else:
        print(f'{status_code} response for {path}')

    curl_redirect_results.write(
        f'{status_code} response for {path}' + "\n")


pool = Pool(pool_size)


def threaded_processing():
    global total_count
    global broken_count
    with open(org_paths) as fp:
        line = fp.readline()
        while line:
            pool.apply_async(worker(line))
            # proceed to next line/path
            line = fp.readline()
            total_count += 1
    print("----------------------------------")
    print(
        f'{100 * round(float(total_count - broken_count)/float(total_count), 2)}% of pages migrated successfully! 404 results hit on {broken_count} paths.')


threaded_processing()
pool.close()
pool.join()
