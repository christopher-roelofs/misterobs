import os
import xmltodict
import json
import sqlite3
from tinydb import TinyDB, Query, database
import pathlib
import uuid

systems = ["Arcade", "Atari 2600", "Atari 5200", "Atari 7800", "Atari Lynx", "Bandai WonderSwan", "Bandai WonderSwan Color", "Coleco ColecoVision", "GCE Vectrex", "Intellivision",
           "NEC PC Engine/TurboGrafx-16", "NEC PC Engine CD/TurboGrafx-CD", "NEC PC-FX", "NEC SuperGrafx", "Nintendo Famicom Disk System", "Nintendo Game Boy", "Nintendo Game Boy Advance",
           "Nintendo Game Boy Color", "Nintendo Entertainment System", "Nintendo Super Nintendo Entertainment System", "Sega Game Gear", "Sega Master System", "Sega CD/Mega-CD", "Sega Genesis/Mega Drive",
           "Sega Saturn", "Sega SG-1000", "Sony PlayStation", "SNK Neo Geo Pocket", "SNK Neo Geo Pocket Color", "Magnavox Odyssey2", "Commodore 64", "Microsoft MSX", "Microsoft MSX2"]

regions = ["Australia", "Asia", "Brazil", "Canada", "China", "Denmark", "Europe", "Finland", "France", "Germany", "Hong Kong", "Italy", "Japan", "Korea", "Netherlands", "Russia", "Spain", "Sweden",
           "Taiwan", "USA", "World", "Asia, Australia", "Brazil, Korea", "Japan, Europe", "Japan, Korea", "Japan, USA", "USA, Australia", "USA, Europe", "USA, Korea", "Europe, Australia", "Greece", "Ireland", "Norway",
           "Portugal", "Scandinavia", "UK", "USA, Brazil", "Poland"]


def generate_uuid():
    return uuid.uuid4().hex


def replace_none(string):
    if string == None:
        return ""
    else:
        return string


def create_patch(new_database, old_database, out_patch):
    updated = TinyDB(new_database,  indent=4, separators=(',', ': ')).all()
    roms = []
    index = 1
    for item in updated:
        database = TinyDB(old_database,  indent=4, separators=(',', ': '))
        query = Query()
        result = database.search(query.uuid == item["uuid"])
        if len(result) > 0:
            if sorted(item.items()) != sorted(result[0].items()):
                roms.append(item)
                print(
                    f'{index}/{len(updated)} - added patch for existing rom: {item["rom_extensionless_file_name"]}')
            else:
                print(
                    f'{index}/{len(updated)} - no patch added for existing rom: {item["rom_extensionless_file_name"]}')
        else:
            result = database.search((query.sha1 == item["sha1"]) & (query.release_name == item["release_name"]) & (
                query.rom_extensionless_file_name == item["rom_extensionless_file_name"]))
            if result < 1:
                roms.append(item)
                print(
                    f'{index}/{len(updated)} - added patch for new rom: {item["rom_extensionless_file_name"]}')

        index += 1
    with open(out_patch, 'w') as outjson:
        json.dump(roms, outjson, indent=4)

def import_patch(file):
    database = TinyDB('database.json',  indent=4, separators=(',', ': '))
    with open(file) as json_file:
        data = json.load(json_file)
        index = 1
        for item in data:
            query = Query()
            database.upsert({"uuid": item['uuid'], "release_name": item['release_name'], "region": item['region'], "system": item['system'], "sha1": item['sha1'], "rom_extensionless_file_name": item['rom_extensionless_file_name'], "developer": item['developer'], "publisher": item['publisher'], "genre": item['genre'],
                            "date": item['date'], "description": item["description"], "reference_url": item["reference_url"], "manual_url": item["manual_url"]}, (query.sha1 == item["sha1"]) & (query.release_name == item["release_name"]) & (query.rom_extensionless_file_name == item["rom_extensionless_file_name"]))
            print(f"{index}/{len(data)} - {item['release_name']}")
            index += 1


