#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from obswebsocket import obsws, requests  # noqa: E402
import logger
import config

SETTINGS = config.get_config()


ws = None


try:
    ws = obsws(SETTINGS['obs']['host'], int(
        SETTINGS['obs']['port']), SETTINGS['obs']['password'])
    ws.connect()
except Exception as e:
    logger.error("Unable to connect to OBS: {}".format(repr(e)))


def obs_call(call):
    try:
        return ws.call(call)
    except Exception as e:
        logger.error("Error making OBS call: {}.".format(repr(e)))


def disconnect():
    ws.disconnect()


def get_current_scene():
    scenes = obs_call(requests.GetSceneList())
    return scenes.getCurrentScene()


def get_scene_list():
    scenes = obs_call(requests.GetSceneList())
    return scenes.getScenes()


def is_in_scene_list(scene_name):
    scenes = obs_call(requests.GetSceneList())
    for scene in scenes.getScenes():
        if scene_name == scene['name']:
            return True
    return False


def setSourceText(name, text):
    try:
        source_settings = obs_call(
            requests.GetSourceSettings(name)).getSourceSettings()
        logger.event('Changing source text of "{}" to "{}"'.format(name, text))
        source_settings["text"] = text
        obs_call(requests.SetSourceSettings(sourceName=name, sourceSettings=source_settings))
    except Exception as e:
        logger.error("Unable to set source text for {}: {}".format(name, repr(e)))


def change_scene(name):
    try:
        logger.event("Switching to {}".format(name))
        ws.call(requests.SetCurrentScene(name))
    except Exception as e:
        logger.error("Unable to scene to {}: {}".format(name, repr(e)))

