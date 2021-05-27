import json
import os

config_file = 'config.json'

config = {}

def create_config():
    config = {}

    main = {}
    main["mister_ip"] = "000.000.00.000"
    main["mister_username"] = "root"
    main["mister_password"] = "1"
    main["change_scenes"] = True
    main["debug"] = False
    main["custom_text_sources"] = { "GameName": "Playing {game} on {core}" }
    main["refresh_rate"] = "1"
    main["core_storage"] = "fat"
    main["pause_scenes"] = [ "Pause Scene" ]
    config["main"] = main

    obs = {}
    obs['host'] = "localhost"
    obs['port'] = "4444"
    obs['password'] = ""
    config["obs"] = obs

    with open(config_file, "w") as write_file:
        json.dump(config, write_file, indent=4)

    

def load_config():
    global config
    if os.path.exists(config_file):
        with open(config_file) as config_text:
            config = json.load(config_text)
    else:
        print("Creating config. Update new conif with proper details")
        create_config()
            
def get_config():
    return config

load_config()

if __name__ == "__main__":
    print(get_config())