# https://github.com/OpenVGDB/OpenVGDB
def openvgdb_to_patch():

    def get_release_by_rom_id(id):
        db_connection = sqlite3.connect(db_file)
        cur = db_connection.cursor()
        cur.execute(f"SELECT * FROM RELEASES WHERE romID=? ", (id,))
        rows = cur.fetchall()
        db_connection.close()
        if len(rows) > 0:
            return rows[0]
        else:
            return ("", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")

    db_file = "openvgdb.sqlite"
    db_connection = sqlite3.connect(db_file)
    roms = db_connection.cursor().execute(f"SELECT * FROM ROMS WHERE systemID == 3  or systemID == 4  or systemID == 5 or systemID == 6 or systemID == 9 or systemID == 10 or systemID == 11 or systemID == 12 or systemID == 13 or systemID == 14 or systemID == 15 or systemID == 16 or systemID == 17 or systemID == 18 or systemID == 19 or systemID == 20 or systemID == 21 or systemID == 25 or systemID == 26 or systemID == 30 or systemID == 31 or systemID == 32 or systemID == 33 or systemID == 34 or systemID == 35 or systemID == 36 or systemID == 37 or systemID == 38 or systemID == 40 or systemID == 41 or systemID == 42 or systemID == 43",).fetchall()
    index = 1
    modb = []
    for item in roms:
        release = get_release_by_rom_id(item[0])
        print(f"{index}/{len(roms)} - {replace_none(release[2])}")
        rom = {}
        rom['uuid'] = generate_uuid()
        rom["release_name"] = replace_none(release[2])
        rom["region"] = replace_none(release[4])
        rom["system"] = replace_none(release[6])
        rom['sha1'] = replace_none(item[5])
        rom["rom_extensionless_file_name"] = replace_none(item[8])
        rom["publisher"] = replace_none(release[13])
        rom["date"] = replace_none(release[15])
        rom["developer"] = replace_none(release[12])
        rom["genre"] = replace_none(release[14])
        rom["description"] = replace_none(release[11])
        rom["reference_url"] = replace_none(release[16])
        rom["manual_url"] = ""
        modb.append(rom)
        index += 1

    with open('import/seed/openvgdb.json', 'w') as outjson:
        json.dump(modb, outjson, indent=4)


def mra_to_patch():
    roms = []
    index = 1
    files = os.listdir("dats/mra/")
    for mra in files:
        with open(f'dats/mra/{mra}') as fd:
            try:
                doc = xmltodict.parse(fd.read())
                name = doc['misterromdescription']['name']
                rbf = doc['misterromdescription']['rbf']
                year = ""
                if 'year' in doc['misterromdescription']:
                    year = doc['misterromdescription']['year']
                manufacturer = ""
                if 'manufacturer' in doc['misterromdescription']:
                    manufacturer = doc['misterromdescription']['manufacturer']
                category = ""
                if "category" in doc['misterromdescription']:
                    category = doc['misterromdescription']['category']
                region = ""
                if 'region' in doc['misterromdescription']:
                    region = doc['misterromdescription']['region']
                author = ""
                if "about" in doc['misterromdescription']:
                    if doc['misterromdescription']['about'] != None:
                        if "author" in doc['misterromdescription']['about']:
                            author = doc['misterromdescription']['about']['@author']
                        if 'mraauthor' in doc['misterromdescription']:
                            author = doc['misterromdescription']['mraauthor']

                rom = {}
                rom["uuid"] = generate_uuid()
                rom["release_name"] = name
                rom["region"] = region
                rom["system"] = "Arcade"
                rom['sha1'] = ""
                rom["rom_extensionless_file_name"] = pathlib.Path(mra).stem
                rom["publisher"] = manufacturer
                rom["date"] = year
                rom["developer"] = manufacturer
                rom["genre"] = category
                rom["description"] = ""
                rom["reference_url"] = ""
                rom["manual_url"] = ""
                roms.append(rom)
                print(f"{index}/{len(files)} - {pathlib.Path(mra).stem}")
                index += 1
            except Exception as e:
                print(f"{index}/{len(files)} - Failed to parse {mra}")
                print(e)
                index += 1

    with open('import/seed/mra.josn', 'w') as outjson:
        json.dump(roms, outjson, indent=4)

# https://github.com/libretro/libretro-database/tree/master/metadat


def libretro_dat_to_patch(filename, system, outname):
    file = open(filename, 'r')
    lines = file.readlines()
    roms = []
    rom = {}
    for line in lines:
        line = line.strip()
        if 'name "' in line and "size" not in line:
            rom = {}
            rom["uuid"] = generate_uuid()
            rom["system"] = system
            rom["region"] = ""
            rom["sha1"] = ""
            release_name = line.replace('name "', "").replace('"', "")
            rom["release_name"] = release_name
            rom["developer"] = ""
            rom["genre"] = ""
            rom["date"] = ""
            rom["publisher"] = ""
            rom["reference_url"] = ""
            rom["manual_url"] = ""
        if 'rom ( name' in line:
            #rom_name = line.split('" size ')[0].replace('rom ( name "',"")
            #rom["rom_extensionless_file_name"] = pathlib.Path(rom_name).stem
            rom["rom_extensionless_file_name"] = release_name
            if "sha1" in line:
                sha1 = line.split('sha1 ')[1].replace(' )', "").upper()
                rom["sha1"] = sha1
                roms.append(rom)
            else:
                roms.append(rom)
        if 'description "' in line:
            rom['description'] = line.replace(
                'description "', "").replace('"', "")
    with open(f'import/seed/libretro_{outname}.json', 'w') as outjson:
        json.dump(roms, outjson, indent=4)


# https://github.com/libretro/libretro-database/blob/master/metadat/fbneo-split/FBNeo_romcenter.dat
def neogeo_to_patch():
    roms = []
    with open('dats/FBNeo_romcenter.dat') as fd:
        doc = xmltodict.parse(fd.read())
        for game in doc['datafile']["game"]:
            if "@romof" in game:
                if game['@romof'] == 'neogeo':
                    rom = {}
                    rom['uuid'] = generate_uuid()
                    rom["release_name"] = game['description']
                    rom["region"] = ""
                    rom["system"] = 'SNK Neo Geo'
                    rom['sha1'] = ""
                    rom["rom_extensionless_file_name"] = game['@name']
                    rom["publisher"] = game['manufacturer']
                    rom["date"] = game['year']
                    rom["developer"] = game['manufacturer']
                    rom["genre"] = ""
                    rom["description"] = ""
                    rom["reference_url"] = ""
                    rom["manual_url"] = ""
                    roms.append(rom)
                    print(f"{game['description']}")

    with open('import/seed/neogeo.json', 'w') as outjson:
        json.dump(roms, outjson, indent=4)


if __name__ == "__main__":
    pass