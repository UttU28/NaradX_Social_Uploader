import json
import os
import time
from pathlib import Path
from datetime import datetime, UTC, timedelta
from youTubeUpload import uploadToYoutube
from instagramUpload import uploadToInstagram
from config import success, error, info, warning, highlight
import platform

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
    print(f"📁 Filename: {video.get('filename', 'N/A')}")
    print(f"📝 Title: {video.get('title', 'N/A')}")
    print(f"📄 Description: {video.get('description', 'N/A')}")
    print(f"📺 Video Checked: {'✅' if video.get('videoChecked', False) else '❌'}")
    print(f"📱 Instagram Upload: {'✅' if video.get('instagramUploaded', False) else '❌'}")
    print(f"🎥 YouTube Upload: {'✅' if video.get('youtubeUploaded', False) else '❌'}")
    if video.get('uploadTimestamp'):
        print(f"⏰ Upload Time: {video['uploadTimestamp']}")
    print("-" * 50)

def getProfileName(filePath):
    return filePath.stem

def findNextUncheckedVideo(videos):
    for i, video in enumerate(videos):
        # Skip videos that don't have videoChecked key
        if 'videoChecked' not in video:
            print(f"⚠️  Skipping video {i+1}: Missing 'videoChecked' field")
            continue
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
    if platform.system() == 'Windows':
        basePath = "C:/Users/UtsavChaudhary/OneDrive - EDGE196/Desktop/NaradX_Social_Uploader"
    else:
        basePath = "/home/kaka/Desktop/NaradX_Social_Uploader"
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
        # Check if any video exists without videoChecked key or with videoChecked=False
        for video in profile['data']['videos']:
            if 'videoChecked' in video and not video['videoChecked']:
                return True
    return False

def main():
    # Record start time
    start_time = time.perf_counter()
    print("🚀 Starting automatic video processing...")
    print(f"⏱️  Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    profiles = loadAllProfiles()
    if not profiles:
        print("❌ No profiles available to process!")
    else:
        foundVideo = False
        for profileName, profile in profiles.items():
            videoIndex = findNextUncheckedVideo(profile['data']['videos'])
            if videoIndex is not None:
                print(f"\n🎯 Processing one video from profile: {profileName}")
                processProfile(profile['path'], profile['data'], profileName)
                foundVideo = True
                break  # Process only one video per 12-hour cycle
        if not foundVideo:
            print("\n✅ All videos in all profiles have been processed!")

    # Calculate processing time and dynamic sleep for 12-hour cycle
    end_time = time.perf_counter()
    processing_time = end_time - start_time

    twelve_hours = 12 * 60 * 60  # 43200 seconds
    sleep_time = twelve_hours - processing_time

    print(f"\n⏱️  Processing completed!")
    print(f"📊 Processing time: {processing_time:.2f} seconds ({processing_time/60:.2f} minutes)")
    print(f"🏁 End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if sleep_time > 0:
        sleep_hours = sleep_time / 3600
        sleep_minutes = (sleep_time % 3600) / 60
        print(f"\n😴 Sleeping for {sleep_time:.2f} seconds ({sleep_hours:.2f} hours or {sleep_minutes:.1f} minutes)")
        print(f"⏰ Next cycle will start at: {(datetime.now() + timedelta(seconds=sleep_time)).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔄 Total cycle time: 12.00 hours (Processing: {processing_time/3600:.2f}h + Sleep: {sleep_hours:.2f}h)")

        remaining_sleep = sleep_time
        while remaining_sleep > 0:
            if remaining_sleep >= 3600:
                print(f"💤 Sleeping... {remaining_sleep/3600:.1f} hours remaining")
                time.sleep(3600)
                remaining_sleep -= 3600
            else:
                print(f"💤 Final sleep... {remaining_sleep/60:.1f} minutes remaining")
                time.sleep(remaining_sleep)
                remaining_sleep = 0
    else:
        print(f"\n⚠️  Processing took longer than 12 hours!")
        print(f"🕐 Overtime: {abs(sleep_time)/3600:.2f} hours")
        print("🔄 Starting next cycle immediately...")
        time.sleep(10)

    # Start the next cycle
    main()


if __name__ == "__main__":
    main()
