#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import shutil

json_file = "splitcores.json"

rbf_files = []

rbf_location = "/media/fat"

# fid all rbf files
print("Scanning {} for core files ...".format(rbf_location))
for root,d_names,f_names in os.walk(rbf_location):
    for filename in f_names:
        if ".rbf" in filename:
            rbf_files.append(os.path.join(root, filename))

def copy_core(src,dest):
    shutil.copy(src,dest)

def get_datestamp(name):
    name = name.split("/")[-1]
    if "_" in name:
        return name.split("_")[1].replace(".rbf","")
    else:
        return ""


def match_core(core):
    matches = []
    for syscore in rbf_files:
        filename = syscore.split("/")[-1]
        corename = filename.replace(".rbf","")
        if "_" in filename:
            corename = filename.split("_")[0]
            datestamp = filename.split("_")[1]
        if corename == core:
            matches.append(syscore)
    return matches


if os.path.exists(json_file):
    with open(json_file) as splitcore_json:
        cores = json.load(splitcore_json)
        for core in cores:
            print("Cleaning up old fores for {}.".format(core))
            for copy in cores[core]:
                matches = match_core(copy)
                for match in matches:
                    print("Removing old core {}.".format(match))
                    os.remove(match)
            print("Done.")
            matches = match_core(core)
            print("Splitting cores ...")
            for match in matches:
                for newcore in cores[core]:
                    rbf_path = os.path.dirname(match)
                    new_rbf_name = "{}_{}.rbf".format(newcore,get_datestamp(match))
                    new_rbf = os.path.join(rbf_path,new_rbf_name)
                    try:
                        print("copying {} to new {}".format(match,new_rbf))
                        copy_core(match, new_rbf)
                    except Exception as e:
                        print(repr(e))
