import json
from examplePlugin import *
from getpass import getpass
if __name__ == "__main__":
    fileName = input("File name: ")
    browser = input("Browser to use(leave empty to choose chrome): ")
    # Input general form data such as a name or password
    name = input("Name: ")
    password = getpass()
    # put in a profile dictonary like so only id and browser need to be in the dictoranry at the first level everything else can be moved
    profile = {
        "id":plugName,
        "browser": browser if browser else None,
        "user": {
            "name": name,
            "password": password
        }
    }
    # writes the profile file
    with open(fileName+".json", "w") as file:
        file.write(json.dumps(profile, indent=4))