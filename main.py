from email.mime import image
from time import sleep
import config
import mister
import cores
import logger
import obs
import images
import database
import threading


SETTINGS = config.get_config()
maps = cores.read_file_map()


RECENTS_FOLDER = '/media/{}/config/'.format(SETTINGS['main']['core_storage'])


last_game = ""
last_core = ""


def replace_text(core, game, displayname, text):
    return text.replace("{core}", core).replace("{game}", game).replace("{displayname}", displayname)

def replace_image(text,boxart,snap,title,system):
    return text.replace("boxart",boxart).replace("snap",snap).replace("title",title).replace("system",system)

def extract_rom_details(rom):
    details = ""
    if rom == "":
        return ""
    for detail in rom:
        if detail == "release_name":
            if rom["release_name"] !="":
                details = details + "name\n"
                details = details + f'{rom["release_name"]} \n'
        if rom["region"] !="":
            if detail == "region":
                details = details + "region\n"
                details = details + f'{rom["region"]} \n'
        if rom["system"] !="":
            if detail == "system":
                details = details + "system\n"
                details = details + f'{rom["system"]} \n'
        if rom["developer"] !="":
            if detail == "developer":
                details = details + "developer\n"
                details = details + f'{rom["developer"]} \n'
        if rom["publisher"] !="":
            if detail == "publisher":
                details = details + "publisher\n"
                details = details + f'{rom["publisher"]} \n'
        if rom["genre"] !="":
            if detail == "genre":
                details = details + "genre\n"
                details = details + f'{rom["genre"]} \n'
        if rom["date"] !="":
            if detail == "date":
                details = details + "date\n"
                details = details + f'{rom["date"]} \n'
        if rom["description"] !="":
            if detail == "description":
                details = details + "description\n"
                details = details + f'{rom["description"]} \n'
        if rom["reference_url"] !="":
            if detail == "reference_url":
                details = details + "url\n"
                details = details + f'{rom["reference_url"]} \n'
        if rom["manual_url"] !="":
            if detail == "manual_url":
                details = details + "manual\n"
                details = details + f'Manual: {rom["manual_url"]} \n'
    return(details)

def write_to_file(content,filename):
    try:
        with open(filename, 'w') as f:
            f.write(content)
    except Exception as e:
        logger.error(f"Failed to write details file to {filename}")
    

