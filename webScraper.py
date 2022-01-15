import selenium, importlib
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class baseChromeWebScraper:
    """Recommended imports:\n
    import selenium\n
    from selenium import webdriver\n
    from selenium.webdriver.common.action_chains import ActionChains\n
    from selenium.webdriver.common.by import By\n
    from selenium.webdriver.chrome.service import Service\n
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities\n
    from selenium.webdriver.support.ui import WebDriverWait\n
    from selenium.webdriver.support import expected_conditions as EC\n
    """
    def __init__(self, url:str = None, webDriverPath:str = "./chromedriver", browser:str = None, browserDownloadPath:str = None, browserHide:str = False, userAgent:str = None, logLevel: int = None):
        # sets up the variables for the webscraper class
        self.url = url
        self.webDriverPath = webDriverPath
        self.browser = browser
        self.browserDownloadPath = browserDownloadPath
        self.browserHide = browserHide
        self.userAgent = userAgent
        self.logLevel = logLevel

    def waitUrlChange(self, currentURL: str, waitTime: int = 10): # function to wait for next page to load before continuing 
        try:
            WebDriverWait(self.driver, waitTime).until(lambda driver: driver.current_url != currentURL)
            return True
        except selenium.common.exceptions.TimeoutException:
            return False

    def setup(self):
        try:
            # set up
            caps = DesiredCapabilities().CHROME
            # caps["pageLoadStrategy"] = "normal"  #  complete
            # caps["pageLoadStrategy"] = "eager"  #  interactive
            # caps["pageLoadStrategy"] = "none"   #  undefined

            chromeOptions = webdriver.chrome.options.Options()
            if self.browserHide == True: # hides web browser if true
                chromeOptions.headless = True
            try:
                if self.browser: # uses chrome by default if put in another browser location trys to use that browser
                    chromeOptions.binary_location = self.browser
            except:
                print("Browser in that location does not exist")
            if self.browserDownloadPath != None:
                chromeOptions.add_experimental_option("prefs", {
                    "download.default_directory": self.browserDownloadPath,
                    "download.prompt_for_download": False # ,
                    # "download.directory_upgrade": True,
                    # "safebrowsing.enabled": True
                    })
            if self.logLevel != None:
                chromeOptions.add_argument("--log-level="+str(self.logLevel))
            if self.userAgent != None:
                chromeOptions.add_argument("user-agent="+self.userAgent)
            # initiating the webdriver. Parameter includes the path of the webdriver.
            self.driver = webdriver.Chrome(desired_capabilities=caps, service=Service(self.webDriverPath), options=chromeOptions)
            if self.url:
                self.driver.get(self.url) # goes to starting url
        except selenium.common.exceptions.WebDriverException:
            if importlib.util.find_spec("autoChromeDriver") is not None:
                import autoChromeDriver
                self.webDriverPath = autoChromeDriver.autoInstall(browserPath=self.browser)
                self.setup()
        except Exception as err:
            print("Driver initiation has stopped working\nShutting down...\n", err) # if something fails in the initiation process it shuts down

    def quit(self):
        self.driver.quit() # quits webdriver