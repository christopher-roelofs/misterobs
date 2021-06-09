# misterobs
Application to integrate MiSTer and OBS

This app requires at least python 3+.

To install the python requirements run "pip install -r requirements.txt" in the root of this folder.
If you get an error about upgrading pip, run " -m pip install --upgrade pip"

You can find a compiled windows version built via pyinstaller in the releases section.

For OBS, you need to install obs-websocket which can be found here: https://github.com/Palakis/obs-websocket/releases.

**You must enable the recents setting in your .ini file on the MiSTer** : recents=1              ; set to 1 to show recently played games

Update **config.json** with your details:

* mister_ip - ip address of MiSTer
* mister_username - ssh username for MiSTer
* mister_password - ssh password for MiSTer
* change_scenes - enable/disable scene switching
* debug - enable/disable debug logs
* custom_text_sources - this is the format that will be used for the source text if you don' have one in the cores.json.
* refresh_rate - polling rate of checking the core and game.
* core_storage - where the cores are stored fat for sd card and usbX for usb 
* pause_scenes - if one of these scenes are manually switched to, the script will skip changing scenes. Source text will still be updated for any scenes in the default conifg.
* host - obs host
* port - obs port
* password - obs password

```json
{
    "main": {
        "mister_ip": "000.000.00.000",
        "mister_username": "root",
        "mister_password": "1",
        "change_scenes":true, 
        "debug":false,
        "custom_text_sources": {
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
You can map the corename,scene name and supported filetypes in the cores.json file.

**cores.json**

* "GBA" - core name. This has to match the name of the rbf without the datestamp.The script removes the datestamp before it does the lookup.
* "description" - description of the core. Not required but added by default on first run.
* "scene" - this is the name of the scene in obs.
* "custom_text_sources" -  # this is the source text that will be updated on game change. You can have multiple. You can use {core} {game} and {displayname}.If display_name is not set in the json file {displayname} will be blank.
* "display_name" - used above. This allows you to set a better looking name for the core.

```json
{
    "GBA": {   
        "description": "GBA Core",
        "scene": "GBA Scene",
        "custom_text_sources": {             
            "GBA Game": "Playing {game} on {core}"
        },
        "display_name": "Nintendo Gameboy Advanced",
    }
}
```


**The following files are independent of the main program and need to be copied to the scripts folder on the MiSTer and run manually.**

**splitcores.py** - This is used for cores that have multiples systems ie SMS can play Game Gear and SG1000 games. You can use this to create copies of those rbf files named differently so you can have different scenes.

**splitcores.json** - This is used to setup which cores you will copy.

```json
{
    "SMS": ["GAMEGEAR","SG-1000"],
    "ColecoVision": ["SG-1000C"],
    "Gameboy": ["GBC"],
    "Turbografx16": ["TGFX-CD"]
}
```

**splitcores.sh** - Copy this to the scripts folder on the MiSTer to run the splitcores.py script.

**update_and_copy.sh** - Copy this to the scripts folder on the MiSTer to run the update_all script and then run the splitcores.py script
