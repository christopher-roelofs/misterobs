import json
import sys
from tinydb import TinyDB, Query
import re

database = TinyDB('database.json',  indent=4, separators=(',', ': '))


def get_rom_by_hash(hash):
    rom = Query()
    result = database.search(rom.sha1 == hash)
    if len(result) > 0:
        return result[0]
    else:
        return {}

def delete_rom(uuid):
    query = Query()
    database.remove(query.uuid == uuid)

def get_rom_by_uuid(uuid):
    rom = Query()
    result = database.search(rom.uuid == uuid)
    if len(result) > 0:
        return result[0]
    else:
        return {}

def search_roms_by_name(name):
    rom = Query()
    result = database.search(rom.rom_extensionless_file_name.matches(name, flags=re.IGNORECASE))
    return result

def is_new_rom(rom):
    query = Query()
    result = database.search((query.sha1 == rom["sha1"]) & (query.release_name == rom["release_name"]) & (query.rom_extensionless_file_name == rom["rom_extensionless_file_name"]))
    if len(result) > 0:
        return False
    else:
        return True


def get_rom_by_name(name,system):
    rom = Query()
    result = database.search((rom.rom_extensionless_file_name == name) & (rom.system == system))
    if len(result) > 0:
        return result[0]
    else:
        return {}

def get_rom_by_hash_or_name(hash,name):
    rom = Query()
    result = database.search((rom.sha1 == hash) | (rom.rom_extensionless_file_name == name))
    if len(result) > 0:
        return result[0]
    else:
        return {}

def update_rom(item):
    rom = Query()
    database.upsert({"uuid":item['uuid'],"release_name": item['release_name'], "region":item['region'],"system":item['system'] ,"sha1":item['sha1'].upper(),"rom_extensionless_file_name":item['rom_extensionless_file_name'],"developer":item['developer'],"publisher":item['publisher'],"genre":item['genre'],"date":item['date'],"description":item["description"],"reference_url":item["reference_url"],"manual_url":item["manual_url"]}, rom.uuid==item["uuid"])


if __name__ == "__main__":
    print(get_rom_by_hash("56FE858D1035DCE4B68520F457A0858BAE7BB16"))