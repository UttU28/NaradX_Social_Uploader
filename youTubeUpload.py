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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from utils import success, error, info, warning, highlight
from selenium_config import SeleniumConfig, PlatformUtils, SeleniumUtils
if os.name == "nt":
    import pyautogui

# YOUTUBE UPLOAD CONFIGURATION
def get_youtube_upload_config():
    """
    Get YouTube upload configuration settings
    
    Returns:
        dict: Configuration settings for YouTube uploads
    """
    return {
        # Video Settings
        "category": "Entertainment",
        "audience": "not_for_kids",  # or "for_kids"
        "visibility": "public",  # "public", "unlisted", "private"
        "select_first_playlist": True,
        
        # Content Settings
        "default_tags": "GRE, IELTS, vocabulary, english, learning, education, words, study, exam prep, english vocabulary",
        "title_suffix": " - Vocabulary Word",
        "description_template": "{word} means to hesitate or refuse to proceed; to stop short and refuse to continue.\n\n#GREprep #IELTSvocab #wordoftheday #englishwithstyle #speaklikeanative #studygram #vocabularyboost #learnenglish #englishreels #explorepage #IELTSpreparation #englishvocabulary #spokenenglish #studymotivation #englishlearning #dailyvocab #englishpractice #fluencygoals #vocabchallenge #englishtips #educationreels #englishgrammar #ieltsvocab #smartvocab",
        
        # Timing Settings
        "wait_after_upload": 3,  # seconds
        "wait_between_steps": 3,  # seconds
        "text_typing_delay": 0.5,  # seconds between text chunks
        
        # Advanced Settings
        "expand_advanced_options": True,
        "add_tags": True,
        "set_category": True,
        
        # Selectors (for maintenance)
        "selectors": {
            "title_field": "#textbox[contenteditable='true'][role='textbox']",
            "description_fields": [
                "ytcp-social-suggestions-textbox[label='Description'] #textbox[contenteditable='true']",
                "#description-textarea #textbox[contenteditable='true']",
                "div[aria-label*='Tell viewers about your video'][contenteditable='true']"
            ],
            "tags_input": "#text-input[aria-label='Tags']",
            "category_dropdown": "#category ytcp-dropdown-trigger",
            "entertainment_category": [
                "tp-yt-paper-item[test-id='CREATOR_VIDEO_CATEGORY_ENTERTAINMENT']",
                "#text-item-3"
            ],
            "playlist_dropdown": [
                "ytcp-dropdown-trigger[aria-label*='Select playlists']",
                "ytcp-dropdown-trigger[aria-label*='Select']",
                "ytcp-text-dropdown-trigger"
            ],
            "not_for_kids": "tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']",
            "public_radio": "tp-yt-paper-radio-button[name='PUBLIC']",
            "next_button": "#next-button",
            "done_button": "#done-button"
        }
    }

def fillTitleAndDescription(driver, title, description):
    try:
        print(info("📝 Setting title and description..."))
        
        # Handle Title with robust typing like Instagram
        titleField = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#textbox[contenteditable='true'][role='textbox']"))
        )
        
        titleField.click()
        time.sleep(0.5)
        
        # Clear and set title using utility functions
        SeleniumUtils.clear_field_with_fallback(driver, titleField)
        time.sleep(0.5)
        SeleniumUtils.set_text_with_fallback(driver, titleField, title)
        
        print(success("✅ Title set"))
        
        # Handle Description with robust typing like Instagram
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
            
            # Clear and set description using utility functions
            SeleniumUtils.clear_field_with_fallback(driver, descriptionField)
            time.sleep(0.5)
            
            if SeleniumUtils.set_text_with_fallback(driver, descriptionField, description):
                print(success("✅ Description set"))
            else:
                # Try alternative selector as fallback
                try:
                    descriptionField = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@contenteditable='true' and @aria-label]"))
                    )
                    descriptionField.click()
                    time.sleep(0.5)
                    
                    if SeleniumUtils.set_text_with_fallback(driver, descriptionField, description):
                        print(success("✅ Description set (alternative method)"))
                    else:
                        print(warning("⚠️ Could not set description"))
                except Exception:
                    print(warning("⚠️ Could not set description"))
        else:
            print(warning("⚠️ Description field not found"))
        
        print(success("✅ Title and description configuration completed"))
        
    except Exception as e:
        print(error(f"❌ Error setting title/description: {e}"))

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
        print(error(f"❌ Audience setting error: {e}"))

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
        print(error(f"❌ Expand options error: {e}"))

def addTags(driver, tags):
    try:
        print(info("🏷️ Adding tags..."))
        
        tagsInput = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#text-input[aria-label='Tags']"))
        )
        tagsInput.click()
        time.sleep(0.5)
        
        # Set tags using utility functions
        if SeleniumUtils.set_text_with_fallback(driver, tagsInput, tags):
            print(success("✅ Tags added"))
        else:
            print(warning("⚠️ Could not add tags"))
        
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
    """Handle file upload using platform utilities"""
    PlatformUtils.handle_file_upload(videoPath)

