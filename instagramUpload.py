#!/usr/bin/env python3
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import success, error, info, warning, highlight, profiles
from browserUtils import BrowserManager, setupLogging

if os.name == "nt":
    import pyautogui

def automateInstagramActions(driver, videoPath=None, caption="Instagram said 'post daily' — so here's me being obedient."):
    try:
        print(info("🔄 Starting Instagram automation..."))
        
        createButton = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create')]"))
        )
        createButton.click()
        
        if videoPath:
            if os.name == "nt":
                selectButton = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Select from computer')]"))
                )
                selectButton.click()
                
                time.sleep(2)
                pyautogui.write(videoPath, interval=0.05)
                time.sleep(1)
                pyautogui.press('enter')
                print(success(f"✅ Selected: {os.path.basename(videoPath)}"))
            else:
                time.sleep(2)
                try:
                    uploadInput = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                    )
                    uploadInput.send_keys(videoPath)
                    print(success(f"✅ Selected: {os.path.basename(videoPath)}"))
                except Exception as e:
                    print(error(f"❌ Upload error: {e}"))
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
                            raise Exception("Crop button not found")
                
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
                        raise Exception("Original format not found")
                
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
                        raise Exception("Next button not found")
                
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
                        raise Exception("Second Next button not found")
                
                time.sleep(3)
                
                try:
                    captionField = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Write a caption...']"))
                    )
                    captionField.click()
                    time.sleep(1)
                    
                    chunkSize = 50
                    for i in range(0, len(caption), chunkSize):
                        chunk = caption[i:i+chunkSize]
                        captionField.send_keys(chunk)
                        time.sleep(0.5)
                except Exception:
                    try:
                        captionField = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//div[@role='textbox']"))
                        )
                        captionField.click()
                        time.sleep(1)
                        
                        chunkSize = 50
                        for i in range(0, len(caption), chunkSize):
                            chunk = caption[i:i+chunkSize]
                            captionField.send_keys(chunk)
                            time.sleep(0.5)
                    except Exception:
                        try:
                            captionField = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
                            
                            try:
                                driver.execute_script("arguments[0].innerText = arguments[1]", captionField, caption)
                            except:
                                driver.execute_script("arguments[0].innerText = ''", captionField)
                                chunkSize = 50
                                for i in range(0, len(caption), chunkSize):
                                    chunk = caption[i:i+chunkSize]
                                    current = driver.execute_script("return arguments[0].innerText", captionField)
                                    driver.execute_script("arguments[0].innerText = arguments[1]", captionField, current + chunk)
                                    time.sleep(0.5)
                        except Exception:
                            raise Exception("Caption field not found")
                
                print(success("✅ Caption added"))
                
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
                        raise Exception("Accessibility button not found")
                
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
                        print(warning("⚠️ Auto-captions not enabled"))
                
                print(success("✅ Captions enabled"))
                
                time.sleep(2)
                try:
                    shareButton = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Share']"))
                    )
                    shareButton.click()
                    print(success("✅ Share button clicked"))
                    
                    try:
                        success_message = WebDriverWait(driver, 60).until(
                            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Your reel has been shared')]"))
                        )
                        print(success("✅ Post shared successfully"))
                    except Exception as e:
                        print(warning(f"⚠️ Share confirmation not detected: {e}"))
                except Exception:
                    try:
                        shareButton = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//*[text()='Share']"))
                        )
                        shareButton.click()
                        print(success("✅ Share button clicked"))
                        
                        try:
                            success_message = WebDriverWait(driver, 60).until(
                                EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Your reel has been shared')]"))
                            )
                            print(success("✅ Post shared successfully"))
                        except Exception as e:
                            print(warning(f"⚠️ Share confirmation not detected: {e}"))
                    except Exception as e:
                        print(error(f"❌ Share error: {e}"))
                
            except Exception as e:
                print(error(f"❌ Error: {e}"))
        
        print(success("✅ Automation complete"))
        return True
        
    except Exception as e:
        print(error(f"❌ Error: {e}"))
        return False

def uploadToInstagram(profileName, word, caption, videoLocation):
    startTime = time.time()
    
    try:
        print(highlight(f"\n=== Instagram Upload: {word.upper()} ==="))
        logger = setupLogging("instagram_upload.log", profileName)
        logger.info(f"Starting upload for: {word}")
        logger.info(f"Caption: {caption}")
        
        if not os.path.exists(videoLocation):
            print(error(f"❌ Video not found: {videoLocation}"))
            logger.error(f"Video not found: {videoLocation}")
            return False
        
        browser = BrowserManager(profiles, profileName)
        url = 'https://www.instagram.com/'
        
        if not browser.startBrowser(url):
            return False
        
        driver = browser.driver
        
        print(info(f"🚀 Starting upload process..."))
        
        result = automateInstagramActions(driver, videoLocation, caption)
        time.sleep(5)
        
        endTime = time.time()
        duration = endTime - startTime
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        
        if result:
            print(success(f"✅ Upload complete in {minutes}m {seconds}s"))
            logger.info(f"Upload successful. Duration: {minutes}m {seconds}s")
            return True
        else:
            print(error(f"❌ Upload failed"))
            logger.error(f"Upload failed")
            return False
    
    except Exception as e:
        print(error(f"❌ Error: {e}"))
        logger.error(f"Upload error: {e}")
        return False
    finally:
        if 'browser' in locals():
            browser.closeBrowser()

if __name__ == "__main__":
    videoLocation = "C:/Users/UtsavChaudhary/OneDrive - EDGE196/Desktop/NaradX_Social_Uploader/Balk.mp4"
    title = videoLocation.split("/")[-1].split(".")[0]
    caption = "BALK means to hesitate or refuse to proceed; to stop short and refuse to continue. #GREprep #IELTSvocab #wordoftheday #englishwithstyle #speaklikeanative #studygram #vocabularyboost #learnenglish #englishreels #explorepage #IELTSpreparation #englishvocabulary #spokenenglish #studymotivation #englishlearning #dailyvocab #englishpractice #fluencygoals #vocabchallenge #englishtips #educationreels #englishgrammar #ieltsvocab #smartvocab"
    result = uploadToInstagram(title, caption, videoLocation) 
    print(success("✅ Success") if result else error("❌ Failed"))
