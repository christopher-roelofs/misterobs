import database_tools
from os.path import exists
import sys

def create_patch():
    print("-------------------------------------")
    print("Creating patch ...")
    print("This process wil create a database.patch file by comparing current database to an older version")
    input("Press enter to continue")
    print("Locating database.json")
    if not exists("database.json"):
        print("database.json not found.")
        input("Press enter to quit")
        sys.exit()
    print("database.json found")
    print("Locating database.old")
    if not exists("database.old"):
        print("database.old not found.")
        input("Press enter to quit")
        sys.exit()
    print("database.old found")
    print("")
    print("-------------------------------------")
    database_tools.create_patch("database.json","database.old","database.patch")


def import_patch():
    print("-------------------------------------")
    print("Importing database.patch ...")
    if not exists("database.patch"):
        print("database.patch not found.")
        input("Press enter to quit")
        sys.exit()
    print("-------------------------------------")
    print("")
    database_tools.import_patch("database.patch")

if len(sys.argv) > 1:
    if sys.argv[1] == "-i" or sys.argv[1] == "-import":
        import_patch()
    elif sys.argv[1] == "-c" or sys.argv[1] == "-createpatch":
        create_patch()
    else:
        print("Use -c or -createpatch to create a database.patch file")
        print("Use -i or -import to import a database.patch file")
else:
    print("Use -c or -createpatch to create a database.patch file")
    print("Use -i or -import to import a database.patch file")