import json
from lib.webScraper import *
import pkgutil

configFile = "user.json"

class autoForm(baseChromeWebScraper):
    def __init__(self, modules, profileFile, url:str = None, webDriverPath:str = "./chromedriver", autoWebDriverModule:str = "lib.autoChromeDriver", browser:str = None, browserDownloadPath:str = None, browserHide:str = False, userAgent:str = None, logLevel: int = None):
        self.modules = modules
        self.profileFile = profileFile
        super().__init__(url, webDriverPath, autoWebDriverModule, browser, browserDownloadPath, browserHide, userAgent, logLevel)

    def run(self):
        with open(self.profileFile, "r") as file:
            profile = json.load(file)
        
        module = self.modules[[importedModule.plugName for importedModule in importedModules].index(profile["id"])]
        self.url = module.form
        self.setup()
        module.fillForm(self, profile)

# Program starts running
if __name__ == '__main__':
    #login
    modulePath = "plugins"
    avalableModules = [module for _, module, _ in pkgutil.iter_modules([modulePath])]
    importedModules = [pkgutil.importlib.import_module("."+module, modulePath) for module in avalableModules]
    form = autoForm(profileFile = configFile, modules=importedModules, browser="/usr/bin/brave", browserHide = False, logLevel = 3)
    form.run()
    form.quit()
    pass
