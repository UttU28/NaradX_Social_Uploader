#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from utils import success, error, info, warning

# SELENIUM CONFIGURATION
class SeleniumConfig:
    # Chrome Data Directory (shared for both Instagram and YouTube)
    CHROME_DATA_DIR = r"chromeData\elitevocabulary"
    
    # Common Configuration
    DEBUGGING_PORT = '9004'
    CHROMEDRIVER_PATH = r"C:\Users\utsav\OneDrive\Desktop\NaradX_Social_Uploader\chromedriver.exe"
    
    # YouTube specific
    YOUTUBE_CHANNEL_ID = 'UC2z9JFAIFovJsyt2iwKOn3g'
    
    @staticmethod
    def get_chrome_path():
        """Get Chrome executable path for current OS"""
        if os.name == "nt":
            chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            if not os.path.exists(chrome_path):
                chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        else:
            chrome_path = "/usr/bin/google-chrome"
            if not os.path.exists(chrome_path):
                chrome_path = "/usr/bin/google-chrome-stable"
            if not os.path.exists(chrome_path):
                chrome_path = "/snap/bin/chromium"
            if not os.path.exists(chrome_path):
                try:
                    chrome_path = subprocess.check_output(["which", "google-chrome"], text=True).strip()
                except subprocess.CalledProcessError:
                    try:
                        chrome_path = subprocess.check_output(["which", "chrome"], text=True).strip()
                    except subprocess.CalledProcessError:
                        print(error("Chrome executable not found. Please install Chrome."))
                        sys.exit(1)
        
        return chrome_path
    
    @staticmethod
    def create_chrome_options():
        """Create Chrome options with common settings"""
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", f"localhost:{SeleniumConfig.DEBUGGING_PORT}")
        return chrome_options
    
    @staticmethod
    def create_chrome_service():
        """Create Chrome service with chromedriver"""
        return Service(executable_path=SeleniumConfig.CHROMEDRIVER_PATH)
    
    @staticmethod
    def get_chrome_args(chrome_data_dir, url):
        """Get Chrome command line arguments"""
        chrome_path = SeleniumConfig.get_chrome_path()
        return [
            chrome_path,
            f"--remote-debugging-port={SeleniumConfig.DEBUGGING_PORT}",
            f"--user-data-dir={chrome_data_dir}",
            "--disable-notifications",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--disable-plugins",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
            "--disable-ipc-flooding-protection",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            f"--profile-directory=Profile_{SeleniumConfig.DEBUGGING_PORT}",
            url
        ]
    
    @staticmethod
    def kill_chrome_on_debugging_port():
        """Kill Chrome processes using our specific debugging port"""
        try:
            if os.name == "nt":
                # Windows - Find processes using our specific port
                cmd = f'netstat -ano | findstr :{SeleniumConfig.DEBUGGING_PORT}'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0 and result.stdout:
                    lines = result.stdout.strip().split('\n')
                    pids = set()
                    for line in lines:
                        parts = line.split()
                        if len(parts) >= 5:
                            pid = parts[-1]
                            if pid.isdigit():
                                pids.add(pid)
                    
                    for pid in pids:
                        try:
                            subprocess.run(["taskkill", "/F", "/PID", pid], 
                                         capture_output=True, check=False)
                            print(info(f"🔄 Closed Chrome process on port {SeleniumConfig.DEBUGGING_PORT} (PID: {pid})"))
                        except:
                            pass
                else:
                    print(info(f"ℹ️ No Chrome process found on port {SeleniumConfig.DEBUGGING_PORT}"))
            else:
                # Linux/Ubuntu - Find processes using our specific port
                cmd = f"lsof -ti:{SeleniumConfig.DEBUGGING_PORT}"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0 and result.stdout:
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        if pid.isdigit():
                            try:
                                subprocess.run(["kill", "-9", pid], 
                                             capture_output=True, check=False)
                                print(info(f"🔄 Closed process on port {SeleniumConfig.DEBUGGING_PORT} (PID: {pid})"))
                            except:
                                pass
                else:
                    print(info(f"ℹ️ No process found on port {SeleniumConfig.DEBUGGING_PORT}"))
            
            time.sleep(1)
        except Exception as e:
            print(warning(f"⚠️ Could not close processes on port {SeleniumConfig.DEBUGGING_PORT}: {e}"))

    @staticmethod
    def start_chrome_process(chrome_data_dir, url):
        """Start Chrome process with specified data directory and URL"""
        # Create chrome data directory if it doesn't exist
        chrome_data_dir = os.path.abspath(chrome_data_dir)
        os.makedirs(chrome_data_dir, exist_ok=True)
        
        print(info(f"🗂️ Using Chrome data directory: {chrome_data_dir}"))
        
        # Kill Chrome processes using our debugging port to avoid conflicts
        SeleniumConfig.kill_chrome_on_debugging_port()
        
        chrome_args = SeleniumConfig.get_chrome_args(chrome_data_dir, url)
        print(info(f"🚀 Starting Chrome with debugging port {SeleniumConfig.DEBUGGING_PORT}"))
        
        chrome_process = subprocess.Popen(chrome_args)
        time.sleep(5)  # Give Chrome more time to start properly
        return chrome_process
    
    @staticmethod
    def wait_for_debugging_port():
        """Wait for Chrome debugging port to be available"""
        import socket
        import time
        
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex(('localhost', int(SeleniumConfig.DEBUGGING_PORT)))
                    if result == 0:
                        print(success(f"✅ Chrome debugging port {SeleniumConfig.DEBUGGING_PORT} is ready"))
                        return True
            except Exception:
                pass
            
            print(info(f"⏳ Waiting for Chrome debugging port... (attempt {attempt + 1}/{max_attempts})"))
            time.sleep(2)
        
        print(error(f"❌ Chrome debugging port {SeleniumConfig.DEBUGGING_PORT} not available"))
        return False

    @staticmethod
    def create_driver():
        """Create WebDriver instance"""
        # Wait for debugging port to be ready
        if not SeleniumConfig.wait_for_debugging_port():
            raise Exception("Chrome debugging port not available")
        
        chrome_options = SeleniumConfig.create_chrome_options()
        service = SeleniumConfig.create_chrome_service()
        return webdriver.Chrome(service=service, options=chrome_options)
    
    @staticmethod
    def close_chrome_session(driver, chrome_process):
        """Safely close Chrome driver and process"""
        try:
            driver.quit()
            print(info("🔒 Closing Chrome session..."))
            chrome_process.terminate()
            chrome_process.wait(timeout=5)
            print(success("✅ Chrome session closed"))
        except Exception as e:
            print(warning(f"⚠️ Error closing Chrome: {e}"))
            try:
                chrome_process.kill()
            except:
                pass

