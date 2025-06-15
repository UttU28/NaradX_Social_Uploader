#!/usr/bin/env python3
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from config import success, error, info, warning, highlight, profiles
from browserUtils import BrowserManager, setupLogging

if os.name == "nt":
    import pyautogui

def fillTitleAndDescription(driver, title, description):
    try:
        print(info("📝 Setting title and description..."))
        
        titleField = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#textbox[contenteditable='true'][role='textbox']"))
        )
        
        titleField.click()
        time.sleep(0.5)
        
        try:
            titleField.send_keys(Keys.CONTROL + "a")
            titleField.send_keys(Keys.DELETE)
        except AttributeError:
            try:
                actions = ActionChains(driver)
                actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
                titleField.send_keys(Keys.DELETE)
            except:
                driver.execute_script("arguments[0].innerText = ''", titleField)
        
        time.sleep(0.5)
        
        try:
            chunkSize = 20
            for i in range(0, len(title), chunkSize):
                chunk = title[i:i+chunkSize]
                titleField.send_keys(chunk)
                time.sleep(0.3)
        except Exception:
            try:
                driver.execute_script("arguments[0].innerText = arguments[1]", titleField, title)
            except Exception:
                titleField.send_keys(title)
        
        print(success("✅ Title set"))
        
        descriptionSelectors = [
            "ytcp-social-suggestions-textbox[label='Description'] #textbox[contenteditable='true']",
            "#description-textarea #textbox[contenteditable='true']",
            "div[aria-label*='Tell viewers about your video'][contenteditable='true']"
        ]
        
        descriptionField = None
        for selector in descriptionSelectors:
            try:
                descriptionField = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                break
            except:
                continue
        
        if descriptionField:
            descriptionField.click()
            time.sleep(0.5)
            
            try:
                descriptionField.send_keys(Keys.CONTROL + "a")
                descriptionField.send_keys(Keys.DELETE)
            except AttributeError:
                try:
                    actions = ActionChains(driver)
                    actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
                    descriptionField.send_keys(Keys.DELETE)
                except:
                    driver.execute_script("arguments[0].innerText = ''", descriptionField)
            
            time.sleep(0.5)
            
            try:
                chunkSize = 50
                for i in range(0, len(description), chunkSize):
                    chunk = description[i:i+chunkSize]
                    descriptionField.send_keys(chunk)
                    time.sleep(0.5)
                print(success("✅ Description set"))
            except Exception:
                try:
                    descriptionField = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@contenteditable='true' and @aria-label]"))
                    )
                    descriptionField.click()
                    time.sleep(0.5)
                    
                    chunkSize = 50
                    for i in range(0, len(description), chunkSize):
                        chunk = description[i:i+chunkSize]
                        descriptionField.send_keys(chunk)
                        time.sleep(0.5)
                    print(success("✅ Description set"))
                except Exception:
                    try:
                        driver.execute_script("arguments[0].innerText = arguments[1]", descriptionField, description)
                        print(success("✅ Description set"))
                    except Exception:
                        try:
                            driver.execute_script("arguments[0].innerText = ''", descriptionField)
                            chunkSize = 50
                            for i in range(0, len(description), chunkSize):
                                chunk = description[i:i+chunkSize]
                                current = driver.execute_script("return arguments[0].innerText", descriptionField)
                                driver.execute_script("arguments[0].innerText = arguments[1]", descriptionField, current + chunk)
                                time.sleep(0.5)
                            print(success("✅ Description set"))
                        except Exception:
                            print(warning("⚠️ Description not set"))
        else:
            print(warning("⚠️ Description field not found"))
        
    except Exception as e:
        print(error(f"❌ Title/Description error: {e}"))

