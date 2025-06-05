#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import success, error, info, warning, highlight

# HARDCODED VARIABLES - Direct paths
CHROME_DATA_DIR = r"C:\Users\utsav\chromeData\instagramChromeData"  # Direct path to chrome data
DEBUGGING_PORT = '9004'
CHROMEDRIVER_PATH = r"C:\Users\utsav\OneDrive\Desktop\NaradX_Social_Uploader\chromedriver.exe"  # Direct path to chromedriver

def getChromePath():
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
                    print(error("Chrome executable not found. Please install Chrome."))
                    sys.exit(1)
    
    return chromePath

def automateInstagramActions(debuggingPort, videoPath, caption="Instagram said 'post daily' — so here's me being obedient."):
    try:
        chromeOptions = Options()
        chromeOptions.add_experimental_option("debuggerAddress", f"localhost:{debuggingPort}")
        
        # Use the specific chromedriver
        service = Service(executable_path=CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chromeOptions)
        
        print(info("Connected to Chrome. Starting automation..."))
        
        createButton = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create')]"))
        )
        createButton.click()
        
        if os.name == "nt":
            import pyautogui
            selectButton = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Select from computer')]"))
            )
            selectButton.click()
            
            time.sleep(2)
            pyautogui.write(videoPath, interval=0.05)
            time.sleep(1)
            pyautogui.press('enter')
            print(success(f"Selected video: {os.path.basename(videoPath)}"))
        else:
            time.sleep(2)
            try:
                uploadInput = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                )
                uploadInput.send_keys(videoPath)
                print(success(f"Selected video (Ubuntu method): {os.path.basename(videoPath)}"))
            except Exception as e:
                print(error(f"Could not find file input to upload video: {e}"))
                raise

        time.sleep(5)
        
        try:
            try:
                cropButtonContainer = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='_abfz _abg1' and @role='button']"))
                )
                cropButtonContainer.click()
            except Exception:
                try:
                    cropButton = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[.//svg[@aria-label='Select crop']]"))
                    )
                    cropButton.click()
                except Exception:
                    try:
                        cropSvg = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//svg[@aria-label='Select crop']"))
                        )
                        cropSvg.click()
                    except Exception:
                        raise Exception("Could not find crop button")
            
            time.sleep(2)
            try:
                originalOption = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Original']"))
                )
                originalOption.click()
            except Exception:
                try:
                    originalOption = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Original')]"))
                    )
                    originalOption.click()
                except Exception:
                    raise Exception("Could not select Original format")
            
            time.sleep(2)
            
            try:
                nextButton = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Next']"))
                )
                nextButton.click()
            except Exception:
                try:
                    nextButton = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[text()='Next']"))
                    )
                    nextButton.click()
                except Exception:
                    raise Exception("Could not click first Next button")
            
            time.sleep(3)
            
            try:
                nextButton2 = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Next']"))
                )
                nextButton2.click()
            except Exception:
                try:
                    nextButton2 = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[text()='Next']"))
                    )
                    nextButton2.click()
                except Exception:
                    raise Exception("Could not click second Next button")
            
            time.sleep(3)
            
            try:
                captionField = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Write a caption...']"))
                )
                captionField.click()
                time.sleep(1)
                
                # Type the caption in smaller chunks to avoid issues
                chunk_size = 50
                for i in range(0, len(caption), chunk_size):
                    chunk = caption[i:i+chunk_size]
                    captionField.send_keys(chunk)
                    time.sleep(0.5)  # Small pause between chunks
            except Exception:
                try:
                    captionField = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@role='textbox']"))
                    )
                    captionField.click()
                    time.sleep(1)
                    
                    # Type the caption in smaller chunks to avoid issues
                    chunk_size = 50
                    for i in range(0, len(caption), chunk_size):
                        chunk = caption[i:i+chunk_size]
                        captionField.send_keys(chunk)
                        time.sleep(0.5)  # Small pause between chunks
                except Exception:
                    try:
                        captionField = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
                        
                        # Use JavaScript to set the caption in case the typing method fails
                        try:
                            driver.execute_script("arguments[0].innerText = arguments[1]", captionField, caption)
                        except:
                            # Fallback: Try to set the caption in smaller chunks
                            driver.execute_script("arguments[0].innerText = ''", captionField)
                            chunk_size = 50
                            for i in range(0, len(caption), chunk_size):
                                chunk = caption[i:i+chunk_size]
                                current = driver.execute_script("return arguments[0].innerText", captionField)
                                driver.execute_script("arguments[0].innerText = arguments[1]", captionField, current + chunk)
                                time.sleep(0.5)
                    except Exception:
                        raise Exception("Could not enter caption")
            
            print(success("Added caption"))
            
            try:
                accessibilityButton = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Accessibility']"))
                )
                accessibilityButton.click()
            except Exception:
                try:
                    accessibilityDiv = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[.//span[contains(text(), 'Accessibility')]]"))
                    )
                    accessibilityDiv.click()
                except Exception:
                    raise Exception("Could not click Accessibility button")
            
            time.sleep(2)
            
            try:
                captionsToggle = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@role='switch']"))
                )
                if captionsToggle.get_attribute("aria-checked") == "false":
                    captionsToggle.click()
            except Exception:
                try:
                    captionsSection = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Auto-generated captions')]"))
                    )
                    captionsToggle = captionsSection.find_element(By.XPATH, "./following::input[@type='checkbox']")
                    if captionsToggle.get_attribute("aria-checked") == "false":
                        captionsToggle.click()
                except Exception:
                    print(warning("Could not enable auto-generated captions"))
            
            print(success("Enabled auto-generated captions"))
            
            # Click the share/submit button to post the content
            time.sleep(2)
            try:
                shareButton = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Share']"))
                )
                shareButton.click()
                print(success("Clicked Share button to post content"))
                
                # Wait for post completion confirmation message (up to 1 minute)
                try:
                    success_message = WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Your reel has been shared')]"))
                    )
                    print(success("Post has been shared successfully - confirmation message detected"))
                except Exception as e:
                    print(warning(f"Warning: Could not detect share confirmation message: {e}"))
                    # Continue anyway as the post might still have been successful
            except Exception:
                try:
                    shareButton = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[text()='Share']"))
                    )
                    shareButton.click()
                    print(success("Clicked Share button to post content"))
                    
                    # Wait for post completion confirmation message (up to 1 minute)
                    try:
                        success_message = WebDriverWait(driver, 60).until(
                            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Your reel has been shared')]"))
                        )
                        print(success("Post has been shared successfully - confirmation message detected"))
                    except Exception as e:
                        print(warning(f"Warning: Could not detect share confirmation message: {e}"))
                        # Continue anyway as the post might still have been successful
                except Exception as e:
                    print(error(f"Could not click Share button: {e}"))
            
        except Exception as e:
            print(error(f"Error: {e}"))
        
        print(success("Automation completed"))
        return True
        
    except Exception as e:
        print(error(f"Error: {e}"))
        return False

