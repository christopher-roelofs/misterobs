import re
import time
import config
import os
from os.path import exists
import json
from fuzzywuzzy import process
import logger
SETTINGS = config.get_config()

use_fuzzy_match = SETTINGS['main']['fuzzy_match_images']
images_folder = ""
if "images_folder" in SETTINGS['main']:
    images_folder = SETTINGS['main']['images_folder']

# https://github.com/orgs/libretro-thumbnails/repositories

folder_map = {}

if os.path.exists('folder_map.json'):
    with open('folder_map.json') as map_json:
            folder_map = json.load(map_json)

def fuzzy_match(name,folder):
    files = os.listdir(folder)
    if len(files) > 0:
        highest = process.extractOne(name,files)
        if highest[1] < 90:
            logger.info(f"Closest match {highest[0]}, match {highest[1]} under threshold of 90")
            return ""
        else:
            return(highest[0])
    else:
        return ""

def get_boxart(system,game,filename,release_name):
    if system in folder_map:
        boxart = os.path.join(images_folder, folder_map[system], folder_map['boxart_folder'], f'{game}.png')
        if not exists(boxart):
            boxart = os.path.join(images_folder, folder_map[system],folder_map['boxart_folder'], f'{filename}.png')
            if not exists(boxart):
                boxart = os.path.join(images_folder, folder_map[system], folder_map['boxart_folder'], f'{release_name}.png')
                if not exists(boxart):
                    if use_fuzzy_match and filename != "":
                        folder = os.path.join(images_folder, folder_map[system],folder_map['boxart_folder'])
                        logger.info(f"Fuzzy match enabled, attempting to match {filename} for boxart in {folder}")
                        matched = ""
                        try:
                            matched = fuzzy_match(filename,folder)
                        except Exception as e:
                            pass
                        if matched != "":
                            boxart = os.path.join(images_folder, folder_map[system], folder_map['boxart_folder'], matched)
                            if not exists(boxart):
                                boxart = os.path.join(images_folder, folder_map[system], folder_map['boxart_folder'], f'default.png')
                            else:
                                logger.info(f"Match {matched} found")
                        else:
                            logger.info(f"No match {matched} found")
                            boxart = os.path.join(images_folder, folder_map[system], folder_map['boxart_folder'], f'default.png')
                    else:
                        boxart = os.path.join(images_folder, folder_map[system], folder_map['boxart_folder'], f'default.png')
        return boxart
    else:
        return ""

def get_snap(system,game,filename,release_name):
    if system in folder_map:
        snap = os.path.join(images_folder, folder_map[system],folder_map['snap_folder'], f'{game}.png')
        if not exists(snap):
            snap = os.path.join(images_folder, folder_map[system], folder_map['snap_folder'], f'{filename}.png')
            if not exists(snap):
                snap = os.path.join(images_folder, folder_map[system], folder_map['snap_folder'], f'{release_name}.png')
                if not exists(snap):
                    if use_fuzzy_match and filename != "":
                        folder = os.path.join(images_folder, folder_map[system],folder_map['snap_folder'])
                        logger.info(f"Fuzzy match enabled, attempting to match {filename} for snap in {folder}")
                        matched = ""
                        try:
                            matched = fuzzy_match(filename,folder)
                        except Exception as e:
                            pass
                        if matched != "":
                            snap = os.path.join(images_folder, folder_map[system], folder_map['snap_folder'], matched)
                            if not exists(snap):
                                snap = os.path.join(images_folder, folder_map[system], folder_map['snap_folder'], f'default.png')
                            else:
                                logger.info(f"Match {matched} found")
                        else:
                            logger.info(f"No match {matched} found")
                            snap = os.path.join(images_folder, folder_map[system], folder_map['snap_folder'], f'default.png')
                    else:
                        snap = os.path.join(images_folder, folder_map[system], folder_map['snap_folder'], f'default.png')
        return snap
    else:
        return ""

def get_title(system,game,filename,release_name):
    if system in folder_map:
        title = os.path.join(images_folder, folder_map[system],folder_map['title_folder'], f'{game}.png')
        if not exists(title):
            title = os.path.join(images_folder, folder_map[system],folder_map['title_folder'], f'{filename}.png')
            if not exists(title):
                title = os.path.join(images_folder, folder_map[system], folder_map['title_folder'], f'{release_name}.png')
                if not exists(title):
                    if use_fuzzy_match and filename != "":
                        folder = os.path.join(images_folder, folder_map[system],folder_map['title_folder'])
                        logger.info(f"Fuzzy match enabled, attempting to match {filename} for title in {folder}")
                        matched = ""
                        try:
                            matched = fuzzy_match(filename,folder)
                        except Exception as e:
                            pass
                        if matched != "":
                            title = os.path.join(images_folder, folder_map[system], folder_map['title_folder'], matched)
                            if not exists(title):
                                title = os.path.join(images_folder, folder_map[system],folder_map['title_folder'], f'default.png')
                            else:
                                logger.info(f"Match {matched} found")
                        else:
                            logger.info(f"No match {matched} found")
                            title = os.path.join(images_folder, folder_map[system],folder_map['title_folder'], f'default.png')
                    else:
                        title = os.path.join(images_folder, folder_map[system], folder_map['title_folder'], f'default.png')
        return title
    else:
        return ""

def get_system(system,game,filename,release_name):
    if system in folder_map:
        system = os.path.join(images_folder,folder_map['system_folder'], f'{system.replace("/","-")}.png')
        if not exists(system):
            system = os.path.join(images_folder, folder_map['system_folder'], f'default.png')
        return system
    else:
        return ""
    
if __name__ == "__main__":
    #print(get_game_images("Nintendo Game Boy Advance", "Punisher, The (USA)")[0])
    #fuzzy_match("Arkanoid (Unl. Lives, slower) [hb]")
    fuzzy_match("Street Fighter Alpha 2 (EU, 960229)")