def selectFirstPlaylist(driver):
    try:
        print(info("📁 Selecting playlist..."))
        
        playlistSelectors = [
            "ytcp-dropdown-trigger[aria-label*='Select playlists']",
            "ytcp-dropdown-trigger[aria-label*='Select']",
            "ytcp-text-dropdown-trigger"
        ]
        
        playlistDropdown = None
        for selector in playlistSelectors:
            try:
                playlistDropdown = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                break
            except:
                continue
        
        if playlistDropdown:
            playlistDropdown.click()
            time.sleep(2)
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "tp-yt-paper-dialog[aria-label='Choose playlists']"))
                )
                
                firstCheckbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#checkbox-0, ytcp-checkbox-lit[id='checkbox-0']"))
                )
                firstCheckbox.click()
                
                doneButton = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "ytcp-button.done-button"))
                )
                doneButton.click()
                print(success("✅ Playlist selected"))
                
            except Exception:
                print(warning("⚠️ Playlist selection failed"))
                try:
                    closeButton = driver.find_element(By.CSS_SELECTOR, "ytcp-button.done-button")
                    closeButton.click()
                except:
                    pass
        
    except Exception as e:
        print(error(f"❌ Playlist error: {e}"))

def setNotMadeForKids(driver):
    try:
        print(info("👶 Setting audience..."))
        
        notForKidsRadio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']"))
        )
        notForKidsRadio.click()
        print(success("✅ Set as not for kids"))
        
    except Exception as e:
        print(error(f"❌ Audience error: {e}"))

def expandAdvancedOptions(driver):
    try:
        print(info("🔽 Expanding options..."))
        
        showMoreSelectors = [
            "ytcp-button[aria-label*='Show advanced settings']",
            "#toggle-button"
        ]
        
        showMoreButton = None
        for selector in showMoreSelectors:
            try:
                if selector == "#toggle-button":
                    showMoreButton = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                else:
                    xpathSelector = "//ytcp-button[.//div[contains(text(), 'Show more')]]"
                    showMoreButton = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, xpathSelector))
                    )
                break
            except:
                continue
        
        if showMoreButton:
            showMoreButton.click()
            time.sleep(2)
            print(success("✅ Options expanded"))
        
    except Exception as e:
        print(error(f"❌ Options error: {e}"))

def addTags(driver, tags):
    try:
        print(info("🏷️ Adding tags..."))
        
        tagsInput = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#text-input[aria-label='Tags']"))
        )
        tagsInput.click()
        time.sleep(0.5)
        
        try:
            chunkSize = 30
            for i in range(0, len(tags), chunkSize):
                chunk = tags[i:i+chunkSize]
                tagsInput.send_keys(chunk)
                time.sleep(0.3)
            print(success("✅ Tags added"))
        except Exception:
            try:
                driver.execute_script("arguments[0].value = arguments[1]", tagsInput, tags)
                print(success("✅ Tags added"))
            except Exception:
                tagsInput.send_keys(tags)
                print(success("✅ Tags added"))
        
    except Exception as e:
        print(error(f"❌ Tags error: {e}"))

def setCategoryToEntertainment(driver):
    try:
        print(info("🎭 Setting category..."))
        
        categoryDropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#category ytcp-dropdown-trigger"))
        )
        categoryDropdown.click()
        time.sleep(2)
        
        entertainmentSelectors = [
            "tp-yt-paper-item[test-id='CREATOR_VIDEO_CATEGORY_ENTERTAINMENT']",
            "#text-item-3"
        ]
        
        entertainmentOption = None
        for selector in entertainmentSelectors:
            try:
                entertainmentOption = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                break
            except:
                continue
        
        if not entertainmentOption:
            xpathSelector = "//tp-yt-paper-item[.//yt-formatted-string[text()='Entertainment']]"
            entertainmentOption = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpathSelector))
            )
        
        entertainmentOption.click()
        print(success("✅ Category set to Entertainment"))
        
    except Exception as e:
        print(error(f"❌ Category error: {e}"))

def clickNextButton(driver):
    try:
        print(info("➡️ Next step..."))
        
        nextButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#next-button"))
        )
        nextButton.click()
        time.sleep(3)
        print(success("✅ Proceeded"))
        
    except Exception as e:
        print(error(f"❌ Next button error: {e}"))

