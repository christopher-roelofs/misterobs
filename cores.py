import json
import paramiko
import shutil
import os
import config
import logger
import mister
import ssh

SETTINGS = config.get_config()

ipaddress = SETTINGS['main']['mister_ip']
username = SETTINGS['main']['mister_username']
password = SETTINGS['main']['mister_password']

map_file = "cores.json"
cores = {}


def build_system_map():
    stdout = ssh.send_command('find /media/fat -type f -name "*.rbf"')
    stdout.sort()
    cores = {}
    for line in stdout:
        line = line.split('/')[-1].strip()
        corename = line.replace(".rbf","")
        if "_" in line:
            corename = line.split("_")[0]
    
        core = {}
        core['description'] = "{} core".format(corename)
        core['scene'] = "{} Scene".format(corename)

        cores[corename] = core
    return cores

def get_cores():
    return cores

def read_file_map():
    global map_file
    if os.path.exists(map_file):
        with open(map_file) as map_json:
            maps = json.load(map_json)
            return maps
    else:
        return {}

def merge_maps():
    if os.path.exists(map_file):
        logger.info("Backing up {} ...".format(map_file))
        shutil.copyfile(map_file, '{}.bak'.format(map_file))
    else:
        logger.info("No map file exists, only using map from system.")
    system_map = build_system_map()
    file_map = read_file_map()
    merged_map = system_map
    for map in file_map:
        merged_map[map] = file_map[map]
    added_maps = []
    for map in system_map:
        if map not in file_map:
            added_maps.append(map)
    if len(added_maps) > 0:
        logger.info("The following cores have been added to the cores.json: {}".format(added_maps))
        
    with open(map_file, "w") as write_file:
        json.dump(merged_map, write_file, indent=4)

def load_map_to_memory():
    global map_file
    global cores
    if os.path.exists(map_file):
        with open(map_file) as map_json:
            maps = json.load(map_json)
            cores = maps

def get_map(corename):
    if corename in cores:
        return cores[corename]
    else:
        return {}

merge_maps()
load_map_to_memory()  

if __name__ == "__main__":
    pass