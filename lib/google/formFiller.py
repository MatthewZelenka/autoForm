from dataclasses import dataclass
from lib.webScraper import *
from typing import Protocol
import time

# protical for question inputs
@dataclass
class question(Protocol):
    def fill(self) -> None:
        """question type for google forms"""

# question types
@dataclass
class textbox():
    def __init__(self, question:str, answer:str) -> None:
        self.question = question
        self.answer = answer
    def fill(self, question) -> None:
        WebDriverWait(question, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "quantumWizTextinputPaperinputInput")))
        textbox = question.find_element(By.CLASS_NAME, "quantumWizTextinputPaperinputInput")
        textbox.send_keys(self.answer)

@dataclass
class multipleChoice():
    def __init__(self, question:str, answer:list[str]) -> None:
        self.question = question
        self.answer = answer
    def fill(self, question) -> None:
        choices = question.find_elements(By.CLASS_NAME, "freebirdFormviewerComponentsQuestionRadioChoice.freebirdFormviewerComponentsQuestionRadioOptionContainer")
        for choice in choices:
            if choice.text in self.answer:
                choice.click()

# clears full form
def clearAll(self):
    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "appsMaterialWizButtonPaperbuttonLabel.quantumWizButtonPaperbuttonLabel.exportLabel")))
    clearForm = self.driver.find_element(By.CLASS_NAME, "freebirdFormviewerViewNavigationClearButton").find_element(By.CLASS_NAME, "appsMaterialWizButtonPaperbuttonLabel.quantumWizButtonPaperbuttonLabel.exportLabel")
    clearForm.click()
    
    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "appsMaterialWizDialogPaperdialogEl.freebirdFormviewerViewNavigationClearDialog.appsMaterialWizDialogPaperdialogTransitionZoom.appsMaterialWizDialogEl.isOpen")))
    clearFormButtons = self.driver.find_element(By.CLASS_NAME, "appsMaterialWizDialogPaperdialogEl.freebirdFormviewerViewNavigationClearDialog.appsMaterialWizDialogPaperdialogTransitionZoom.appsMaterialWizDialogEl.isOpen").find_elements(By.CLASS_NAME, "appsMaterialWizButtonPaperbuttonLabel.quantumWizButtonPaperbuttonLabel.exportLabel")
    for button in clearFormButtons:
        if button.text == "Clear form":
            button.click()
    time.sleep(1) # gotta get rid of this

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

# fills form
def fillForm(self, *questionAnswers: question):
    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "freebirdFormviewerComponentsQuestionBaseRoot")))
    questions = self.driver.find_elements(By.CLASS_NAME, "freebirdFormviewerComponentsQuestionBaseRoot")
    for question in questions:
        qTry = 1
        WebDriverWait(question, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "freebirdFormviewerComponentsQuestionBaseHeader")))
        for answer in questionAnswers:
            if answer.question == str(question.find_element(By.CLASS_NAME, "freebirdFormviewerComponentsQuestionBaseHeader").text):
                answer.fill(question)
                print("Answered question", qTry)
                break
            elif qTry == len(questionAnswers): # try and figure out indexing answer because it was jumping by 2 before and not getting to the end questionAnswers.index(answer)
                print("Question not found\n{}\nStoping form fillout".format(repr(str(question.find_element(By.CLASS_NAME, "freebirdFormviewerComponentsQuestionBaseHeader").text))))
                return
            qTry += 1

# submits form
def submit(self):
    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "freebirdFormviewerViewNavigationLeftButtons")))
    submit = self.driver.find_element(By.CLASS_NAME, "freebirdFormviewerViewNavigationLeftButtons").find_element(By.CLASS_NAME, "appsMaterialWizButtonPaperbuttonContent")
    submit.click()
