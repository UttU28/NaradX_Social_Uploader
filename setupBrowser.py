#!/usr/bin/env python3
"""
Browser Setup Utility
Simple interface to set up Chrome sessions for different profiles
"""

import os
import sys
import time
from config import success, error, info, warning, highlight, profiles
from browserUtils import BrowserManager

def listAvailableProfiles():
    """Display all available profiles from config"""
    print(highlight("\n=== Available Profiles ==="))
    for i, (profileName, profileData) in enumerate(profiles.items(), 1):
        print(f"{i}. {info(profileName)}")
        print(f"   - YouTube Channel: {profileData['youtubeChannelId']}")
        print(f"   - Debug Port: {profileData['debuggingPort']}")
        print(f"   - Tags: {profileData['tags'][:50]}...")
        print()

def setupBrowserSession(profileName, url="https://www.google.com"):
    """
    Set up a Chrome session for the specified profile
    
    Args:
        profileName (str): Name of the profile from config
        url (str): URL to open in the browser (default: Google)
    
    Returns:
        BrowserManager: Browser manager instance if successful, None if failed
    """
    print(highlight(f"\n=== Setting up Browser Session ==="))
    print(info(f"Profile: {profileName}"))
    print(info(f"Opening URL: {url}"))
    
    if profileName not in profiles:
        print(error(f"❌ Profile '{profileName}' not found"))
        print(warning("Available profiles:"))
        for profile in profiles.keys():
            print(f"   - {profile}")
        return None
    
    try:
        # Create browser manager instance
        browser = BrowserManager(profiles, profileName)
        
        # Start the browser session
        if browser.startBrowser(url):
            print(success(f"✅ Browser session started successfully for {profileName}"))
            print(info(f"🌐 Chrome opened with debugging port: {profiles[profileName]['debuggingPort']}"))
            print(info(f"📁 Profile data: {browser.chromeDataDir}"))
            return browser
        else:
            print(error(f"❌ Failed to start browser session for {profileName}"))
            return None
            
    except Exception as e:
        print(error(f"❌ Error setting up browser: {e}"))
        return None

def setupYouTubeSession(profileName):
    """Set up a Chrome session specifically for YouTube Studio"""
    if profileName not in profiles:
        print(error(f"❌ Profile '{profileName}' not found"))
        return None
    
    channelId = profiles[profileName]["youtubeChannelId"]
    youtubeUrl = f"https://studio.youtube.com/channel/{channelId}"
    
    print(info(f"🎬 Setting up YouTube Studio session..."))
    return setupBrowserSession(profileName, youtubeUrl)

def setupInstagramSession(profileName):
    """Set up a Chrome session specifically for Instagram"""
    instagramUrl = "https://www.instagram.com/"
    
    print(info(f"📸 Setting up Instagram session..."))
    return setupBrowserSession(profileName, instagramUrl)

def interactiveSetup():
    """Interactive mode to select profile and platform"""
    print(highlight("🚀 Interactive Browser Setup"))
    
    # Show available profiles
    listAvailableProfiles()
    
    # Get profile selection
    profileNames = list(profiles.keys())
    while True:
        try:
            choice = input(f"\n{info('Select profile (1-' + str(len(profileNames)) + '):')} ")
            profileIndex = int(choice) - 1
            if 0 <= profileIndex < len(profileNames):
                selectedProfile = profileNames[profileIndex]
                break
            else:
                print(error("❌ Invalid selection. Please try again."))
        except (ValueError, KeyboardInterrupt):
            print(error("\n❌ Invalid input or cancelled."))
            return None
    
    # Get platform selection
    print(f"\n{highlight('Choose platform:')}")
    print("1. 🌐 General (Google)")
    print("2. 🎬 YouTube Studio")
    print("3. 📸 Instagram")
    
    while True:
        try:
            platform_choice = input(f"\n{info('Select platform (1-3):')} ")
            if platform_choice == "1":
                return setupBrowserSession(selectedProfile)
            elif platform_choice == "2":
                return setupYouTubeSession(selectedProfile)
            elif platform_choice == "3":
                return setupInstagramSession(selectedProfile)
            else:
                print(error("❌ Invalid selection. Please try again."))
        except (ValueError, KeyboardInterrupt):
            print(error("\n❌ Invalid input or cancelled."))
            return None

def main():
    """Main function for command line usage"""
    print(highlight("🌐 Chrome Browser Setup Utility"))
    
    if len(sys.argv) == 1:
        # Interactive mode
        browser = interactiveSetup()
    elif len(sys.argv) == 2:
        # Profile specified
        profileName = sys.argv[1]
        browser = setupBrowserSession(profileName)
    elif len(sys.argv) == 3:
        # Profile and URL specified
        profileName = sys.argv[1]
        url = sys.argv[2]
        browser = setupBrowserSession(profileName, url)
    else:
        print(error("❌ Usage:"))
        print(f"  {info('python setupBrowser.py')}                    # Interactive mode")
        print(f"  {info('python setupBrowser.py <profile>')}          # Open with profile")
        print(f"  {info('python setupBrowser.py <profile> <url>')}    # Open with profile and URL")
        print(f"\n{warning('Available profiles:')}")
        for profile in profiles.keys():
            print(f"   - {profile}")
        return
    
    if browser:
        print(success("\n🎉 Browser session is ready!"))
        print(info("Press Ctrl+C to close the browser session"))
        
        try:
            # Keep the session running until user interrupts
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(info("\n🔒 Closing browser session..."))
            browser.closeBrowser()
            print(success("✅ Browser session closed"))
    else:
        print(error("❌ Failed to set up browser session"))

if __name__ == "__main__":
    main() 