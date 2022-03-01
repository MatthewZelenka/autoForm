# AutoCovidForm
Auto fill covid form for yrdsb\
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
2. Make a copy of "userExample.json" and rename it to "user.json"
3. Fill out the required information on "user.json" (fillTimes is WIP)

*If chromedrive is not installed automaticly on run time go to the chrome webdrivers site and download for your version of chrome: https://chromedriver.chromium.org/downloads/*

## How to run
Run autoCovidForm.py and it will fill out the google form
```
python autoForm.py
```
*This program has not been tested on macOS and on windows 7 or lower so it may not work correctly on those operating systems*
> Disclaimer: for educational purpose only.
