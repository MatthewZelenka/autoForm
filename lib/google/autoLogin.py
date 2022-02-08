from lib.webScraper import *
from dataclasses import dataclass

@dataclass
class googleRedirect:
    url = "https://accounts.google.com/ServiceLogin?service"
    def doPage(self, profile):
        print("Google login redirecting...")

@dataclass
class googleEmail:
    url = "https://accounts.google.com/signin/v2/identifier?service"
    def doPage(self, profile):
        print("Logging in to google...")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".whsOnd.zHQkBf")))
        login = self.driver.find_element(By.CSS_SELECTOR, ".whsOnd.zHQkBf")
        login.send_keys(profile["user"]["email"])
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "VfPpkd-dgl2Hf-ppHlrf-sM5MNb")))
        self.driver.find_element(By.CLASS_NAME, "VfPpkd-dgl2Hf-ppHlrf-sM5MNb").click()

@dataclass
class googlePassword:
    url = "https://accounts.google.com/signin/v2/challenge/pwd?"
    def doPage(self, profile):
        print("Putting in password...")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".whsOnd.zHQkBf")))
        login = self.driver.find_element(By.CSS_SELECTOR, ".whsOnd.zHQkBf")
        login.send_keys(profile["user"]["password"]) 
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "VfPpkd-dgl2Hf-ppHlrf-sM5MNb")))
        self.driver.find_element(By.CLASS_NAME, "VfPpkd-dgl2Hf-ppHlrf-sM5MNb").click()

@dataclass
class googleContinuing:
    url = "https://accounts.google.com/signin/continue?"
    def doPage(self, profile):
        print("Google login continuing...")

@dataclass
class googleSpeedbump:
    url = "https://accounts.google.com/speedbump/"
    def doPage(self, profile):
        print("Speedbumping...")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.qIypjc.TrZEUc.lw1w4b")))
        self.driver.find_element(By.CLASS_NAME, "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.qIypjc.TrZEUc.lw1w4b").click()

def login(self, profile, pageProcedures:list=[]):
    pageProcedure = [googleRedirect, googleEmail, googlePassword, googleContinuing, googleSpeedbump]
    pageProcedure.extend(pageProcedures)
    while True:
        currentUrl = self.driver.current_url
        for procedure in pageProcedure:
            if currentUrl.find(procedure.url) != -1:
                procedure.doPage(self, profile)
                break
            elif procedure == pageProcedure[-1]:
                return
        self.waitUrlChange(currentURL=currentUrl, waitTime=2)