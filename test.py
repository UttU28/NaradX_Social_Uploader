import json
import os
import time
from pathlib import Path
from datetime import datetime, UTC
from youTubeUpload import uploadToYoutube
from instagramUpload import uploadToInstagram
from config import success, error, info, warning, highlight

def loadProfile(profilePath):
    try:
        with open(profilePath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {profilePath}: {e}")
        return None

def saveProfile(profilePath, profileData):
    try:
        with open(profilePath, 'w') as f:
            json.dump(profileData, f, indent=2)
        return True
    except Exception as e:
        print(f"❌ Error saving profile: {e}")
        return False

def printVideoInfo(video):
    print("\n📹 Video Details:")
    print(f"📁 Filename: {video['filename']}")
    print(f"📝 Title: {video['title']}")
    print(f"📄 Description: {video['description']}")
    print(f"📺 Video Checked: {'✅' if video['videoChecked'] else '❌'}")
    print(f"📱 Instagram Upload: {'✅' if video['instagramUploaded'] else '❌'}")
    print(f"🎥 YouTube Upload: {'✅' if video['youtubeUploaded'] else '❌'}")
    if video['uploadTimestamp']:
        print(f"⏰ Upload Time: {video['uploadTimestamp']}")
    print("-" * 50)

def getProfileName(filePath):
    return filePath.stem

def findNextUncheckedVideo(videos):
    for i, video in enumerate(videos):
        if not video['videoChecked']:
            return i
    return None

def processProfile(profilePath, profileData, profileName):
    videoIndex = findNextUncheckedVideo(profileData['videos'])
    
    if videoIndex is None:
        return False
    
    video = profileData['videos'][videoIndex]
    print(f"\n📼 Processing video ({videoIndex + 1}/{len(profileData['videos'])}):")
    printVideoInfo(video)
    
    # Construct video path
    basePath = "C:/Users/UtsavChaudhary/OneDrive - EDGE196/Desktop/NaradX_Social_Uploader"
    videoLocation = os.path.join(basePath, video['filename'])
    
    if not os.path.exists(videoLocation):
        print(error(f"❌ Video file not found: {videoLocation}"))
        return False
    
    # Try YouTube upload
    print(info("\n📺 Attempting YouTube upload..."))
    youtube_result = uploadToYoutube(profileName, video['title'], video['description'], videoLocation)
    
    # Try Instagram upload
    print(info("\n📱 Attempting Instagram upload..."))
    instagram_result = uploadToInstagram(profileName, video['title'], video['description'], videoLocation)
    
    # Update video status based on upload results
    currentTime = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    video.update({
        'videoChecked': True,
        'youtubeUploaded': youtube_result,
        'instagramUploaded': instagram_result,
        'uploadTimestamp': currentTime
    })
    
    # Show updated status
    print("\n📊 Upload Results:")
    printVideoInfo(video)
    
    if saveProfile(profilePath, profileData):
        print("✅ Status updated in profile!")
        return True
    else:
        print("❌ Failed to save changes!")
        return False

def loadAllProfiles():
    profilesDir = Path("profiles")
    profileFiles = list(profilesDir.glob("*.json"))
    
    if not profileFiles:
        print("❌ No profile files found in the profiles directory!")
        return None
    
    profiles = {}
    for filePath in profileFiles:
        profileName = getProfileName(filePath)
        profileData = loadProfile(filePath)
        if profileData:
            profiles[profileName] = {
                'path': filePath,
                'data': profileData
            }
    return profiles

def hasUncheckedVideos(profiles):
    for profile in profiles.values():
        if findNextUncheckedVideo(profile['data']['videos']) is not None:
            return True
    return False

def main():
    print("🚀 Starting automatic video processing...")
    
    while True:
        profiles = loadAllProfiles()
        if not profiles:
            print("❌ No profiles available to process!")
            return
        
        if not hasUncheckedVideos(profiles):
            print("\n✅ All videos in all profiles have been processed!")
            break
            
        print("\n📊 Processing all profiles...")
        for profileName, profile in profiles.items():
            uncheckedCount = sum(1 for video in profile['data']['videos'] 
                               if not video['videoChecked'])
            
            if uncheckedCount > 0:
                print(f"\n🎯 Profile: {profileName} (🎥 {uncheckedCount} unchecked)")
                processProfile(profile['path'], profile['data'], profileName)
        
        print(f"\n⏳ Waiting for 2 seconds before next check...")
        time.sleep(2)

if __name__ == "__main__":
    main()
