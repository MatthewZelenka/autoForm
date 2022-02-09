import json
from lib.webScraper import *
# from lib.google import autoLogin
from plugins import yrdsbCovidForm as yrdsbCovidForm

configFile = "user.json"

class autoForm(baseChromeWebScraper):
    def run(self):
        self.setup()
        with open(configFile, "r") as file:
            yrdsbCovidForm.fillForm(self, json.load(file))
        # self.autoLogin()
        # self.fillForm()

# Program starts running
if __name__ == '__main__':
    #login
    form = autoForm(url = yrdsbCovidForm.form, browserHide = False, logLevel = 3)
    form.run()
    form.quit()
    pass
