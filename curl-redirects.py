#!/usr/bin/env python3

import os
import subprocess
from multiprocessing.pool import ThreadPool as Pool

base_path = "mansion-docsredesign.gtsb.io"

total_count = 0
broken_count = 0

org_paths = 'org_paths.txt'
broken_links = open("broken_links.txt", "w", newline="")
curl_redirect_results = open("curl_redirect_results.txt", "w", newline="")


with open(org_paths) as fp:
    line = fp.readline()
    while line:
        path = line.strip()

        try:
            status_code = subprocess.check_output(
                f'curl -L -s -o /dev/null -w "%{{http_code}}" {base_path}{path}', shell=True, universal_newlines=True).strip()
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

        # proceed to next line/path
        line = fp.readline()
        total_count += 1

print("----------------------------------")
print(
    f'{100 * round(float(total_count - broken_count)/float(total_count), 2)}% of pages migrated successfully! 404 results hit on {broken_count} paths.')
