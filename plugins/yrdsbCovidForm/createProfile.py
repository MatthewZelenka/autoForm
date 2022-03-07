import json
from yrdsbCovidForm import *
from getpass import getpass
if __name__ == "__main__":
    fileName = input("File name: ")
    browser = input("Browser to use(leave empty to choose chrome): ")
    userName = input("Username: ")
    email = input("Email: ")
    password = getpass()
    firstName = input("First name: ")
    lastName = input("Last name: ")
    profile = {
        "id":plugName,
        "browser": browser if browser else None,
        "user": {
            "userName": userName,
            "email": email,
            "password": password
        },
        "formInfo": {
            "firstName": firstName,
            "lastName": lastName
        }
    }
    with open(fileName+".json", "w") as file:
        file.write(json.dumps(profile, indent=4))