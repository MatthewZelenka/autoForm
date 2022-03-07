from dataclasses import dataclass
from lib.webScraper import *
from typing import Protocol
import time

# protocol for question inputs
@dataclass(order=True)
class question(Protocol):
    question:str 
    answer:str
    def fill(self) -> None:
        """question type for google forms"""

# question types
@dataclass(order=True)
class textbox():
    question:str 
    answer:str
    def fill(self, question) -> None:
        # gets textbox web element from question
        WebDriverWait(question, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "whsOnd.zHQkBf")))
        textbox = question.find_element(By.CLASS_NAME, "whsOnd.zHQkBf")
        textbox.send_keys(self.answer)

@dataclass(order=True)
class multipleChoice():
    question:str 
    answer:str
    def fill(self, question) -> None:
        # gets choices web elements from question
        WebDriverWait(question, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "nWQGrd.zwllIb")))
        choices = question.find_elements(By.CLASS_NAME, "nWQGrd.zwllIb")
        for choice in choices:
            if choice.text in self.answer:
                WebDriverWait(question, 10).until(EC.element_to_be_clickable(choice))
                choice.click()

# clears full form
def clearAll(self):
    # gets web element for the clear form button
    try:
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "uArJ5e.UQuaGc.kCyAyd.l3F1ye.TFBnVe")))
        clearForm = self.driver.find_element(By.CLASS_NAME, "uArJ5e.UQuaGc.kCyAyd.l3F1ye.TFBnVe")
    except:
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "uArJ5e.UQuaGc.kCyAyd.l3F1ye.TFBnVe.M9Bg4d")))
        clearForm = self.driver.find_element(By.CLASS_NAME, "uArJ5e.UQuaGc.kCyAyd.l3F1ye.TFBnVe.M9Bg4d")
    clearForm.click()

    # gets web elements for the two buttons in the clear form menu and clicks the clear form button
    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "OE6hId.J9fJmf")))
    clearFormButtonsMenu = self.driver.find_element(By.CLASS_NAME, "OE6hId.J9fJmf")
    # gets web elements for buttons and checks under 2 classes because they change when interacted in some way
    clearFormButtons = []
    clearFormButtons.extend(clearFormButtonsMenu.find_elements(By.CLASS_NAME, "uArJ5e.UQuaGc.kCyAyd.ARrCac"))
    clearFormButtons.extend(clearFormButtonsMenu.find_elements(By.CLASS_NAME, "uArJ5e.UQuaGc.kCyAyd.ARrCac.M9Bg4d"))
    for button in clearFormButtons: # goes through every element and if it still exists then check to see if its the clear form button then click if it is
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(button))
            if button.text == "Clear form":
                button.click()
        except exceptions.StaleElementReferenceException:
            continue
    # checks to see if button dialog is invisibile
    WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "OE6hId.J9fJmf")))

# get form state
def getFormState(self):
    url = self.driver.current_url
    match(url[url.rindex("/"):]):
        case "/closedform":
            return "closed"
        case "/alreadyresponded":
            return "answered"
        case "/viewform":
            return "uncomplete"
        case "/formResponse":
            return "compleated"
        case _:
            return "unknown"

# fills form
def fillForm(self, *questionAnswers: question):
    for _ in range(3):
        try:
            # gets question elements form the form
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Qr7Oae")))
            questions = self.driver.find_elements(By.CLASS_NAME, "Qr7Oae")
            for question in questions:
                qTry = 1
                # Gets web element text
                try: # need to add this in as items that are not questions can be inclueded
                    WebDriverWait(question, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "z12JJ")))
                except exceptions.TimeoutException:
                    continue
                for answer in questionAnswers:
                    if answer.question == str(question.find_element(By.CLASS_NAME, "z12JJ").text): # if web element text is same as answer text it completes it
                        answer.fill(question)
                        print("Answered question", qTry)
                        break
                    elif qTry == len(questionAnswers): # WIP try and figure out indexing answer because it was jumping by 2 before and not getting to the end questionAnswers.index(answer)
                        print("Question not found\n{}\nStoping form fillout".format(repr(str(question.find_element(By.CLASS_NAME, "z12JJ").text))))
                        return
                    qTry += 1
            break
        except exceptions.StaleElementReferenceException:
            self.waitUrlChange(currentURL=self.driver.current_url, waitTime=0.5)
    

# submits form
def submit(self):
    # gets web element for the submit button
    try:
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "uArJ5e.UQuaGc.Y5sE8d.VkkpIf.NqnGTe")))
        submit = self.driver.find_element(By.CLASS_NAME, "uArJ5e.UQuaGc.Y5sE8d.VkkpIf.NqnGTe")
    except:
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "uArJ5e.UQuaGc.Y5sE8d.VkkpIf.NqnGTe.M9Bg4d")))
        submit = self.driver.find_element(By.CLASS_NAME, "uArJ5e.UQuaGc.Y5sE8d.VkkpIf.NqnGTe.M9Bg4d")
    submit.click()
