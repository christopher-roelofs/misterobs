import pathlib
import logger
import config
import cores
import ssh
import os

SETTINGS = config.get_config()
RECENTS_FOLDER = '/media/{}/config/'.format(SETTINGS['main']['core_storage'])

def get_running_core():
    try:
        stdout = ssh.send_command("ps aux | grep [r]bf")
        current_core = 'menu'
        for line in stdout:
            if '.rbf' in line:
                for part in line.split(" "):
                    if ".rbf" in part:
                        line = part
                core_name = line.split('/')[-1].replace('.rbf','').strip()
                if "_" in core_name:
                    base_name = core_name.split('_')[0]
                    current_core = base_name

                else:
                    core_name = core_name.replace('.rbf','').strip()
                    current_core = core_name
        return current_core
    except Exception as e:
        logger.error(repr(e))
        return ""

def get_file_hash(filepath, filename):
    stdout = ""
    if ".zip" in filepath:
        stdout = ssh.send_command(f'unzip -p "../media/{filepath}" "{filename}" | sha1sum')
    else:
        stdout = ssh.send_command(f'sha1sum "../media/{filepath}/{filename}"')
    if len(stdout) > 0:
        return stdout[0].split()[0].upper()
    return ""

def get_last_game(core):
    ignore = ["cores_recent.cfg"]
    last_game = "","",""
    try:
        processes = ssh.send_command("ps aux | grep [r]bf")
        for line in processes:
            if ".mra" in line:
                last_game = line.split('/')[-1].replace('.mra','').strip()
                filename = line.split('/')[-1].strip()
                # adding ../ to path to match the format of the console recents file. Should probbaly not do this
                filepath = line.split(' /media/')[-1].strip().replace("/"+filename,"")
                return last_game,filepath,filename
            else:
                timeframe = 0.15 * int(SETTINGS['main']['refresh_rate'])
                last_changed = ssh.send_command(f'find /media/fat/config/ -mmin -{timeframe}')
                if len(last_changed) > 0:
                    for line in last_changed:
                        if "cores_recent.cfg" not in line:
                            recent = ssh.send_command('strings {}'.format(line.strip()))
                            if len(recent) > 0:
                                return pathlib.Path(recent[1].strip()).stem,recent[0].strip()[3:],recent[1].strip()
        return last_game

    except Exception as e:
        logger.error(repr(e))
        return "","",""



if __name__ == "__main__":
    pass