while True:
    try:
        core = mister.get_running_core()
        map_core = cores.get_map(core)
        game,filepath,filename = mister.get_last_game(core)
        sources = None
        image_sources = None
        displayname = ""
        boxart = ""
        snap = ""
        title = ""
        rom = {}

        if "display_name" in map_core:
            displayname = map_core["display_name"]

        if "custom_text_sources" in map_core:
            sources = map_core["custom_text_sources"]
        elif "custom_text_sources" in SETTINGS["main"]:
            sources = SETTINGS["main"]["custom_text_sources"]

        if "custom_image_sources" in map_core:
            image_sources = map_core["custom_image_sources"]

        if obs.get_current_scene() != map_core['scene'] and obs.is_in_scene_list(map_core["scene"]):
            pause_enabled = False

            if "pause_scenes" in SETTINGS["main"]:
                pause_enabled = True
            if pause_enabled and obs.get_current_scene() not in SETTINGS["main"]["pause_scenes"]:
                if SETTINGS["main"]["change_scenes"]:
                    obs.change_scene(map_core['scene'])

        if game != "" and game != last_game:
            if "system" in map_core:
                system = map_core['system']
            else:
                system = core
            pause_enabled = False
            hash = mister.get_file_hash(filepath,filename)
            rom = {}
            if hash != "":
                rom = database.get_rom_by_hash(hash)
                if len(rom) != 0:
                    logger.info(f"Hash: {hash} matched in database")
                else:
                    logger.info(f"Hash: {hash} not matched in database")
            if len(rom) == 0:
                rom = database.get_rom_by_name(game,system)
            if "rom_extensionless_file_name" in rom:
                logger.info(f"Rom match in database for Game: {game}, System: {system}")
                rom_name = rom["rom_extensionless_file_name"]
            else:
                logger.info(f"Game {game} not found in database, defaulting to game")
                rom_name = game
            if "release_name" in rom:
                release_name = rom["release_name"]
            else:
                release_name = game
                rom["release_name"] = game
                rom["region"] = ""
                rom["developer"] = ""
                rom["publisher"] = ""
                rom["genre"] = ""
                rom["date"] = ""
                rom["description"] = ""
                rom["reference_url"] = ""
                rom["manual_url"] = ""
                if "system" in map_core:
                    rom["system"] = map_core["system"]
                else:
                    rom["system"] = ""
                


            if image_sources != None:
                    for source in image_sources:
                        if image_sources[source] == "boxart":
                            boxart = images.get_boxart(system,rom_name,game,release_name.replace("/","_"))
                        if image_sources[source] == "snap":
                            snap = images.get_snap(system,rom_name,game,release_name.replace("/","_"))
                        if image_sources[source] == "title":
                            title = images.get_title(system,rom_name,game,release_name.replace("/","_"))
                        if image_sources[source] == "system":
                            system = images.get_system(system,rom_name,game,release_name.replace("/","_"))

            if "pause_scenes" in SETTINGS["main"]:
                pause_enabled = True

            if pause_enabled and obs.get_current_scene() in SETTINGS["main"]["pause_scenes"]:
                for source in SETTINGS["main"]["custom_text_sources"]:
                    if obs.is_in_source_list(source):
                        obs.setSourceText(source, replace_text(core, release_name, displayname, sources[source]))
                        if "write_to_file" in SETTINGS["main"]:
                            write_to_file(extract_rom_details(rom),SETTINGS["main"]["write_to_file"]["file"])
                    
            else:
                if sources != None:
                    for source in sources:
                        if obs.is_in_source_list(source):
                            threading.Thread(target=obs.setSourceText, args=(source, replace_text(core, release_name, displayname, sources[source]))).start()
                            #obs.setSourceText(source, replace_text(core, release_name, displayname, sources[source]))
                            if "write_to_file" in SETTINGS["main"]:
                                write_to_file(extract_rom_details(rom),SETTINGS["main"]["write_to_file"]["file"])

                if image_sources != None:
                    for source in image_sources:
                        if obs.is_in_source_list(source):
                            threading.Thread(target=obs.setSourceImage, args=(source,replace_image(image_sources[source],boxart,snap,title,system))).start()
                            #obs.setSourceImage(source,replace_image(image_sources[source],boxart,snap,title,system))
                        
        if core != last_core:
            if "system" in map_core:
                system = map_core['system']
            else:
                system = core
            if SETTINGS["main"]['change_scenes']:
                current_scene = obs.get_current_scene()
                hash = mister.get_file_hash(filepath,filename)
                rom = {}
                if hash != "":
                    rom = database.get_rom_by_hash(hash)
                    if len(rom) != 0:
                        logger.info(f"Hash: {hash} matched in database")
                    else:
                        logger.info(f"Hash: {hash} not matched in database")
                if len(rom) == 0:
                    rom = database.get_rom_by_name(game,system)
                if "rom_extensionless_file_name" in rom:
                    logger.info(f"Rom match in database for Game: {game}, System: {system}")
                    rom_name = rom["rom_extensionless_file_name"]
                else:
                    logger.info(f"Game {game} not found in database, defaulting to game")
                    rom_name = game
                if "release_name" in rom:
                    release_name = rom["release_name"]
                else:
                    release_name = game
                    rom["release_name"] = game
                    rom["region"] = ""
                    rom["developer"] = ""
                    rom["publisher"] = ""
                    rom["genre"] = ""
                    rom["date"] = ""
                    rom["description"] = ""
                    rom["reference_url"] = ""
                    rom["manual_url"] = ""
                    if "system" in map_core:
                        rom["system"] = map_core["system"]
                    else:
                        rom["system"] = ""
                if image_sources != None:
                    for source in image_sources:
                        if image_sources[source] == "boxart":
                            boxart = images.get_boxart(system,rom_name,game,release_name.replace("/","_"))
                        if image_sources[source] == "snap":
                            snap = images.get_snap(system,rom_name,game,release_name.replace("/","_"))
                        if image_sources[source] == "title":
                            title = images.get_title(system,rom_name,game,release_name.replace("/","_"))
                        if image_sources[source] == "system":
                            system = images.get_system(system,rom_name,game,release_name.replace("/","_"))

                if "pause_scenes" in SETTINGS["main"]:
                    pause_enabled = True

                if pause_enabled and current_scene in SETTINGS["main"]["pause_scenes"]:
                    for source in SETTINGS["main"]["custom_text_sources"]:
                        if obs.is_in_source_list(source):
                            obs.setSourceText(source,"")
                        if "write_to_file" in SETTINGS["main"]:
                            write_to_file(extract_rom_details(""),SETTINGS["main"]["write_to_file"]["file"])
                else:
                    if sources != None:
                        for source in sources:
                            if obs.is_in_source_list(source):
                                #threading.Thread(target=obs.setSourceText, args=(source,"")).start()
                                obs.setSourceText(source,"")
                                if "write_to_file" in SETTINGS["main"]:
                                    write_to_file(extract_rom_details(""),SETTINGS["main"]["write_to_file"]["file"])

                    if image_sources != None:
                        for source in image_sources:
                            if obs.is_in_source_list(source):
                                threading.Thread(target=obs.setSourceImage, args=(source,replace_image(image_sources[source],boxart,snap,title,system))).start()
                                #obs.setSourceImage(source,replace_image(image_sources[source],'',"","",system))
                        
                    if game != last_game:
                        if sources != None:
                            for source in sources:
                                if obs.is_in_source_list(source):
                                    #obs.setSourceText(source, replace_text(core, release_name, displayname, sources[source]))
                                    threading.Thread(target=obs.setSourceText, args=(source, replace_text(core, release_name, displayname, sources[source]))).start()
                                    if "write_to_file" in SETTINGS["main"]:
                                        write_to_file(extract_rom_details(rom),SETTINGS["main"]["write_to_file"]["file"])

                        if image_sources != None:
                            for source in image_sources:
                                #obs.setSourceImage(source,replace_image(image_sources[source],boxart,snap,title,system))
                                threading.Thread(target=obs.setSourceImage, args=(source,replace_image(image_sources[source],boxart,snap,title,system))).start()
                    if current_scene != map_core["scene"] and obs.is_in_scene_list(map_core["scene"]):
                        obs.change_scene(map_core['scene'])

        last_core = core
        last_game = game

    except Exception as e:
        logger.error(repr(e))
    sleep(int(SETTINGS["main"]["refresh_rate"]))


