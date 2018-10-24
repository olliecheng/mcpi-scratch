from __future__ import print_function
import json
import sys

print("Updating extensions.json to include custom plugin...")

with open("/usr/lib/scratch2/scratch_extensions/extensions.json") as extensionsFile:
    extensions = json.loads(extensionsFile.read())

for e in extensions:
    if e["name"] == "MCPi-Scratch":
        # already exists!
        print("Entry for MCPi-Scratch already exists in /usr/lib/scratch2/scratch_extensions/extensions.json - deleting existing entry.")
        extensions.remove(e)  # delete existing entry

extensions.append({
    "name": "MCPi-Scratch",
    "type": "extension",
    "file": "mcpi-scratch.js",
    "url" : "https://denosawr.github.io/mcpi-scratch/",
    "tags": ["software"],
    "md5" : "mcpi-scratch.png"  # I think this is supposed to be an MD5 hash,
                                # but this format is used by existing extensions
})

with open("/usr/lib/scratch2/scratch_extensions/extensions.json", "w") as extensionsFile:
    extensionsFile.write(json.dumps(extensions))

print("Updated /usr/lib/scratch2/scratch_extensions/extensions.json to include custom plugin!")


