# misterobs
Application to integrate MiSTer and OBS

This app requires at least python 3+.

To install the python requirements run "pip install -r requirements.txt" in the root of this folder.
Ff you get an error about upgrading pip, run " -m pip install --upgrade pip"

For OBS, you need to install obs-websocket which can be found here: https://github.com/Palakis/obs-websocket/releases.

Update config.json with your details:

```json
{
    "main": {
        "mister_ip": "000.000.00.000",
        "mister_username": "root",
        "mister_password": "1",
        "change_scenes":true, 
        "debug":false,
        "custom_text_sources": { # This is the format that will be used for the source text if you don' have one in the cores.json.
            "GameName": "Default:playing {game} on {core}"
        },
        "refresh_rate": "1",
        "core_storage": "fat",
        "pause_scenes": [
            "Pause Scene"
        ]
    },
    "obs": {
        "host": "localhost",
        "port": "4444",
        "password": ""
    }
}
```
You can map the corename,scene name and supported filetypes in the map.json file;
map.json schema:

```json
{
    "GBA": { # core name. This has to match the name of the rbf without the datestamp.The script removes the datestamp before it does the lookup. 
        "description": "GBA Core", # description of the core. Not required but added by default on first run.
        "scene": "GBA Scene", # this is the name of the scene in obs.
        "custom_text_sources": { # this is the source text that will be updated on game change. You can have multiple. YOu can use {core} {game} and {displayname}.
                                    If display_name is not set in the json file this will be blank.
            "GBA Game": "Playing {game} on {core}"
        },
        "display_name": "Nintendo Gameboy Advanced", # This us used with {displayname} above.
    }
}
```
splitcores.py - This is used for cores that have multiples systems ie SMS can play Game Gear and SG1000 games. You can use this to create copies of those rbf files named differently so you can have different scenes.

splitcores.json - This is used to setup which cores you will copy.

{
    "SMS": ["GAMEGEAR","SG-1000"],
	"ColecoVision": ["SG-1000C"],
	"Gameboy": ["GBC"],
	"Turbografx16": ["TGFX-CD"]
}

splitcores.sh - Copy this to the scripts folder on the MiSTer to run the splitcores.py script.

update_and_copy.sh - Copy this to the scripts folder on the MiSTer to run the update_all script and then run the splitcores.py script