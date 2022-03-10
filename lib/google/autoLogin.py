from lib.webScraper import *
from dataclasses import dataclass

# waits for redirect
@dataclass
class googleRedirect:
    url = "https://accounts.google.com/ServiceLogin?service"
    def doPage(self, profile) -> str:
        return "Google login redirected"

# fills in email
@dataclass
class googleEmail:
    url = "https://accounts.google.com/signin/v2/identifier?service"
    def doPage(self, profile) -> str:
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".whsOnd.zHQkBf")))
        login = self.driver.find_element(By.CSS_SELECTOR, ".whsOnd.zHQkBf")
        login.send_keys(profile["user"]["email"])
        # gets web element of submit button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-dgl2Hf-ppHlrf-sM5MNb")))
        self.driver.find_element(By.CLASS_NAME, "VfPpkd-dgl2Hf-ppHlrf-sM5MNb").click()
        return "Logged into google"

# fills in password
@dataclass
class googlePassword:
    url = "https://accounts.google.com/signin/v2/challenge/pwd?"
    def doPage(self, profile) -> str:
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".whsOnd.zHQkBf")))
        login = self.driver.find_element(By.CSS_SELECTOR, ".whsOnd.zHQkBf")
        login.send_keys(profile["user"]["password"]) 
        # gets web element of submit button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-dgl2Hf-ppHlrf-sM5MNb")))
        self.driver.find_element(By.CLASS_NAME, "VfPpkd-dgl2Hf-ppHlrf-sM5MNb").click()
        return "Submited password"

# waits for google to continue logging in
@dataclass
class googleContinuing:
    url = "https://accounts.google.com/signin/continue?"
    def doPage(self, profile) -> str:
        return "Google login continued"

# click continue on speedbump
@dataclass
class googleSpeedbump:
    url = "https://accounts.google.com/speedbump/"
    def doPage(self, profile) -> str:
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.qIypjc.TrZEUc.lw1w4b")))
        self.driver.find_element(By.CLASS_NAME, "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.qIypjc.TrZEUc.lw1w4b").click()
        return "Speedbumped"

def login(self, profile, pageProcedures:list=[], printOut=False):
    pageProcedure = [googleRedirect, googleEmail, googlePassword, googleContinuing, googleSpeedbump]
    # adds all protocols for login in together 
    pageProcedure.extend(pageProcedures)
    while True: # runs every url to see if one of the protocols can solve the page if not then assume login is over and exits
        currentUrl = self.driver.current_url
        for procedure in pageProcedure:
            if currentUrl.find(procedure.url) != -1:
                process = procedure.doPage(self, profile)
                if printOut: print(process)
                break
            elif procedure == pageProcedure[-1]:
                return
        self.waitUrlChange(currentURL=currentUrl, waitTime=2)