# Platform-specific utilities
class PlatformUtils:
    @staticmethod
    def handle_file_upload(video_path):
        """Handle file upload based on platform"""
        if os.name == "nt":
            import pyautogui
            try:
                pyautogui.typewrite(video_path, interval=0.05)
                time.sleep(0.5)
                pyautogui.press('enter')
                print(success("✅ File selected (Windows)"))
            except Exception as e:
                print(error(f"❌ File upload error: {e}"))
                raise
        else:
            # This should be handled by the calling function for Ubuntu
            # as it requires finding the file input element
            pass

# Common Selenium utilities
class SeleniumUtils:
    @staticmethod
    def chunked_typing(element, text, chunk_size=50, delay=0.5):
        """Type text in chunks to avoid issues with long strings"""
        try:
            for i in range(0, len(text), chunk_size):
                chunk = text[i:i+chunk_size]
                element.send_keys(chunk)
                time.sleep(delay)
            return True
        except Exception as e:
            print(error(f"❌ Chunked typing error: {e}"))
            return False
    
    @staticmethod
    def set_text_with_fallback(driver, element, text):
        """Set text with multiple fallback methods"""
        try:
            # Method 1: Chunked typing
            if SeleniumUtils.chunked_typing(element, text):
                return True
        except:
            pass
        
        try:
            # Method 2: JavaScript
            driver.execute_script("arguments[0].innerText = arguments[1]", element, text)
            return True
        except:
            pass
        
        try:
            # Method 3: Simple send_keys
            element.send_keys(text)
            return True
        except:
            pass
        
        return False
    
    @staticmethod
    def clear_field_with_fallback(driver, element):
        """Clear input field with multiple fallback methods"""
        try:
            # Method 1: Ctrl+A + Delete
            from selenium.webdriver.common.keys import Keys
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            return True
        except:
            pass
        
        try:
            # Method 2: ActionChains
            from selenium.webdriver.common.action_chains import ActionChains
            from selenium.webdriver.common.keys import Keys
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
            element.send_keys(Keys.DELETE)
            return True
        except:
            pass
        
        try:
            # Method 3: JavaScript
            driver.execute_script("arguments[0].innerText = ''", element)
            return True
        except:
            pass
        
        return False 