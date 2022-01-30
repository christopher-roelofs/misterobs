
# MiSTerOBS
Application to integrate MiSTer and OBS

This app requires at least python 3+.

To install the python requirements run "pip install -r requirements.txt" in the root of this folder.
If you get an error about upgrading pip, run " -m pip install --upgrade pip"

You can find a compiled windows version built via pyinstaller in the releases section.

For OBS, you need to install obs-websocket which can be found here: https://github.com/Palakis/obs-websocket/releases.

**You must enable the recents setting in your .ini file on the MiSTer** : recents=1              ; set to 1 to show recently played games

![image](https://user-images.githubusercontent.com/1930031/151707368-76b2ce0e-9a03-421e-bb6e-7eb9e95bb38a.png)


Update **config.json** with your details:

|  Config | Example  | Details   |
| ------------ | ------------ | ------------ |
| mister_ip  | 192.168.1.34 or MiSTer   | ip address or hostname of MiSTer  |
| mister_username  |  root  |  ssh username for MiSTer  |
| mister_password  | 1  |  ssh password for MiSTer  |
|  change_scenes |  true or false | enable/disable scene switching  |
|  debug | true or false  | enable/disable debug logs  |
|  custom_text_sources |  see json code below for example |  this is the format that will be used for the source text if you don' have one in the cores.json |
| refresh_rate  |  1 |  polling rate of checking the core and game |
| core_storage  | fat or usbx   |  where the cores are stored fat for sd card and usbX for usb |
| pause_scenes  | see json code below for example  | if one of these scenes are manually switched to, the script will skip changing scenes. Source text will still be updated for any scenes in the default conifg  |
| obs/host  |  localhost  | obs websocket host/ip address  |
| obs/port  | 4444  |  obs websocket port |
|  obs/password | password  | obs websocket password |
|images_folder|C:\\path\\to\\art|base folder for image source art. you must escape backslashes|
|fuzzy_match_images| true or false| use fuzzy string match on image file names if not matched by name|
|write_to_file| see json code below for example| write rom details to file on game change|


```json
{
   "main":{
      "mister_ip":"MiSTer",
      "mister_username":"root",
      "mister_password":"1",
      "change_scenes":true,
      "debug":false,
      "custom_text_sources":{
         "GameName":"Default:playing {game} on {core}"
      },
      "refresh_rate":"1",
      "core_storage":"fat",
      "pause_scenes":[
         "Pause Scene"
      ],
      "images_folder":"C:\\path\\to\\art",
      "fuzzy_match_images":true,
      "write_to_file":{
         "file":"C:\\path\\to\\details.txt"
      }
   },
   "obs":{
      "host":"localhost",
      "port":"4444",
      "password":"crazyfire"
   }
}
```

Write to file option

if you have the write_to_file config set, a file will be written to the path in the following format:
key
value

example

name
Super Mario Land
region
Europe


If a value in the database is empty for that rom, it will not be written to the file.


You can map the corename, scene name, system name, custom text and custom images sources in the cores.json file.

**cores.json**

* "GBA" - core name. This has to match the name of the rbf without the datestamp. The script removes the datestamp before it does the lookup.
* "description" - description of the core. Not required but added by default on first run.
* "scene" - this is the name of the scene in obs.
* "custom_text_sources" - this is the source text that will be updated on game change. You can have multiple. You can use {core} {game} and {displayname}.If display_name is not set in the json file {displayname} will be blank.
* "custom_image_sources" - Put the name of the image sources you would like to change here. You can set each image source name to either boxart,snap,title or system. The name of the source can be custom as long as the value is one of the previous mentioned.
* "display_name" - used above. This allows you to set a better looking name for the core.

```json
{
   "GBA":{
      "description":"GBA Core",
      "scene":"GBA Scene",
      "system":"Nintendo Game Boy Advance",
      "display_name": "Nintendo Game Boy Advance",
      "custom_text_sources":{
         "GBA Game":"Playing {game} on {core}"
      },
      "custom_image_sources":{
         "Boxart":"boxart",
         "Snap":"snap",
         "Title":"title",
         "System":"system"
      }
   }
}
```

**folder_map.json**

This is where the name of the system from the database and the system field in the cores.json file will be mapped to an art folder per system. The folder names can be custom but the system name needs to match the database. By default the folder names match the [libretro-thumbnails](https://github.com/libretro-thumbnails) folders.

The boxart,snap,title, and system folders are the subfolder in each system folder including base art folder 
Example
c:\\path\\to\\art\\SNK_-_Neo_Geo\\Named_Boxarts

the image names in the systems folder need to match the system names below. if the name has a "/" in it, you need to place it with "-".
Example "Sega CD/Mega-CD" becomes "Sega Genesis-Mega Drive.png"


```json
{
   "boxart_folder":"Named_Boxarts",
   "snap_folder":"Named_Snaps",
   "title_folder":"Named_Titles",
   "system_folder":"systems",
   "Atari 2600":"Atari_-_2600",
   "Atari 5200":"Atari_-_5200",
   "Atari 7800":"Atari_-_7800",
   "Atari Lynx":"Atari_-_Lynx",
   "Bandai WonderSwan":"Bandai_-_WonderSwan",
   "Bandai WonderSwan Color":"Bandai_-_WonderSwan_Color",
   "Coleco ColecoVision":"Coleco_-_ColecoVision",
   "GCE Vectrex":"GCE_-_Vectrex",
   "Intellivision":"Mattel_-_Intellivision",
   "NEC PC Engine/TurboGrafx-16":"NEC_-_PC_Engine_-_TurboGrafx_16",
   "NEC PC Engine CD/TurboGrafx-CD":"NEC_-_PC_Engine_CD_-_TurboGrafx-CD",
   "NEC SuperGrafx":"NEC_-_PC_Engine_SuperGrafx",
   "Nintendo Famicom Disk System":"Nintendo_-_Family_Computer_Disk_System",
   "Nintendo Game Boy":"Nintendo_-_Game_Boy",
   "Nintendo Game Boy Color":"Nintendo_-_Game_Boy_Color",
   "Nintendo Game Boy Advance":"Nintendo_-_Game_Boy_Advance",
   "Nintendo Entertainment System":"Nintendo_-_Nintendo_Entertainment_System",
   "Nintendo Super Nintendo Entertainment System":"Nintendo_-_Super_Nintendo_Entertainment_System",
   "Sega Game Gear":"Sega_-_Game_Gear",
   "Sega Master System":"Sega_-_Master_System_-_Mark_III",
   "Sega CD/Mega-CD":"Sega_-_Mega-CD_-_Sega_CD",
   "Sega Genesis/Mega Drive":"Sega_-_Mega_Drive_-_Genesis",
   "Sega Saturn":"Sega_-_Saturn",
   "Sega SG-1000":"Sega_-_SG-1000",
   "SNK Neo Geo":"SNK_-_Neo_Geo",
   "SNK Neo Geo Pocket":"SNK_-_Neo_Geo_Pocket",
   "SNK Neo Geo Pocket Color":"SNK_-_Neo_Geo_Pocket_Color",
   "Magnavox Odyssey2":"Magnavox_-_Odyssey2",
   "Commodore 64":"Commodore_-_64",
   "Microsoft MSX":"Microsoft_-_MSX",
   "Microsoft MSX2":"Microsoft_-_MSX2",
   "Sony PlayStation":"Sony_-_PlayStation",
   "Arcade":"Arcade"
}
```
**Database Manager**

The database manager allows you to edit and add new records to the database. The database is based on the [OpenVGDB](https://github.com/OpenVGDB/OpenVGDB) database but slimmed down with some added fields.

 - To create a new record make sure the fields have been cleared. add your new record details and click submit. 
  - To edit a record, select the record from the table, edit the fields and then submit. 
  - To create a new record based on an existing record, select the record from the table, click duplicate, edit the fields and then submit. A new record with a new uuid will be created. The new record should have a different sha1 or rom name or you will get an error and the record will not be created.

![image](https://user-images.githubusercontent.com/1930031/151707023-f0ae6dfd-0295-4273-afcc-34abcd9e756f.png)


**Database Tool**

Create Patch.bat (DatabaseTool.exe -c or -createpatch) - This will take a while bceause there are a lot of records and it has to iterate over both databases.

This allows you to create a patch that is a comparison of your current database.json file to an existing database.json file (database.old). Any record that is new or different from the current to the other will be added to a database.patch file that can be used as a backup of changes. This could be applied over a new database.json file after an update to maintain your local changes.

Import Patch.bat (DatabaseTool.exe -i or -import)

This allows you to import a patch

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
