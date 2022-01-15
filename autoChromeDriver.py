import os, sys, requests, zipfile
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, SoupStrainer

def autoInstall(browserPath = None):
    def getLinkFromKeyword(site, keyword): #gets chrome driver version link from the site and current version of browser
        req = Request(site)
        html_page = urlopen(req) # gets webpage data

        soup = BeautifulSoup(html_page, features="lxml", parse_only=SoupStrainer('a')) # into bs object

        links = []
        for link in soup.findAll('a'): # goes throught all the links in the html file and gets the ones with the keyword
            if keyword in str(link.get('href')):
                links.append(link.get('href'))
        return links[0] # returns first instance as it is probably 99% of the time the correct link
    
    def downloadDriver(downloadPage: str, osType): # gets driver version then inserts it in to the download link for supported os
        downloadUrlBase = "https://chromedriver.storage.googleapis.com/"
        osTypeToDriverZip = {
            "win32":"chromedriver_win32.zip",
            "linux":"chromedriver_linux64.zip"
        }
        url = downloadUrlBase+downloadPage[downloadPage.find("path=")+5:]+osTypeToDriverZip[osType] # the combining
        r = requests.get(url, allow_redirects=True)
        with open(os.path.join(sys.path[0], osTypeToDriverZip[osType]), 'wb') as file:
            file.write(r.content)
            file.close()
        return os.path.join(sys.path[0], osTypeToDriverZip[osType])

    def extractDriver(filePath):
        with zipfile.ZipFile(filePath) as zip_ref:
            zip_ref.extractall(os.path.dirname(filePath))
            zip_ref.close()
        os.remove(filePath)
        return os.path.dirname(filePath)+"/chromedriver"

    chromeDriverSite = "https://chromedriver.chromium.org/downloads"
    if sys.platform == "win32": # checks to see if platform is windows
        if sys.getwindowsversion().major == 10: # checks to see if running windows 10
            possiblePaths = [os.environ["ProgramFiles"]+"\Google\Chrome\Application\chrome.exe",os.environ["ProgramFiles(x86)"]+"\Google\Chrome\Application\chrome.exe",os.environ["LocalAppData"]+"\Google\Chrome\Application\chrome.exe"]
            if browserPath == None: # if browser path is not predetermined runs through expected locations
                for path in possiblePaths:
                    if os.path.isfile(path):
                        browserPath = path
                        break
                    elif path == possiblePaths[-1]:
                        print("Chrome browser not found please download or set explicit location")
                        exit()
            else:
                if os.path.isfile(browserPath) == False: 
                    print(browserPath,"is not a valid path to file")
                    exit()
            version = os.popen("wmic datafile where 'name=\""+browserPath.replace("\\", "\\\\").replace("/", "\\\\")+"\"' get version").read().splitlines()[2] # wmic datafile where 'name="C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"' get version
            finalDriverPath = extractDriver(downloadDriver(downloadPage=getLinkFromKeyword(site=chromeDriverSite, keyword=version.split(".")[0]), osType=sys.platform))
        else:
            raise Exception("Automatic drivers unable to be downloaded for Windows "+str(sys.getwindowsversion().major)+" go to \""+chromeDriverSite+"\" to download manually for your chrome based browser and put in the folder \""+os.path.dirname(__file__)+"\"")
    elif sys.platform == "linux":
        possiblePaths = ["/usr/bin/google-chrome"]
        if browserPath == None: # if browser path is not predetermined runs through expected locations
            for path in possiblePaths:
                if os.path.isfile(path):
                    browserPath = path
                    break
                elif path == possiblePaths[-1]:
                    print("Chrome browser not found please download or set explicit location")
                    exit()
        else:
            if os.path.isfile(browserPath) == False: 
                print(browserPath,"is not a valid path to file")
                exit()
        version = os.popen(browserPath+" --version").read().split(" ")[-2]
        finalDriverPath = extractDriver(downloadDriver(downloadPage=getLinkFromKeyword(site=chromeDriverSite, keyword=version.split(".")[0]), osType=sys.platform))
        os.chmod(finalDriverPath, 755)
    else:
        raise Exception("Automatic drivers unable to be downloaded for "+sys.platform+" go to \""+chromeDriverSite+"\" to download manually for your chrome based browser and put in the folder \""+os.path.dirname(__file__)+"\"")
    return finalDriverPath

if __name__=="__main__":
    autoInstall()