def clickCreateAndUpload(driver, videoPath):
    try:
        createButton = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "ytcp-button#create-icon"))
        )
        createButton.click()
        
        uploadOption = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "tp-yt-paper-item[test-id='upload-beta']"))
        )
        uploadOption.click()
        
        if not os.path.exists(videoPath):
            print(error(f"❌ Video not found: {videoPath}"))
            raise Exception(f"Video file not found: {videoPath}")
        
        print(info(f"📁 Uploading {os.path.basename(videoPath)}..."))
        
        if os.name == "nt":
            # Windows: Click the select files button and use pyautogui
            selectFilesButton = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#select-files-button"))
            )
            selectFilesButton.click()
            time.sleep(2)
            handleFileUpload(driver, videoPath)
        else:
            # Ubuntu: Find the hidden file input and send file path directly (like Instagram)
            time.sleep(2)
            try:
                uploadInput = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                )
                uploadInput.send_keys(videoPath)
                print(success(f"✅ File selected (Ubuntu method): {os.path.basename(videoPath)}"))
            except Exception as e:
                print(error(f"Could not find file input to upload video: {e}"))
                raise
        
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ytcp-video-metadata-editor"))
        )
        print(success("✅ Upload started"))
        
    except Exception as e:
        print(error(f"❌ Upload initiation error: {e}"))
        raise

def uploadToYoutube(videoPath, title, description, tags=None, config=None):
    """
    Upload a video to YouTube
    
    Args:
        videoPath (str): Full path to the video file
        title (str): Video title
        description (str): Video description
        tags (str): Video tags (comma separated, optional)
        config (dict): Configuration settings (optional)
    
    Returns:
        bool: Whether the upload was successful
    """
    start_time = time.time()
    
    try:
        # Load configuration
        if config is None:
            config = get_youtube_upload_config()
        
        # Use default tags if not provided
        if tags is None:
            tags = config["default_tags"]
        
        print(highlight(f"\n=== YouTube Upload Started ==="))
        print(info(f"Video: {os.path.basename(videoPath)}"))
        print(info(f"Title: {title}"))
        
        chrome_data_dir = SeleniumConfig.CHROME_DATA_DIR
        channel_id = SeleniumConfig.YOUTUBE_CHANNEL_ID
        url = f'https://studio.youtube.com/channel/{channel_id}'
        
        osName = "Windows" if os.name == "nt" else "Ubuntu"
        print(highlight(f"🚀 YouTube Upload ({osName})"))
        print(info("="*50))
        
        chromeProcess = SeleniumConfig.start_chrome_process(chrome_data_dir, url)
        driver = SeleniumConfig.create_driver()
        
        print(success(f"✅ Connected to Chrome ({osName})"))
        
        clickCreateAndUpload(driver, videoPath)
        
        print(info("📋 Configuring video..."))
        fillTitleAndDescription(driver, title, description)
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
        time.sleep(config["wait_after_upload"])
        
        print(info("="*50))
        if uploadSuccess:
            print(success("🎉 YouTube Upload Complete!"))
        else:
            print(error("❌ Upload Failed"))
        print(info("="*50))
        
        # Close Chrome session
        SeleniumConfig.close_chrome_session(driver, chromeProcess)
        
        end_time = time.time()
        duration = end_time - start_time
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        
        if uploadSuccess:
            print(success(f"YouTube upload completed successfully in {minutes}m {seconds}s"))
            return True
        else:
            print(error(f"YouTube upload failed"))
            return False
        
    except Exception as e:
        print(error(f"❌ YouTube upload error: {e}"))
        # Cleanup on error
        try:
            if 'driver' in locals() and 'chromeProcess' in locals():
                SeleniumConfig.close_chrome_session(driver, chromeProcess)
        except:
            pass
        return False


if __name__ == "__main__":
    # Example usage with direct video path
    videoPath = r"C:\Users\utsav\OneDrive\Desktop\NaradX_Social_Uploader\Balk.mp4"  # Direct path to video
    title = "BALK - Vocabulary Word"
    description = "BALK means to hesitate or refuse to proceed; to stop short and refuse to continue.\n\n#GREprep #IELTSvocab #wordoftheday #englishwithstyle #speaklikeanative #studygram #vocabularyboost #learnenglish #englishreels #explorepage #IELTSpreparation #englishvocabulary #spokenenglish #studymotivation #englishlearning #dailyvocab #englishpractice #fluencygoals #vocabchallenge #englishtips #educationreels #englishgrammar #ieltsvocab #smartvocab"
    
    result = uploadToYoutube(videoPath, title, description)
    print(success("✅ Success") if result else error("❌ Failed"))
