import paramiko
from time import sleep
import json
import config
import ssh
import mister
import cores
import logger
import obs


SETTINGS = config.get_config()
maps = cores.read_file_map()


RECENTS_FOLDER = '/media/{}/config/'.format(SETTINGS['main']['core_storage'])


last_game = ""
last_core = ""


def replace_text(core, game, displayname, text):
    return text.replace("{core}", core).replace("{game}", game).replace("{displayname}", displayname)


while True:
    try:
        core = mister.get_running_core()
        map_core = cores.get_map(core)
        game = mister.get_last_game(core)

        sources = None
        displayname = ""

        if "display_name" in map_core:
            displayname = map_core["display_name"]

        if "custom_text_sources" in map_core:
            sources = map_core["custom_text_sources"]
        elif "custom_text_sources" in SETTINGS["main"]:
            sources = SETTINGS["main"]["custom_text_sources"]

        if obs.get_current_scene() != map_core['scene'] and obs.is_in_scene_list(map_core["scene"]):
            pause_enabled = False

            if "pause_scenes" in SETTINGS["main"]:
                pause_enabled = True
            if pause_enabled and obs.get_current_scene() not in SETTINGS["main"]["pause_scenes"]:
                if SETTINGS["main"]["change_scenes"]:
                    obs.change_scene(map_core['scene'])

        if game != "" and game != last_game:
            pause_enabled = False

            if "pause_scenes" in SETTINGS["main"]:
                pause_enabled = True

            if pause_enabled and obs.get_current_scene() in SETTINGS["main"]["pause_scenes"]:
                logger.debug("Pause scene active, not changing source text.")
            else:
                for source in sources:
                    obs.setSourceText(source, replace_text(
                        core, game, displayname, sources[source]))
        if core != last_core:
            if SETTINGS["main"]['change_scenes']:
                current_scene = obs.get_current_scene()

                if "pause_scenes" in SETTINGS["main"]:
                    pause_enabled = True

                if pause_enabled and current_scene in SETTINGS["main"]["pause_scenes"]:
                    logger.debug("Pause scene active, not changing scene.")
                else:
                    for source in sources:
                        obs.setSourceText(source, "")
                    if game != last_game:
                        for source in sources:
                            obs.setSourceText(source, replace_text(
                                core, game, displayname, sources[source]))
                    if current_scene != map_core["scene"] and obs.is_in_scene_list(map_core["scene"]):
                        obs.change_scene(map_core['scene'])
        last_core = core
        last_game = game

    except Exception as e:
        logger.error(repr(e))
    sleep(int(SETTINGS["main"]["refresh_rate"]))

client.close()
