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
from selenium_config import SeleniumConfig, PlatformUtils, SeleniumUtils

# INSTAGRAM UPLOAD CONFIGURATION
def get_instagram_upload_config():
    """
    Get Instagram upload configuration settings
    
    Returns:
        dict: Configuration settings for Instagram uploads
    """
    return {
        # Video Settings
        "crop_format": "Original",  # "Original", "Square", "Portrait"
        "enable_auto_captions": True,
        "post_type": "reel",  # "reel", "post"
        
        # Content Settings
        "caption_template": "{word} means to hesitate or refuse to proceed; to stop short and refuse to continue.\n\n#GREprep #IELTSvocab #wordoftheday #englishwithstyle #speaklikeanative #studygram #vocabularyboost #learnenglish #englishreels #explorepage #IELTSpreparation #englishvocabulary #spokenenglish #studymotivation #englishlearning #dailyvocab #englishpractice #fluencygoals #vocabchallenge #englishtips #educationreels #englishgrammar #ieltsvocab #smartvocab",
        "default_caption": "Instagram said 'post daily' — so here's me being obedient.",
        
        # Timing Settings
        "wait_after_upload": 5,  # seconds
        "wait_between_steps": 2,  # seconds
        "text_typing_delay": 0.5,  # seconds between text chunks
        "wait_for_processing": 3,  # seconds
        
        # Feature Settings
        "enable_accessibility": True,
        "skip_location": True,
        "skip_music": True,
        
        # Selectors (for maintenance)
        "selectors": {
            "create_button": "//span[contains(text(), 'Create')]",
            "select_from_computer": "//button[contains(text(), 'Select from computer')]",
            "file_input": "//input[@type='file']",
            "crop_button": [
                "//div[@class='_abfz _abg1' and @role='button']",
                "//button[.//svg[@aria-label='Select crop']]",
                "//svg[@aria-label='Select crop']"
            ],
            "original_format": [
                "//span[text()='Original']",
                "//span[contains(text(), 'Original')]"
            ],
            "next_button": [
                "//div[@role='button' and text()='Next']",
                "//*[text()='Next']"
            ],
            "caption_field": [
                "//div[@aria-label='Write a caption...']",
                "//div[@role='textbox']",
                "//div[@contenteditable='true']"
            ],
            "accessibility_button": [
                "//span[text()='Accessibility']",
                "//div[.//span[contains(text(), 'Accessibility')]]"
            ],
            "captions_toggle": "//input[@role='switch']",
            "share_button": [
                "//div[@role='button' and text()='Share']",
                "//*[text()='Share']"
            ],
            "success_message": "//h3[contains(text(), 'Your reel has been shared')]"
        }
    }

def automateInstagramActions(debuggingPort, videoPath, caption="Instagram said 'post daily' — so here's me being obedient."):
    try:
        driver = SeleniumConfig.create_driver()
        
        print(info("Connected to Chrome. Starting automation..."))
        
        createButton = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create')]"))
        )
        createButton.click()
        
        if os.name == "nt":
            selectButton = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Select from computer')]"))
            )
            selectButton.click()
            
            time.sleep(2)
            PlatformUtils.handle_file_upload(videoPath)
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
                
                if not SeleniumUtils.set_text_with_fallback(driver, captionField, caption):
                    raise Exception("Could not set caption with primary field")
            except Exception:
                try:
                    captionField = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@role='textbox']"))
                    )
                    captionField.click()
                    time.sleep(1)
                    
                    if not SeleniumUtils.set_text_with_fallback(driver, captionField, caption):
                        raise Exception("Could not set caption with secondary field")
                except Exception:
                    try:
                        captionField = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
                        
                        if not SeleniumUtils.set_text_with_fallback(driver, captionField, caption):
                            raise Exception("Could not set caption with fallback field")
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

def uploadToInstagram(videoPath, caption=None, config=None):
    """
    Upload a video to Instagram
    
    Args:
        videoPath (str): Full path to the video file
        caption (str): The caption to use for the Instagram post (optional)
        config (dict): Configuration settings (optional)
    
    Returns:
        bool: Whether the upload was successful
    """
    start_time = time.time()
    
    # Load configuration
    if config is None:
        config = get_instagram_upload_config()
    
    # Use default caption if not provided
    if caption is None:
        caption = config["default_caption"]
    
    print(highlight(f"\n=== Instagram Upload Started ==="))
    print(info(f"Video: {os.path.basename(videoPath)}"))
    print(info(f"Caption: {caption[:50]}..."))
    
    try:
        chrome_data_dir = SeleniumConfig.CHROME_DATA_DIR
        
        if not os.path.exists(videoPath):
            print(error(f"Error: Video file {videoPath} not found"))
            return False
        
        url = 'https://www.instagram.com/'
        
        print(info(f"Starting upload process..."))
        
        try:
            chromeProcess = SeleniumConfig.start_chrome_process(chrome_data_dir, url)
            time.sleep(config["wait_for_processing"])
            
            # Call the Instagram automation function
            result = automateInstagramActions(SeleniumConfig.DEBUGGING_PORT, videoPath, caption)
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
    videoPath = r"C:\Users\utsav\OneDrive\Desktop\NaradX_Social_Uploader\Balk.mp4"  # Direct path to video
    caption = "BALK means to hesitate or refuse to proceed; to stop short and refuse to continue.\n\n#GREprep #IELTSvocab #wordoftheday #englishwithstyle #speaklikeanative #studygram #vocabularyboost #learnenglish #englishreels #explorepage #IELTSpreparation #englishvocabulary #spokenenglish #studymotivation #englishlearning #dailyvocab #englishpractice #fluencygoals #vocabchallenge #englishtips #educationreels #englishgrammar #ieltsvocab #smartvocab"
    
    uploadToInstagram(videoPath, caption) 