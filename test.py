import json

# Read input from aa.json
with open('greWords.json', 'r') as infile:
    data = json.load(infile)

# Convert dict to list
videosList = list(data.values())

# Wrap into desired structure
outputData = {
    "videos": videosList
}

# Write to new file or overwrite
with open('profiles/elitevocabulary.json', 'w') as outfile:
    json.dump(outputData, outfile, indent=2)
