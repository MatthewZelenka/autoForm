from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from datetime import time as dttime
import time, json, os, sys, re, webScraper

print(len(sys.argv))
print(sys.argv)

covidForm = "https://docs.google.com/forms/d/e/1FAIpQLSedNWLgRdQKVfNqT4gwYrq0PEJqj2vnOL5GHqfopjwnakC-0g/viewform"

valURL = re.compile( # regex to see if valid url
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

configFile = "user.json"

class autoForm(webScraper.baseChromeWebScraper):
    def autoLogin(self):
        while True:
            currentUrl = self.driver.current_url
            print(self.driver.current_url)
            if currentUrl.find("https://accounts.google.com/signin/v2/identifier?") != -1: # logs you in to google in order to access the link provided 
                print("Logging in to google...")
                with open(configFile, "r") as read_file: # puts email in to google login from user.json
                    data = json.load(read_file)
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".whsOnd.zHQkBf")))
                    login = self.driver.find_element(By.CSS_SELECTOR, ".whsOnd.zHQkBf")
                    login.send_keys(data["user"]["email"])
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "VfPpkd-dgl2Hf-ppHlrf-sM5MNb")))
                    self.driver.find_element(By.CLASS_NAME, "VfPpkd-dgl2Hf-ppHlrf-sM5MNb").click()
                self.waitUrlChange(currentUrl)
                
            elif currentUrl.find("https://accounts.google.com/signin/v2/challenge/pwd?") != -1: # next step in google log in for password
                print("Putting in password...")
                with open(configFile, "r") as read_file: # puts password in to google login from user.json
                    data = json.load(read_file)
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".whsOnd.zHQkBf")))
                    login = self.driver.find_element(By.CSS_SELECTOR, ".whsOnd.zHQkBf")
                    login.send_keys(data["user"]["password"])
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "VfPpkd-dgl2Hf-ppHlrf-sM5MNb")))
                    self.driver.find_element(By.CLASS_NAME, "VfPpkd-dgl2Hf-ppHlrf-sM5MNb").click()
                self.waitUrlChange(currentUrl)
            
            elif currentUrl.find("https://accounts.google.com/speedbump/") != -1: # next step in google log in for password
                print("Speedbumping...")
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.qIypjc.TrZEUc.lw1w4b")))
                self.driver.find_element(By.CLASS_NAME, "VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.qIypjc.TrZEUc.lw1w4b").click()
                self.waitUrlChange(currentUrl)
            
            elif currentUrl.find("https://google.yrdsb.ca/LoginFormIdentityProvider/Login.aspx?") != -1: # YRDSB has stupid special login page for google accounts so it goes through that
                print("Logging in to YRDSB...")
                time.sleep(0.5)
                with open(configFile, "r") as read_file: # gets user and password from user.json and puts it into login page for YRDSB
                    data = json.load(read_file)
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "UserName")))
                    login = self.driver.find_element(By.ID, "UserName")
                    login.send_keys(data["user"]["userName"])
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Password")))
                    login = self.driver.find_element(By.ID, "Password")
                    login.send_keys(data["user"]["password"])
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "LoginButton")))
                    self.driver.find_element(By.NAME, "LoginButton").click()
                self.waitUrlChange(currentUrl)
            elif currentUrl.find("https://accounts.google.com/signin/continue?") != -1: # YRDSB has stupid special login page for google accounts so it goes through that
                self.waitUrlChange(currentURL=currentUrl, waitTime=2)
            else:
                break
        pass

    def fillForm(self):
        while True:
            currentUrl = self.driver.current_url
            if currentUrl.find("https://docs.google.com/forms/d/e/1FAIpQLSedNWLgRdQKVfNqT4gwYrq0PEJqj2vnOL5GHqfopjwnakC-0g/viewform") != -1: # fills out form 
                print("Filling out form...")
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "appsMaterialWizButtonPaperbuttonLabel.quantumWizButtonPaperbuttonLabel.exportLabel")))
                clearForm = self.driver.find_element(By.CLASS_NAME, "freebirdFormviewerViewNavigationClearButton").find_element(By.CLASS_NAME, "appsMaterialWizButtonPaperbuttonLabel.quantumWizButtonPaperbuttonLabel.exportLabel")
                clearForm.click()
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "appsMaterialWizDialogPaperdialogEl.freebirdFormviewerViewNavigationClearDialog.appsMaterialWizDialogPaperdialogTransitionZoom.appsMaterialWizDialogEl.isOpen")))
                clearFormButtons = self.driver.find_element(By.CLASS_NAME, "appsMaterialWizDialogPaperdialogEl.freebirdFormviewerViewNavigationClearDialog.appsMaterialWizDialogPaperdialogTransitionZoom.appsMaterialWizDialogEl.isOpen").find_elements(By.CLASS_NAME, "appsMaterialWizButtonPaperbuttonLabel.quantumWizButtonPaperbuttonLabel.exportLabel")
                for button in clearFormButtons:
                    if button.text == "Clear form":
                        button.click()
                # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mG61Hd > div.freebirdFormviewerViewFormCard.exportFormCard > div > div.freebirdFormviewerViewNavigationNavControls > div.freebirdFormviewerViewNavigationButtonsAndProgress.hasClearButton > div.freebirdFormviewerViewNavigationClearButton > div")))
                # clearForm = self.driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.freebirdFormviewerViewFormCard.exportFormCard > div > div.freebirdFormviewerViewNavigationNavControls > div.freebirdFormviewerViewNavigationButtonsAndProgress.hasClearButton > div.freebirdFormviewerViewNavigationClearButton > div")
                # clearForm.click()
                # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.appsMaterialWizDialogBackground.isOpen > div > div.appsMaterialWizDialogPaperdialogEl.freebirdFormviewerViewNavigationClearDialog.appsMaterialWizDialogPaperdialogTransitionZoom.appsMaterialWizDialogEl.isOpen > div.appsMaterialWizDialogPaperdialogBottomButtons.exportButtons > div:nth-child(2)")))
                # clearForm = self.driver.find_element(By.CSS_SELECTOR, "body > div.appsMaterialWizDialogBackground.isOpen > div > div.appsMaterialWizDialogPaperdialogEl.freebirdFormviewerViewNavigationClearDialog.appsMaterialWizDialogPaperdialogTransitionZoom.appsMaterialWizDialogEl.isOpen > div.appsMaterialWizDialogPaperdialogBottomButtons.exportButtons > div:nth-child(2)")
                # clearForm.click()
                time.sleep(1)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "freebirdFormviewerComponentsQuestionBaseRoot")))
                questions = self.driver.find_elements(By.CLASS_NAME, "freebirdFormviewerComponentsQuestionBaseRoot")
                print(len(questions))
                with open(configFile, "r") as read_file: # puts email in to google login from user.json
                    data = json.load(read_file)
                    for question in questions:
                        WebDriverWait(question, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "freebirdFormviewerComponentsQuestionBaseHeader")))
                        print("\""+question.find_element(By.CLASS_NAME, "freebirdFormviewerComponentsQuestionBaseHeader").text+"\"")                        
                        match (str(question.find_element(By.CLASS_NAME, "freebirdFormviewerComponentsQuestionBaseHeader").text)):
                            case "Student First Name *":
                                WebDriverWait(question, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "quantumWizTextinputPaperinputInput")))
                                textbox = question.find_element(By.CLASS_NAME, "quantumWizTextinputPaperinputInput")
                                textbox.send_keys(data["user"]["firstName"])
                            case "Student Last Name *":
                                WebDriverWait(question, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "quantumWizTextinputPaperinputInput")))
                                textbox = question.find_element(By.CLASS_NAME, "quantumWizTextinputPaperinputInput")
                                textbox.send_keys(data["user"]["lastName"])
                            case "Have you completed the self-screening test? *\nCOVID 19 School and Child Care Screening Tool is available at https://covid-19.ontario.ca/school-screening/":
                                choices = question.find_elements(By.CLASS_NAME, "freebirdFormviewerComponentsQuestionRadioChoice.freebirdFormviewerComponentsQuestionRadioOptionContainer")
                                for choice in choices:
                                    if choice.text == "Yes":
                                        choice.click()
                            case _:
                                print("Question not found")
                time.sleep(5)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "freebirdFormviewerViewNavigationLeftButtons")))
                submit = self.driver.find_element(By.CLASS_NAME, "freebirdFormviewerViewNavigationLeftButtons").find_element(By.CLASS_NAME, "appsMaterialWizButtonPaperbuttonContent")
                print(submit.text)
                # submit.click()
                self.waitUrlChange(currentUrl)
                break
            elif currentUrl.find("https://docs.google.com/forms/d/e/1FAIpQLSedNWLgRdQKVfNqT4gwYrq0PEJqj2vnOL5GHqfopjwnakC-0g/closedform") != -1: 
                print("Form is closed")
                break
            elif currentUrl.find("https://docs.google.com/forms/d/e/1FAIpQLSedNWLgRdQKVfNqT4gwYrq0PEJqj2vnOL5GHqfopjwnakC-0g/alreadyresponded") != -1:
                print("Form already answered")
                break
            elif currentUrl.find("https://docs.google.com/forms/d/e/1FAIpQLSedNWLgRdQKVfNqT4gwYrq0PEJqj2vnOL5GHqfopjwnakC-0g/closedform") != -1:
                print("Form is closed")
                break

    def run(self):
        self.setup()
        self.autoLogin()
        self.fillForm()

# Program starts running
if __name__ == '__main__':
    #login
    form = autoForm(url = "https://docs.google.com/forms/d/e/1FAIpQLSedNWLgRdQKVfNqT4gwYrq0PEJqj2vnOL5GHqfopjwnakC-0g/viewform", browserHide = False, logLevel = 3)
    form.run()
    form.quit()
    pass
