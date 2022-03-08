# autoForm
Auto fill online forms\
Uses selenium and chrome webdriver
## Requirements
- [Python 3.10+](https://www.python.org/downloads/)
- pip (*should come installed with python else follow [guide](https://pip.pypa.io/en/latest/installation/)*)
- Chrome based browser
## Modules
- selenium
- beautifulsoup4
- requests
- lxml
## How to setup
1. Install the program requirements with command below
```
pip install -r requirements.txt
```
2. Go in plugins go into the plugin folder that you want to create a profile for and run createProfile.

3. move the profile create in to formProfles folder

*If chromedrive is not installed automaticly on run time go to the chrome webdrivers site and download for your version of chrome: https://chromedriver.chromium.org/downloads/*

## How to run
Run autoForm.py and it will fill out all forms set up in formProfiles folder form
```
python autoForm.py
```
To run a form by itself or multiple specific forms do the command as following
```
python autoForm.py --forms a.json b.json ...
```
*This program has not been tested on macOS and on windows 7 or lower so it may not work correctly on those operating systems*
