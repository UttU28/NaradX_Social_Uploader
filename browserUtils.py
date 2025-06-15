import os
import sys
import time
import logging
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from config import success, error, info, warning, highlight

class BrowserManager:
    def __init__(self, profiles, profileName):
        if profileName not in profiles:
            print(error(f"❌ Profile '{profileName}' not found"))
            sys.exit(1)
            
        self.profile = profiles[profileName]
        self.chromeDataDir = self.profile["chromeDataDir"]
        self.debuggingPort = self.profile["debuggingPort"]
        self.profileName = profileName
        
        # Set chromedriver path with proper extension for Windows
        chromeDriverName = "chromedriver.exe" if os.name == "nt" else "chromedriver"
        self.chromeDriverPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), chromeDriverName)
        
        self.chromeProcess = None
        self.driver = None
        
        print(info(f"🔧 Using profile: {self.profileName}"))
        
    def pathStr(self, path):
        return os.path.normpath(path)
    
    def getChromePath(self):
        if os.name == "nt":
            chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            if not os.path.exists(chromePath):
                chromePath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        else:
            chromePath = "/usr/bin/google-chrome"
            if not os.path.exists(chromePath):
                chromePath = "/usr/bin/google-chrome-stable"
            if not os.path.exists(chromePath):
                chromePath = "/snap/bin/chromium"
            if not os.path.exists(chromePath):
                try:
                    chromePath = subprocess.check_output(["which", "google-chrome"], text=True).strip()
                except subprocess.CalledProcessError:
                    try:
                        chromePath = subprocess.check_output(["which", "chrome"], text=True).strip()
                    except subprocess.CalledProcessError:
                        print(error("❌ Chrome not found. Please install Chrome."))
                        sys.exit(1)
        
        return chromePath
    
    def startBrowser(self, url):
        try:
            chromePath = self.getChromePath()
            userDataDir = self.pathStr(self.chromeDataDir)
            
            if not os.path.exists(userDataDir):
                os.makedirs(userDataDir, exist_ok=True)
                print(info(f"📁 Created profile directory: {userDataDir}"))
            
            chromeArgs = [
                chromePath,
                f"--remote-debugging-port={self.debuggingPort}",
                f"--user-data-dir={userDataDir}",
                "--disable-notifications",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-blink-features=AutomationControlled",
                url
            ]
            
            self.chromeProcess = subprocess.Popen(chromeArgs)
            time.sleep(2)
            
            chromeOptions = Options()
            chromeOptions.add_experimental_option("debuggerAddress", f"localhost:{self.debuggingPort}")
            
            service = Service(executable_path=self.chromeDriverPath)
            self.driver = webdriver.Chrome(service=service, options=chromeOptions)
            
            osName = "Windows" if os.name == "nt" else "Ubuntu"
            print(success(f"✅ Connected to Chrome ({osName}) - Profile: {self.profileName}"))
            return True
            
        except Exception as e:
            print(error(f"❌ Browser startup error: {e}"))
            return False
    
    def closeBrowser(self):
        try:
            if self.driver:
                self.driver.quit()
                print(info(f"🔒 Closing Chrome session for {self.profileName}..."))
            
            if self.chromeProcess:
                self.chromeProcess.terminate()
                self.chromeProcess.wait(timeout=5)
                print(success(f"✅ Chrome session closed for {self.profileName}"))
                
        except Exception as e:
            print(warning(f"⚠️ Error closing Chrome for {self.profileName}: {e}"))
            try:
                if self.chromeProcess:
                    self.chromeProcess.kill()
            except:
                pass

def setupLogging(logFile, profileName):
    os.makedirs('logs', exist_ok=True)
    logPath = os.path.join('logs', f"{profileName}_{logFile}")
    
    logging.basicConfig(
        filename=logPath,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(logFile.replace('.log', '')) 