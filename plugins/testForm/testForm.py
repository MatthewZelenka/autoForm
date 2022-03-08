import pathlib
from dataclasses import dataclass
try:
    from lib import google
    from lib.webScraper import *
except ImportError:
    pass

plugName = pathlib.Path(__file__).stem

form = "https://docs.google.com/forms/d/e/1FAIpQLScOwuXKSvr7Lg2PwrIg-sUQNMAyVJXS59M2aaO5db0bbFK_Sg/viewform"

# page procedures when in yrdsb login page
@dataclass
class yrdsbRedirect:
    url = "https://google.yrdsb.ca/EasyConnect/"
    def doPage(self, profile) -> str:
        return "YRDSB redirection"

@dataclass
class yrdsbLogin:
    url = "https://google.yrdsb.ca/LoginFormIdentityProvider/Login.aspx?"
    def doPage(self, profile) -> str:
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "UserName")))
        login = self.driver.find_element(By.ID, "UserName")
        login.send_keys(profile["user"]["userName"])
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Password")))
        login = self.driver.find_element(By.ID, "Password")
        login.send_keys(profile["user"]["password"])
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "LoginButton")))
        self.driver.find_element(By.NAME, "LoginButton").click()
        return "Logging in to YRDSB"

def waitToComplete(self, waitTime: int = 10): # function to wait for next page to load before continuing 
    try:
        WebDriverWait(self.driver, waitTime).until(lambda driver: google.formFiller.getFormState(self) != "uncomplete")
        return True
    except selenium.common.exceptions.TimeoutException:
        return False

def fillForm(self, profile):
    # does google login and attaches yrdsb login code
    google.autoLogin.login(self=self, profile=profile, pageProcedures=[yrdsbRedirect, yrdsbLogin])

    # fills google form
    if google.formFiller.getFormState(self) == "uncomplete": # fills out form 
        print("Filling out form...")
        google.formFiller.clearAll(self)

        test = google.formFiller.multipleChoice(question="Did you read this *", answer=["Yes"])

        google.formFiller.fillForm(self, test)
        google.formFiller.submit(self)
    waitToComplete(self)
    print("Form is {}".format(google.formFiller.getFormState(self)))