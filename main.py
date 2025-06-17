import os
from youTubeUpload import uploadToYoutube
from instagramUpload import uploadToInstagram
from config import success, error, info, warning, highlight, profiles, basePath

# Video configuration
videoLocation = os.path.join(basePath, "Balk.mp4")
title = videoLocation.split("/")[-1].split(".")[0]
caption = "BALK means to hesitate or refuse to proceed; to stop short and refuse to continue. #GREprep #IELTSvocab #wordoftheday #englishwithstyle #speaklikeanative #studygram #vocabularyboost #learnenglish #englishreels #explorepage #IELTSpreparation #englishvocabulary #spokenenglish #studymotivation #englishlearning #dailyvocab #englishpractice #fluencygoals #vocabchallenge #englishtips #educationreels #englishgrammar #ieltsvocab #smartvocab"
tags = "GRE, IELTS, vocabulary, english, learning, education, words, study, exam prep, english vocabulary"  # Default tags

def uploadWithProfile(profileName, videoLocation, title, caption):
    print(highlight(f"\n=== Starting Upload Process for Profile: {profileName} ==="))
    if profileName not in profiles:
        print(error(f"❌ Profile '{profileName}' not found"))
        return False, False
    
    # Upload to YouTube
    print(info("\n📺 Starting YouTube Upload..."))
    youtube_result = uploadToYoutube(profileName, title, caption, videoLocation)
    if youtube_result:
        print(success("✅ YouTube Upload Successful"))
    else:
        print(error("❌ YouTube Upload Failed"))
    
    # Upload to Instagram
    print(info("\n📸 Starting Instagram Upload..."))
    instagram_result = uploadToInstagram(profileName, title, caption, videoLocation)
    if instagram_result:
        print(success("✅ Instagram Upload Successful"))
    else:
        print(error("❌ Instagram Upload Failed"))
    
    # Final status
    print(highlight(f"\n=== Upload Process Complete for {profileName} ==="))
    if youtube_result and instagram_result:
        print(success("🎉 All uploads completed successfully!"))
    else:
        print(warning("⚠️ Some uploads may have failed. Check the logs for details."))
    
    return youtube_result, instagram_result

if __name__ == "__main__":
    profileName = "elitevocabulary"  # Default profile
    youtube_result, instagram_result = uploadWithProfile(profileName, videoLocation, title, caption)
    
    # You can uncomment below to upload with another profile
    # profileName = "wokyabolrahi"
    # youtube_result, instagram_result = uploadWithProfile(profileName, videoLocation, title, caption)
