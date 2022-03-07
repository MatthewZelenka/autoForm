import pathlib
from lib.webScraper import *

plugName = pathlib.Path(__file__).stem

# starting link to get to the form
form = "https://formExample.com"

# function gets run when file is found that matchs this plugin
def fillForm(self, profile):
    pass # do something