def uploadToInstagram(videoPath, caption):
    """
    Upload a video to Instagram
    
    Args:
        videoPath (str): Full path to the video file
        caption (str): The caption to use for the Instagram post
    
    Returns:
        bool: Whether the upload was successful
    """
    start_time = time.time()
    
    print(highlight(f"\n=== Instagram Upload Started ==="))
    print(info(f"Video: {os.path.basename(videoPath)}"))
    print(info(f"Caption: {caption[:50]}..."))
    
    try:
        # Create chrome data directory if it doesn't exist
        os.makedirs(CHROME_DATA_DIR, exist_ok=True)
        
        chromePath = getChromePath()
        
        if not os.path.exists(videoPath):
            print(error(f"Error: Video file {videoPath} not found"))
            return False
        
        url = 'https://www.instagram.com/'
        
        print(info(f"Starting upload process..."))
        
        chromeArgs = [
            chromePath,
            f"--remote-debugging-port={DEBUGGING_PORT}",
            f"--user-data-dir={CHROME_DATA_DIR}",
            "--disable-notifications",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-blink-features=AutomationControlled",
            url
        ]
        
        try:
            chromeProcess = subprocess.Popen(chromeArgs)
            time.sleep(5)
            
            # Call the Instagram automation function
            result = automateInstagramActions(DEBUGGING_PORT, videoPath, caption)
            time.sleep(5)
            
            print(info("Complete the process in the browser. Press Ctrl+C to close Chrome."))
            
            print(info("\nClosing Chrome..."))
            try:
                chromeProcess.terminate()
                chromeProcess.wait(timeout=5)
            except:
                chromeProcess.kill()        
        except KeyboardInterrupt:
            print(info("\nClosing Chrome..."))
            try:
                chromeProcess.terminate()
                chromeProcess.wait(timeout=5)
            except:
                chromeProcess.kill()
        
        except Exception as e:
            print(error(f"Error: {e}"))
            return False
        
        end_time = time.time()
        duration = end_time - start_time
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        
        if result:
            print(success(f"Instagram upload completed successfully in {minutes}m {seconds}s"))
            return True
        else:
            print(error(f"Instagram upload failed"))
            return False
    
    except Exception as e:
        print(error(f"Error during Instagram upload: {e}"))
        return False

if __name__ == "__main__":
    # Example usage with direct video path
    videoPath = r"C:\Users\utsav\Videos\Balk.mp4"  # Direct path to video
    caption = "BALK means to hesitate or refuse to proceed; to stop short and refuse to continue.\n\n#GREprep #IELTSvocab #wordoftheday #englishwithstyle #speaklikeanative #studygram #vocabularyboost #learnenglish #englishreels #explorepage #IELTSpreparation #englishvocabulary #spokenenglish #studymotivation #englishlearning #dailyvocab #englishpractice #fluencygoals #vocabchallenge #englishtips #educationreels #englishgrammar #ieltsvocab #smartvocab"
    
    uploadToInstagram(videoPath, caption) 