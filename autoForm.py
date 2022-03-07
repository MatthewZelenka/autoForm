#!/usr/bin/env /env/bin/python
import json, argparse, sys, os
from lib.webScraper import *
import pkgutil

class autoForm(baseChromeWebScraper):
    def __init__(self, modules, profile, url:str = None, webDriverPath:str = "./chromedriver", autoWebDriverModule:str = "lib.autoChromeDriver", browser:str = None, browserDownloadPath:str = None, browserHide:str = False, userAgent:str = None, logLevel: int = None):
        self.modules = modules
        self.profile = profile
        super().__init__(url, webDriverPath, autoWebDriverModule, browser, browserDownloadPath, browserHide, userAgent, logLevel)

    def run(self):
        module = self.modules[[importedModule.plugName for importedModule in self.modules].index(self.profile["id"])]
        self.url = module.form
        self.setup()
        module.fillForm(self, self.profile)

def formRun(profileFile: str):
    print(profileFile)
    with open(os.path.join("formProfiles", profileFile), "r") as file:
        profile = json.load(file)
    modulePath = "plugins"
    avalableModules = [module for _, module, _ in pkgutil.iter_modules([modulePath])]
    importedModules = [pkgutil.importlib.import_module("."+module, modulePath) for module in avalableModules]
    form = autoForm(profile = profile, modules=importedModules, browser=profile["browser"], browserHide = False, logLevel = 3)
    form.run()
    form.quit()

# Program starts running
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process online forms automatically")
    parser.add_argument("--forms", metavar="forms", type=str, nargs="*", help="Forms to fill out")
    args = parser.parse_args()

    formProfiles = args.forms if args.forms and len(args.forms) > 0 else [profileFile for profileFile in os.listdir(os.path.join(sys.path[0],"formProfiles")) if profileFile.endswith('.json')]
    [formRun(profile) for profile in formProfiles]