# AutoCovidForm
Auto fill covid form for yrdsb\
Uses selenium and chrome webdriver
## How to setup
1. Install the program requirements with command below
```
pip install -r requirements.txt
```
2. Make a copy of "userExample.json" and rename it to "user.json"
3. Fill out the required information on "user.json"
4. Download the chrome webdrivers form the chrome webdrivers site for your version of chrome and put it in the current directory: https://chromedriver.chromium.org/downloads/*

## How to run
Run autoCovidForm.py and it will fill out the google form
```
python autoCovidForm.py
```