def setPublicAndSave(driver):
    try:
        print(info("🌍 Publishing..."))
        
        publicRadio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "tp-yt-paper-radio-button[name='PUBLIC']"))
        )
        publicRadio.click()
        time.sleep(2)
        
        saveButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#done-button"))
        )
        saveButton.click()
        print(success("✅ Video published"))
        return True
        
    except Exception as e:
        print(error(f"❌ Publishing error: {e}"))
        return False

def handleFileUpload(driver, videoPath):
    try:
        pyautogui.typewrite(videoPath, interval=0.05)
        time.sleep(0.5)
        pyautogui.press('enter')
        print(success("✅ File selected"))
    except Exception as e:
        print(error(f"❌ File upload error: {e}"))
        raise

def clickCreateAndUpload(driver, videoLocation):
    try:
        createButton = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "ytcp-button#create-icon"))
        )
        createButton.click()
        
        uploadOption = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "tp-yt-paper-item[test-id='upload-beta']"))
        )
        uploadOption.click()
        
        if videoLocation:
            print(info(f"📁 Uploading {os.path.basename(videoLocation)}..."))
            
            if os.name == "nt":
                selectFilesButton = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#select-files-button"))
                )
                selectFilesButton.click()
                time.sleep(2)
                handleFileUpload(driver, videoLocation)
            else:
                time.sleep(2)
                try:
                    uploadInput = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                    )
                    uploadInput.send_keys(videoLocation)
                    print(success(f"✅ File selected: {os.path.basename(videoLocation)}"))
                except Exception as e:
                    print(error(f"❌ Upload error: {e}"))
                    raise
            
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ytcp-video-metadata-editor"))
            )
            print(success("✅ Upload started"))
        
    except Exception as e:
        print(error(f"❌ Upload initiation error: {e}"))

def uploadToYoutube(profileName, word, caption, videoLocation):
    startTime = time.time()
    
    try:
        print(highlight(f"\n=== YouTube Upload: {word.upper()} ==="))
        logger = setupLogging("youtube_upload.log", profileName)
        logger.info(f"Starting upload for: {word}")
        logger.info(f"Caption: {caption}")
        
        # Get tags from config based on profile
        tags = profiles[profileName]["tags"]
        logger.info(f"Using tags: {tags}")
        
        browser = BrowserManager(profiles, profileName)
        url = f'https://studio.youtube.com/channel/{profiles[profileName]["youtubeChannelId"]}'
        
        if not browser.startBrowser(url):
            return False
        
        driver = browser.driver
        
        print(success(f"✅ Connected to Chrome ({os.name})"))
        
        clickCreateAndUpload(driver, videoLocation)
        
        print(info("📋 Configuring video..."))
        fillTitleAndDescription(driver, word, caption)
        selectFirstPlaylist(driver)
        setNotMadeForKids(driver)
        expandAdvancedOptions(driver)
        addTags(driver, tags)
        setCategoryToEntertainment(driver)
        
        print(info("🔄 Processing..."))
        clickNextButton(driver)
        clickNextButton(driver)
        clickNextButton(driver)
        
        time.sleep(3)
        
        uploadSuccess = setPublicAndSave(driver)
        time.sleep(10)
        
        print(info("="*50))
        if uploadSuccess:
            print(success("🎉 YouTube Upload Complete!"))
        else:
            print(error("❌ Upload Failed"))
        print(info("="*50))
        
        endTime = time.time()
        duration = endTime - startTime
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        
        if uploadSuccess:
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
    caption = "BALK means to hesitate or refuse to proceed; to stop short and refuse to continue. \n\n#GREprep #IELTSvocab #wordoftheday #englishwithstyle #speaklikeanative #studygram #vocabularyboost #learnenglish #englishreels #explorepage #IELTSpreparation #englishvocabulary #spokenenglish #studymotivation #englishlearning #dailyvocab #englishpractice #fluencygoals #vocabchallenge #englishtips #educationreels #englishgrammar #ieltsvocab #smartvocab"
    result = uploadToYoutube("elitevocabulary", title, caption, videoLocation)
    print(success("✅ Success") if result else error("❌ Failed"))