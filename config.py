#!/usr/bin/env python3
"""
Configuration and utility functions for Social Media Uploader
"""
from colorama import init, Fore, Style
import os

# Initialize colorama
init(autoreset=True)

# Color formatting functions
def success(text): return f"{Fore.GREEN}{text}{Style.RESET_ALL}"
def error(text): return f"{Fore.RED}{text}{Style.RESET_ALL}"
def info(text): return f"{Fore.CYAN}{text}{Style.RESET_ALL}"
def warning(text): return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"
def highlight(text): return f"{Fore.MAGENTA}{Style.BRIGHT}{text}{Style.RESET_ALL}"

# Base configuration
basePath = "C:/Users/UtsavChaudhary/OneDrive - EDGE196/Desktop/NaradX_Social_Uploader"

# User Profiles
profiles = {
    "elitevocabulary": {
        "profileName": "elitevocabulary",
        "youtubeChannelId": "UC2z9JFAIFovJsyt2iwKOn3g",
        "chromeDataDir": os.path.join(basePath, "chromeData", "elitevocabulary"),
        "debuggingPort": "9004"
    },
    "wokyabolrahi": {
        "profileName": "wokyabolrahi",
        "youtubeChannelId": "UC2z9JFAIFovJsyt2iwKOn3g",
        "chromeDataDir": os.path.join(basePath, "chromeData", "wokyabolrahi"),
        "debuggingPort": "9005"
    }
} 