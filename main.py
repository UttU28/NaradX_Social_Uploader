#!/usr/bin/env python3
"""
Main uploader script for YouTube and Instagram
"""
import os
import sys
from pathlib import Path
from youTubeUpload import uploadToYoutube, get_youtube_upload_config
from instagramUpload import uploadToInstagram, get_instagram_upload_config
from utils import success, error, info, warning, highlight

def get_video_title_from_filename(video_path):
    """Extract title from video filename"""
    filename = Path(video_path).stem
    # Convert underscores and hyphens to spaces and title case
    title = filename.replace('_', ' ').replace('-', ' ').title()
    return title



def upload_to_both_platforms(video_path):
    """
    Upload video to both YouTube and Instagram
    
    Args:
        video_path (str): Full path to the video file
    
    Returns:
        dict: Results from both platforms
    """
    
    # Validate video file exists
    if not os.path.exists(video_path):
        print(error(f"❌ Video file not found: {video_path}"))
        return {"youtube": False, "instagram": False}
    
    print(highlight("🚀 Starting Multi-Platform Upload"))
    print(info("="*60))
    print(info(f"📹 Video: {os.path.basename(video_path)}"))
    print(info("="*60))
    
    # Load platform configurations
    youtube_config = get_youtube_upload_config()
    instagram_config = get_instagram_upload_config()
    
    # Extract title from filename
    title = get_video_title_from_filename(video_path)
    print(info(f"📝 Title: {title}"))
    
    # Create content for both platforms using config templates
    youtube_description = youtube_config["description_template"].format(word=title.upper())
    instagram_caption = instagram_config["caption_template"].format(word=title.upper())
    youtube_tags = youtube_config["default_tags"]
    
    results = {"youtube": False, "instagram": False}
    
    # Upload to YouTube
    print(highlight("\n🎬 Starting YouTube Upload..."))
    try:
        youtube_result = uploadToYoutube(
            videoPath=video_path,
            title=f"{title}{youtube_config['title_suffix']}",
            description=youtube_description,
            tags=youtube_tags,
            config=youtube_config
        )
        results["youtube"] = youtube_result
        
        if youtube_result:
            print(success("✅ YouTube upload completed successfully!"))
        else:
            print(error("❌ YouTube upload failed"))
            
    except Exception as e:
        print(error(f"❌ YouTube upload error: {e}"))
        results["youtube"] = False
    
    print(info("\n" + "="*60))
    
    # Upload to Instagram
    print(highlight("\n📸 Starting Instagram Upload..."))
    try:
        instagram_result = uploadToInstagram(
            videoPath=video_path,
            caption=instagram_caption,
            config=instagram_config
        )
        results["instagram"] = instagram_result
        
        if instagram_result:
            print(success("✅ Instagram upload completed successfully!"))
        else:
            print(error("❌ Instagram upload failed"))
            
    except Exception as e:
        print(error(f"❌ Instagram upload error: {e}"))
        results["instagram"] = False
    
    # Summary
    print(info("\n" + "="*60))
    print(highlight("📊 UPLOAD SUMMARY"))
    print(info("="*60))
    
    youtube_status = "✅ SUCCESS" if results["youtube"] else "❌ FAILED"
    instagram_status = "✅ SUCCESS" if results["instagram"] else "❌ FAILED"
    
    print(info(f"🎬 YouTube:   {youtube_status}"))
    print(info(f"📸 Instagram: {instagram_status}"))
    
    total_success = sum(results.values())
    print(info(f"📈 Success Rate: {total_success}/2 platforms"))
    
    if total_success == 2:
        print(success("🎉 All uploads completed successfully!"))
    elif total_success == 1:
        print(warning("⚠️ Partial success - some uploads failed"))
    else:
        print(error("❌ All uploads failed"))
    
    print(info("="*60))
    
    return results

def main():
    """Main function"""
    print(highlight("🌟 NaradX Social Media Uploader"))
    print(info("Upload videos to YouTube and Instagram simultaneously"))
    print(info("="*60))
    
    # Get video path from command line argument or user input
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        video_path = input("Enter the full path to your video file: ").strip().strip('"')
    
    if not video_path:
        print(error("❌ No video path provided"))
        return
    
    # Convert to absolute path if relative
    video_path = os.path.abspath(video_path)
    
    # Start upload process
    results = upload_to_both_platforms(video_path)
    
    # Exit with appropriate code
    if results["youtube"] and results["instagram"]:
        sys.exit(0)  # Success
    elif results["youtube"] or results["instagram"]:
        sys.exit(1)  # Partial success
    else:
        sys.exit(2)  # Total failure

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(info("\n\n🛑 Upload process interrupted by user"))
        print(info("👋 Goodbye!"))
        sys.exit(130)
    except Exception as e:
        print(error(f"\n❌ Unexpected error: {e}"))
        sys.exit(1) 